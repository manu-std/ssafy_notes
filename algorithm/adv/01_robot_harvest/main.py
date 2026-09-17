import sys
# sys.setrecursionlimit(10**7)

sys.stdin = open('input.txt')
dr = [0, -1, 0 ,1]
dc =[1,0,-1,0]
T = int(input())

def dfs (r,c,k, harv,dir):
    max_harv = harv

    nr=r
    nc=c
    n_dir = dir

    for idx in range(4):

        tmp_r = dr[(idx+dir)%4] + r
        tmp_c = dc[(idx+dir)%4] + c
        tmp_dir = (idx+dir)%4
        cond = 0<= tmp_r < N and 0<= tmp_c <N and (arr[tmp_r][tmp_c]== 0 or  arr[tmp_r][tmp_c] <= k)
        if cond:
            nr = tmp_r
            nc = tmp_c
            n_dir = tmp_dir
            can_move = True
            break
    else:
        can_move = False

    val = arr[r][c]
    if k < M:
        if val == 0:
            if can_move:
                arr[r][c] = k + 3

                max_harv= max(max_harv, dfs(nr,nc,k+1,harv,n_dir))
                arr[r][c]=0
            else:
                max_harv= max(max_harv, dfs(r,c,k+1,harv,n_dir))

        elif val <= k:
            if can_move:
                arr[r][c] = 0
                max_harv = max (max_harv, dfs(nr,nc,k+1,harv+1,n_dir))


            else:
                arr[r][c] = 0
                max_harv = max (max_harv,dfs(r,c,k+1,harv+1,n_dir))

        else:
            if can_move:
                max_harv = max(max_harv, dfs(nr, nc, k + 1, harv,n_dir))
            else:
                max_harv = max(max_harv, dfs(r, c, k + 1, harv,n_dir))

    if k>=M:
        return max_harv
    return max_harv







for tc in range(1, T+1):
    N , M = map(int, input().split())
    arr = [list(map(int,input().split())) for _ in range(N)]

    max_val = 0
    for i in range(N):
        for j in range(N):
            if arr[i][j]==0:
                for dir in range(4):
                    tmp =dfs(i,j,0,0,dir)
                    if tmp>max_val:
                        max_val =tmp

    print(max_val)
