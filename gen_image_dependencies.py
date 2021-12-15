
import sys
from pathlib import Path
from bs4 import BeautifulSoup

FILENAME = Path(sys.argv[1])
PREFIX_DIR = Path(sys.argv[2])
DEPS_DIR = Path(sys.argv[3])
IMG_DIR = Path(sys.argv[4])

assert FILENAME.parts[0] == str(PREFIX_DIR)

DEPS_FILENAME_LIST = list(FILENAME.parts[1:])
DEPS_FILENAME_LIST.insert(0, str(DEPS_DIR))
DEPS_FILENAME = Path(*DEPS_FILENAME_LIST).with_suffix(".d")
DEPS_FILENAME.parent.mkdir(parents=True, exist_ok=True)

with open(FILENAME, "r") as html_file, open(DEPS_FILENAME, "w") as deps_file:
    soup = BeautifulSoup(html_file, "html.parser")
    print(f"{FILENAME}:", end="", file=deps_file)
    for img_el in soup.find_all("img"):
        print(f" {img_el['src'].replace('##IMG_DIR##', str(IMG_DIR))}", end="", file=deps_file)
    print("", end="\n", file=deps_file)
