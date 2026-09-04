DATA  = [0,4,1,3,1,2,4,1] # 0~4범위라고 알려져 있음
COUNTS = [0]*(4+1)
K = max(DATA)
N = len(DATA)
TEMP = [0]* N
for x in DATA:
    COUNTS[x] +=1

## 0 1 을 합쳐서 몇개가 있니?
# COUNTS[0]+COUNT[1]
# 0 1 2 를 합쳐서 몇개가 있니?
# COUNTS[1]+COUNT[2]
# ...
# 바로 직전 인덱스와 더하면 됨

print(COUNTS)

for i in range(1, K+1):
    COUNTS[i] += COUNTS[i-1]

print(COUNTS)


#DATA의 마지막 원소부터 TEMP 에 넣기
for j in range(N-1, -1 ,-1):
    COUNTS[DATA[j]] -=1
    TEMP[COUNTS[DATA[j]]] = DATA[j]

print(TEMP)