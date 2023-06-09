import os
import random
import string


def generate_random_string(size: int) -> str:
    return ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(size))


def avatar_upload_path(instance, filename):
    file_name, file_extension = os.path.splitext(filename)
    return 'avatars/{}/{}_{}{}'.format(
        'users' if instance.profile_type == 1 else 'drivers',
        file_name,
        generate_random_string(8),
        file_extension
    )