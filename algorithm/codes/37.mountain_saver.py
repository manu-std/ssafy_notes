import sys
import heapq
sys.stdin = open('input.txt')
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
INF = float('INF')
T = int(input())

for tc in range(1,T+1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]
    dist = [[INF]*N for _ in range(N)]
    hq = []
    heapq.heappush(hq, (0, 0, 0))
    dist[0][0] = 0
    while hq:
        
        c_cost, cr, cc = heapq.heappop(hq)
        if c_cost> dist[cr][cc]:
            continue
        for i in range(4):
            nr = dr[i] + cr
            nc = dc[i] + cc
             
            if 0 <= nr < N and 0 <= nc < N:
                if arr[nr][nc]>arr[cr][cc]:
                    n_cost = c_cost + (arr[nr][nc] - arr[cr][cc]) * 2
                elif  arr[nr][nc] == arr[cr][cc]:
                    n_cost = c_cost + 1
                else:
                    n_cost = c_cost

                if n_cost < dist[nr][nc]:
                    heapq.heappush(hq, (n_cost, nr, nc))
                    dist[nr][nc] = n_cost 
    ans = dist[N-1][N-1]
    
    print(f'#{tc} {ans}')
    