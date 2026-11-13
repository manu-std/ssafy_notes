import sys
import heapq
sys.stdin = open('input.txt')
T = int(input())
for tc in range(1,T+1):

    N,M,K = map(int,input().split())

    ans_arr = [1]*N
    n = N//K
    while n:
        if sum(ans_arr) == M:
            break
        ans_arr[n*K-1] = 0 
        n -= 1 

    
    if sum(ans_arr) != M:
        score = M 
    else:
        score = 0
        cur_K = 0
        for  i in ans_arr:
            if i == 1:
                score +=1
                cur_K +=1
                if cur_K == K:
                    cur_K = 0
                    score *=2
            else:
                cur_K = 0 
    print(f'#{tc} {score}')
    

