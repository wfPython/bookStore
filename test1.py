a=[1,3,5,6,7,8]
b=[]
for i in range(0,len(a)-1,2):
    b.append([a[i],a[i+1]])

print(b)