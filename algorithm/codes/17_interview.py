import sys
sys.stdin = open('input.txt')
# 기본 아이디어
# 두배 이벤트가 일어나야한다면 최대한 앞쪽에서 일어나는게
# 최솟값을 찾기 좋지 않을까?
# 아마도 (N//K)-(N-M) 만큼 두배 이벤트가 일어난다
# 이걸 최대한 앞쪽으로
# 그러면 N-M을 배치하는 문제로 바뀐다
# 더블 이벤트를 앞쪽에서 횟수만큼 터뜨리고, 
# 뒷쪽은 적절히      

for tc in range(1, T+1):
    # N 문제의 개수
    # M 맞힌 문제의 개수
    # K 카운터 도달시 0으로 리셋 후 전체점수  2배
    N, M, K = map(int, input().split())
    # (N//K)-(N-M) 만큼 더블 이벤트가 일어난다 음수면 0 
    double_event = (N//K)-(N-M) if (N//K)-(N-M)>0 else 0
    # 어레이를 모두 맞힌걸로 채워둔다
    arr = [True] * N
    res_arr = [0] * N
    counter = 0
    for idx in range(N):
        # 더블 이벤트를 끊어줄 위치 
        if idx % K == K-1 and idx / K > double_event:
            arr[idx] = False

        # 정답위치 연산
        if arr[idx]:
            # idx 가 0일때 초기값설정
            if idx ==0:
                counter = 1
                res_arr[idx] = 1 
            elif counter == K-1:
                res_arr[idx] = (res_arr[idx - 1] + 1) * 2
                counter = 0
            else:
                res_arr[idx] = res_arr[idx - 1] + 1
                counter += 1
        # 오답 위치 연산
        else: 
            counter = 0
            res_arr[idx] = res_arr[idx-1]


    result = res_arr[N-1]
        # 더블 이벤트가 0 일 경우 이상하게 동작하므로, 강제로 M점으로 설정
    if double_event == 0:
        result = M
    print(f'#{tc} {result}')
