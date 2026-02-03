def selection_sort(arr):
    n=len(arr)
    for i in range(n):
        min_arr=i
        for j in range(i+1,n):
            if arr[j]<arr[min_arr]:
                min_arr=j
        arr[i],arr[min_arr]=arr[min_arr],arr[i]
    return arr
if __name__=='__main__':
    result=selection_sort([1,5,0,3,4,9])
    for i in result:
        print(i)
