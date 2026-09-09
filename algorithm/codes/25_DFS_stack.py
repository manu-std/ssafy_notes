import sys
sys.stdin = open('input.txt')

N, M = map(int, input().split())
arr = list(map(int, input().split()))

connection = [[] for _ in range(N+1)]

for i in range(1,len(arr),2):
    a = arr[i-1]
    b = arr[i]
    connection[a].append(b)
    connection[b].append(a)
    
visited = [False] * (N+1)
stack = [1]


res_list= []
while stack:
    a = stack.pop()
    if not visited[a]:
        for i in reversed(connection[a]):
            if visited[i]==False:
                stack.append(i)
        visited[a] = True
        res_list.append(a)

print(res_list)

