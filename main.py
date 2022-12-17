#!/usr/bin/env python3

from lib import feeds
from rofi import Rofi
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog = 'RofiYTFeed',
        description = 'Shows latest videos from subscribed YouTube channels in Rofi and plays them in MPV.'
    )
    parser.add_argument('subscriptions', help="A subscriptions file in the CSV format grabbed from Google Takeout")
    args = parser.parse_args()

    while True:
        feed = feeds.get_feed()[::-1]
        rofi = Rofi()
        index, _ = rofi.select('', ["↻ 𝗥𝗲𝗳𝗿𝗲𝘀𝗵 𝗙𝗲𝗲𝗱", *[f"{entry.get('author')} - {entry.get('title')}" for entry in feed]])
        if index == -1: 
            break
        if index == 0:
            feeds.create_feed_file(args.subscriptions)
            continue
        subprocess.run(['mpv', f"https://youtu.be/{feed[index-1]['video_id']}"])
        break

if __name__ == "__main__":
    main()
