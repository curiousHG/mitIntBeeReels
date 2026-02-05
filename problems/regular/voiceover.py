from gtts import gTTS
from pydub import AudioSegment




def generate_voiceover(script, output: str = "voiceover_q1.mp3", tld: str = "com.au"):
    """Generate the Q1 voiceover optimized for 30 seconds.
    
    Args:
        output: path to write the mp3 file.
        tld: top-level domain to influence the voice/accent (e.g. 'com', 'com.au').
    """
    tts = gTTS(script, lang="en", slow=False, tld=tld)
    tts.save(output)

    # Add minimal silence padding (200ms each side)
    audio = AudioSegment.from_mp3(output)
    silence = AudioSegment.silent(duration=200)
    final_audio = silence + audio + silence
    final_audio.export(output, format="mp3")
    
    # Print duration for verification
    duration_sec = len(final_audio) / 1000
    print(f"Generated voiceover duration: {duration_sec:.2f} seconds")


if __name__ == "__main__":
    generate_voiceover("MIT Integration Bee Regular Season 2026 Problem 1.", "test_voiceover_q1.mp3")