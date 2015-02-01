def stripregex(pattern, default=None):
    if pattern.startswith("#") and pattern.endswith("#"):
        return pattern[1:len(pattern) - 1]
    return default


def tolist(thing):
    return thing if isinstance(thing, list) else [thing]
