import sys

sys.stdin = open('input.txt')
T = int(input())

for tc in range(1, T+1):
    str1 = input()
    str2 = input()

    print(f'#{tc} {str2.count(str1)}')