import sys
from collections import deque
# 기본아이디어
# 다익스트라를 모르므로, D를 순회 하며, 
# 가능한 D의 최소값을 출력한다
sys.stdin = open('input.txt')
T = int(input())

def bfs(N:int, M:int, arr:list):

    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]


    D = 1
    while True:
        visited = [[False]*M for _ in range(N)]

        q = deque([(N-1, 0)])
        visited[N-1][0] = True

        while q:
            r, c = q.popleft()
            for i in range(4):
                nc = c+dc[i]

                # 비효율적인 반복이 숨어있다 i가 2,3 일때는 해당 반복을 돌 필요가 없지만
                # 시간이 부족하므로 여기까지....                   
                for d in range(1,D+1):
                    nr = r+dr[i]*d
                    if 0<= nc <M and 0 <= nr <N and not visited[nr][nc] and (arr[nr][nc] == 1 or arr[nr][nc] == 3):
                        q.append((nr,nc))
                        visited[nr][nc] = True
                        if arr[nr][nc] == 3:
                            # 깊은 반복을 탈출할때는 return으로 한방에 탈출!
                            return D
        D += 1

for tc in range(1, T+1):
    N ,M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    res = bfs(N, M, arr)

    print(f'#{tc} {res}') 