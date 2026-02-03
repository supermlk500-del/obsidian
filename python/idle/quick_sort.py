def quick_sort(arr,start,end):
    #至少两个元素才能排序
    if start < end:
        mid=partition(arr,start,end)
        #左边的情况,递归
        quick_sort(arr,start,mid-1)
        #右边的情况,递归
        quick_sort(arr,mid+1,end)

def partition(arr,start,end):
    #取列表第一个为对照像
    temp=arr[start]
    while start<end:
        #从右边开始
        while arr[end]>=temp and start<end:
            end-=1
        #把右边的值放到左边
        arr[start]=arr[end]
        #从左边开始
        while arr[start]<=temp and start<end:
            start+=1
        #把左边的值放到右边
        arr[end]=arr[start]
    #上面的循环结束，位置就找到了
    arr[start]=temp
    return start

if __name__=='__main__':
    arr=[2,9,7,8,5,4]
    quick_sort(arr,0,len(arr)-1)
    print(arr)
