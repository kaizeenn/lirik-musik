#  LIBRARIES / PACKAGES IMPORTS.

import sys
from rich import print
from time import sleep

#  CODE EXECUTION

#  Code reference: 'https://www.tiktok.com/@pyatsplusom/video/7535003211887889695'.
#  Song: Lemon Demon - Fine
# - URL: 'https://www.youtube.com/watch?v=xRiGeDMKpKU'.

lines = [
    (". . .", 0.2),
    ("Light is on the way", 0.058),
    ("We'll be having a fun time", 0.048),
    ("It's such a lovely day", 0.048),
    ("We should pocket the sunshine", 0.048),
    ("And never give it back", 0.05),
    ("Even if there's a heat wave", 0.04),
    ("Or terrorist attack", 0.05),
    ("It will just be a close shave", 0.05),
    ("I know", 0.1),
    ("I know", 0.15),
    ("That every bomb has a silver lining", 0.07),
    ("I know", 0.1),
    ("I know", 0.1)
]

delays = [0.9, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 1.2, 0.1, 0.1, 0.1]

def printLyrics():
    for i, (line, char_delay) in enumerate(lines):
        for char in line:
            print(f"[grey78]{char}[/grey78]", end = '')
            sys.stdout.flush()
            sleep(char_delay)
        print()
        sleep(delays[i])

printLyrics()
