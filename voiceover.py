from gtts import gTTS
from pydub import AudioSegment

SCRIPT = """
We are given the integral of x over x squared plus one.
Notice that the denominator’s derivative is two x.
So we use substitution: let u be x squared plus one.
This transforms the integral into one half log of u.
Substituting back, the final answer is
one half log of x squared plus one plus C.
"""

def generate_voiceover(output="voiceover.mp3"):
    tts = gTTS(SCRIPT, lang="en", slow=False)
    tts.save(output)

    # Add short silence padding
    audio = AudioSegment.from_mp3(output)
    silence = AudioSegment.silent(duration=500)
    final_audio = silence + audio + silence
    final_audio.export(output, format="mp3")
