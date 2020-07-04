from app.models import File


def has_permission(file, user_id):
    if not file or file.user_id != user_id:
        return False
    return True
