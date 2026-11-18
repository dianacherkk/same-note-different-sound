"""Crop the original Iowa AIFF files and write the WAV data used in this project.

Requires Python 3.12 when extracting from AIFF. The included WAV files
already contain these crops, so this preparation step is optional.
"""

import aifc
import argparse
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "docs" / "audio"
CLIPS = (
    ("Flute.nonvib.mf.B3B4.aiff", 28.65, "flute-a4.wav"),
    ("Violin.arco.mf.sulA.A4B4.aiff", 4.0, "violin-a4.wav"),
)


def crop_note(source_path, start_seconds, output_path):
    with aifc.open(str(source_path)) as source:
        if source.getnchannels() != 1 or source.getsampwidth() != 2:
            raise ValueError("Expected the original mono, 16-bit recording.")
        rate = source.getframerate()
        source.setpos(round(start_seconds * rate))
        # AIFF samples are big-endian. WAV samples are little-endian.
        frames = source.readframes(rate)

    little_endian = bytearray(len(frames))
    little_endian[::2] = frames[1::2]
    little_endian[1::2] = frames[::2]
    with wave.open(str(output_path), "wb") as target:
        target.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        target.writeframes(little_endian)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_folder", type=Path)
    args = parser.parse_args()
    AUDIO.mkdir(parents=True, exist_ok=True)
    for filename, start, output in CLIPS:
        crop_note(args.source_folder / filename, start, AUDIO / output)


if __name__ == "__main__":
    main()
