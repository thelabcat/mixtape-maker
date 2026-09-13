# Mixtape Maker
**Automatically fit the max amount of tracks onto your audio tape cassette**

*Designed for use with the CR-669 Portable Cassette Player and Recorder AKA Phillips TAR5109*

## Quickstart (absolutely no config)
1. Select a 60-minute recordable audio tape cassette (30 minutes on each side) to be your mixtape.
2. Put your music files in a folder named `music` in the same folder as this script (must be mp3, wma, or wav).
3. Run the script.
4. Copy the generated `A` folder (in the same folder as the script) onto an otherwise empty USB flash memory drive or micro SD card (must be 32 GB capacity ***or less***).
5. Make sure the "Trash" or "Recycle bin" on the drive or card is empty.
6. Safely eject the drive or card, and plug it into the cassette recorder.
7. Switch the cassette recorder into USB/Micro SD mode. After a few seconds, it will start playing the first track.
8. Skip to the second file (a silence gap 3 seconds long), and ***immediately pause the digital player***.
9. Manually wind forward the takeup reel of the cassette, until the splice from transparent leader tape to magnetic tape is only just at the openings in the bottom of the cassette. The goal here is that the cassette recorder's erase head will still touch all of the magnetic tape, but recording will start immediately.
10. Insert the cassette into the recorder.
11. Toggle on the pause key of the cassette mechanism, then press down the record and play key. This will allow the motor system and other circuitry of the cassette recorder to start and get up to full operating speed, without actually starting recording.
12. Showtime! Unpause the cassette mechanism, wait a second or so for magnetic tape to reach the play/record head, then skip back one track on the digital player. Having been skipped back, it will start playing again from the very beginning of the first track. You may hear a skip of the first second or so of track audio, but this skip occurs only to the speaker output, and thankfully not to the tape recording system.
13. Wait for recording to finish. If your machine is a CR-669 AKA Phillips TAR5109, feel free to turn the volume down to silent, as the recording volume from the digital player bypasses the output ampplifier and its volume control. The cassette recorder will audibly click off when it reaches the end of the tape.
14. Remove the memory drive from the cassette recorder, and plug it back into the computer.
15. ***Permanently delete*** the `A` folder from the memory drive.
16. If the script also generated a `B` folder, repeat steps 4 through 13 with that folder and the other side of the cassette.
17. **DO NOT ENJOY.** It is not allowed (jk).

## More detailed options
this program supports some configuration options. Most importantly, you can set a different tape size than the default 60 minutes. It's all UNIX style CLI options, so here's the full CLI `--help`:
```
usage: mixtape_maker.py [-h] [-t TAPE_SIZE] [-g GAP] [-e END_MARGIN] [input_folder] [output_folder]

Find the optimal combination of tracks to fit on your mixtape. Designed for use with the CR-669 Portable Cassette Player and Recorder AKA Phillips TAR5109.

positional arguments:
  input_folder          What folder to search for track options (default: .)
  output_folder         Where to place the generated A and B folders (default: .)

options:
  -h, --help            show this help message and exit
  -t, --tape-size TAPE_SIZE
                        Tape cassette size (in minutes) (default: 60)
  -g, --gap GAP         Gap (in seconds) between tracks (default: 3)
  -e, --end-margin END_MARGIN
                        Margin of silence (in seconds) at the end to prevent looping (default: 300)

S.D.G.
```
That `--end-margin` option is because of two things. First, most recordable tapes have a minute or two extra of space. I can guess why, but it doesn't matter. Second, the CR-669 AKA Phillips TAR5109's digital player will loop around to the first track after completing the last one. So, I add 5 minutes of silence to cover any such margin, to prevent the first half of a track from being recorded on the very end of the tape.

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
