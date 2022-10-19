import json
from pathlib import Path
import time
import shutil
from typing import BinaryIO, Literal, List
from urllib.parse import urlparse

from transmission_rpc import Client
import bencodepy


def add_torrent_and_skip_check(
        client: Client,
        torrent_find_path: BinaryIO | str | bytes | Path,
        download_dir: str,
        transmission_resume_path: Path,
        transmission_torrents_path: Path
):
    # Add torrent
    torrent = client.add_torrent(torrent_find_path, download_dir=download_dir, paused=True)

    # Get torrent hash, resume file path and torrent file path
    resume_path = transmission_resume_path.joinpath(f"{torrent.hashString}.resume")
    torrent_path = transmission_torrents_path.joinpath(f"{torrent.hashString}.torrent")

    # Get the torrent
    torrent = client.get_torrent(torrent.id)
    torrent_file_count = len(torrent.files())
    torrent_added_date = int(time.time())
    torrent_tracker_domain_list = [urlparse(tracker['announce']).netloc for tracker in torrent.trackers]

    # Copy the torrent file to current directory
    shutil.copy2(torrent_path, Path('./'))

    # Remove torrent
    client.remove_torrent(torrent.id, delete_data=False)

    # Generate resume data
    resume_data = {
        b'activity-date': 0,
        b'added-date': torrent_added_date,
        b'bandwidth-priority': 0,
        b'corrupt': 0,
        b'destination': bytes(download_dir, encoding='utf-8'),
        b'dnd': [0] * torrent_file_count,
        b'done-date': 0,
        b'downloaded': 0,
        b'downloading-time-seconds': 0,
        b'idle-limit': {
            b'idle-limit': 30,
            b'idle-mode': 0
        },
        b'labels': [],
        b'max-peers': 500,
        b'name': bytes(torrent.name, encoding='utf-8'),
        b'paused': 1,
        b'priority': [0] * torrent_file_count,
        b'progress': {
            b'blocks': b'all',  # Skip check
            b'have': b'all',  # Skip check
            b'time-checked': [torrent_added_date] * torrent_file_count,  # Skip check
        },
        b'ratio-limit': {
            b'ratio-limit': b'2.000000',
            b'ratio-mode': 0
        },
        b'seeding-time-seconds': 0,
        b'speed-limit-down': {
            b'speed-Bps': 100000,
            b'use-global-speed-limit': 1,
            b'use-speed-limit': 0
        },
        b'speed-limit-up': {
            b'speed-Bps': 100000,
            b'use-global-speed-limit': 1,
            b'use-speed-limit': 0
        },
        b'uploaded': 0
    }

    # Save the resume file
    with open(f"./{torrent.hashString}.resume", 'wb') as f:
        f.write(bencodepy.encode(resume_data))

    # Copy the resume file and torrent file to transmission-daemon
    shutil.copy2(f"./{torrent.hashString}.resume", resume_path)
    shutil.copy2(f"./{torrent.hashString}.torrent", torrent_path)

    # Add torrent again
    client.add_torrent(torrent_find_path, download_dir=download_dir, paused=True)

    print(f"Add torrent: {torrent.name}, download_dir: {download_dir}, tracker: {torrent_tracker_domain_list[0]}")

    # Clean up
    Path(f"./{torrent.hashString}.resume").unlink()
    Path(f"./{torrent.hashString}.torrent").unlink()


def main():
    # Get config from config.json
    config = json.load(open('./config.json', 'r'))

    protocol: Literal['http', 'https'] = config['protocol']

    username = config['username']
    if username == '':
        username = None
    password = config['password']
    if password == '':
        password = None

    host = config['host']
    port = config['port']
    client_path = config['path']
    transmission_resume_path = Path(config['transmission_resume_path'])
    transmission_torrents_path = Path(config['transmission_torrents_path'])
    default_download_dir = config['default_download_dir']

    torrent_find_path_list: List[Path] = []

    # Input torrent_find_path and download_dir
    torrent_find_path = input('Path or url of ONE torrent, press ENTER to use torrents in torrents folder: ')
    if torrent_find_path == '':
        for path in Path('./torrents').glob('*.torrent'):
            torrent_find_path_list.append(path)
    else:
        torrent_find_path_list.append(Path(torrent_find_path))

    download_dir = input('Full path of download directory, press ENTER to use default dir in config.json: ')
    if download_dir == '':
        download_dir = default_download_dir

    # Connect to client
    client = Client(protocol=protocol, username=username, password=password, host=host, port=port, path=client_path)

    # Add torrent and skip check
    for path in torrent_find_path_list:
        add_torrent_and_skip_check(client, path, download_dir, transmission_resume_path, transmission_torrents_path)

    # Clean up all *.torrent in ./torrents
    for path in Path('./torrents').glob('*.torrent'):
        path.unlink()


if __name__ == '__main__':
    main()
