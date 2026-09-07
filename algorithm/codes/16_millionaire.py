# # 시간 초과 버전 

# T = int(input())

# for tc in range(1, T + 1):
#     N = int(input())
#     arr = list(map(int, input().split()))  
#     max_price = max(arr)
#     a= arr.index(max_price)
#     # print(a)
#     benefit = 0
#     for idx in range(len(arr)):
#         # 매 이터마다 뒤쪽을 다시 훑으므로, 시간복잡도 폭발 
#         max_price = max(arr[idx:])
#         if arr[idx]<max_price:
#             benefit += max_price-arr[idx]

#     print(f'#{tc} {benefit}')



import sys

sys.stdin = open('input.txt')
T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    arr = list(map(int, input().split()))  
    max_price = 0
    benefit = 0
    # 뒤에서 부터 돌아서 맥스를 들고 있는다
    for i in reversed(arr):
        if i> max_price:
            max_price = i
        
        if i < max_price:
            benefit += max_price-i

    print(f'#{tc} {benefit}')

