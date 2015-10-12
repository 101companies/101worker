#!/bin/bash
USAGE="$0 <githubrepository> <absoluteTargetDirectory>"
GITHUB_REPOSITORY=${1?$USAGE}
TARGET_DIRECTORY=${2?$USAGE}
CURRENT_DIRECTORY=`pwd`
echo "  pullgithub.sh ${GITHUB_REPOSITORY?} ${TARGET_DIRECTORY?}"

#----- clone the repository in target dir if not already present
if [ -d "${TARGET_DIRECTORY?}/.git" ]
then
  echo "    The directory ${TARGET_DIRECTORY?}/.git does exist. Just fine. No need to clone."
else
  echo "    The directory ${TARGET_DIRECTORY?}/.git does not exist. So we clone."
  if git clone https://github.com/${GITHUB_REPOSITORY?} ${TARGET_DIRECTORY?}
  then
    echo "    clone successful"
  else
    echo "    ERROR: clone failed."    
    exit 1
  fi
fi

#----- pull the repository
# get back to the directory where the script was before. 
# this is necessary as the target directory might be relative. 
cd ${TARGET_DIRECTORY?}
echo "    pulling ${GITHUB_REPOSITORY?} into ${TARGET_DIRECTORY?}"
if git pull
then
  echo "    pull successful"
else
  echo "    ERROR: pull failed."
  exit 2
fi
