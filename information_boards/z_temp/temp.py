def p(s):
    powerset = set()
    for i in xrange(2**len(s)):
        l = []
        for j, x in enumerate(s):
            if (i >> j) & 1:
                l += [x]
        subset = tuple(l)
        powerset.add(subset)
    return powerset


print p([2,3,4])
