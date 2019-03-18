import math
#x e mejdu 1 i 12 vkl.
#y e necqlo chislo m/y 0 i 180 vkl.
#Chasut e m/y x i x+1 kogato ugulut mejdu dvete strelki e y gradusa
#po daden HH:MM da se opredeli ugulut mejdu dvete strelki.

flag=True

while(flag==True):
    try:
        hour=0
        minutes=-1
        while(hour<1 or hour>12 or minutes<0 or minutes>60):
            hour=int(input("Input hour"))
            minutes=int(input("input minutes"))
            flag=False
    except ValueError:
        print("Invalid input, try again")
        
        
print("Entered time: "+str(hour)+":"+str(minutes))
small_arrow=6*minutes
if(small_arrow>180):
    small_arrow=small_arrow - 360
#12 hours = 720 minutes = 0.5 degrees per minute
big_arrow=0.5*(60*hour+minutes)
if(big_arrow>180):
    big_arrow = big_arrow -360
answer=small_arrow-big_arrow
if(answer<0):
    answer*=-1
if(answer>0):
    answer = 360 - answer
print("{:.3f}".format(answer))

