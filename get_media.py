#!/usr/bin/env python
from __future__ import unicode_literals
from sys import argv, exit
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import youtube_dl


class Media:
    def __init__(self, media_type, url):
        self.media_type = media_type
        self.url = url
        self.media_opts = {
            'format': self.media_type,
            'outtmpl': f"%(id)s.mp4",
            'noplaylist': True,
            'progress_hooks': [self.p_hook],
        }

    def p_hook(self, download):
        if download['status'] == 'finished':
            print("[+] Downloads complete- converting media...")

    def download_media(self):
        with youtube_dl.YoutubeDL(self.media_opts) as ydl:
            ydl.download([self.url])


def usage(error_message):
    print(f"[!] Usage: {argv[0]} [-a || --audio] <URL>")
    print(error_message)
    exit(0)


def check_url(url):
    try:
        urlopen(url).read()
    except Exception as e:
        print(f"[x] Error: {e.__class__.__name__}:\n{e}")


def check_args():
    if len(argv) < 2 or len(argv) > 3:
        usage("[x] Please provide at least one valid url...")
    else:
        if len(argv) == 2:
            check_url(argv[1])
            return "best", argv[1]
        if len(argv) == 3:
            if argv[1] == "-a" or argv[1] == "--audio":
                check_url(argv[2])
                return "bestaudio/best", argv[2]


if __name__ == '__main__':
    media_type, url = check_args()
    new_media = Media(media_type, url)
    new_media.download_media()
