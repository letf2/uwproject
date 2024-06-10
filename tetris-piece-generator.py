_A = {0 : 0, 1 : 1, 2 : 4}

def A(x):
    if x in _A:
        return _A[x]
    
    n = (x - 1).bit_length() - 1 if x != 1 else 1
    i = x - 2 ** n
    
    if i <= 2**(n-1):
        ret = A(2**n) + A(2**(n-1)+i) - A(2**(n-1))
    else:
        ret = 2*A(i) + A(i - 2**(n-1)) + 2*A(2**n) - 3*A(2**(n-1))
        
    _A[x] = ret
    return ret
