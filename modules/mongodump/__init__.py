import os
import shutil

config = {
    'wantsfiles': False
}

def run(context):
    os.system('mongodump')
    os.system('tar -zcvf wiki_db.tar.gz dump')
    shutil.rmtree('dump')
    shutil.copy('wiki_db.tar.gz', context.get_env('dumps101dir'))
    os.unlink('wiki_db.tar.gz')

def test():
    pass
