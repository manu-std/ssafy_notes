import sys
sys.stdin = open('input.txt')

T =int(input())
 
def solve(N):
    # 우 하 좌 상 순으로  dr/ dc를 배치
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    snail_arr= [[0]*N for _ in range(N)]
    cur_r, cur_c = 0,0
    idx = 0
    # 1부터 N**2 까지 순회
    for i in range(1, N**2+1):
        # 먼저 현재 자리에 입력하고
        snail_arr[cur_r][cur_c] = i

        # 다음 이동 위치를 결정하기 위해 검사 (인덱스가 넘쳤거나, 이동 해야할 위치의 값이 0이 아닐때)
        if not (0 <= cur_r + dr[idx] < N) or not (0 <= cur_c + dc[idx] < N) or snail_arr[cur_r + dr[idx]][cur_c + dc[idx]] !=0:

            # 모듈러 연산을 통해 idx를 0 ~ 3 범위에서 클리핑한다
            idx = (idx + 1) % 4

        cur_r += dr[idx]
        cur_c += dc[idx]
    return snail_arr

for tc in range(1, T+1):
    N = int(input())

    snail_arr = solve(N)
    print(f'#{tc}')
    for row in snail_arr:
        for i in row:
            print(i, end = ' ')
        print()