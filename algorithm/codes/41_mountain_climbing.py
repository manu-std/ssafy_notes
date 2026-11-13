import sys
import heapq
sys.stdin = open('input.txt')
T = int(input())

dr = [1, 0, 0]
dc = [0, -1, 1]
INF = float('INF')
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    dist = [[INF] * M for _ in range(N)]
    hq = []
    heapq.heappush(hq, (0, N-1, 0))
    dist[N-1][0] = 0

    while hq:
        cur_level, cr, cc = heapq.heappop(hq)
        if cur_level>dist[cr][cc]:
            continue
        for i in range(3):
            if i == 0 :

                for jump in range(-cr, N-cr):
                    nr = cr + dr[i] * jump       
                    nc = cc + dc[i]
                    if 0 <= nr < N and 0 <= nc < M and arr[nr][nc] != 0 and max(cur_level, abs(jump)) < dist[nr][nc]:

                        nxt = max(cur_level, abs(jump))
                        dist[nr][nc] =nxt

                        heapq.heappush(hq, (nxt, nr, nc))
            else:           
                nr = cr + dr[i]           
                nc = cc + dc[i]
                if 0 <= nr < N and 0 <= nc < M and cur_level<dist[nr][nc] and arr[nr][nc] != 0:
                    dist[nr][nc] = cur_level
                    heapq.heappush(hq, (cur_level, nr, nc))
                
    for r in range(N):
        for c in range(M):
            if arr[r][c] == 3:
                print(f'#{tc} {dist[r][c]}')

        



    # 출발지점은 언제나 0, N-1 
    # 목표지점은 3(완탐으로 검색해야할듯)
    # 1은 발판
    # 좌우 이동은 공짜 
    # 상하 이동은 가격을 매긴다
    # 델타 행렬을 박아넣고 델타 부터 다녀야할듯