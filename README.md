# DS4DJ
[![CI](https://github.com/sam-k0/DS4DJ-dx/actions/workflows/nuitka.yml/badge.svg)](https://github.com/sam-k0/DS4DJ-dx/actions/workflows/nuitka.yml)<br>
An automated toolchain for fetching a list of songs from YouTube and converting them to the desired format (in this case .m4a). <br>

## Flags / Options when executing
Command line arguments are as following: 
+ -k : Keep the temporary files (mp4 and jpg)
+ -nocover : Does not add a cover image to the converted m4a
+ -playlist : Tells the program to start in playlist mode
    + you will need to provide the full playlist during runtime

## Setup
* Rename / Copy the ``config.template`` file to a ``config.txt`` file
    * Input your temporary & output folder, and your input file
* Rename / Copy / add the ``music.txt`` file. It will hold the songs you want to scrape from YouTube.
    * Each line in the file corresponds to one search/song on YouTube.
    * If you want to automatically save your music in named folders (genres for example) you can use the "Sections" that are shown in the ``music.template`` example. This is not a must however. Songs not belonging to any section will just be placed into the output folder.
* Please set up your virtual environment for python (Version 3.9) using the provided ``requirements.txt`` file by executing ``pip install -r requirements.txt``.
* Make sure you have ffmpeg installed...

## Usage
After activating your virtual environment, you can execute the script by just calling main.py with ``python main.py``.

````text
usage: DS4DJ [-h] [-k | --keep_temporary_content | --no-keep_temporary_content] [-c | --no_cover_in_metadata | --no-no_cover_in_metadata] [-p PLAYLIST_URL] [-g GENRE_NAME_PLAYLIST]

An automated toolchain for fetching a list of songs from YouTube and converting them to the desired format (in this case .m4a.)

optional arguments:
  -h, --help            show this help message and exit
  -k, --keep_temporary_content, --no-keep_temporary_content
                        If set, keeps the temporary files in the temporary folder. (default: False)
  -c, --no_cover_in_metadata, --no-no_cover_in_metadata
                        If set, does not add a cover image to the sound-files. (default: False)
  -p PLAYLIST_URL, --playlist_url PLAYLIST_URL
                        Allows you to parse an url to a YouTube playlist to be used as the input
  -g GENRE_NAME_PLAYLIST, --genre_name_playlist GENRE_NAME_PLAYLIST
                        Requires a playlist url to be specified. Allows you to automatically sort all files into the given directory name
  -mp3                  Switches converting from m4a to mp3 files
This utility was made for private use
````
