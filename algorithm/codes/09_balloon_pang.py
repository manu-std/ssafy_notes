import sys
sys.stdin = open('input.txt')
T = int(input())

def solve(N, M, arr):
    # 사용할 축들, 배수를 곱해서 사용한다.
    axes = [(1,0),(0,1)]
    max_pollen = 0 

    for r in range(N):
        for c in range(M):
            # 터뜨린 풍선의 꽃가루 개수
            num = arr[r][c]
            tmp = 0
            # 이 코드는 N X N 정방형을 계산하므로 폐기한다
            # for i in range(-num,num+1):
            #     for j in range(-num,num+1):
            #         if 0 <= (r + i) < N and 0 <= (c + j) < M:
            #             tmp += arr[r+i][c+j]
            
            # dir에 i배 만큼을 순회 하며 더한다
            for i in range(-num,num+1):
                for axis in axes:
                    if 0 <= r+axis[0] * i < N and 0 <= c + axis[1] * i < M:
                        tmp += arr[r+axis[0] * i][c + axis[1] * i] 
            # 중심은 두번 더해지므로, for문 바깥에서 한번 빼준다
            tmp -= arr[r][c]
            if tmp > max_pollen:
                max_pollen = tmp
    return max_pollen

for tc in range(1,T + 1):
    N , M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    max_pollen = solve(N, M, arr)
    print(f'#{tc} {max_pollen}')
