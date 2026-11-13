import sys
sys.stdin = open('input.txt')
from copy import deepcopy

dr = [-1, 0, 1, 0]
dc = [0, -1, 0, 1]
T = int(input())
for tc in range(1,T+1):
    N, M = map(int, input().split())
    arr = [list(map(lambda x: -int(x), input().split())) for _ in range(N)]
    # 몇번째 심었는지에 대한 자료
    k_arr = [[1]*N for _ in range(N)] 
    # 1. 농지 == 0 / 산 == -1 => 수확 가능 일자를 양수로 관리하려함
    # 2. d 일에 심으면 d+1일에 싹이 남
    # 3. k 번째로 싹이 난 후 3+k 이후에 곡식이 열림
    # 4. d 일에 심으면 d + k + 4일에 싹남
    # 5. if 빈농지 and 무브 할 수 있음? 씨 심음
    # 6. elif 빈농지 and 무브 할 수 있음? 스테이
    # 7. elif 곡식 열림? 수확
    
    # 8. 바라보는 방향 오른쪽 앞쪽 왼쪽 뒤쪽 순으로 이동한다
    # 9. 이동 가능한 곳은 빈농지/곡식이 열린 농지-> 산이나 싹이 나는 농지는 이동 불가
    # 10. 산에서는 출발하지 못하게 잠궈야하고 
    # 11. 산으로는 못들어가게 잠궈야함
    # 12. 배열들을 계속 돌려써야하므로 매번 수정이 필요할때 복사해야함
    # 12 검사할때
    max_harv_count = 0
    for r in range(1, N - 1): # 맨 끝은 어차피 1이므로 
        for c in range(1, N - 1):
            if arr[r][c] == -1: # 산이면 들어오자 마자 프루닝
                continue 
            for i in range(4): # 여기까지가 한단위 테스트
                cr, cc, ci = r, c, i
                d = 1 # 날짜를 초기화 
                harv_count = 0

                # 몇번째 심었는지에 대한 자료
                k_arr = [[1]*N for _ in range(N)] 
                arr_copy = deepcopy(arr)
                while d != M + 1 : #M일까지 동작하고 M + 1 일 일때 탈출 

                    for idx in (-1, 0, 1, 2):
                        ni = (ci + idx) % 4
                        nr = cr + dr[ni]
                        nc = cc + dc[ni]
                        is_movable = 0 <= arr_copy[nr][nc] <= d
                        if is_movable:
                            break
                    else : # is_movable == False <- 인경우에는 날짜만 올리고 다음 와일루프
                        is_movable == False

                    # 오전에 할일 들
                    if arr_copy[cr][cc] == 0:
                        if is_movable:
                            arr_copy[cr][cc] = d+k_arr[cr][cc]+4
                            k_arr[cr][cc] += 1
                        else:
                            pass #위에서 방어하지만 명시적으로 건너뜀
                    elif  arr_copy[cr][cc] <= d:
                        harv_count += 1
                        arr_copy[cr][cc] = 0 


                    # 오후에 할일 들
                    if is_movable:
                        # 움직이기
                        ci = ni
                        cr = nr
                        cc = nc
                    d += 1
                max_harv_count = max(max_harv_count, harv_count)

    print(f'#{tc} {max_harv_count}')

                            


