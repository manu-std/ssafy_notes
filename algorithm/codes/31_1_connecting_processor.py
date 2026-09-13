import sys
sys.stdin = open('input.txt')

T  = int(input())
for tc in range(1,T+1):
    N  = int(input())
    arr= [list(map(int, input().split()))for _ in range(N)]
    core_idx_list = []

    for r in range(N):
        for c in range(N):
            if r==0 or r ==N-1 or c==0 or c==-1:
                continue 
            elif arr[r][c] == 1:
                core_idx_list.append((r,c))