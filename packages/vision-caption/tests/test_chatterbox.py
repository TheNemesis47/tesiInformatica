import asyncio
from vision_caption.adapters.speech.chatterbox_synth import *

async def test_speech():
    synth = ChatterboxSynthesizer(api_url="http://localhost:4123")
    print("inizio sintesi vocale")
    try:
        result = await synth.synthesize("Ciao mi chiamo Samuel e questa é una prova", "it")

        print(f"Successo! Tempo impiegato: {result.synthesis_time_ms}ms")
        print(f"dimensione audioo: {len(result.audio_bytes)} Bytes")

        with open("test_output.wav", "wb") as f:
            f.write(result.audio_bytes)
        print("File creato, ascolalo!")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(test_speech())