import sys

sys.stdin = open('input.txt')
T = int(input())

for tc in range(1, T+1):
    a = input().split()
    s = a[0]
    # print(s[0])
    res = 0
    for idx in range(len(s)//2):
        if s[idx] != s[len(s)-1-idx]:
            break
    else:
        res = 1 
   

    print(f'#{tc} {res}')