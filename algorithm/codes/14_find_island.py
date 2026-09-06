import sys
from collections import deque
sys.stdin = open('input.txt')

# 기본 아이디어
# BFS를 한번 돌리면 연결된 땅이 전부 visited로 찍히므로,
# 나중에 같은 섬의 다른 칸을 만나도 이미 방문한 상태라 그냥 지나가게 된다
# 즉 BFS를 새로 시작하게 되는 횟수가 곧 섬의 개수이다
# 최단거리를 묻는 문제가 아니므로 거리는 세지 않고 방문 여부만 사용한다

N , M = map(int, input().split())
# 입력이 '11000' 형태의 문자열이므로, split 없이 map(int, ...)로 한글자씩 끊는다
arr = [list(map(int, input())) for _ in range(N)]
# 격자와 같은 크기의 방문 배열
# [[False]*M]*N 은 같은 행을 N번 참조하게 되므로 반드시 컴프리헨션으로 만든다
visited = [[False]*M for _ in range(N)]
# BFS가 끝나면 큐는 반드시 비어있으므로, 섬마다 새로 만들지 않고 재사용한다
q = deque()
# 최종 출력을 위한 변수
isla_count = 0

# 시작점이 정해져 있지 않고 모든 칸이 후보이므로, 격자 전체를 훑는다
for r in range(N):
    for c in range(M):
        # 땅이면서 아직 방문하지 않았다면, 이전 섬들과 이어지지 않은 새로운 섬이다
        if arr[r][c] == 1 and visited[r][c] == False:
            # 섬을 발견한 시점에서만 센다
            # 아래 while문 안쪽에서 세면 섬의 개수가 아니라 섬의 크기가 되어버린다
            isla_count += 1
            # 큐에 넣는것과 방문 표시는 항상 한 쌍으로 처리한다
            # 꺼낼때 표시하면 같은 칸이 큐에 여러번 들어간다
            q.append((r,c))
            visited[r][c] = True

            # 이 섬에 연결된 땅을 남김없이 방문 처리한다
            while q:
                a , b =q.popleft()
                # 대각선을 포함한 8방향이므로, 델타 행렬 대신 -1 ~ 1 의 조합으로 대신한다
                # 십자(4방향) 문제에서는 이 방법을 쓸 수 없다
                for i in range(-1,2):
                    for j in range(-1,2):
                        # (0, 0)은 자기 자신이므로 건너뛴다
                        if i==0 and j==0:
                            continue
                        # 범위 검사를 arr 인덱싱보다 반드시 앞에 둔다
                        # 파이썬은 음수 인덱스를 에러없이 받아 반대편 끝을 참조하므로,
                        # 검사가 없으면 격자가 도넛처럼 이어져 모든 섬이 하나로 붙는다
                        # and는 앞이 거짓이면 뒤를 실행하지 않으므로 이 순서가 곧 방어가 된다
                        if 0<= a+i< N and 0<= b+j < M and arr[a+i][b+j] == 1 and visited[a+i][b+j] == False:
                            q.append((a+i, b+j))
                            visited[a+i][b+j] = True

print(isla_count)
