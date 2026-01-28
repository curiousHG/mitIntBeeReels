import os
import subprocess
from voiceover import generate_voiceover

SCENE_NAME = "IntegrationReel"
VIDEO_PATH = f"media/videos/scene/1080p60/{SCENE_NAME}.mp4"
FINAL_OUTPUT = "output/final_reel.mp4"

def render_scene():
    subprocess.run([
        "manim",
        "-pqh",
        "scene.py",
        SCENE_NAME,
        "--resolution",
        "1080,1920",
        "--frame_rate",
        "60"
    ])

def merge_audio():
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", VIDEO_PATH,
        "-i", "voiceover.mp3",
        "-shortest",
        FINAL_OUTPUT
    ])

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    generate_voiceover()
    render_scene()
    merge_audio()
