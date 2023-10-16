import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
MY_OTHER = []
ARCHIVES = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'ZIP': ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()  # suffix[1:] -> .jpg -> jpg


def scan(folder: Path):
    for item in folder.iterdir():
        # Work with folder
        if item.is_dir():  # Check if item is folder
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        # Work with file
        extension = get_extension(item.name)  # Get file extension
        full_name = folder / item.name  # Get full path to file
        if not extension:
            MY_OTHER.append(full_name)
        else:
            if REGISTER_EXTENSION.get(extension) != '':
                EXTENSIONS.add(extension)
            else:
                UNKNOWN.add(extension)  # .mp4, .mov, .avi
                MY_OTHER.append(full_name)


if __name__ == '__main__':
    folder_process = sys.argv[1]
    scan(Path(folder_process))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images png: {PNG_IMAGES}')
    print(f'AUDIO mp3: {MP3_AUDIO}')
    print(f'Archives zip: {ARCHIVES}')
    print(f'EXTENSIONS: {EXTENSIONS}')
    print(f'UNKNOWN: {UNKNOWN}')
