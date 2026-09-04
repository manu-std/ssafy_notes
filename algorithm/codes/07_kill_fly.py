import sys
sys.stdin = open('input.txt')
# 기본 아이디어
# 적힌 대로 구현했습니다...
T = int(input())

def solve(N, M, arr):
    max_fly_count = 0
    for r in range(N-M+1):
        for c in range(N-M+1):

            # tmp는 매 (r,c)에서 다시 계산해야하므로, 
            # r/ c for 문 내부에서 초기화한다.

            tmp = 0
            for i in range(M):
                for j in range(M):
                    tmp += arr[r+i][c+j]
            # tmp 초기화 되기전에, 
            # tmp가 현재 max_fly_count 보다 크다면 상태를 업데이트 한다
            if tmp> max_fly_count:
                max_fly_count = tmp
    return max_fly_count


for tc in range(1,T+1):
    N , M  = map(int, input().split())
    arr = [list(map(int,input().split()))for _ in range(N)]

    max_fly_count = solve(N, M, arr)

    print(f'#{tc} {max_fly_count}')