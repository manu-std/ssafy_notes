import sys

from collections import deque 
sys.stdin = open('input.txt')
T = int (input())



def solve_using_selection_sort(arr:list):
        
    for i in range(0, len(arr),2):
        # 제일 큰 밸류의 idx 를 i 로 초기화하고
        # 큰 값과 i번째 값을 교환한다
        # 반복은 i번부터 돌아서 이미 검사한 값을 다시 검사하지 않도록한다 

        max_val_idx = i
        for idx in range(i, len(arr)):
            if arr[idx] > arr[max_val_idx]:
                max_val_idx = idx
        arr[max_val_idx], arr[i] = arr[i] , arr[max_val_idx]  

        # min 블록 제일 작은 것도 마찬가지
        min_val_idx = i+1
        for idx in range(i+1, len(arr)):
            if arr[idx] < arr[min_val_idx]:
                min_val_idx = idx
        arr[min_val_idx], arr[i+1] = arr[i+1], arr[min_val_idx]

    return arr
# sort 메서드를 활용한 간편한 풀이
def solve_using_sort(N, arr:deque):
    arr = deque(sorted(arr))
    ans_list = []
    for i in range(N):
        if not i % 2:
            ans_list.append(arr.pop())
        else:
            ans_list.append(arr.popleft())
    return ans_list

for tc in range(1,T+1):
    N = int(input())
    # arr_q = deque(map(int,input().split()))
    # ans_list = solve_using_sort(N, arr_q)
    arr = list(map(int,input().split()))
    ans_list = solve_using_selection_sort(arr)

    print(f'#{tc}', end=' ')
    print(*ans_list[:10])

