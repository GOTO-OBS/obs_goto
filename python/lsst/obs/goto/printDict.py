from collections import Mapping, Set, Sequence

def printDict(a, path=['']):
    
    for k, v in a.items():
        path.append(k)
        if hasattr(v, 'keys'):
            printDict(v, path=path)
            path.pop()
        else:
            string = '.'.join([str(i) for i in path])
            print "{0}:{1}".format(string, v)
            path.pop()

