import sys

sys.stdin= open('algorithm\codes\input.txt')
T = int(input())



# 재사용을 위해 함수로 추출
def print_min_max(test_case : int, number_list : list)-> None:
    # min과 max 는 누수 방지를 위해 실제 리스트의 0번 인덱스로 초기화한다
    min = number_list[0]
    max = number_list[0]
    # 0번 인덱스는 사용하였으므로, 1번 인덱스부터 순회한다
    for i in number_list[1:]:
        if min > i:
            min = i
        if max < i:
            max = i
    print(f'#{test_case} {max-min}')

for tc in range(T):
    N = int(input())
    a = list(map(int, input().split()))
 

    print_min_max(tc, a)

    # 또는 내장함수 민/맥스를 사용하여 간편하게 구현할 수 있다.
    # print(f'#{tc} {max(a)-min(a)}')