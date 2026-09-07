import sys

sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T+1):
    arr = list(map(str,input()))
    # print(arr)
    stack=[]
    result = 0
    for i in arr:
        if i =='(':
            stack.append(i)
        elif i ==')':
            try:
                stack.pop()
            except IndexError:
                result = -1
                break
    else:
        if len(stack)==0 :   
            result = 1
        else: 
            result = -1
   
    print(f'#{tc} {result}')