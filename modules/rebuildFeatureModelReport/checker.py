import contribToClafer
import sys
import tempfile
import shutil
import os
import re
from subprocess import Popen, PIPE

def check(contribName):
  try:
    contribClafer = contribToClafer.contribToClafer(contribName)
  except Exception as e:
    return {'success': False, 'message': e.message}
  tempClaferf = tempfile.NamedTemporaryFile(dir=".", delete=True)
  shutil.copyfileobj(open("features.clf", "rb"), tempClaferf)
  tempClaferf.write(contribClafer)
  tempClaferf.flush()

  # compile to alloy
  claferProcess = Popen(["clafer-tools-0.3/clafer", "--mode=alloy", tempClaferf.name], stdout=PIPE, stderr=PIPE)
  (pid, code) = os.waitpid(claferProcess.pid, 0)
  result = {'success': code == 0}
  if code == 0:
    # check if satisfiable
    checkerProcess = Popen(["java", "-cp", "bin:lib/alloy/alloy4.jar", "org.softlang.clafer.SimpleSatChecker", tempClaferf.name + ".als"], stdout=PIPE)
    result['sat'] = checkerProcess.communicate()[0].startswith("1")
  else:
    errorMessage = claferProcess.communicate()[1]
    m = re.search(r'(.*):(.*)', errorMessage)
    if m:
      result['message'] = m.group(2).strip()
    else:
      result['message'] = errorMessage
  tempClaferf.close()
  claferFileName = tempClaferf.name + ".als"
  try:
    os.remove(tempClaferf.name + ".als")
  except OSError:
    pass
  return result







