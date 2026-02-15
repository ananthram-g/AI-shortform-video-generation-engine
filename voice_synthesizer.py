import edge_tts
import asyncio
import os
import config
import json

async def generate_audio(script_data, output_dir):
    """
    Generates audio files for each dialogue line in the script.
    Returns the list of generated audio files with metadata (duration, file path, and sentence timings).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_files = []
    
    for i, line in enumerate(script_data):
        speaker_id = line["id"]
        text = line["text"]
        
        if speaker_id == "avatar_1":
            voice = config.AVATAR_1_VOICE
        elif speaker_id == "avatar_2":
            voice = config.AVATAR_2_VOICE
        else:
            voice = config.AVATAR_1_VOICE # Fallback

        filename = f"{i:03d}_{speaker_id}.mp3"
        filepath = os.path.join(output_dir, filename)
        
        communicate = edge_tts.Communicate(text, voice, rate=config.VOICE_RATE)
        
        # Capture audio and events
        sentences = []
        with open(filepath, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    # Convert ticks (100ns) to seconds: ticks / 10,000,000
                    start = chunk["offset"] / 10000000
                    duration = chunk["duration"] / 10000000
                    text_chunk = chunk["text"]
                    sentences.append({
                        "text": text_chunk,
                        "start": start,
                        "end": start + duration
                    })

        audio_files.append({
            "index": i,
            "speaker": speaker_id,
            "text": text,
            "file_path": filepath,
            "sentences": sentences  # List of {text, start, end}
        })
        
    return audio_files

# Wrapper for synchronous calls
def run_tts(script_data, output_dir="temp"):
    return asyncio.run(generate_audio(script_data, output_dir))

if __name__ == "__main__":
    # Test
    test_script = [
        {"id": "avatar_1", "text": "This is sentence one. This is sentence two.", "mood": "happy"},
    ]
    meta = run_tts(test_script)
    print(json.dumps(meta, indent=2))
