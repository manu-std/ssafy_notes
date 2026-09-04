import sys
sys.stdin = open('input.txt')

T =int(input())
 
def solve(N):
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    snail_arr= [[0]*N for _ in range(N)]
    cur_r, cur_c = 0,0
    idx = 0
    for i in range(1, N**2+1):
        snail_arr[cur_r][cur_c] = i

        if not (0 <= cur_r+dr[idx] < N) or not (0 <= cur_c+dc[idx] < N) or snail_arr[cur_r+dr[idx]][cur_c+dc[idx]] !=0:
            idx = (idx+1) % 4

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