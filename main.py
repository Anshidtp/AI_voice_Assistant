import asyncio

from dotenv import load_dotenv
load_dotenv()

from livekit.agents import AutoSubscribe,JobContext,WorkerOptions,cli,llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from agent import AssistantFunc

async def entrypoint(ctx:JobContext):
    initial_ctx = llm.ChatContent().append(
        role = "system",
        text = (
            "You are a voice assistant created by LiveKit. Your interface with users will be voice."
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuations"
        ),

    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_temp = AssistantFunc()

    assistant = VoiceAssistant(
        vad = silero.VAD.load(),
        stt = openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_temp
    )
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hey, How can i help you today!",allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))