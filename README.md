# Transmission Skip Verify

[中文](./README.zh.md)

A simple Python script to help you skip verifying torrents in [Transmission](https://transmissionbt.com/) without restarting Transmission process.

**Warning: Use with caution! I am not responsible for any consequences.**

## Usage

1. Download this repository.

2. Make sure the script can access the Transmission's torrent file directory and resume file directory.
   
   The torrent file directory contains all torrent files <torrent_hash>.torrent.
   
   The resume file directory contains all resume files <torrent_hash>.resume.
   
   If Transmission runs in a Docker container, make sure that the torrent file directory and the resume file directory are mounted from the host to the Docker container.

3. Make sure that the Python 3 runtime exists.

4. Create config.json in repository folder according to config.json.template:

   + protocol: in "http" or "https"
   + host: IP address of Transmission Web
   + port: port of Transmission Web
   + path: no need to modify
   + username
   + password
   + transmission_resume_path: resume file directory. If Transmission runs in a Docker container, it is ** a path in the host**
   + transmission_torrents_path: directory of torrent files. If Transmission runs in a Docker container, it is **a path in the host**
   + default_download_dir: The default download directory when no download directory is specified at running. If Transmission runs in a Docker container, it is **a path in the container**

5. Run the script: `python3 main.py` or `python main.py`.

6. Enter the path or download link of the torrent. If you need to add multiple torrents at once, put the torrents folder and press ENTER. **The torrents folder will be emptied after running**.

7. Enter the download directory. If Transmission runs in a Docker container, it is **a path inside the container**. Press ENTER to use default_download_dir in config.json.

8. After running, start torrents manually.

## Thanks

+ [【原创】Transmission 手动跳过校验 教程.md](https://github.com/ylxb2016/PT-help/blob/master/PT%20Tutorial/%E3%80%90%E5%8E%9F%E5%88%9B%E3%80%91Transmission%20%E6%89%8B%E5%8A%A8%E8%B7%B3%E8%BF%87%E6%A0%A1%E9%AA%8C%20%E6%95%99%E7%A8%8B.md)
+ [transmission-rpc](https://github.com/trim21/transmission-rpc)
+ [bencode.py](https://github.com/fuzeman/bencode.py)