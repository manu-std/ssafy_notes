import sys
from collections import deque

sys.stdin = open('input.txt')
N , M = map(int , input().split())
arr = [list(map(int, input())) for _ in range(N)]


def solve(N, M, arr):
    # 상우하좌 시계방향
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    q = deque()
# 0,0(문제에선 1,1)의 이동시간을 0으로 해야하므로, 
# -1 로 채운 배열을 visited 배열로 사용
    visited = [[-1]*M for _ in range(N)]

# q에 초기값을 밀어넣고 visited를 업데이트한다
# 세트이므로 항상 기억할 것
    q.append((0,0))
    visited[0][0] = 0

# q가 마를때까지
    while q:
        r, c = q.popleft()
        for idx in range(4):
            nr = dr[idx]+ r
            nc = dc[idx] + c
            if 0 <= nr < N and 0 <= nc < M and visited[nr][nc] == -1 and arr[nr][nc] == 1:
                q.append((nr,nc))
            # visited 어레이에서 나를 이끈 친구에서 1을 더한게 나
                visited[nr][nc] = visited[r][c] + 1
    return visited


visited = solve(N, M, arr)
print(visited[N-1][M-1])
            