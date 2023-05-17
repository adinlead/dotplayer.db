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
"""


def convert600(input_file_path: str, output_file_path: str) -> None:
    try:
        xml = '<?xml version="1.0" encoding="UTF-8"?><playlist xmlns="http://xspf.org/ns/0/" version="1"><trackList>'
        with open(input_file_path, "r") as r:
            for line in r.readlines():
                split = line.index(",http")
                if split > 0:
                    xml = xml + ('<track>'
                                 '<title>%(title)s</title>'
                                 '<creator>%(creator)s</creator>'
                                 '<location>%(url)s</location>'
                                 '</track>' % {
                                     "title": line[:split].strip(),
                                     "creator": "Unknown",
                                     "url": line[split + 1:].strip()
                                 }).replace("&", "&amp;")
        xml = minidom.parseString(xml + "</trackList></playlist>").toprettyxml(indent="    ")
        with open(output_file_path, "w") as w:
            w.write(xml)
    except Exception as e:
        raise RuntimeError(e)


if __name__ == '__main__':
    convert600("600.txt", "600.xspf")
