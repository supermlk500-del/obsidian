def combination(arr,n):
    def backtrack(start,path):
        if len(path)==n:
            result.append(path[:])
            return
        for i in range(start,len(arr)):
            path.append(arr[i])
            backtrack(i+1,path)
            path.pop()
    result=[]
    backtrack(0,[])
    return result

print(combination([1,2,3,4,5],3))
