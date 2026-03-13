"""
Transcription Module — AssemblyAI Speech-to-Text + Speaker Diarization

Usage:
    from transcriber import transcribe_audio
    transcript = transcribe_audio("meeting.mp3")
"""

import os
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio/video file with speaker diarization.

    Args:
        file_path: Path to an .mp3 or .mp4 file.

    Returns:
        A formatted transcript string with speaker labels, e.g.:
            Speaker A: Hello everyone.
            Speaker B: Hi, let's get started.
    """
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    # Map raw speaker IDs (e.g. "A", "B") to friendly labels
    speaker_map: dict[str, str] = {}
    formatted_lines: list[str] = []

    for utterance in transcript.utterances:
        speaker_id = utterance.speaker
        if speaker_id not in speaker_map:
            label = f"Speaker {chr(65 + len(speaker_map))}"  # A, B, C, ...
            speaker_map[speaker_id] = label
        formatted_lines.append(f"{speaker_map[speaker_id]}: {utterance.text}")

    return "\n".join(formatted_lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <path_to_audio_file>")
        sys.exit(1)

    result = transcribe_audio(sys.argv[1])
    print(result)
