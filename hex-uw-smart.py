from math import factorial, floor, log, ceil


_t = {-1: 0, 1: 2, 3: 8, 5: 16, 7: 26, 9: 40, 11: 56, 13: 74, 15: 94, 17: 118, 19: 146, 21: 174, 23: 202, 25: 236, 27: 274, 29: 312, 31: 352, 33: 396, 35: 446, 37: 496, 39: 542, 41: 598, 43: 656, 45: 714, 47: 772, 49: 836, 51: 908, 53: 978, 55: 1044, 57: 1116, 59: 1196, 61: 1276, 63: 1356, 65: 1440, 67: 1532, 69: 1624, 71: 1716, 73: 1814, 75: 1912, 77: 2008, 79: 2096, 81: 2208, 83: 2322, 85: 2434, 87: 2536, 89: 2650, 91: 2772, 93: 2892, 95: 3010, 97: 3134, 99: 3270, 101: 3406, 103: 3530, 105: 3664, 107: 3806, 109: 3946, 111: 4082, 113: 4224, 115: 4380, 117: 4536, 119: 4682, 121: 4830, 123: 4990, 125: 5154, 127: 5316, 129: 5480, 131: 5654, 133: 5828, 135: 6014, 137: 6182, 139: 6374, 141: 6548, 143: 6724, 145: 6916, 147: 7116, 149: 7304, 151: 7476, 153: 7676, 155: 7854, 157: 8078, 159: 8220, 161: 8478, 163: 8698, 165: 8918, 167: 9124, 169: 9342, 171: 9566, 173: 9784, 175: 9988, 177: 10218, 179: 10460, 181: 10700, 183: 10920, 185: 11148, 187: 11392, 189: 11638, 191: 11878, 193: 12122, 195: 12382, 197: 12644, 199: 12902, 201: 13166, 203: 13430, 205: 13686, 207: 13920, 209: 14188, 211: 14476, 213: 14758, 215: 15018, 217: 15286, 219: 15572, 221: 15858, 223: 16136, 225: 16418, 227: 16720, 229: 17028, 231: 17316, 233: 17606, 235: 17910, 237: 18216, 239: 18512, 241: 18810, 243: 19128, 245: 19454, 247: 19766, 249: 20070, 251: 20386, 253: 20714, 255: 21042, 257: 21368}
A = {1 : 1, 2 : 7, 4 : 31, 8 : 127, 16 : 499, 32 : 1975, 64 : 7855, 128 : 31327, 256 : 125119, 512 : 500083, 1024 : 1999507}

s = lambda x : (A[x] + 6*x - 1) // 6

def ntoki(n):
    #i.e. T(n) -> T(k, i)
    k = n.bit_length()
    i = (((2 ** k) - n) - 1) // 2
    return k, i


def kiton(k, i):
    #T(k, i) -> T(n)
    return 2 ** k - 2 * i - 1


def reduceki(k, i):
    return ntoki(kiton(k, i))


def minki(i):
    #require 2^k - 2i - 1 > 2^(k - 1) - 1
    #-> i < 2^(k - 2)
    #-> k > log2(i) + 2
    #-> k = floor(log(i, 2) + 3) 
    
    k = floor(log(i, 2) + 3) if i != 0 else 1
    return k, i


def const(i):
    #initial conds
    if i in [-1, 0]:
        return 2
    
    k, i = minki(i)

    #get constituents k - 1, i and k - 1, i + 1
    
    #T = TSC - C_(i-1), TSC = T + C_(i-1)
    #T(k, i) = T(k-1,i) + T(k-1,i+1) + 2S(2^(k-1))  - 2^(k-1) + C_i
    #TSC(k,i)-C(i-1) = T(k1,i1) + T(k2,i2) + 2S(2^(k-1)) - 2^(k-1) + C_i
    #TSC(k,i)-C(i-1) = TSC(k1,i1) - C(i1 - 1) + TSC(k2,i2) - C(i2 - 1) + 2S(2^(k-1)) - 2^(k-1) + C_i
    #C_i = TSC(k,i) - C(i-1) - TSC(k1,i1) + C(i1 - 1)  - TSC(k2,i2) + C(i2 - 1) - 2S(2^(k-1)) - 2^(k-1)
    
    k1, i1 = reduceki(k-1,i)
    k2, i2 = reduceki(k-1,i+1)
    
    return tsc(k,i) - const(i-1) - tsc(k1,i1) - tsc(k2,i2) + const(i1-1) + const(i2-1) - 2*s(2**(k-1)) + 2**(k-1)


