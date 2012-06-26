# Look up all metadata values, if any, for a certain metadata key
def valuesByKey(entry, key):
   return [ x[key]
                 for x in map(lambda u: u["metadata"], entry["units"])
                 if key in x ]
