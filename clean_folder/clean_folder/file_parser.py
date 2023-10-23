import sys
from pathlib import Path

GROUPS_BY_CATEGORIES = {
    'archives': ('ZIP', 'GZ', 'TAR'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'MY_OTHER': ()
}

REGISTERED_EXTENSIONS = {}

for category in GROUPS_BY_CATEGORIES.keys():
    for group in GROUPS_BY_CATEGORIES[category]:
        REGISTERED_EXTENSIONS[group] = {
            'category': category,
            'file_names': []
        }

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()
MY_OTHER = []


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()  # suffix[1:] -> .jpg -> jpg -> JPG


def scan(folder: Path):
    for item in folder.iterdir():
        # Work with folder
        if item.is_dir():  # Check if item is folder
            if item.name not in GROUPS_BY_CATEGORIES.keys():
                FOLDERS.append(item)
                scan(item)
            continue

        # Work with file
        extension = get_extension(item.name)  # Get file extension
        full_name = folder / item.name  # Get full path to file
        if not extension:
            MY_OTHER.append(full_name)
        else:
            if REGISTERED_EXTENSIONS.get(extension):
                REGISTERED_EXTENSIONS.get(extension).get('file_names').append(full_name)
                EXTENSIONS.add(extension)
            else:
                UNKNOWN.add(extension)  # .mp4, .mov, .avi
                MY_OTHER.append(full_name)


if __name__ == '__main__':
    folder_process = sys.argv[1]
    scan(Path(folder_process))
