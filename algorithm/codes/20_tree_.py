import sys
sys.stdin= open('input.txt')

V = int(input())
arr = list(map(int, input().split()))

connection = [[] for _ in range(V+1) ]

for i in range(1, len(arr),2):
    n = arr[i-1]
    m = arr[i]
    connection[n].append(m) 
    connection[m].append(n)

visited = [False] * (V+1)

stack =[1]

visited[1] = True
result = []
while stack:
    node = stack.pop()
    result.append(node)
    for a in reversed(connection[node]) :
        a = connection[node].pop()
        if visited[a] == False:
            stack.append(a)
            visited[a] = True

    

print(*result)