def addDict(key,value,dictionary={}):
    if key in dictionary.keys():
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]
    
def sort_sequence_id(d):
    for v in d.values():
        v.sort()
    a = sorted(d.items())      
    ans = {}
    for i in range(len(a)):
        k = a[i][0]
        count = 0
        for stop in a[i][1]:
            addDict(k,stop,ans)
            count+=1
    return ans