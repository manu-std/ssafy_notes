import sys
from collections import deque
sys.stdin = open('input.txt')

T = int(input())

# 여러번 사용해야하므로, 함수로 추출한다
def bfs(n, adj)-> int:
    visited = [False]*(N+1)
    res_list = []
    q= deque([n])
    visited[n] = True
    while q:
        now = q.popleft()
        for item in adj [now]:
            if visited[item] == False:
                q.append(item)
                visited[item] = True     
                res_list.append(item)

    return len(res_list)

for tc in range(1,T+1):
    N = int(input())
    M = int(input())
    arr = [tuple(map(int, input().split())) for _ in range(M)]

    taller_than_me_list = [[] for _ in range(N+1)]
    smaller_than_me_list = [[] for _ in range(N+1)]
    for a, b in arr:
        taller_than_me_list[a].append(b)
        smaller_than_me_list[b].append(a)
    counter = 0
    for n in range(1,N+1):

        result = bfs(n, smaller_than_me_list)+bfs(n,taller_than_me_list)
        if result == N-1:
            counter += 1

    print(f'#{tc} {counter}')

