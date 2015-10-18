import atexit
import shutil
import tempfile

def tempdir():
    tempdir = tempfile.mkdtemp()
    atexit.register(shutil.rmtree, tempdir, True)
    return tempdir
