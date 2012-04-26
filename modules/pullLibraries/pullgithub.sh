USAGE="$0 <githubrepository> <targetdirectory>"
GITHUB_REPOSITORY=${1?$USAGE}
TARGET_DIRECTORY=${2?$USAGE}

echo "  pullgithub.sh $1"
# clone the repository in target dir if not already present
if [ -d "${TARGET_DIRECTORY?}" ]
then
  echo "    Directory ${TARGET_DIRECTORY?} exist. Fine."
else
  echo "    Cloning ${GITHUB_REPOSITORY?}"
  cd `basename ${TARGET_DIRECTORY?}`
  git clone https://github.com/${GITHUB_REPOSITORY?}
  echo "    done"
fi

# pull the repository
cd ${TARGET_DIRECTORY?}
echo "    pulling ${GITHUB_REPOSITORY?}"
git pull -q
echo "    done"