def addDict(key,value,dictionary={}):
    if key in dictionary.keys():
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]
    
def sort(d):
    from operator import itemgetter
    for v in d.values():
        v.sort(key=itemgetter(1))

    a = sorted(d.items())      
    ans = {}

    for i in range(len(a)):
        k = a[i][0]
        count = 0
        for stop,stop_seq in a[i][1]:
            stop_seq = count
            addDict(k,(stop, stop_seq),ans)
            count+=1
    return ans
