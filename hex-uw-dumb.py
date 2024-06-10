from math import floor, log

#raw
#T = {-1: 0, 1: 2, 3: 8, 5: 16, 7: 26, 9: 40, 11: 56, 13: 74, 15: 94, 17: 118, 19: 146, 21: 174, 23: 202, 25: 236, 27: 274, 29: 312, 31: 352, 33: 396, 35: 446, 37: 496, 39: 542, 41: 598, 43: 656, 45: 714, 47: 772, 49: 836, 51: 908, 53: 978, 55: 1044, 57: 1116, 59: 1196, 61: 1276, 63: 1356, 65: 1440, 67: 1532, 69: 1624, 71: 1716, 73: 1814, 75: 1912, 77: 2008, 79: 2096, 81: 2208, 83: 2322, 85: 2434, 87: 2536, 89: 2650, 91: 2772, 93: 2892, 95: 3010, 97: 3134, 99: 3270, 101: 3406, 103: 3530, 105: 3664, 107: 3806, 109: 3946, 111: 4082, 113: 4224, 115: 4380, 117: 4536, 119: 4682, 121: 4830, 123: 4990, 125: 5154, 127: 5316, 129: 5480, 131: 5654, 133: 5828, 135: 6014, 137: 6182, 139: 6374, 141: 6548, 143: 6724, 145: 6916, 147: 7116, 149: 7304, 151: 7476, 153: 7676, 155: 7854, 157: 8078, 159: 8220, 161: 8478, 163: 8698, 165: 8918, 167: 9124, 169: 9342, 171: 9566, 173: 9784, 175: 9988, 177: 10218, 179: 10460, 181: 10700, 183: 10920, 185: 11148, 187: 11392, 189: 11638, 191: 11878, 193: 12122, 195: 12382, 197: 12644, 199: 12902, 201: 13166, 203: 13430, 205: 13686, 207: 13920, 209: 14188, 211: 14476, 213: 14758, 215: 15018, 217: 15286, 219: 15572, 221: 15858, 223: 16136, 225: 16418, 227: 16720, 229: 17028, 231: 17316, 233: 17606, 235: 17910, 237: 18216, 239: 18512, 241: 18810, 243: 19128, 245: 19454, 247: 19766, 249: 20070, 251: 20386, 253: 20714, 255: 21042, 257: 21368}

#trimmed
T = {-1: 0, 1: 2, 5: 16, 11: 56, 9: 40, 23: 202, 21: 174, 19: 146, 17: 118, 47: 772, 45: 714, 43: 656, 41: 598, 39: 542, 37: 496, 35: 446, 33: 396, 95: 3010, 93: 2892, 91: 2772, 89: 2650, 87: 2536, 85: 2434, 83: 2322, 81: 2208, 79: 2096, 77: 2008, 75: 1912, 73: 1814, 71: 1716, 69: 1624, 67: 1532, 65: 1440, 191: 11878, 189: 11638, 187: 11392, 185: 11148, 183: 10920, 181: 10700, 179: 10460, 177: 10218, 175: 9988, 173: 9784, 171: 9566, 169: 9342, 167: 9124, 165: 8918, 163: 8698, 161: 8478, 159: 8220, 157: 8078, 155: 7854, 153: 7676, 151: 7476, 149: 7304, 147: 7116, 145: 6916, 143: 6724, 141: 6548, 139: 6374, 137: 6182, 135: 6014, 133: 5828, 131: 5654, 129: 5480}

A = {1 : 1, 2 : 7}
C = {1 : 2}


s = lambda n : (A[n] + 6*n - 1) // 6
iit = lambda it, n : 6*it + 10 - 3*n + 3*A[n//2]  #only for use with powers of 2
diff = lambda n : 2 ** (n.bit_length()) - n 

    
def add(n, hat, beard, const):
    k = 2 ** (n.bit_length() - 1) 
    return 2 * s(k) + hat + beard + const - k


def get_const(n, hat, beard):
    return T[n] - add(n, hat, beard, 0)  #hack


def get_triangle(n):
    if n in T:
        return T[n]
    
    d = diff(n)
    t = 2 ** (n.bit_length() - 1)
    
    hat = get_triangle(t - d)
    beard = get_triangle(t - d - 2)

    if d not in C:
        #calculate const with min triangle. this is the bottleneck
        #and inevitably errors when we run out of n-triangles
        min_n = 2 ** (floor(log((d - 1) // 2, 2) + 3)) - d if d != 1 else 1  #fine to use logarithms since d is small
        min_t = 2 ** ((min_n).bit_length() - 1)

        C[d] = get_const(min_n, T[min_t - d], T[min_t - d - 2])

    ret = add(n, hat, beard, C[d])
    T[n] = ret 
    
    return T[n]


A_target = 4
while True:
    T_target = (A_target // 2) - 1  #to get A(2^{n+1}) requires T(2^{n-1} - 1) 

    target = get_triangle(T_target)
    A[A_target] = iit(target, A_target)

    print(f"A({A_target}) = {A[A_target]}")
        
    A_target *= 2


    
