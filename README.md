# Mixtape Maker
**Automatically fit the max amount of tracks onto your audio tape cassette**

*Designed for use with the CR-669 Portable Cassette Player and Recorder AKA Phillips TAR5109*

## Quickstart (minimal config, using all defaults)

Versions of software here are just the version I was using, because it was the latest at the time. Default to the latest, unless something I wrote isn't forward compatible.

1. Have [Python](https://www.python.org/downloads/) and [FFmpeg](https://www.ffmpeg.org/download.html) installed. I used Python 3.14.7 and FFmpeg  n9.0.1.
2. Have [PyDub](https://pypi.org/project/pydub/) installed to that Python. I used 0.25.1.
3. Select a 60-minute recordable audio tape cassette (30 minutes on each side) to be your mixtape.
4. Put your music files in a folder named `music` in the same folder as this script (must be mp3, wma, or wav).
5. Run the script.
6. Copy the generated `A` folder (in the same folder as the script) onto an otherwise empty USB flash memory drive or micro SD card (must be 32 GB capacity ***or less***).
7. Make sure the "Trash" or "Recycle bin" on the drive or card is empty.
8. Safely eject the drive or card, and plug it into the cassette recorder.
9. Switch the cassette recorder into USB/Micro SD mode. After a few seconds, it will start playing the first track.
10. Skip to the second file (a silence gap 3 seconds long), and ***immediately pause the digital player***.
11. Manually wind forward the takeup reel of the cassette, until the splice from transparent leader tape to magnetic tape is only just at the openings in the bottom of the cassette. The goal here is that the cassette recorder's erase head will still touch all of the magnetic tape, but recording will start immediately.
12. Insert the cassette into the recorder.
13. Toggle on the pause key of the cassette mechanism, then press down the record and play key. This will allow the motor system and other circuitry of the cassette recorder to start and get up to full operating speed, without actually starting recording.
14. Showtime! Unpause the cassette mechanism, wait a second or so for magnetic tape to reach the play/record head, then skip back one track on the digital player. Having been skipped back, it will start playing again from the very beginning of the first track. You may hear a skip of the first second or so of track audio, but this skip occurs only to the speaker output, and thankfully not to the tape recording system.
15. Wait for recording to finish. If your machine is a CR-669 AKA Phillips TAR5109, feel free to turn the volume down to silent, as the recording volume from the digital player bypasses the output ampplifier and its volume control. The cassette recorder will audibly click off when it reaches the end of the tape.
16. Remove the memory drive from the cassette recorder, and plug it back into the computer.
17. ***Permanently delete*** the `A` folder from the memory drive.
18. If the script also generated a `B` folder, repeat steps 6 through 15 with that folder and the other side of the cassette.
19. **DO NOT ENJOY.** It is not allowed (jk).

## More detailed options
this program supports some configuration options. Most importantly, you can set a different tape size than the default 60 minutes. It's all UNIX style CLI options, so here's the full CLI `--help`:
```
usage: mixtape_maker.py [-h] [-t TAPE_SIZE] [-g GAP] [-e END_MARGIN] [-u] [-p] [input_folder] [output_folder]

Find the optimal combination of tracks to fit on your mixtape. Designed for use with the CR-669 Portable Cassette Player and Recorder AKA Phillips TAR5109.

positional arguments:
  input_folder          What folder to search for track options (default: ./music)
  output_folder         Where to place the generated A and B folders (default: .)

options:
  -h, --help            show this help message and exit
  -t, --tape-size TAPE_SIZE
                        Tape cassette size (in minutes) (default: 60)
  -g, --gap GAP         Gap (in seconds) between tracks (default: 3)
  -e, --end-margin END_MARGIN
                        Margin of silence (in seconds) at the end to prevent looping (default: 300)
  -u, --unlock-formats  Allow ANY file with an audio stream, not just CR-669 supported ones (default: False)
  -p, --print-only      Only print generated ordering, do not create output folders (default: False)

S.D.G.
```
The silent `### blank loopstop.mp3` at the end of the generated mix, of a duration which the `--end-margin` option adjusts in part, is there because of two things. First, the CR-669 AKA Phillips TAR5109's digital player will loop around to the first track after completing the last one. This file will pad out the rest of the tape. Second, most recordable tapes have a minute or two extra of time. I can guess why, but it doesn't matter. This file will thus have an additional margin of silence to cover any such margin of extra tape, to prevent the first half of a track from being recorded on the very end of the tape. That margin is what this option adjusts. I figured 5 minutes was a good default, as even on slow decks that should probably be enough to cover any extra tape space, and end the tape recording before the digital player loops.
The `--unlock-formats` option is mainly for if you wanted to use this script with a different tape deck, perhaps hooked to your computer as the audio source. You would play the files with any software that supports playing multiple files in filename sorted order (such as VLC Media Player). It will accept anything that FFmpeg can find an audio stream in, including videos, and as far as I know will also check the longest audio stream, not the first one. Use with caution.

## The law of the land
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

## S.D.G.
