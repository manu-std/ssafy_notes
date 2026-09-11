import sys
sys.stdin = open('input.txt')


# N (7~12) 이 작은 범위가 들어오므로, 4중으로  포문을 돌아도 괜찮을듯
# rc for문 안에서 dfs를 호출하고 dfs 안에서 rc를 모두 검사하면서 돌아야하나??
# 일단 같은 배열에서 프로세서는 1로 표현 되어있으니 전선은 2 로 표현해서 채워넣자
# 벽까지 닿아야하니 모든 프로세스 위치에서 상하좌우방향 끝까지 0으로 되어있는 방향이 있어야 전선이연결 가능
# 이왕 도는김에 벽에 이미 닿아있는걸 검사해서 카운터 채워넣자
# 방향 배열 (상, 하, 좌, 우)
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

# idx_now: 이번에 연결 방법을 정할 코어 번호 (core_idx_list 기준)
# counter: 지금까지 연결된 코어 수 (가장자리 코어 포함해서 시작)
# line_counter: 지금까지 깐 전선 길이 합
def dfs(idx_now:int, counter, line_counter):


    if idx_now>= len(core_idx_list):
        return counter, line_counter

    max_counter = -1
    min_line_counter = float('inf')
    r, c  =core_idx_list[idx_now]
    idx_nxt = idx_now+1
    # 하위 경우들 중 최선의 결과 (TODO: 초기값, 두 값을 한 쌍으로 비교)
  
    # {0:상, 1:하, 2:좌, 3:우, 4:연결안함}


    # 상하좌우 4방향으로 연결 시도
    for idx in range(4):
        # 해당 방향으로 벽까지 전부 빈칸(0)인지 확인
        tmp = 0
        for i in range(1, N-1):
            nr = r + dr[idx]*i
            nc = c + dc[idx]*i
            if 0<= nr <N and 0<= nc <N:
                tmp += arr[nr][nc]
                        
        # 빈칸이면 전선(2)을 깔면서 이번 방향 전선 길이를 따로 셈
        if tmp==0:
            line = 0
            for i in range(1, N-1):
                nr = r + dr[idx]*i
                nc = c + dc[idx]*i
                if 0<= nr <N and 0<= nc <N:
                    arr[nr][nc] = 2
                    line += 1
            # 다음 코어로 넘어감 (연결했으니 코어 수 +1, 길이는 이번 방향만큼 더해서 넘김)
            result =  dfs(idx_nxt, counter+1, line_counter+line)
            for i in range(1, N-1):
                nr = r + dr[idx]*i
                nc = c + dc[idx]*i
                if 0<= nr <N and 0<= nc <N:
                    arr[nr][nc] = 0
                    line -= 1
            if result[0]>max_counter or (result[0]==max_counter and result[1]<min_line_counter):
                max_counter = result[0]
                min_line_counter = result[1]
    # 연결 안함 (막혀 있든 말든 항상 시도, 코어 수와 길이는 그대로 넘김)
    result = dfs(idx_nxt, counter, line_counter)
    if result[0]>max_counter or (result[0]==max_counter and result[1]<min_line_counter):
        max_counter = result[0]
        min_line_counter = result[1]

    return max_counter , min_line_counter


T = int(input())
for tc in range(1,T+1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]
    counter = 0
    core_idx_list = []
    for r in range(N):
        for c in range(N):
            # 가장자리 코어는 이미 연결된 걸로 보고 카운트만 올림
            if (r == 0 or r == N-1 or c==0 or c== N-1 ) and arr[r][c] == 1:
                counter+=1


            # 안쪽 코어만 탐색 대상으로 모아둠
            elif arr[r][c] == 1:
               core_idx_list.append((r,c))
    # 0번 코어부터 한 번만 시작 (순서 고정해도 모든 조합을 다 봄)
    
    res=dfs(0, counter,0)
    print(f'#{tc} {res[1]}')