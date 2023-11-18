# otr2podcast

This is a Python script that generates podcast RSS XML files from a provided Internet Archive Old Time Radio program file list.


## Usage

Download the rss.py script. Make sure Python is installed. Install the Pillow Python module. The URL of a OTR radio program file list is needed. First go to the Internet Archive page for the program. Under download options click show all. Copy the URL from the browser address bar. Open a Command Prompt/Terminal window in the same directory as the rss.py script. Type `python3 rss.py`. Next paste the URL copied earlier. Make sure there is a space between rss.py and the URL. Press enter. If all went well, a new XML RSS file will appear in the output directory along with the podcast image. The podcast image is sized 3000x3000 to be compatible with Apple Podcasts.


## Caching

Files downloaded from the Internet Archive are stored in the cache directory. The cached files are always reused if they are present.


## Regenerate All Podcast Files

Run the command `python3 regen.py`
