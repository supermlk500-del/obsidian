def binary_search(arr,target):
    left=0
    right=len(arr)-1
    while left<=right:
        mid=(left+right)//2
        if arr[mid]==target:
            return mid
        elif arr[mid]<target:
            left=mid+1
        elif arr[mid]>target:
            right=mid-1
    return -1


def bubble_sort(arr):
    n=len(arr)
    for i in range(n):
        for j in range(0,n-i-1):
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
    return arr

arr=[5,3,55,44,21,8]
arr1=bubble_sort(arr)
print(arr1)
result=binary_search(arr1,44)
print(result)
