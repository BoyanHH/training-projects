##Suzdavame fail i pishem v nego.
try:
    file=open("aFile","w+")
##+ shte suzdade faila, ako ne sushtestvuva
    for a in range(10):
        file.write("%d"%(a))
        print("wrote",a)
except:
    pass
finally:
    file.write('\n')
    file.close()
    ##dobavqme tekst v kraq
try:
    file=open("aFile","a")
    for a in range(10,20):
        file.write("%d"%(a))
        print("wrote",a)
except:
    pass
finally:
    file.write('\n')
    file.close()
    ##chetem celiq fail
file=open("aFile","r")
##entire file
content=file.read()
print(content)
file.seek(0,0)
##line by line
f1 = file.readlines()
for i in range(len(f1)):
    for x in f1:    
        print("line %d %s"%(i,x))
        
