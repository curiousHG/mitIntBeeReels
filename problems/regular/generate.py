#!/usr/bin/env python3
"""
Generic video generator for MIT Integration Bee problems.
This script can generate videos for any problem with proper configuration.
"""

import os
import sys
import subprocess
import glob
import argparse
from pydub import AudioSegment


# ============================================================================
# VIDEO GENERATION PIPELINE
# ============================================================================

def run(cmd):
    """Execute command with error checking."""
    subprocess.run(cmd, check=True)


def render_scene(scene_name, module_path, frame_rate=60, quality="4k"):
    """Render the Manim scene in high quality."""
    print("\n" + "="*60)
    print("STEP 1: Rendering Manim scene (4K quality)...")
    print("="*60)
    
    # 4K quality settings for vertical video (9:16)
    quality_map = {
        "4k": ("2160", "3840"),  # 4K vertical
        "1080p": ("1080", "1920"), # Full HD vertical
    }
    
    width, height = quality_map.get(quality, quality_map["4k"])
    
    run([
        "manim",
        "-qk",  # 4K quality
        "--renderer=opengl",
        module_path,
        scene_name,
        "--resolution",
        f"{width},{height}",
        "--frame_rate",
        str(frame_rate),
    ])
    print(f"✓ Scene rendered successfully at {width}x{height}")


def find_latest_render(scene_name):
    """Find the most recently rendered video file."""
    candidates = glob.glob(f"media/videos/**/{scene_name}*.mp4", recursive=True)
    candidates = [p for p in candidates if os.path.isfile(p) and os.path.getsize(p) > 1000]
    if not candidates:
        raise SystemExit(f"❌ No rendered video found for {scene_name} under media/videos.")
    latest = max(candidates, key=lambda p: os.path.getmtime(p))
    print(f"✓ Found rendered video: {latest}")
    return latest


def get_duration(path):
    """Get video/audio duration using ffprobe."""
    try:
        out = subprocess.check_output([
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path,
        ])
        return float(out)
    except Exception:
        return None


def normalize_video(input_path, output_path, target_duration, frame_rate):
    """Normalize video to exact target duration with high quality encoding."""
    print(f"\nNormalizing video to {target_duration}s (high quality encoding)...")
    dur = get_duration(input_path) or target_duration
    print(f"  Original duration: {dur:.2f}s")
    
    # High quality encoding parameters
    base_cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-c:v", "libx264",           # H.264 codec
        "-preset", "slow",            # Slower = better quality
        "-crf", "18",                 # Constant Rate Factor (18 = visually lossless)
        "-profile:v", "high",         # High profile for best quality
        "-level", "4.2",              # H.264 level
        "-r", str(frame_rate),        # Frame rate
        "-pix_fmt", "yuv420p",        # Pixel format for compatibility
        "-an",                        # No audio for now
    ]
    
    if dur < target_duration:
        pad = target_duration - dur
        vf = f"tpad=stop_mode=clone:stop_duration={pad}"
        run(base_cmd + ["-vf", vf, "-t", str(target_duration), output_path])
    else:
        run(base_cmd + ["-t", str(target_duration), output_path])
    
    print(f"✓ Video normalized with high quality: {output_path}")


def normalize_audio(input_path, output_path, target_duration):
    """Normalize audio to exact target duration."""
    print(f"\nNormalizing audio to {target_duration}s...")
    audio = AudioSegment.from_mp3(input_path)
    audio_ms = len(audio)
    target_ms = int(target_duration * 1000)
    
    print(f"  Original duration: {audio_ms/1000:.2f}s")
    
    if audio_ms > target_ms:
        audio = audio[:target_ms]
        print("  ✂ Trimmed audio")
    elif audio_ms < target_ms:
        silence = AudioSegment.silent(duration=target_ms - audio_ms)
        audio = audio + silence
        print("  ➕ Added silence padding")
    
    audio.export(output_path, format="mp3")
    print(f"✓ Audio normalized: {output_path}")


