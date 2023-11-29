# -*- coding: utf-8 -*-
"""
UpgradeDate:2023-07-28

Author: Zhihao Cao
Paper: Detecting Latent Causation in Time Series
"""
import random
#print("Import GenerateData.py")

#0: Y → X
#1: X → Y
direction = 1
# Default choice is no noise
is_noise = 0

def CoupleFormulation(libsize_all):
    xs, ys = [], []
    x0, y0 = 0.5, 0.2
    xs.append(x0)
    ys.append(y0)   
    
    for i in range(libsize_all):
        x1 = 3.8*x0*(1.0-x0)-0.09*x0*y0      # Y → X
        y1 = 3.8*y0*(1.0-y0)-0.01*y0*x0      # X → Y 0.01
        x0, y0 = x1, y1
        xs.append(x0)
        ys.append(y0)
        
    if (direction == 1):
        return xs, ys, "X", "Y"
    else:
        return ys, xs, "Y", "X"


# Choose the combination of X, Y and Z
# 01-06 
# 07-12
flag = 12
# Main parameters
Bxy = 0.00          # Y → X
Byx = 0.35          # X → Y
Byz = 0.00          # Z → Y
Bzy = 0.00          # Y → Z
Bzx = 0.00          # X → Z
Bxz = 0.20          # Z → X
# Supplementary paremeters
Bzn = 0.00          # N → Z 
Bxn = 0.00          # N → X
Byn = 0.00          # N → Y

print("Network Structure")
if (Bxy != 0.0):
    print("Y → X",Bxy)
if (Byx != 0.0):
    print("X → Y",Byx)
if (Byz != 0.0):
    print("Z → Y",Byz)
if (Bzy != 0.0):
    print("Y → Z",Bzy)
if (Bzx != 0.0):
    print("X → Z",Bzx)
if (Bxz != 0.0):
    print("Z → X",Bxz) 
print("------------------------")

def CoupleFormulationThreeVariable2(libsize_all):
    xs, ys, zs = [], [], []
    # Initial values which are not important
    x0, y0, z0 = 0.5, 0.2, 0.1
    xs.append(x0)
    ys.append(y0)   
    zs.append(z0)
    for i in range(libsize_all):
        if (is_noise == 1):
            x1 = x0*(3.60 - 3.60*x0 - Bxy*y0 - Bxz*z0) + random.gauss(0,0.005)
            y1 = y0*(3.72 - 3.72*y0 - Byx*x0 - Byz*z0) + random.gauss(0,0.005)
            z1 = z0*(3.68 - 3.68*z0 - Bzx*x0 - Bzy*y0) + random.gauss(0,0.005)
        else:
            x1 = x0*(3.60 - 3.60*x0 - Bxy*y0 - Bxz*z0)
            y1 = y0*(3.72 - 3.72*y0 - Byx*x0 - Byz*z0)
            z1 = z0*(3.68 - 3.68*z0 - Bzx*x0 - Bzy*y0) 
        x0, y0, z0 = x1, y1, z1
        xs.append(x0)
        ys.append(y0)
        zs.append(z0)    
    if (flag == 1):   
        return xs, ys, zs, "X", "Y", "Z"  # Y → X
    elif(flag == 2):    
        return ys, xs, zs, "Y", "X", "Z"  # X → Y
    elif(flag == 3):
        return xs, zs, ys, "X", "Z", "Y"  # Z → X
    elif(flag == 4):
        return zs, xs, ys, "Z", "X", "Y"  # X → Z
    elif(flag == 5):
        return ys, zs, xs, "Y", "Z", "X"  # Z → Y
    elif(flag == 6):
        return zs, ys, xs, "Z", "Y", "X"  # Y → Z
    
    # X couple Z
    elif(flag == 7):
        return xs, xs, zs, "X", "X", "Z"  # X → X  S:Z    X |M( X + Z )
    elif(flag == 8):
        return zs, zs, xs, "Z", "Z", "X"  # Z → Z  S:X    Z |M( Z + X )
    # Z couple Y
    elif(flag == 9):
        return ys, ys, zs, "Y", "Y", "Z"  # Y → Y  S:Z    Y |M( Y + Z )
    elif(flag == 10):
        return zs, zs, ys, "Z", "Z", "Y"  # Z → Z  S:Y    Z |M( Z + Y )
    # X couple Y
    elif(flag == 11):
        return xs, xs, ys, "X", "X", "Y"  # X → X  S:Y   X |M( X + Y )
    elif(flag == 12):
        return ys, ys, xs, "Y", "Y", "X"  # Y → Y  S:X   Y |M( Y + X )

def CoupleFormulationFourVariable(libsize_all):
    xs, ys, zs, ns = [], [], [], []
    x0, y0, z0, n0 = 0.5, 0.2, 0.1, 0.1
    xs.append(x0)
    ys.append(y0)   
    zs.append(z0)
    ns.append(n0)
    for i in range(libsize_all):
        if (is_noise == 1):
            x1 = x0*(3.60 - 3.60*x0 - Bxy*y0 - Bxz*z0 - Bxn*n0) + random.gauss(0,0.005)
            y1 = y0*(3.72 - 3.72*y0 - Byx*x0 - Byz*z0 - Byn*n0) + random.gauss(0,0.005)
            z1 = z0*(3.68 - 3.68*z0 - Bzx*x0 - Bzy*y0 - Bzn*n0) + random.gauss(0,0.005)
            n1 = n0*(3.68 - 3.68*n0) + random.gauss(0,0.005)
        else:
            x1 = x0*(3.60 - 3.60*x0 - Bxy*y0 - Bxz*z0 - Bxn*n0)
            y1 = y0*(3.72 - 3.72*y0 - Byx*x0 - Byz*z0 - Byn*n0)
            z1 = z0*(3.68 - 3.68*z0 - Bzx*x0 - Bzy*y0 - Bzn*n0)
            n1 = n0*(3.68 - 3.68*n0)
        x0, y0, z0, n0 = x1, y1, z1, n1
        xs.append(x0)
        ys.append(y0)
        zs.append(z0)
        ns.append(n0)
    if (flag == 1):   
        return xs, ys, zs, "X", "Y", "Z"  # Y → X
    elif(flag == 2):    
        return ys, xs, zs, "Y", "X", "Z"  # X → Y
    elif(flag == 3):
        return xs, zs, ys, "X", "Z", "Y"  # Z → X
    elif(flag == 4):
        return zs, xs, ys, "Z", "X", "Y"  # X → Z
    elif(flag == 5):
        return ys, zs, xs, "Y", "Z", "X"  # Z → Y
    elif(flag == 6):
        return zs, ys, xs, "Z", "Y", "X"  # Y → Z
    # X couple Z
    elif(flag == 7):
        return xs, xs, zs, "X", "X", "Z"  # X → X  S:Z
    elif(flag == 8):
        return zs, zs, xs, "Z", "Z", "X"  # Z → Z  S:X
    # Z couple Y
    elif(flag == 9):
        return ys, ys, zs, "Y", "Y", "Z"  # Y → Y  S:Z
    elif(flag == 10):
        return zs, zs, ys, "Z", "Z", "Y"  # Z → Z  S:Y
    # X couple Y
    elif(flag == 11):
        return xs, xs, ys, "X", "X", "Y"  # X → X  S:Y
    elif(flag == 12):
        return ys, ys, xs, "Y", "Y", "X"  # Y → Y  S:X
    # N couple Z
    elif(flag == 13):
        return zs, zs, ns, "Z", "Z", "N"  # Z → Z  S:N
    elif(flag == 14):
        return ns, ns, zs, "N", "N", "Z"  # N → N  S:Y