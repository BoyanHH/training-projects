import math
A=670
xdots = [int(x) for x in range(0,A+1)]
ydots = [int(y) for y in range(0,A+1)]

max=0
contains = []
diff=0
d1=0
d3=0
d2=0
d4=0
h=0
print("a")
z=0
for d3 in xdots:
    d4=0
    while d4<A:
        d4+=1
        if(d1==d3):
                break;
        if(d2==d4):
               break;
        sq=d3-d1
        sq=sq*sq
        dq=d4-d2
        dq=dq*dq
        total=sq+dq
        len=math.sqrt(total)
        if(len.is_integer()):
           if len not in contains:
               diff+=1
               contains.append(len)
           if(len>max):
                max=len
print(d3,d4)            
print("Max len:"+str(max))
print("diff:"+str(diff))    
print(str(max)+" "+str(diff))
