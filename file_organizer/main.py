from pathlib import Path
import shutil
import sys
import file_parser
from normalize import normalize


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


def main(folder: Path):
    file_parser.scan(folder)
    for group_name in file_parser.REGISTERED_EXTENSIONS.keys():
        group = file_parser.REGISTERED_EXTENSIONS.get(group_name)
        category_name = group.get('category')
        for file_name in group.get('file_names'):
            if category_name == 'archives':
                handle_archive(file_name, folder / category_name / group_name)
            else:
                handle_media(file_name, folder / category_name / group_name)

    for file in file_parser.MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')

    for folder in file_parser.FOLDERS[::-1]:
        # Remove empty folders after sorting
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


if __name__ == '__main__':
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())
