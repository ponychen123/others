import sys
import time

scale = 20
print("start")
for i in range(scale+1):
    a = "*"*i
    b = "."*(scale-i)
    c = i/scale*100
    print("\r",end=" ")
    print("{:^3.0f}%[{}->{}]".format(c,a,b),end="")
    sys.stdout.flush()
    time.sleep(1)
print("end")
