#!/usr/bin/env python3
"""
LiveKit Voice AI Agent
A simple voice assistant using LiveKit Agents framework
"""

import logging
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai, 
    cartesia, 
    deepgram,
    noise_cancellation,
    silero
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables
load_dotenv(".env.local")

# Set up logging
logger = logging.getLogger("voice-assistant")
logger.setLevel(logging.INFO)

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful AI voice assistant. Keep your responses concise and conversational.")

async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint for the voice assistant agent"""
    
    # Create the assistant session
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))