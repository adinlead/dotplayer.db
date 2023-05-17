import time
from datetime import datetime
from typing import List
from xml.dom import minidom

"""
<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" version="1">
<trackList>
<track>
  <title>Another Song Title</title>
  <creator>Another Artist Name</creator>
  <album>Another Album Title</album>
  <location>http://example.com/another_song.mp3</location>
  <image>http://example.com/another_artwork.jpg</image>
  <duration>240000</duration>
</track>
</trackList>
</playlist>

在 XSPF 文件中，<track> 元素是用来描述单个媒体项的。其中一些标签是必须的，而其他标签则是可选的。
以下是 track 元素中必须出现的标签：
<location>：指定媒体文件的位置。这通常是一个 URL 或本地文件路径。
<title>：指定媒体文件的标题或名称。这是人类可读的字符串，用于标识媒体文件。
<creator>：指定媒体文件的作者或制作人。
除了上述必须出现的标签之外，还有许多其他标签用于提供更详细的信息和元数据。例如：
<duration>：指定媒体文件的持续时间，以毫秒为单位。
<album>：指定包含媒体文件的专辑名称。
<image>：指定与媒体文件相关联的图像。这通常是专辑封面或艺术家图片。
<trackNum>：指定媒体文件在专辑或播放列表中的曲目编号。
需要注意的是，并非所有播放器都支持 XSPF 文件的所有标签。不同的播放器可能会忽略某些标签，或者使用它们提供的默认值。因此，在创建 XSPF 文件时，请考虑您的目标播放器所支持的标签和功能。
"""


def read_lines(input_file_path: str) -> List[str]:
    with open(input_file_path, "r") as r:
        return r.readlines()


def write_to_file(output_file_path: str, tracks: list) -> None:
    with open(output_file_path, "w") as w:
        xml = '<?xml version="1.0" encoding="UTF-8"?><playlist xmlns="http://xspf.org/ns/0/" version="1"><trackList>'
        for track in tracks:
            xml = xml + track
        xml = xml + "</trackList></playlist>"
        w.write(minidom.parseString(xml.replace("&", "&amp;")).toprettyxml(indent="    "))


def convert_600(input_file_path: str, output_file_path: str) -> None:
    try:
        tracks = []
        for line in read_lines(input_file_path):
            split = line.index(",http")
            if split > 0:
                tracks.append('<track>'
                              '<title>%(title)s</title>'
                              '<creator>%(creator)s</creator>'
                              '<location>%(url)s</location>'
                              '<duration>%(ts)s</duration>'
                              '</track>' % {
                                  "title": line[:split].strip(),
                                  "creator": "Unknown",
                                  "url": line[split + 1:].strip(),
                                  "ts": -1
                              })
        write_to_file(output_file_path, tracks)
    except Exception as e:
        raise RuntimeError(e)


def convert_md(input_file_path: str, output_file_path: str) -> None:
    """
    终止：资源不可用
    """
    doc_time_key = ",时长:"
    doc_time_key_len = len(doc_time_key)
    doc_name_key = "-"
    tracks = []
    last_line = ""
    for line in read_lines(input_file_path):
        if line and last_line:
            doc_time_split = last_line.find(doc_time_key)
            if line.find("http") == 0 and last_line.find("#EXTINF") == 0 and doc_time_split > 0:
                doc = last_line[doc_time_split + doc_time_key_len:]
                time_split = doc.find(doc_name_key)
                time_info = doc[:time_split]
                ts = -1
                if len(time_info) == 5:
                    ts = int(datetime.strptime(time_info, '%M:%S').timestamp()) * 1000
                elif len(time_info) == 8:
                    ts = int(datetime.strptime(time_info, '%H:%M:%S').timestamp()) * 1000
                title = doc[time_split + 1:]
                if title.find(doc_name_key) > 0:
                    creator_like = title[title.rfind(doc_name_key)+1:]
                    print(title.strip(), '  |  ', creator_like)
                creator = "Unknown"

                tracks.append('<track>'
                              '<title>%(title)s</title>'
                              '<creator>%(creator)s</creator>'
                              '<location>%(url)s</location>'
                              '<duration>%(ts)s</duration>'
                              '</track>' % {
                                  "title": title,
                                  "creator": creator,
                                  "url": line,
                                  "ts": ts
                              })
            pass
        last_line = line
    pass


if __name__ == '__main__':
    convert_md("/home/adinlead/Documents/md.m3u", "/home/adinlead/Documents/md.xspf")
