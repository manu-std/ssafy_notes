import sys
sys.stdin = open('input.txt')
T = int (input())



def selection_sorting(arr:list):
        
    for i in range(0, len(arr),2):
        
        max_val_idx = i
        min_val_idx = i+1
        for idx in range(i, len(arr)):
            if arr[idx] > arr[max_val_idx]:
                max_val_idx = idx
        arr[max_val_idx], arr[i] = arr[i] , arr[max_val_idx]  

        for idx in range(i+1, len(arr)):
            if arr[idx] < arr[min_val_idx]:
                min_val_idx = idx



        arr[min_val_idx], arr[i+1] = arr[i+1], arr[min_val_idx]

    return arr

def solve_using_sort(N, arr):
    arr.sort()
    ans_list = []
    for i in range(N):
        if not i % 2:
            ans_list.append(arr.pop())
        else:
            ans_list.append(arr.pop(0))
    return ans_list

for tc in range(1,T+1):
    N = int(input())
    arr = list(map(int,input().split()))
    # ans_list = solve_using_sort(N, arr)
    ans_list = selection_sorting(arr)

    print(f'#{tc}', end=' ')
    print(*ans_list[:10])

