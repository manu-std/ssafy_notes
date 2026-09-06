import sys
sys.stdin = open('input.txt')

T = int(input())
# 기본 아이디어
# 이차원 배열을 완전 탐색하되, 
# 최대한 반복문을 줄이기 위해 
# 한번의 반복문 안쪽에서 
# 최대한 수행할 수 있는 계산을 모두 수행


def solve(N, M, arr):
    # 십자 모양의 델타 행렬
    dr_plus = [-1, 0, 1, 0]
    dc_plus = [0, 1, 0, -1]

    # X 모양의 델타행렬
    dr_x = [-1,-1, 1, 1]
    dc_x = [-1, 1, 1, -1]

    # 최종 출력을 위한 변수
    max_fly_kill_count = 0

    # 완전탐색 
    for r in range(N):
        for c in range(N):

            # 이 자리의 계산값을 담을 변수들
            tmp_plus = arr[r][c]
            tmp_x = tmp_plus

            # 뻗어나가는 칸수를 표현
            for i in range(1, M):
                for idx in range(4):

                    # 십자 모양의 인덱스 클리핑을 위한 조건문
                    if 0 <= dr_plus[idx]*i + r< N and 0 <= dc_plus[idx]*i + c< N:
                        tmp_plus += arr[dr_plus[idx]*i + r][dc_plus[idx]*i + c]

                    # X 모양의 인덱스 클리핑을 위한 조건문
                    if 0 <= dr_x[idx]*i + r < N and 0 <= dc_x[idx]*i + c< N:
                        tmp_x += arr[dr_x[idx]*i + r][dc_x[idx]*i + c]

             
            if max_fly_kill_count< tmp_plus:
                max_fly_kill_count = tmp_plus
            # 앞의 조건을 만족하면 뒤 조건을 검사하지 않는 
            # elif는 사용하지 않고 두번 검사 
            if max_fly_kill_count < tmp_x:
                max_fly_kill_count = tmp_x
    return max_fly_kill_count


for tc in range(1, T+1):
    # N: 배열의 행렬
    # M: 중심을 포함에 뻗어나가는 칸수
    N , M = map(int, input().split())
    arr =[list(map(int, input().split())) for _ in range(N)]

    max_fly_kill_count = solve(N, M, arr)
    print(f'#{tc} {max_fly_kill_count}')
                        
