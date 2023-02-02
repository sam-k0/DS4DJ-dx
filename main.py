import os
import asyncio
import configparser  # for reading config file
import os.path  # for path joining
import cmdargs  # cmd line args

from youtube_utils import get_id_by_name, download_video, download_cover, resolve_playlist, full_url_to_id
from conversion_utils import convert_to_m4a, clean_temp_folder, set_meta_tags
from pathlib import Path


async def run(song_list: list):
    """
    Iterates over a list of song names, fetches them from youtube and converts them into .m4a format
    :param song_list: the list of songs to be fetched
    :return: None
    """
    for song_name in song_list:
        print(f"Working on {song_name}...")

        # Get video id
        video_id = await get_id_by_name(song_name)

        # Download Video to wanted location
        mp4_name, video_author, video_title, video_cover_url = download_video(video_id,
                                                                              config["LOCATIONS"]["Mp4TempFolder"])

        # Convert .mp4 video to .m4a SoundFile
        mp4_path = os.path.join(config["LOCATIONS"]["Mp4TempFolder"], Path(mp4_name))
        m4a_path = os.path.join(config["LOCATIONS"]["M4aSaveFolder"], Path(mp4_name).with_suffix('.m4a'))
        convert_to_m4a(mp4_path, m4a_path)
        # Set meta-tags

        # Download cover (-nocover will stop this)
        if not cmdargs.find_arg("-nocover"):
            jpg_path = download_cover(video_cover_url, video_id, config["LOCATIONS"]["Mp4TempFolder"])
        else:
            jpg_path = "NONE"

        # Set the meta-tags
        set_meta_tags(m4a_path, video_title, video_author, jpg_path)


if __name__ == "__main__":

    # Valid command line arguments: 
    # -k       : keep the temporary files (mp4 and jpg)
    # -nocover : Does not add a cover image to the converted m4a

    # Read configuration file config.ini
    if os.path.isfile("config.ini"):  # check if config file exists
        config = configparser.ConfigParser()
        config.read("config.ini")
    else:  # File could not be found
        print("Could not find config.ini file, using default fallbacks (your 'Downloads' folder)")
        config = "DEFAULT"

        # Set default save/temp locations to the download directory if not found in the config
    if "LOCATIONS" not in config or "Mp4TempFolder" not in config["LOCATIONS"]:
        config["LOCATIONS"]["Mp4TempFolder"] = rf"{os.path.join(Path.home(), 'Downloads')}"
    if "LOCATIONS" not in config or "M4aSaveFolder" not in config["LOCATIONS"]:
        config["LOCATIONS"]["M4aSaveFolder"] = rf"{os.path.join(Path.home(), 'Downloads')}"

    songs = []
    # This is where we decide if we download a playlist or nah
    if cmdargs.find_arg("-playlist"):  # we download a whole playlist
        # get user input
        full_urls = resolve_playlist(input("YouTube Playlist url: "))
        for full_url in full_urls:
            songs.append(full_url_to_id(full_url))
    else:  # Download from the file
        # Read input file line by line
        with open(config["INPUT"]["ScrapeFile"].strip(), 'r') as scrape_file:
            for song_line in scrape_file:
                song = song_line.strip()
                songs.append(song)

    # Exit condition if no songs were found
    if len(songs) < 1: exit(0)

    # Scrape all Videos
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(songs))
    loop.close()

    # Clean temp folder (argument -k missing)
    if not cmdargs.find_arg("-k"):
        clean_temp_folder(config["LOCATIONS"]["Mp4TempFolder"])
    else:
        print("Keeping temporary mp4 files.")

    print("Done. You can now close the window.")
