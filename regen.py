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
    "https://archive.org/download/OTRR_Cloak_and_Dagger_Singles",
    "https://archive.org/download/OTRR_Space_Patrol_Singles",
    "https://archive.org/download/OTRR_Sound_of_War_Singles",
    "https://archive.org/download/OTRR_The_Six_Shooter_Singles",
    "https://archive.org/download/FrontierGentleman-All41Episodes",
    "https://archive.org/download/stories-of-sherlock-holmes-sa-85-04-28-x-the-sarussi-pea",
    "https://archive.org/download/OTRR_Black_Museum_Singles",
    "https://archive.org/download/OTRR_X_Minus_One_Singles",
    "https://archive.org/download/father-brown-xx-xx-xx-the-dagger-with-wings",
    "https://archive.org/download/OTRR_Case_Dismissed_Singles",
]

command = "python"

if which("python3") is not None:
    command = "python3"

for url in urls:
    print("Converting: " + url)
    subprocess.run([command, "rss.py", url])
