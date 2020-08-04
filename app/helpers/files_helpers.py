import pathlib
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet

from app import user_files


def upload_file(user, file):
    user_dir = user.get_dir()
    filename = secure_filename(file.filename)

    if not user_files.file_allowed(file, filename):
        return {'error': f'{filename} has forbidden extension'}

    file_path = user_dir / filename
    if file_path.exists():
        filename = user_files.resolve_conflict(user_dir, filename)
        file_path = user_dir / filename

    user_files.save(file, folder=str(user.id), name=filename)
    return {
        'name': file_path.stem,
        'extension': file_path.suffix,
        'fullname': filename,
        'size': file_path.stat().st_size,
        'path': str(file_path),
        'user_id': user.id
    }


def edit_file(user, file, new_filename):
    filename = secure_filename(new_filename)
    fullname = filename + file.extension
    old_path = Path(file.path)
    old_path.rename(path.with_name(fullname))
    new_path = user.get_dir() / fullname

    return {
        'name': filename,
        'fullname': fullname,
        'path': str(new_path)
    }


def delete_folder(path):
    for child in path.iterdir():
        if child.is_dir():
            delete_folder(child)
        else:
            path.unlink()
    path.rmdir()


# Below functions are not used currently
def encrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)


def decrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)
