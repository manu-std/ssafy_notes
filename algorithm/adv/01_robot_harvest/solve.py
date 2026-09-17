import sys

sys.stdin = open('input.txt')
# 우 상 좌 하 (반시계 순서)
# 인덱스 +1 = 왼쪽으로 회전, -1 = 오른쪽으로 회전
dr = [0,-1,0,1]
dc = [1,0,-1,0]
# 수확 한 곳은 harv_cnt로 관리
def solve(r,c,d_idx):
    today = 1
    arr_copy = [row[:] for row in arr]  
    harv_cnt = [[0]*N for _ in range(N)]
    
    while today <= M:

        # 로봇 기준 오른쪽(d_idx-1)부터 시작해서 왼쪽으로 한 칸씩 돌며 확인
        # i=0 오른쪽, i=1 앞, i=2 왼쪽, i=3 뒤
        for i in range(4):
            n_d_idx= (d_idx-1+i) % 4
            nr = dr[n_d_idx] + r
            nc = dc[n_d_idx] + c
            can_move = 0 <= nr < N and 0<= nc <N and (arr_copy[nr][nc]==0 or 1< arr_copy[nr][nc] <= today)
            if can_move:
                
                break
        else: can_move = False; 

        # 오전에 할일들
        if arr_copy[r][c]==0 and can_move:
           
            arr_copy[r][c] = 5+harv_cnt[r][c]+today
                
            
        elif 1< arr_copy[r][c] <= today:
            arr_copy[r][c] = 0
            harv_cnt[r][c]+=1

        # 오후에 할일
        if can_move:
            r,c,d_idx = nr, nc, n_d_idx       

        today += 1 

    return sum(map(sum,harv_cnt))


        




T = int(input())
for tc in range(1, T+1):
    N, M = map(int, input().split())
    arr= [list(map(int,input().split())) for _ in range(N)]
    

    cand = []
    for r in range(N):
        for c in range(N):
            if arr[r][c]==0:
                cand.append((r,c))
    # 네 방향과 가능한 모든 스타트 위치를 본다
    max_val = 0
    for r,c in cand:
        for idx in range(4):
            tmp=solve(r,c,idx)
            if tmp> max_val:
                max_val = tmp


    print(f'#{tc} {max_val}')
