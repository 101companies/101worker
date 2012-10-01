Clone/pull "101repo" to show up in "101results".

pullRepo.py is a generic script for cloning/pulling a repo into a directory

pull101Repo.py pulls the 101repo into the 101results folder

pullGitdeps.py uses the .gitdeps file in the 101repo folder to pull additional dependencies like other contributions. It then saves the .gitdeps file to check for changes when the script is executed next time.
