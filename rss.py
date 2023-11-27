import xml.etree.ElementTree as ET
import sys
from datetime import date
import urllib.parse
import urllib.request
from PIL import Image
import io
import os.path
import re

if len(sys.argv) == 1:
    print("example usage:\n\npython3 rss.py https://ia800901.us.archive.org/1/items/OTRR_Dragnet_Singles\n")
    exit()

base_url = sys.argv[1] + "/"
base_file_name = base_url.split("/")[-2]

def parsed_xml_from_url(base_url, file_name):
    file_path = "cache/" + file_name
    if not os.path.isfile(file_path):
        urllib.request.urlretrieve(base_url + file_name, file_path)
    return ET.parse("cache/" + file_name, ET.XMLParser(encoding = "cp1252")).getroot()

meta_root = parsed_xml_from_url(base_url, base_file_name + "_meta.xml")
collection_title = meta_root.find("title").text
description = meta_root.find("description").text
description_text = re.sub('(<.+?>)', "", description)

if len(description_text) > 4000:
    new_description = ""
    for line in description_text.split("\n"):
        if len(new_description) + len(line) < 4000:
            new_description += f"{line}<br />"
        else:
            break
    description = f"<blockquote>{new_description}</blockquote>"

if len(description_text) < 8:
    description = collection_title

license_url = meta_root.find("licenseurl") and meta_root.find("licenseurl").text or "http://creativecommons.org/licenses/by-nc-sa/3.0/us/"
creator = meta_root.find("creator") and meta_root.find("creator").text or "Old Time Radio Researchers Group"

output = f"""<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>{collection_title}</title>
<category>Old Time Radio</category>
<itunes:category text="History"></itunes:category>
<copyright>{license_url}</copyright>
<description><![CDATA[{description}]]></description>
<image><url>https://raw.githubusercontent.com/MrRar/otr2podcast/master/output/{base_file_name}.jpg</url></image>
<itunes:image href="https://raw.githubusercontent.com/MrRar/otr2podcast/master/output/{base_file_name}.jpg" />
<language>en</language>
<itunes:explicit>false</itunes:explicit>
<itunes:author>{creator}</itunes:author>
<author>{creator}</author>
<link>https://archive.org/details/{base_file_name}</link>
<generator>https://github.com/MrRar/otr2podcast</generator>
"""

files_parsed_xml = parsed_xml_from_url(base_url, base_file_name + "_files.xml")

for child in files_parsed_xml:
    file_name = child.attrib["name"]
    if not file_name.endswith(".mp3"):
        continue

    length_secs = round(float(child.find("length").text))
    title = child.find("title")!= None and child.find("title").text or file_name
    #author = child.find("artist").text
    album = child.find("album") != None and child.find("album").text or ""
    size_bytes = child.find("size").text
    year = ""
    month = ""
    day = ""

    date_pattern = re.compile(".*?(\d{2,4})[-/](\d{2})[-/](\d{2,4}).*")
    match = date_pattern.match(album) or date_pattern.match(title) or date_pattern.match(file_name)
    if match and match.group(1) and match.group(2) and match.group(3):
        if len(match.group(1)) == 4 or len(match.group(3)) == 2 and int(match.group(1)) > 12: # WTH Gunsmoke!
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
        else:
            month = match.group(1)
            day = match.group(2)
            year = match.group(3)
        
        if len(year) == 2:
            year = "19" + year
    
    episode_date = None
    try:
        episode_date = date.fromisoformat(f"{year}-{month}-{day}")
    except:
        print(f"Bad date: {year}-{month}-{day} for {file_name}")
        pass
    mp3_url = base_url + urllib.parse.quote(file_name)
    
    # pubDate format from https://stackoverflow.com/questions/12270531/how-to-format-pubdate-with-python
    output += f"""<item>
<description>{title}</description>
<guid isPermaLink="true">{mp3_url}</guid>
<itunes:summary>{title}</itunes:summary>
<enclosure length="{size_bytes}" type="audio/mpeg" url="{mp3_url}" />
<itunes:duration>{int(length_secs / 60)}:{length_secs % 60}</itunes:duration>
<link>{mp3_url}</link>
<pubDate>{episode_date and episode_date.strftime("%a, %d %b %Y %H:%M:%S %z") or ""}</pubDate>
<source url="{base_url}">{collection_title}</source>
<title>{title}</title>
</item>
"""

output += """</channel>
</rss>
"""

f = open("output/" + base_file_name + ".xml", "a")
f.truncate(0)
f.write(output)
f.close()


# Make the image file

image_file_name = ""

for child in files_parsed_xml:
    file_name = child.attrib["name"]
    if "thumb" in file_name:
        continue
    if child.attrib["source"] != "original":
        continue
    if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
        image_file_name = file_name
        break

image_path = "cache/" + image_file_name
if not os.path.isfile(image_path):
    urllib.request.urlretrieve(base_url + urllib.parse.quote(image_file_name), image_path)
image = Image.open(image_path).convert("RGB")

width, height = image.size

new_size = min(width, height)

left = (width - new_size) / 2
top = (height - new_size) / 2
image = image.crop((left, top, left + new_size, top + new_size))
image = image.resize((3000, 3000))
image.save("output/" + base_file_name + ".jpg", "JPEG")
