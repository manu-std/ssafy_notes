import sys 
import heapq

# 다익스트라
# 힙에 무엇을 넣어야하는지가 포인트가 아닐까
# 일단 좌표는 아님 (최솟값을 뽑는게 힙의 포인트인데 좌표의 최솟값은 의미가 없잖아)
# 어차피 지나간 길을 다시 지나가는건 생각할 필요가 없고,
# 최소기만 하면 되니까
# 민 퓨얼에는 도달하는데 소모한 연료의 누적합이 들어와야겠지?
sys.stdin = open('input.txt')

# 무한대로 초기화 하고 조정한다
INF = float('inf')
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
T = int(input())

def dijkstra(N, arr):
    min_fuel = [[INF]*N for _ in range(N)]    

    hq= []
    min_fuel[0][0] = 0
    # 힙큐 사용법에 유의
    heapq.heappush(hq,(min_fuel[0][0],0,0))

    while hq :
        val, r, c = heapq.heappop(hq)

        # 꺼낸 val값이 낡았으면 이번 루프를 통째로 넘어간다
        if val > min_fuel[r][c]:
            continue
        
        for idx in range(4):
            nr = r + dr[idx]
            nc = c + dc[idx]
            if 0 <= nr <N and 0<=nc<N :
                height_diff = arr[nr][nc]- arr[r][c]
                        
                if height_diff > 0:
                    new_val = 2 * height_diff + val
                    
                elif height_diff == 0: 
                    new_val = 1 + val
           
                else:
                    new_val = val
                
                if new_val< min_fuel[nr][nc]:
                    min_fuel[nr][nc] = new_val
                    heapq.heappush(hq,(min_fuel[nr][nc],nr,nc))
    return min_fuel[N-1][N-1]

for tc in range(1,T+1):
    N= int(input())
    arr= [list(map(int, input().split())) for _ in range(N)]
    result  = dijkstra(N, arr)


    print(f'#{tc} {result}')
    