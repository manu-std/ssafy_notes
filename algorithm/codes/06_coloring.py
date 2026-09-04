import sys

# 기본 아이디어
# bool 10 X 10 의 배열을 두개를 각생상을 위해 선언하고, 
# 색상이 칠해져 있는 곳을 True 로 반전한다
# 이때 두 배열이 모두 True 인 영역이 보라색 색칠된 영역이다.

sys.stdin= open('input.txt')
T = int(input())

for tc in range(1,T+1):
    N = int(input())

    # if 문을 사용하지 않기 위해 리스트로 한번 더 감싸서 인덱스로 접근한다
    # arr_for_red = [[False] * 10 for _ in range(10)]
    # arr_for_blue = [[False] * 10 for _ in range(10)]

    arrs = [[[False] * 10 for _ in range(10)]for _ in range(2)]

    for _ in range(N):
        r1 ,c1, r2,c2, color = map(int, input().split())
        

        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                arrs[color-1][r][c] = True
    count = 0
    for r in range(10):
        for c in range(10):
            if arrs[0][r][c] and arrs[1][r][c]:
                count += 1
    print(f'#{tc} {count}')



