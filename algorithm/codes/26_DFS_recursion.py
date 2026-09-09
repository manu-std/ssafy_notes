import sys
sys.stdin = open('input.txt')
sys.setrecursionlimit(10**6)
def recur(now):
    visited[now] = True
    res_list.append(now)

    for nxt in connection[now]:
        if not visited[nxt]:
            recur(nxt)
    
N, M = map(int, input().split())
arr = list(map(int, input().split()))

connection = [[] for _ in range(N+1)]

for i in range(1,len(arr),2):
    a = arr[i-1]
    b = arr[i]
    connection[a].append(b)
    connection[b].append(a)
visited = [False] * (N+1)
res_list = []
recur(1)

print(res_list)