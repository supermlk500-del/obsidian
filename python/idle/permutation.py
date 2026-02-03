str="abc"
visited=list()
def permutation(n):
    #先写递归的出口
    if n==3:
        print(visited)
    else:
        for i in str:
            if i not in visited:
                visited.append(i)
                permutation(n+1)
                visited.remove(i)
        
permutation(0)
