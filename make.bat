@echo off

:main
if %1 == init (
call :init
)

if %1 == install-pip-pkgs (
call :install-pip-pkgs
)

if %1 == download (
call :download
)

if %1 == full-reset (
call :full-reset
)

goto :end

:init
cd ..
md 101web\data\dumps
md 101web\data\resources
md 101web\data\views
md 101logs
md 101temps
md 101results
md 101diffs
cd 101worker
goto :end

:install-pip-pkgs
pip3 install gitpython
pip3 install jinja2
pip3 install pymongo
pip3 install inflection
goto :end

:download
python bin/download_resources
goto :end

:full-reset
rm -rf ../101web ../101logs ../101temps ../101results ../101diffs ../101test
goto :end

:end