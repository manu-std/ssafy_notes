import sys
from collections import deque
sys.stdin = open('input.txt')
T = int(input())

# 기본 아이디어
# 정류장을 정점으로, 한번 충전으로 갈 수 있는 이동을 간선으로 보면 그래프가 된다
# 그러면 최소 충전 횟수는 0번에서 N번까지의 최단 거리(간선 개수)와 같은 말이 된다
# 인접 리스트를 미리 만들지 않고, now+1 ~ now+K 범위를 훑어 그때그때 이웃을 뽑아낸다
# 최단 거리를 구해야 하므로 visited에 방문 여부가 아니라 충전 횟수를 담는다


for tc in range(1,T+1):
    # K 한번 충전으로 갈 수 있는 정류장 수
    # N 종점 정류장
    # M 충전기가 설치된 정류장 수
    # charger_list 충전기가 설치된 정류장 위치
    K, N, M = map(int, input().split())
    charger_list = list(map(int, input().split()))
 
    # 충전기의 위치 목록을, 위치로 바로 조회할 수 있는 표로 뒤집는다
    # charger_list에 in을 쓰면 매번 전체를 훑지만 road[i]는 한번에 끝난다
    # 크기의 기준은 충전기 개수 M이 아니라 정류장 번호의 최대값인 N이다
    road = [False] * (N + 1)
    for i in charger_list:
        road[i] = True

    # 방문 여부와 충전 횟수를 한 배열에 같이 담는다
    # 미방문을 0으로 두면 출발점의 실제 충전 횟수 0과 구분되지 않으므로 -1을 쓴다
    visited = [-1] * (N+1) 
    q = deque()
    q.append(0)
    
    # 출발점까지 오는데 든 충전 횟수는 0이다
    visited[0] = 0
    while q:
        now = q.popleft()
        # 인접 리스트가 없으므로, K 범위를 훑어 이웃을 직접 만들어낸다
        for idx in range(now+1, now+K+1):
            # 범위 검사를 road 인덱싱보다 앞에 두어야 IndexError를 막을 수 있다
            # 종점 N에는 충전기가 없을 수 있으므로 road와 별개로 검사한다
            # and가 or보다 먼저 묶이므로, 괄호가 없으면 종점이 나머지 검사를 전부 건너뛴다
            if idx<N+1 and (road[idx] or idx == N) and visited[idx] == -1 :
                q.append(idx)
                # 나를 넣어준 now의 충전 횟수에 1을 더한 값이 나의 충전 횟수이다
                # 큐에는 충전 횟수가 서로 다른 정류장이 섞여 있으므로
                # 카운터 변수 하나로 세는 방법은 쓸 수 없다
                visited[idx] = visited[now]+1
    # 큐가 비었는데 종점이 미방문이면 도달하지 못한 것이다
    # 04_elec_bus 처럼 예외를 던져 반복문을 탈출할 필요가 없다
    if visited[N] == -1:
        charge_count = 0
    else: 
        # 종점에 도착하는 것은 충전이 아니므로, 마지막에 더해진 1을 빼준다
        charge_count = visited[N]- 1

    print(f'#{tc} {charge_count}')
