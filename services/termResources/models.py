
def lookup(term, resource, mapping, backlinks):
    if resource in mapping:
        if term in mapping[resource]:
            if mapping[resource][term] in backlinks:
                return backlinks[mapping[resource][term]][resource]
            else:
                return {'error' : "No backlinks found for " + mapping[resource][term]}
        else:
            return {'error' : "No mapping found for " + term}
    else:
        return {'error' : "Unknown resource " + '"' + resource + '"'}



