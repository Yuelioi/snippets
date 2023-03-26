from pathlib import Path
import pysrt
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from yt_dlp import YoutubeDL
import os


from pydantic import BaseModel
from typing import List


class Caption(BaseModel):
    text: str
    start: float
    duration: float


def title_rename(y2bTitle):
    for ch in ['|', "'", '?', '\\', '/', '"', '<', '>', ':', '*']:
        if ch in y2bTitle:
            y2bTitle = y2bTitle.replace(ch, " ")
            y2bTitle = ' '.join(y2bTitle.split())
    return y2bTitle


def ffmpeg_convert(path: str):
    """
    @param path: full path without extension
    """
    if not os.path.exists(f'{path}.mp4'):
        video_type = ['.webm', '.mkv']
        for vtp in video_type:
            if os.path.exists(path + vtp):
                ffmpeg_param1 = 'ffmpeg -i ' + '"' + path + vtp + '" ' + \
                    '-vcodec copy -acodec copy "' + path + ".mp4" + '"'
                os.system(ffmpeg_param1)

    # 转换图片
    if not os.path.exists(f'{path}.jpg') and not os.path.exists(f'{path}.png'):
        ffmpeg_param2 = 'ffmpeg -i ' + '"' + path + '.webp' + '" ' + \
            '-vcodec copy -acodec copy "' + path + ".png" + '"'
        os.system(ffmpeg_param2)


def ytb_dl_download(url: str, out_path: str):
    '''
    :param url: like https://www.youtube.com/watch?v=77j7odhPV2c
    :param output_path: :G:/Motion/1.mp4
    :return: 贴图：webp 视频：webm。需要后续转化
    '''

    if not os.path.exists(f'{out_path}.mkv') and not os.path.exists(
        f'{out_path}.mp4'
    ):
        ydl_opts = {
            'outtmpl': out_path,
            'writethumbnail': True,
            'external_downloader': 'aria2c',
            'external_downloader_args': '-j 8 -s 8 -x 16 -k 1M',
            'proxy': '127.0.0.1:10809'
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    else:
        '视频已存在，跳过下载'

    # # 转换视频
    # ffmpeg_convert(out_path)

    v_path = f'{out_path}.mp4'
    t_path = f'{out_path}.png'
    return v_path, t_path


def yt_dlp_download(url: str, output_path: Path, down_sub: bool = False):
    # update: python -m pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz

    # todo: file name filter
    ydl_opts = {
        # 'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'writethumbnail': True,
        'external_downloader': 'aria2c',
        'external_downloader_args': '-c -j 8 -s 8 -x 8 -k 1M',
        'proxy': '127.0.0.1:10809',
        'format': 'bestvideo+bestaudio',
    }
    if down_sub:
        ydl_opts['writesubtitles'] = True
        ydl_opts['subtitlesformat'] = 'vtt'
        ydl_opts['writeautomaticsub'] = "auto"

    with YoutubeDL(ydl_opts) as ydl:
        if video_info := ydl.extract_info(url, download=False):

            video_title = video_info.get('title', "Untitled")
            video_title = title_rename(video_title)
            video_id = video_info.get("id", "NoID")

            current_path = f"{str(output_path)}/{video_title} {video_id}"

            ydl.params["outtmpl"]['default'] = f"{current_path}.%(ext)s"

            if not os.path.exists(f'{current_path}.mkv') and not os.path.exists(f'{current_path}.mp4') and not os.path.exists(f'{current_path}.webm'):

                ydl.download([url])
                # 转换视频
                ffmpeg_convert(str(current_path))
            elif not os.path.exists(f'{current_path}.mp4'):
                ffmpeg_convert(str(current_path))
            else:
                print("文件已存在")
            return current_path

    return None


def pytube_download(url, output_path):
    import socks
    import socket
    proxy_ip = "127.0.0.1"  # fill in your proxy ip
    proxy_port = 10809

    socks.set_default_proxy(socks.PROXY_TYPE_HTTP, proxy_ip, proxy_port)
    socket.socket = socks.socksocket

    youtubeObject = YouTube(url)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        if youtubeObject:
            youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


def get_captions_by_YouTubeTranscriptApi(video_id: str, langs: List[str] = ['en']) -> List[Caption]:
    """AI is creating summary for captions_get1

    Args:
        video_id (str): youtube video identifier
        langs (List[str], optional):  Defaults to ['en'].
            Available languages: en, ja, zh-Hans, zh-Hant, fr, de...

    Returns:
        List[Caption]: [description]
    """

    print('使用字幕引擎1')

    return YouTubeTranscriptApi.get_transcript(video_id, languages=langs)


def writeSub(captions):
    # 创建一个字幕对象
    subs = pysrt.SubRipFile()

    # 循环遍历每一个字幕
    for i in range(len(captions)):
        # 创建一个字幕条目
        caption = captions[i]
        sub = pysrt.SubRipItem(index=i + 1,
                               start=pysrt.SubRipTime(
                                   milliseconds=caption["start"]*1000),
                               end=pysrt.SubRipTime(milliseconds=(
                                   caption["start"] + caption["duration"])*1000),
                               text=caption["text"])
        # 将字幕条目添加到字幕对象中
        subs.append(sub)

    # 将字幕文件保存到磁盘中
    subs.save('my_subtitles.srt')


if __name__ == '__main__':

    script_dir = Path(__file__).resolve().parent
    os.chdir(script_dir)
    url = "https://www.youtube.com/watch?v=-IWSJamdVp4"

    yt_dlp_download(url=url, output_path=script_dir / "output", down_sub=True)

    # SAVE_PATH = ""
    # print("start download")
    # try:

    #     yt = YouTube(url)

    #     if h := yt.streams.filter(progressive=True).order_by(
    #             'resolution'):
    #         # h.download(SAVE_PATH)
    #         print(h)
    #         print('Video Downloaded!')
    # except Exception as e:
    #     print("Error occurred!\n", e)
    # print()
   # ffmpeg_convert(
   #     "H:\Snippets\Program-Learning\Python\Snippets\sub_progress\How to Color Your Animation and Comic⧸Webtoon Like a PRO (Cel Shading Tutorial)")
