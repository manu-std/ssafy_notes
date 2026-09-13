import sys 
import heapq

sys.stdin = open('input.txt')
INF = float('inf')
dr = [-1,1,0,0]
dc = [0,0,-1,1]
T = int(input())
for tc in range(1, T+1):
    N= int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]
    dist = [[INF]*N for _ in range(N)]

    hq = []
    dist[0][0] = 0 
    heapq.heappush(hq,(dist[0][0],0,0))
    while hq:
        cur_val, r, c = heapq.heappop(hq)
        if cur_val> dist[r][c]:
            continue

        for idx in range(4):
            nr = dr[idx]+r
            nc = dc[idx]+c
            if 0<=nr<N and 0<=nc<N:
                if arr[r][c] == arr[nr][nc] and cur_val + 1 < dist[nr][nc]:
                    dist[nr][nc]= cur_val + 1
                    heapq.heappush(hq,(dist[nr][nc],nr,nc))
                elif arr[r][c] > arr[nr][nc] and cur_val< dist[nr][nc]:
                    dist[nr][nc]= cur_val
                    heapq.heappush(hq,(dist[nr][nc],nr,nc))
                elif arr[r][c] < arr[nr][nc] and cur_val+ 2 * (arr[nr][nc]-arr[r][c]) < dist[nr][nc]:
                    dist[nr][nc]= cur_val+ 2 * (arr[nr][nc]-arr[r][c])
                    heapq.heappush(hq,(dist[nr][nc],nr,nc))
    print(dist[N-1][N-1])