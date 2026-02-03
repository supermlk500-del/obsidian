def permutation(arr):
    def backtrack(path,choices):
        if len(path)==len(arr):
            result.append(path[:])
            return
        for i in range(len(choices)):
            path.append(choices[i])
            backtrack(path,choices[:i]+choices[i+1:])
            path.pop()
    result=[]
    backtrack([],arr)
    return result
arr=[1,2,3]
print(permutation(arr))
