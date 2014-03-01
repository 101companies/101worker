__author__ = 'Martin Leinberger'

import os
import git
import json
from datetime import datetime


class ChangeLog():
    filePath = "changes.json"
    savedRuns = 10

    def __init__(self):
        self.__log = json.load(open(ChangeLog.filePath, 'r')) if os.path.exists(ChangeLog.filePath) else []

    def add(self, changes):
        """
        @type changes: list of ChangeObject
        """
        entry = {
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "changes": [{"op": c.operation, "file": c.path} for c in changes]
        }

        while len(self.__log) >= ChangeLog.savedRuns:
            self.__log.pop()

        self.__log.insert(0, entry)

    def save(self):
        json.dump(self.__log, open(ChangeLog.filePath, 'w'), indent=4)

Changes = ChangeLog()