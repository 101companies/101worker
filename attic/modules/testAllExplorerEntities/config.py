import os

# A float specifying the time in seconds that shall be spent collection errors
# per execution. For example, a value of '60' would mean that this module runs
# 60 seconds per worker cycle. Executions are incremental.
# A value of '0' means that on every execution all old results are invalidated
# and that the program runs until all calculations are finished.
incremental_update_time = 30

# An int specifying the maximal out-degree of child entities per entity added
# to the recursion. For example, a value of '5' would mean that for each
# analyzed entity, only the first five child-entities are processed further.
# This is done because most nodes on the same layer usually yield the same
# errors.
# A value of '0' means that all for each entity all child-entities are analyzed.
# Empirically we have found a good value to be '40'. It significantly reduces
# runtime will still capturing all types of errors.
max_out_degree = 40

# Perform a full run if the file "force_full_run" exists.
full_run_file = os.path.join(os.environ['worker101dir'], 'modules',
                             'testAllExplorerEntities', 'force_full_run.txt')
if os.path.exists(full_run_file):
    incremental_update_time = 0
    max_out_degree = 0
    os.remove(full_run_file)
