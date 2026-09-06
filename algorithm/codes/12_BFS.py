import sys
from collections import deque
sys.stdin = open('input.txt')

N, M = map(int, input().split())
arr = list(map(int, input().split()))
connection = [[] for _ in range(N+1)]
for i in range(0,len(arr),2):
    a = arr[i]
    b = arr[i+1]
    connection[a].append(b)
    connection[b].append(a)
visited = [False] * (N + 1)
q = deque([1])
visited[1] = True

res = ['1']
while q:
    now = q.popleft()
    for i in connection[now]:
        if not visited[i]:
            q.append(i)
            res.append(str(i))
            visited[i] = True

print ('-'.join(res))