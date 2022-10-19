# Transmission Skip Verify

用于在 [Transmission](https://transmissionbt.com/) 中跳过种子验证的 Python 脚本。与其它方法相比，此脚本不需要重启 Transmission 进程。

**警告：谨慎使用！作者不为一切跳检造成的后果负责**

## 使用方法

1. 下载项目。

2. 确保脚本可以访问到 Transmission 的种子文件目录和 resume 文件目录。
   
   种子文件目录包含所有种子文件，文件命名方式为种子 hash.torrent。
   
   resume 文件目录包含所有种子的下载进度等信息，文件命名方式为种子 hash.resume。
   
   若 Transmission 运行在 Docker 容器中，则需确保种子文件目录和 resume 文件目录是从宿主机挂载到 Docker 容器中的。

3. 确保已配置 Python 3 运行环境。

4. 进入项目目录，依照 config.json.template 创建 config.json 文件。各字段如下：

   + protocol: 填写 "http" 或 "https"
   + host: 填写 Transmission Web 服务的 IP 地址。一般为本机，填 127.0.0.1
   + port: 填写 Transmission Web 服务的端口。一般为 9091。不可加双引号
   + path: 一般填 "/transmission/"，无需修改
   + username: 登录用户名
   + password: 登录密码
   + transmission_resume_path: resume 文件目录。若 Transmission 运行在 Docker 容器中，此路径应填写**宿主机内的路径**
   + transmission_torrents_path: 种子文件目录。若 Transmission 运行在 Docker 容器中，此路径应填写**宿主机内的路径**
   + default_download_dir: 运行时没有指定下载目录时的默认下载目录。若 Transmission 运行在 Docker 容器中，此路径应填写**容器内的路径**

5. 运行脚本：`python3 main.py` 或 `python main.py`。

6. 输入要跳过验证的种子的路径或下载链接，只能输入一条。如需要一次添加多个种子，请将种子放入项目 torrents 文件夹中，并直接按 ENTER 跳过。**种子添加完成后 torrents 文件夹将被清空**。

7. 输入下载目录。若 Transmission 运行在 Docker 容器中，此路径应填写**容器内的路径**。若按 ENTER 跳过，则使用 config.json 中的 default_download_dir 字段。

8. 此时脚本将进行跳过验证的操作。运行完成后，种子将处于暂停状态，请手动开始种子。

## 推荐使用场景

在多个 PT 站点进行辅种并跳过检测的操作：

1. 确保种子已下载完成。

2. 将其他需要辅种的 PT 站点的种子文件放入 torrents 文件夹中。

3. 运行脚本，跳过输入种子地址步骤，在第二步输入已完成种子内容的保存路径

4. 在 Transmission 界面中手动启动种子

## 工作原理

种子的校验状态被记录在 resume 文件中。修改 resume 文件，即可实现跳过检测。但既有的方法都需要重启 Transmission 进程，造成不便。

此脚本在运行时，先添加种子，依据获得的种子信息伪造出校验成功的 resume 文件，再将种子删除。之后将 resume 文件复制到 resume 文件目录中、种子文件复制到种子文件目录中。再次添加种子时，种子会处于校验完成的状态，从而实现了无重启跳检。

## 感谢

+ [【原创】Transmission 手动跳过校验 教程.md](https://github.com/ylxb2016/PT-help/blob/master/PT%20Tutorial/%E3%80%90%E5%8E%9F%E5%88%9B%E3%80%91Transmission%20%E6%89%8B%E5%8A%A8%E8%B7%B3%E8%BF%87%E6%A0%A1%E9%AA%8C%20%E6%95%99%E7%A8%8B.md)
+ [transmission-rpc](https://github.com/trim21/transmission-rpc)
+ [bencode.py](https://github.com/fuzeman/bencode.py)