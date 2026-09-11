import sys
sys.stdin = open('input.txt')
sys.setrecursionlimit(10**6)

# 수색할 델타 행렬
dr = [-1,1,0,0]
dc = [0,0,-1,1]

def dfs(r,c,K, counter, cur_height):
    # 들어오자 마자 비지티드 처리를 한다
    visited[r][c]= True
    counter += 1

    # 들어온 순간 베스트는 지금 현재 카운터이다
    best = counter

    for idx in range(4):
        nr = r+dr[idx]
        nc = c+dc[idx]
        # 경계검사
        if 0 <= nr <N and 0<=nc <N and visited[nr][nc]==False:
            # 내려갈 수 있으면
            if arr[nr][nc]< cur_height:
                # 카운터 간만큼의 최대값을 계속 위쪽으로 퍼올림
                best = max(best, dfs(nr,nc,K,counter,arr[nr][nc]))
            elif arr[nr][nc]-K<cur_height:
                best = max(best, dfs(nr,nc,0,counter,cur_height-1))
    # 감을때 비지티드 처리 취소
    visited[r][c]= False
    # 더이상 갈 곳이 없으면 다시 감는다
    return best

     

    


T = int(input())

for tc in range(1, T+1):
    N, K = map(int,input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    visited = [[False]*N for _ in range(N)]
    max_indexes = []
    max_val = max(map(max, arr))
    for  r_idx, row in enumerate(arr):
        for c_idx, i in enumerate(row):
            if i==max_val:
                max_indexes.append((r_idx,c_idx))

    result= 0
    for r,c in max_indexes:
        tmp = dfs(r,c,K,0,max_val)
        if tmp > result:
            result = tmp
    print(f'#{tc} {result}')