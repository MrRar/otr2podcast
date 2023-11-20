import subprocess
from shutil import which

urls = [
    "https://archive.org/download/OTRR_Escape_Singles",
    "https://archive.org/download/OTRR_Dragnet_Singles",
    "https://archive.org/download/life-of-riley-1944-04-23-15-proxy-wedding-part-2",
    "https://archive.org/download/OTRR_This_Is_Your_FBI_Singles",
    "https://archive.org/download/OTRR_YoursTrulyJohnnyDollar_Singles",
    "https://archive.org/download/Speed_Gibson_Of_The_International_Secret_Police",
    "https://archive.org/download/OTRR_Gunsmoke_Singles",
    "https://archive.org/download/OTRR_Dimension_X_Singles",
]

command = "python"

if which("python3") is not None:
    command = "python3"

for url in urls:
    print("Converting: " + url)
    subprocess.run([command, "rss.py", url])