def c(n, i):
    if i > n or i < 0:
        return 0
    return factorial(n) // (factorial(i) * factorial(n - i))


a = lambda i, j : ((-1)**(i-j+1) * (c(i+1,j) + 2*c(i,j))) - 2*sum([(-1)**(n+j) * c(n,j) for n in range(0, i)])

def tsc(k, i):
    #use eqn 23 but leave out the constant term. more convenient this way
    return (2**k)*(1 - i) + (2 + sum([a(i, j) * A[2**(k + j)] for j in range(0, i+2)]))//6


"""
def ts(k, i_min, mint):
    #get T(k,0) with prev.
    return mint + sum([tsc(k-i-1,i) + 2*s(2**(k-i-1)) - 2**(k-i-1) for i in range(i_min)]) + const(i_min - 1) - const(0)


def ts(k, i_min, mint):
    #get T(k,0) with prev.
    return mint + sum([(2 + sum([a(i, j) * A[2**(k-i-1 + j)] for j in range(0, i+2)]))//6 + 2*s(2**(k-i-1)) for i in range(i_min)]) + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1)
"""

def ts(k, i_min, mint):
    #get T(k,0) with prev.
    b = lambda i : sum([a(j, j - i + 1) for j in range(i_min)])
    b = lambda i : sum([a(j - 1, j - i) for j in range(1, i_min+1)])
    
    return mint + (i_min*A[2**k] + sum([(b(i) + 2) * A[2**(k-i)] for i in range(1, i_min+1)]))//6 + const(i_min - 1) - const(0) + (2**(k-i_min))*(2**i_min + i_min - 1)

    return mint + (i_min*A[2**k] + sum([(b(i) + 2) * A[2**(k-i)] for i in range(1, i_min+1)]))//6 + const(i_min - 1) - const(0) + 2**k + (2**(k-i_min))*(i_min - 1)

    return mint + (i_min*A[2**k] + sum([(b(i) + 2) * A[2**(k-i)] for i in range(1, i_min+1)]))//6 + const(i_min - 1) - const(0) + i_min*(2**(k-i_min)) - 2**(k-i_min) + 2**k

    return mint + (i_min*A[2**k] + sum([(b(i) + 2) * A[2**(k-i)] for i in range(1, i_min+1)]))//6 + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1) + (2**k)*(2 - 2**(1-i_min))

    return mint + (sum([b(i) * A[2**(k-i)] for i in range(i_min+1)]) + 2*sum([A[2**(k-i-1)] for i in range(i_min)]))//6 + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1) + (2**k)*(2 - 2**(1-i_min))

    return mint + (sum([b(i) * A[2**(k-i)] for i in range(i_min+1)]) + 2*sum([A[2**(k-i-1)] for i in range(i_min)]))//6 + (2**k)*(2 - 2**(1-i_min)) + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1)

    return mint + (sum([b(i) * A[2**(k-i)] for i in range(i_min+1)]) + 2*i_min)//6 + (sum([A[2**(k-i-1)] for i in range(i_min)]) - i_min)//3 + (2**k)*(2 - 2**(1-i_min)) + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1)

    #k-i_min -> k inclusive
    return mint + (sum([b(i) * A[2**(k-i)] for i in range(i_min+1)]) + 2*i_min + 12*sum([s(2**(k-i-1)) for i in range(i_min)]))//6 + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1)

    #i = 0, j = 1
    return mint + (sum([(sum([a(i, j) * A[2**(k-i-1 + j)] for j in range(0, i+2)])) for i in range(i_min)]) + 2*i_min + 12*sum([s(2**(k-i-1)) for i in range(i_min)]))//6 + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1)

    return mint + (sum([(sum([a(i, j) * A[2**(k-i-1 + j)] for j in range(0, i+2)])) + 12*s(2**(k-i-1)) for i in range(i_min)]) + 2*i_min)//6 + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1)

    return mint + sum([(2 + sum([a(i, j) * A[2**(k-i-1 + j)] for j in range(0, i+2)])) + 12*s(2**(k-i-1)) for i in range(i_min)])//6 + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1)

    return mint + sum([(2 + sum([a(i, j) * A[2**(k-i-1 + j)] for j in range(0, i+2)]))//6 + 2*s(2**(k-i-1)) for i in range(i_min)]) + const(i_min - 1) - const(0) - (2**(k-i_min)) * (2**i_min - i_min - 1)




assert ts(3,1,_t[1])==26 and ts(4,1,_t[5]) == 94 and ts(6,2,_t[11])==1356 and ts(5,2,_t[3])==352 and ts(2,1,_t[-1])==8




