from pathlib import Path
from filetype import guess_extension
from shutil import rmtree, unpack_archive
from sys import argv

def extract(archive_path : Path):
    archive_path = archive_path.resolve()
    file_type = guess_extension(archive_path)
    if not file_type in ['zip', 'tar', 'gz', 'xz', 'bz2']:
        return
    # Directory to unpack with archive name without extension
    extract_to = Path(archive_path.parent / archive_path.name.rsplit('.', 1)[0])
    # If the archive did not have an extension
    if (archive_path == extract_to):
        extract_to = extract_to.with_name(extract_to.name + '_')
    # If the directory to unpack is already exists and not empty
    if extract_to.exists() and extract_to.is_dir() and any(extract_to.iterdir()):
        rmtree(extract_to, ignore_errors=True)
    try:
        if file_type in ['zip', 'tar']:
            unpack_archive(archive_path, extract_to, file_type)
        elif file_type in ['gz', 'xz']:
            unpack_archive(archive_path, extract_to, file_type+'tar')
        elif file_type == 'bz2':
            unpack_archive(archive_path, extract_to, 'bztar')
        else:
            return
    except:
        return
    # Recursive unpacking for nested archives
    for extracted in extract_to.rglob('*'):
        if extracted.is_file():
            extract(extracted)

if __name__ == '__main__' and len(argv) > 1:
    extract(Path(argv[1]))
