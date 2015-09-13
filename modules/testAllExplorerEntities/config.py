# A float specifying the time in seconds that shall be spent collection errors
# per execution. For example, a value of '60' would mean that this module runs
# 60 seconds per worker cycle. Executions are incremental.
# A value of '0' means that on every execution all old results are invalidated
# and that the program runs until all calculations are finished.
incremental_update_time = 15

# This value specifies the maximal out-degree of the child entities added for
# each layer of recursion. For example, a value of '5' would mean that for each
# analyzed entity, only the first five child-entities are processed further.
# This is done because most nodes on the same layer usually yield the same
# errors.
# A value of '0' means that all for each entity all child-entities are analyzed.
# UNIMPLEMENTED AT THE MOMENT
max_out_degree = 5