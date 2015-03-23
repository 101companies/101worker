#!/usr/bin/python
import sys, os, shutil, grp, pwd

env = os.getenv('DJANGO_ENV') or 'development'
uid = int(os.getenv('SUDO_UID'))
gid = int(os.getenv('SUDO_GID'))
user = os.getenv('SUDO_USER')
manage_path = os.path.abspath('./manage.py')


settings_target_file = 'services/settings.py'
settings_file = 'services/settings_{}.py'.format(env)
shutil.copy2(settings_file, settings_target_file)
os.chown(settings_target_file, uid, gid)

os.system('sudo pip install -r requirements.txt')

if env == 'production':
    os.system('apt-get install nginx')
    shutil.copy2('deploy/worker.101companies.org.conf', '/etc/nginx/sites-enabled/worker.101companies.org.conf')
    os.system('service nginx restart')

os.system('su - {} -c "{} runserver"'.format(user, manage_path))
