import shutil
import tempfile

# Python can't do this on its own apparently
class tempdir:
    def __enter__(self):
        self.tempdir = tempfile.mkdtemp()
        return self.tempdir

    def __exit__(self, *args):
        shutil.rmtree(self.tempdir, True)
