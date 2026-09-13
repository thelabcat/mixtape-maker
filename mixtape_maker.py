#!/usr/bin/env python3
#coding : utf - 8
"""Mixtape Maker

Find the optimal combination of music tracks to fit on your mixtape size.
Designed for use with the CR-669 Portable Cassette Player and Recorder AKA Phillips TAR5109.

Copyright 2026 Wilbur Jaywright

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

S.D.G."""

import argparse
import glob
import itertools
import os
from os import path as op
import shutil
import subprocess
from typing import Sequence
from pydub import AudioSegment

parser = argparse.ArgumentParser(
    description="""
Find the optimal combination of tracks to fit on your mixtape.
Designed for use with the CR-669 Portable Cassette Player and Recorder AKA
Phillips TAR5109.""",
    epilog="S.D.G.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument("-t", "--tape-size", type=int, default=60,
                    help="Tape cassette size (in minutes)")
parser.add_argument("-g", "--gap", type=int, default=3,
                    help="Gap (in seconds) between tracks")
parser.add_argument("-e", "--end-margin", type=int, default=5 * 60,
                    help="Margin of silence (in seconds) at the end to prevent looping")
parser.add_argument("input_folder", nargs="?", default=".",
                    help="What folder to search for track options")
parser.add_argument("output_folder", nargs="?", default=".",
                    help="Where to place the generated A and B folders")

args = parser.parse_args()

DURATION_COMMAND = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1".split()
"""Command to run to get the duration of a media file, suffixed by the path"""

EXTENSIONS = "mp3", "wma", "wav"
"""Filename extensions supported by that cassette recorder"""

TAPE_SIDE_SECONDS: int = args.tape_size * 30
"""Size of one tape side in seconds"""

GAP_SEG = AudioSegment.silent(args.gap * 1000)
"""Segment of silence to go between tracks"""

assert shutil.which("ffmpeg"), "This program relies on FFmpeg being on PATH"


def get_duration(filename: str) -> float:
    """Determine the duration of a media file via FFmpeg"""
    return float(subprocess.run(
        DURATION_COMMAND + [filename],
        capture_output=True,
        check=True,
        encoding="utf-8",
        ).stdout.strip())


# Search out files
files = []
for ext_raw in EXTENSIONS:
    for ext in (ext_raw, ext_raw.upper()):
        files += glob.glob(op.join(args.input_folder,
                           "**/*." + ext), recursive=True)

assert files, "No files in allowed formats found"

durations_sec = {f: get_duration(f) for f in files}
totaltime_sec = sum(durations_sec.values())


def get_list_duration(filelist: Sequence[str]) -> float:
    """Calculate the duration of a track file list, with gaps"""
    # The durations of all the files,
    # plus the durations of the gaps between them
    return sum(durations_sec[f] for f in filelist) + \
        args.gap * (len(filelist) - 1)


print(f"Found {len(files)} files, {totaltime_sec: .2f} seconds of audio total.")

assert min(durations_sec.values()
           ) < TAPE_SIDE_SECONDS, "No tracks will fit on tape side"

# Ends up being files we didn't use for one, then either side
remaining_files = files.copy()

# Fill each side of the tape to max
sides = {"A": [], "B": []}
for side_name in sides:
    # Count down from max size to min
    for filecount in range(len(remaining_files), 0, -1):
        # Find all the possible combos of X songs, and sort them by length, longest first
        combos = sorted(itertools.combinations(remaining_files,
                        filecount), key=get_list_duration, reverse=True)

        # Find the longest combo that will fit, or good = False if none do
        good = False
        for combo in combos:
            if get_list_duration(combo) <= TAPE_SIDE_SECONDS:
                good = True
                break

        # One combo was short enough
        if good:
            sides[side_name] = combo

            # While we're iterating through the side to remove the files we used,
            # we might as well do the telling the user what's on there
            print(
                f"Side {side_name}, duration {get_list_duration(combo):.02f} seconds:")
            for f in combo:
                print("\t", f)
                remaining_files.remove(f)
            break

if remaining_files:
    print("Some files could not fit:")
    for f in remaining_files:
        print("\t", f)
else:
    print("All files fit on tape.")

for side_name, side in sides.items():
    # Should only happen when the second side is empty
    if not side:
        print("No files for side", side_name, "so not copying")
        continue

    # Folder for this side
    folder = op.join(args.output_folder, side_name)
    os.makedirs(folder, exist_ok=True)

    # Number of tracks on this side
    track_count = len(side)

    # Number of digits the last gap track, and thus all the tracks will need
    digits = len(str(track_count * 2))

    # Copy over the tracks, with numbering to put them in order, and gaps in between
    for i, f in enumerate(side):
        shutil.copy(f, op.join(folder, f"{i * 2:0{digits}} {op.basename(f)}"))

        # We are not on the last track, so add a gap
        if i + 1 != track_count:
            GAP_SEG.export(op.join(folder, f"{i * 2 + 1:0{digits}} blank gap.mp3"))

    # Replace the last gap with one long enough to fill the cassette and then some
    AudioSegment.silent((TAPE_SIDE_SECONDS - get_list_duration(side) + args.end_margin)
                        * 1000).export(op.join(folder, f"{i * 2 + 1:0{digits}} blank loopstop.mp3"))

print("Done.")
