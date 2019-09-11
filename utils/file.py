import os


def assert_src(src):
    if not src:
        return False
    if not os.path.exists(abspath(src)):
        return False
    return True


def assert_path(src, dest):
    if not src or not dest:
        return False
    if not os.path.exists(abspath(src)):
        return False
    return True


def abspath(path):
    return os.path.abspath(os.path.expanduser(path))


def set_working_dir(path):
    os.chdir(os.path.expanduser(os.path.abspath(os.path.dirname(path))))


def exists(path):
    return os.path.exists(abspath(path))


def dirname(path):
    return os.path.dirname(abspath(path))


def assure_parent(path):
    folder = dirname(abspath(path))
    if not exists(folder):
        print("making {}".format(folder))
        os.makedirs(folder)