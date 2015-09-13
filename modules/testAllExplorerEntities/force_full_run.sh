touch force_full_run.txt  # this is being checked for in config.py
cd ../../  # should now be in 101worker dir
RUNONLY=testAllExplorerEntities make production.run
