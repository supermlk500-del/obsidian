arr = list(map(int,input().split()))
nums = arr[:-1]
target = arr[-1]
def erfen(nums,target):
    left,right = 0,len(nums)-1
    while left <= right:
        mid = (left + right) //2
        if target < nums[mid] :
            right = mid - 1
        elif target == nums[mid]:
            return mid
        else:left = mid + 1
    return -1

print(erfen(nums,target))

