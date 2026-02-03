arr=[1,2,3,4]
vistied=[]
def combination(num):
    if num==3:
        if sorted(vistied)==vistied:
            print(vistied)
        return
    for i in range(1,6):
        if i not in vistied:
            vistied.append(i)
            combination(num+1)
            vistied.remove(i)

combination(0)
