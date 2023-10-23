from pathlib import Path
import shutil
import sys
from .file_parser import scan, REGISTERED_EXTENSIONS, MY_OTHER, FOLDERS
from .normalize import normalize


def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / (normalize(Path(file_name.name).stem) + file_name.suffix))


def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(Path(file_name.name).stem)
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def clean(path: str):
    folder = (Path.cwd() / Path(path)).resolve()
    scan(folder)
    for group_name in REGISTERED_EXTENSIONS.keys():
        group = REGISTERED_EXTENSIONS.get(group_name)
        category_name = group.get('category')
        for file_name in group.get('file_names'):
            if category_name == 'archives':
                handle_archive(file_name, folder / category_name / group_name)
            else:
                handle_media(file_name, folder / category_name / group_name)

    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')

    for folder in FOLDERS[::-1]:
        # Remove empty folders after sorting
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


if __name__ == '__main__':
    if sys.argv[1]:
        clean(sys.argv[1])
    else:
        print("Path to folder not provided")
