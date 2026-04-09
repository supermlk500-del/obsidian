get = list(map(int,input().split()))
nums = get[:-2]
left = get[-2]
right = get[-1]
def he(nums):
    n = len(nums)
    p = [0] * (n+1)
    for i in range(1,n + 1):
        p[i] = p[i-1] + nums[i-1]
    return p
def res(p,left,right):
    return p[right+1] - p[left]

p = he(nums)
print(res(p,left,right))


