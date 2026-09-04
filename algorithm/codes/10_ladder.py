import sys 
sys.stdin = open('input.txt')
    # 기본 아이디어
     
    # 제일 아래에서부터 시작한다.
    # 오른쪽으로 밀때는 끝까지 쭉 밀고 바로 올라간다 
    # if 에서 이미 검사했으므로, elif를 다시 검사하여 좌우로 진동하는 경우는 없다
    
def solve(arr):
    r = 99
    # 2의 위치 인덱스
    c = arr[r].index(2)
    while r > 0:
        # 좌 방향부터 검사(여기서 조건이 걸려 끝까지 밀고나면
        # 우방향을 다시 검사하는 경우는 없다)
        if c > 0 and arr[r][c-1] == 1:
            while c > 0 and arr[r][c-1] == 1:
                c -= 1
        elif c < 99 and arr[r][c+1] == 1:
            while c < 99 and arr[r][c+1] == 1:
                c += 1
        # 바로 위로 한칸 올라감
        r -= 1
    return c

for _ in range(10):
    tc = int(input())
    arr = [list(map(int, input().split())) for _ in range(100)]
    c = solve(arr)

    print(f'#{tc} {c}')

    # 상태굴리기 조건이 너무 복잡하고 엣지케이스를 생각하기 너무 어려우므로 포기 

    # 상 좌 우  
    # dir_r = [-1, 0, 0]
    # dir_c = [0, -1, 1]
    # # ex) 오른쪽으로 가고 있던 경우 오른쪽으로 가는 방향을 유지하기 위해 상태를 사용
    # state_idx = 0
    # while cur_r != 0:
    #     if cur_c ==0 and arr[cur_r][cur_c + 1] == 0:
    #         state_idx == 0
    #     elif cur_c ==0 and  arr[cur_r][cur_c + 1] == 1:
    #         state_idx = 2
    #     elif cur_c == 99 and arr[cur_r][cur_c - 1] == 0:
    #         state_idx == 0
    #     elif cur_c == 99 and  arr[cur_r][cur_c - 1] == 1:
    #         state_idx = 1
    #     elif arr[cur_r][cur_c+1] == 1 and arr[cur_r][cur_c - 1]==1:
    #         ...
    #     elif state_idx == 1 and  arr[cur_r][cur_c + 1] == 1 or state_idx == 2 and  arr[cur_r][cur_c - 1] == 1:
    #         state_idx =0
    #     elif arr[cur_r][cur_c + 1] == 1:
    #         state_idx = 2
    #     elif arr[cur_r][cur_c - 1] == 1:
    #         state_idx = 1
    #     else: state_idx = 0
    #     cur_r += dir_r[state_idx]
    #     cur_c += dir_c[state_idx]
    