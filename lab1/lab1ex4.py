def ohms_law(R, V):
    return V/R

def series(r1, r2 ):
    return r1 + r2

def parallel(r1, r2):
    return (1/(1/r1 + 1/r2))

def parallel_three(r1, r2, r3):
    return (1/(1/r1 + 1/r2 + 1/r3))

r1=123; r2=234; r3=345; r4=456; r5=567; r6=678; r7=789;


result  = ohms_law(parallel_three(series(r1, r2), parallel(r3, r4), series(r5, parallel(r6,r7))), 12)

print(result)