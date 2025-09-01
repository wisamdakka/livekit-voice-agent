# LiveKit Voice Agent - AI Beauty Consultant

A production-ready AI voice assistant powered by LiveKit that provides personalized beauty advice and recommendations through natural voice conversations.

## 🎯 Overview

This system integrates multiple AI services to create a seamless voice chat experience:
- **Voice Recognition**: Deepgram for accurate speech-to-text
- **AI Assistant**: OpenAI GPT-4o-mini for intelligent beauty consultation
- **Voice Synthesis**: Cartesia for natural-sounding responses
- **Voice Activity Detection**: Silero VAD for conversation flow
- **Authentication**: Integrated with existing beauty service

## 🚀 Quick Start for Developers

**Ready to use!** The production endpoint is live at:
```
https://the-ultimate-beauty-318968771808.us-west2.run.app/beauty.beauty.v1.BackendService/GetLiveKitToken
```

1. **Copy the TokenService.swift code** from section below
2. **Add LiveKit SDK** to your iOS project: `https://github.com/livekit/client-sdk-swift`
3. **Test the connection** with any room/participant name
4. **Start voice conversations** immediately!

## 🏗️ Architecture

```
iOS App → Beauty Service (Token) → LiveKit Cloud → Voice Agent → AI Services
```

## 🚀 Production Integration for iOS Apps

### Prerequisites
- LiveKit SDK for iOS
- Access to your beauty service production endpoint
- iOS 15.0+

### 1. Add TokenService.swift to your project:

```swift
import Foundation

actor TokenService {
    struct ConnectionDetails: Codable {
        let serverUrl: String
        let roomName: String
        let participantName: String
        let participantToken: String
    }

    // Production Beauty Service URL
    private let tokenServerUrl: String = "https://the-ultimate-beauty-318968771808.us-west2.run.app/beauty.beauty.v1.BackendService/GetLiveKitToken"
    
    func fetchConnectionDetails(roomName: String, participantName: String) async throws -> ConnectionDetails? {
        return try await fetchConnectionDetailsFromTokenServer(roomName: roomName, participantName: participantName)
    }

    private func fetchConnectionDetailsFromTokenServer(roomName: String, participantName: String) async throws -> ConnectionDetails? {
        var request = URLRequest(url: URL(string: tokenServerUrl)!)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let requestBody = [
            "room_name": roomName,
            "participant_name": participantName
        ]
        
        request.httpBody = try JSONSerialization.data(withJSONObject: requestBody, options: [])
        
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                print("❌ Failed to connect to token server")
                return nil
            }
            
            guard (200...299).contains(httpResponse.statusCode) else {
                print("❌ Token server error: \(httpResponse.statusCode)")
                return nil
            }
            
            guard let connectionDetails = try? JSONDecoder().decode(ConnectionDetails.self, from: data) else {
                print("❌ Error parsing token server response")
                return nil
            }
            
            return connectionDetails
        } catch {
            print("❌ Network error: \(error)")
            return nil
        }
    }
}
```

### 2. Usage in your ViewModel:

```swift
import LiveKit

class VoiceAgentViewModel: ObservableObject {
    private let tokenService = TokenService()
    private let room = Room()
    
    func connect() async {
        do {
            // Generate unique room and participant names
            let roomName = "room-\(Int.random(in: 1000...9999))"
            let participantName = "user-\(Int.random(in: 1000...9999))"
            
            // Get connection details from your beauty service
            guard let connectionDetails = try await tokenService.fetchConnectionDetails(
                roomName: roomName,
                participantName: participantName
            ) else {
                print("❌ Failed to get connection details")
                return
            }
            
            // Connect to LiveKit room
            try await room.connect(
                url: connectionDetails.serverUrl,
                token: connectionDetails.participantToken
            )
            
            print("✅ Connected to voice agent!")
            
        } catch {
            print("❌ Connection failed: \(error)")
        }
    }
}
```

## 📡 API Integration

### Token Endpoint
```
POST /beauty.beauty.v1.BackendService/GetLiveKitToken
Content-Type: application/json
```

### Request Format
```json
{
  "room_name": "room-1234",
  "participant_name": "user-john"
}
```

### Response Format
```json
{
  "serverUrl": "wss://test1-kl2nyv4s.livekit.cloud",
  "roomName": "room-1234",
  "participantName": "user-john",
  "participantToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 🎤 Voice Agent Features

- **Real-time Voice Chat**: Natural conversation with AI assistant
- **Beauty Consultation**: Personalized skincare and beauty advice
- **Conversation Flow**: Automatic turn detection and response timing
- **Multi-language Support**: Supports multiple languages via Deepgram
- **High-quality Audio**: Crystal clear voice synthesis
- **Scalable**: Handles multiple concurrent users

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- Go 1.21+
- LiveKit Cloud account
- Required API keys:
  - OpenAI API Key
  - Deepgram API Key  
  - Cartesia API Key
  - LiveKit API credentials

### Environment Variables
Create `.env.local` file:
```bash
LIVEKIT_API_KEY="your_livekit_api_key"
LIVEKIT_API_SECRET="your_livekit_secret"
LIVEKIT_URL="wss://your-project.livekit.cloud"
OPENAI_API_KEY="your_openai_key"
DEEPGRAM_API_KEY="your_deepgram_key"
CARTESIA_API_KEY="your_cartesia_key"
```

### Run Voice Agent Locally
```bash
# Install dependencies
uv sync

# Start the agent
python agent.py dev
```

### Run Beauty Service Locally
```bash
# Set environment variables
export OPENAI_API_KEY="your_key"
export GEMINI_API_KEY="your_key"

# Start the service
go run cmd/private/server/main.go
```

## 🏭 Production Deployment

### Beauty Service Integration
The LiveKit token generation is integrated into the production beauty service at:
- **Endpoint**: `https://the-ultimate-beauty-318968771808.us-west2.run.app/beauty.beauty.v1.BackendService/GetLiveKitToken`
- **Method**: POST
- **Status**: ✅ **LIVE IN PRODUCTION**
- **Authentication**: Uses existing beauty service authentication

### Voice Agent Deployment
The voice agent runs automatically on LiveKit Cloud workers when users connect.

## 📱 iOS Integration Steps

1. **Add LiveKit SDK** to your iOS project
2. **Copy TokenService.swift** with your production URL
3. **Implement VoiceAgentViewModel** for connection management
4. **Handle microphone permissions** in your app
5. **Test with unique room/participant names**

## 🔧 Configuration

### LiveKit Settings
- **Server**: `wss://test1-kl2nyv4s.livekit.cloud`
- **Region**: UAE
- **Token Expiry**: 24 hours
- **Audio Quality**: 24kHz, mono

### AI Model Configuration
- **STT**: Deepgram Nova-3 (multilingual)
- **LLM**: OpenAI GPT-4o-mini
- **TTS**: Cartesia Sonic-2
- **VAD**: Silero VAD

## 🚨 Troubleshooting

### Common Issues

**Connection Failed**
- Verify production URL is correct
- Check network connectivity
- Ensure API keys are valid

**No Audio**
- Check microphone permissions
- Verify audio input/output settings
- Test with different devices

**Token Expired**
- Tokens expire after 24 hours
- Implement token refresh logic
- Check server time synchronization

### Debug Logs
Enable debug logging by adding print statements in TokenService for detailed connection information.

## 📚 Additional Resources

- [LiveKit iOS SDK Documentation](https://docs.livekit.io/client-sdks/ios/)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [Beauty Service API Documentation](your-beauty-service-docs)

## 🤝 Support

For technical support or integration questions, contact the development team.

## 📄 License

[Your License Here]