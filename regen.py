import subprocess

urls = [
    "https://archive.org/download/OTRR_Escape_Singles",
    "https://archive.org/download/OTRR_Dragnet_Singles",
    "https://archive.org/download/life-of-riley-1944-04-23-15-proxy-wedding-part-2",
]

for url in urls:
    print("Converting: " + url)
    subprocess.run(["python3", "rss.py", url])
