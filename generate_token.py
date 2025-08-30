#!/usr/bin/env python3
"""Generate a LiveKit token for the iOS app"""

import os
import jwt
import time
from datetime import datetime, timedelta

# Get credentials from .env.local
LIVEKIT_API_KEY = "APIxGFLR9fcu5Qg"
LIVEKIT_API_SECRET = "BilhzYvahmU91oKM6kG7oez262nseYJdZ5zqwQZ544c"
LIVEKIT_URL = "wss://test1-kl2nyv4s.livekit.cloud"

def generate_token(room_name: str, participant_name: str, valid_for_hours: int = 24):
    """Generate a LiveKit access token"""
    
    # Create the payload
    now = int(time.time())
    payload = {
        "iss": LIVEKIT_API_KEY,
        "sub": participant_name,
        "iat": now,
        "exp": now + (valid_for_hours * 3600),  # valid for specified hours
        "video": {
            "room": room_name,
            "roomJoin": True,
            "canPublish": True,
            "canSubscribe": True,
        }
    }
    
    # Generate the token
    token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")
    
    return {
        "serverUrl": LIVEKIT_URL,
        "roomName": room_name,
        "participantName": participant_name,
        "token": token
    }

if __name__ == "__main__":
    # Generate a token for testing
    room_name = "test-room"
    participant_name = "ios-user"
    
    token_info = generate_token(room_name, participant_name, valid_for_hours=24)
    
    print("Generated LiveKit Token:")
    print(f"Server URL: {token_info['serverUrl']}")
    print(f"Room Name: {token_info['roomName']}")
    print(f"Participant: {token_info['participantName']}")
    print(f"Token: {token_info['token']}")
    print("")
    print("Copy the token above to use in the iOS app TokenService.swift")