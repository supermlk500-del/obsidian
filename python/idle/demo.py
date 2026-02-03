def quick_sort(arr,start,end):
    if start<end:
        mid=depart(arr,start,end)
        quick_sort(arr,start,mid-1)
        quick_sort(arr,mid+1,end)

def depart(arr,start,end):
    temp=arr[start]
    while start<end:
        while arr[end]>=temp and start<end:
            end-=1
        arr[start]=arr[end]
        while arr[start]<=temp and start<end:
            start+=1
        arr[end]=arr[start]
    arr[start]=temp 
    return start
arr=[8,4,6,5,9,2]
quick_sort(arr,0,len(arr)-1)
print(arr)
            
