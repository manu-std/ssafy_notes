import sys
from collections import deque
sys.stdin= open('input.txt')

T = int(input())

# 기본 bfs 연습
# 모든 하위 노드를
#넓이 우선으로 방문

def bfs(E, N):
    # 트리를 레프트 라이트 배열로 입력
    left = [0]*(E+2)
    right = [0]*(E+2)
    visited = [False]*(E+2)
    q = deque()
    for i in range(E):
        a = arr[i*2]
        b = arr[i*2+1]
        if left[a] == 0:
            left[a] = b
        else: right[a] = b  
    # deque 초기값 밀어 넣기
    q.append(N)
    visited[N] = True
    # q가 마를때까지 반복
    while q:
        cur = q.popleft()
        if left[cur] != 0 and visited[left[cur]]==False:
                q.append(left[cur])
                visited[left[cur]]= True  
        if right[cur] != 0 and visited[right[cur]]==False:
            q.append(right[cur])
            visited[right[cur]] = True
    # boolean 타입은  0,1로 취급된다
    return sum(visited)

for tc in range(1, T+1):

    E, N = map(int, input().split())
    arr = list(map(int,input().split()))
    cnt = bfs(E, N)  

    print(f'#{tc} {cnt}')