def merge_av(video_path, audio_path, output_path):
    """Merge video and audio into final output with high quality audio."""
    print("\n" + "="*60)
    print("STEP 4: Merging video and audio (high quality)...")
    print("="*60)
    run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",              # Copy video (already encoded)
        "-c:a", "aac",               # AAC audio codec
        "-b:a", "320k",              # High quality audio bitrate
        "-ar", "48000",              # 48kHz sample rate
        "-shortest",
        output_path,
    ])
    print(f"✓ Final video created: {output_path}")


def generate_voiceover(problem_num, output_path, tld="com.au"):
    """Generate voiceover for a problem."""
    print("\n" + "="*60)
    print("STEP 3: Generating voiceover...")
    print("="*60)
    
    # Import and call the appropriate voiceover function
    from voiceover import generate_voiceover

    # script is part of the question.py file only as a string variable, so we need to import it dynamically
    module_name = f"{problem_num}"
    try:
        module = __import__(module_name, fromlist=["SCRIPT"])
        script = getattr(module, "SCRIPT")
    except (ImportError, AttributeError) as e:
        raise SystemExit(f"❌ Could not import script for {problem_num}: {e}")
    
    generate_voiceover(script=script, output=output_path, tld=tld)


def main():
    """Main pipeline with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Generate MIT Integration Bee video reels"
    )
    parser.add_argument(
        "problem",
        type=str,
        help="Problem identifier (e.g., q1, q2)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=35.0,
        help="Target video duration in seconds (default: 35.0)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=60,
        help="Frame rate (default: 60)",
    )
    parser.add_argument(
        "--quality",
        type=str,
        choices=["4k", "1080p"],
        default="4k",
        help="Video quality (default: 4k)",
    )
    parser.add_argument(
        "--tld",
        type=str,
        default="com.au",
        help="TLD for voice accent (default: com.au)",
    )
    
    args = parser.parse_args()
    
    # Problem configuration
    problem_num = args.problem.lower()
    scene_name = f"{problem_num.upper()}Integral"
    module_path = f"problems/regular/{problem_num}.py"
    output_dir = f"output/{problem_num}"
    
    video_out = os.path.join(output_dir, f"{problem_num}_video.mp4")
    audio_out = os.path.join(output_dir, f"{problem_num}_voice.mp3")
    final_out = os.path.join(output_dir, f"{problem_num}_reel.mp4")
    
    print("\n" + "="*60)
    print(f"MIT INTEGRATION BEE VIDEO GENERATOR - {problem_num.upper()}")
    print("="*60)
    print(f"Scene: {scene_name}")
    print(f"Module: {module_path}")
    print(f"Quality: {args.quality.upper()}")
    print(f"Duration: {args.duration}s")
    print(f"FPS: {args.fps}")
    print("="*60)
    
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Render the scene
    render_scene(scene_name, module_path, args.fps, args.quality)

    # Step 2: Locate and normalize video
    print("\n" + "="*60)
    print("STEP 2: Processing video...")
    print("="*60)
    rendered = find_latest_render(scene_name)
    normalize_video(rendered, video_out, args.duration, args.fps)

    # Step 3: Generate and normalize voiceover
    generate_voiceover(problem_num, audio_out, args.tld)
    normalize_audio(audio_out, audio_out, args.duration)

    # Step 4: Merge into final reel
    merge_av(video_out, audio_out, final_out)

    # Get final video resolution
    quality_map = {"4k": "2160x3840", "1080p": "1080x1920"}
    resolution = quality_map.get(args.quality, "2160x3840")
    
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"Final video: {final_out}")
    print(f"Quality: {args.quality.upper()} ({resolution})")
    print(f"Duration: {args.duration}s")
    print(f"Frame rate: {args.fps} fps")
    print(f"Video codec: H.264 (CRF 18 - visually lossless)")
    print(f"Audio codec: AAC 320kbps @ 48kHz")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
