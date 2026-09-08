
T = int(input())

for tc in range(1,T+1):
    str_input = input().strip()     
    stack = []
    res = 0
    for s in str_input:
        if s == '{':
            stack.append(s)
        elif s == '(':
            stack.append(s)

        elif s == ')':
            if not stack:
                break
            if stack[-1] != '(':
                break
            else: 
                stack.pop()

        elif s == '}':
            if not stack:
                break
            if stack[-1] != '{':
                break
            else: 
                stack.pop()
    else: 
        if not stack:
            res = 1

    print(f'#{tc} {res}')