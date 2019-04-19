def insert_sort(ilist):
    for i in range(len(ilist)):
        for j in range(i):
            if ilist[i] < ilist[j]:
                ilist.insert(j, ilist.pop(i))
                break
    return ilist

ilist = insert_sort([4, 5, 6, 7, 3, 2, 6, 9, 8])
print(ilist)

# 希尔排序
def shell_sort(lists):
    # 希尔排序
    count = len(lists)
    step = 2
    group = count / step
    while group > 0:
        for i in range(0, group):
            j = i + group
            while j < count:
                k = j - group
                key = lists[j]
                while k >= 0:
                    if lists[k] > key:
                        lists[k + group] = lists[k]
                        lists[k] = key
                    k -= group
                j += group
        group /= step
    return lists

# 堆排序
# 建堆


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[i]:
        largest = l
    if r < n and arr[r] > arr[i]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, i)

def heapSort(arr):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

# 冒泡排序
def bubble_sort(arr):
    count = len(arr)
    for i in range(0, count):
        for j in range(i + 1, count):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr

# 快速排序
# 最常见的排序方式
def quick_sort(array, left, right):
    if left >= right:
        return
    low = left
    high = right
    key = array[low]
    while left < right:
        while left < right and array[right] >= key:
            right -= 1
        array[left] = array[right]
        while left < right and array[left] <= key:
            left += 1
        array[right] = array[left]
    array[right] = key
    quick_sort(array, low, left-1)
    quick_sort(array, left+1 , high)
    return array
# 算法导论的方法
def quick_sort1(array, l, r):
    if l < r:
        q = partition(array, l, r)
        quick_sort1(array, l, q - 1)
        quick_sort1(array, q + 1, r)

    return array


def partition(array, l, r):
    x = array[r]
    i = l - 1
    for j in range(l, r):
        if array[j] <= x:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[r] = array[r], array[i + 1]
    return i + 1


list_q = quick_sort1([4, 5, 6, 7, 3, 2, 6, 9, 8, 10],0,9)
print(list_q)

