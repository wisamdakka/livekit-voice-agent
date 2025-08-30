package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/mux"
	"github.com/rs/cors"
)

type TokenRequest struct {
	RoomName        string `json:"roomName"`
	ParticipantName string `json:"participantName"`
}

type TokenResponse struct {
	ServerURL       string `json:"serverUrl"`
	RoomName        string `json:"roomName"`
	ParticipantName string `json:"participantName"`
	Token           string `json:"participantToken"`
}

type Claims struct {
	Video map[string]interface{} `json:"video"`
	jwt.RegisteredClaims
}

var (
	liveKitAPIKey    = os.Getenv("LIVEKIT_API_KEY")
	liveKitAPISecret = os.Getenv("LIVEKIT_API_SECRET")
	liveKitURL       = os.Getenv("LIVEKIT_URL")
)

func generateToken(roomName, participantName string) (string, error) {
	now := time.Now()
	claims := Claims{
		Video: map[string]interface{}{
			"room":         roomName,
			"roomJoin":     true,
			"canPublish":   true,
			"canSubscribe": true,
		},
		RegisteredClaims: jwt.RegisteredClaims{
			Issuer:    liveKitAPIKey,
			Subject:   participantName,
			IssuedAt:  jwt.NewNumericDate(now),
			ExpiresAt: jwt.NewNumericDate(now.Add(24 * time.Hour)), // 24 hours
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(liveKitAPISecret))
}

func tokenHandler(w http.ResponseWriter, r *http.Request) {
	var req TokenRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

	token, err := generateToken(req.RoomName, req.ParticipantName)
	if err != nil {
		http.Error(w, "Failed to generate token", http.StatusInternalServerError)
		return
	}

	response := TokenResponse{
		ServerURL:       liveKitURL,
		RoomName:        req.RoomName,
		ParticipantName: req.ParticipantName,
		Token:           token,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	if liveKitAPIKey == "" || liveKitAPISecret == "" || liveKitURL == "" {
		log.Fatal("Missing required environment variables: LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL")
	}

	r := mux.NewRouter()
	r.HandleFunc("/api/token", tokenHandler).Methods("POST")

	// Setup CORS
	c := cors.New(cors.Options{
		AllowedOrigins: []string{"*"},
		AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders: []string{"*"},
	})

	handler := c.Handler(r)

	port := os.Getenv("TOKEN_SERVER_PORT")
	if port == "" {
		port = "8081"
	}

	log.Printf("Token server starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, handler))
}