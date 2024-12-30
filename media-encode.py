#!/usr/bin/env python3

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def convert(src: Path, tgt: Path):
    tmpFile = tempfile.NamedTemporaryFile(suffix=".mkv")

    try:
        command = [
            "ffmpeg",
            "-nostdin",
            "-hide_banner",
            "-y",
            "-i",
            src,
            "-c:v",
            "libsvtav1",
            "-crf",
            "30",
            "-preset",
            "6",
            "-pix_fmt",
            "yuv420p10le",
            "-svtav1-params",
            "tune=3:film-grain=10:enable-overlays=1",
            "-c:a",
            "libopus",
            "-b:a",
            "128k",
            "-ac",
            "6",
            "-c:s",
            "copy",
            "-map",
            "0",
            tmpFile.name,
        ]

        subprocess.run(command, check=True)

    except subprocess.CalledProcessError:
        print(f"Error occurred while converting {src}")
        tmpFile.close()
        raise ValueError()

    shutil.copyfile(tmpFile.name, tgt)
    tmpFile.close()


def main():
    print("Media encoder script")

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source directory> <target directory>")

    srcDir = Path(sys.argv[1]).resolve()
    tgtDir = Path(sys.argv[2]).resolve()

    if srcDir == tgtDir:
        print("Source and target cannot be the same directory")
        sys.exit(1)

    print(f"Source: {srcDir}")
    print(f"Target: {tgtDir}")

    for srcFile in srcDir.rglob("*.mkv"):
        srcFileRel = srcFile.relative_to(srcDir)
        tgtFile = tgtDir / srcFileRel

        if tgtFile.exists():
            print(f"Skipping existing file {srcFileRel}")
            continue

        tgtFile.parent.mkdir(parents=True, exist_ok=True)

        print(f"Converting file {srcFileRel}: {srcFile} -> {tgtFile}")
        try:
            convert(srcFile, tgtFile)

        except ValueError:
            sys.exit(1)


if __name__ == "__main__":
    main()
