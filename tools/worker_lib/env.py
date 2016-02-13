import json
import os
from subprocess import Popen, PIPE

load_env = os.path.abspath('../tools/loadenv')
production_yaml = os.path.abspath('../configs/env/production.yml')

process = Popen([
    load_env,
    production_yaml], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()

env = json.loads(output)
