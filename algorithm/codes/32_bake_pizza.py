import sys
from collections import deque
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1,T+1):
    N, M = map(int, input().split())
    Ci = deque(map(int, input().split()))
    q= deque()

    # 화덕의 개수만큼 피자를 미리 밀어넣음
    # 이때 치즈 양과, 인덱스를 함께 넣음
    for i in range(1, N+1):
        q.append((Ci.popleft(),i))

    # 큐가 마르기 직전까지(마지막 남은)
    while len(q) != 1:
        # 화덕을 직접 돌리기 보다는
        # 팝레프트 하고 어펜드로 화덕을 돌리는 것을 간접 구현
        a , index= q.popleft()
        a = a//2
        if a != 0:
            q.append((a, index))
        # 피자를 꺼내서 화덕에 빈자리가 생기면 새 피자를 넣는다
        elif len(Ci) != 0:
            q.append((Ci.popleft(), M-len(Ci)))

    print(f'#{tc} {q[0][1]}')
    