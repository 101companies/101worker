import os
import shutil

config = {
    'wantsfiles': False
}

def run(context):
    os.system('mongodump')
    os.system('tar -zcvf wiki_db.tar.gz dump')
    os.system('rm -rf dump')
    shutil.move('wiki_db.tar.gz', context.get_env('dumps101dir'))
