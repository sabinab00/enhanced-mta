def addDict(key,value,dictionary={}):
    if key in dictionary.keys():
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

def getSequence(object):
    return object.stop_sequence

def sort(routes):
    new = {}
    # print("sort_d")
    for k,vs in routes.items():
        new_val = sorted(vs, key= getSequence)
        new[k] = new_val
    for k,vs in new.items():
        count = 0
        for v in vs:
            v.setStopSeq(count)
            count+=1
    return new

def findTopPath(paths):
    # sorted_paths = sorted(paths, key=lambda x:[ len(x[0]),x[2],x[1]])
    sorted_paths = sorted(paths, key=lambda x:[len(x[0]),x[1],x[2]])

    return sorted_paths

