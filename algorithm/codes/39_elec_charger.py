import sys
sys.stdin = open('input.txt')
T = int(input())

def calc(arr):
    INF =  float('INF')
    rtn_dist = INF
    for xc in range(-15, 16):
        for yc in range(-15, 16):
            t_dist = 0
            for xh, yh, d in arr:
                mht_dist = abs(xh-xc)+abs(yh-yc)
                if mht_dist>d or mht_dist == 0:
                    break
                else:
                    t_dist+=mht_dist
            else: 
                if t_dist < rtn_dist:
                    rtn_dist = t_dist
    return rtn_dist if rtn_dist != INF else calc_two(arr)

def calc_two(arr):
    INF =  float('INF')
    rtn_dist = INF
    for xc_1 in range(-15, 16):
        for yc_1 in range(-15, 16):
            for xc_2 in range(-15, 16):
                for yc_2 in range(-15, 16):
                    t_dist = 0
                    for xh, yh, d in arr:
                        mht_dist_1 = abs(xh-xc_1)+abs(yh-yc_1)
                        mht_dist_2 = abs(xh-xc_2)+abs(yh-yc_2)
                        if mht_dist_1==0 or mht_dist_2 == 0:
                            break
                        selected_mht = min(mht_dist_1, mht_dist_2) 
                        if selected_mht>d : 
                            break
                        else: 
                            t_dist += selected_mht
                    else:
                        rtn_dist = min(rtn_dist, t_dist)
    return rtn_dist if rtn_dist != INF else -1
             
                    

for tc in range(1,T+1):
    N = int(input())
    arr = [tuple(map(int, input().split())) for _ in range(N)]
 
    ans = calc(arr)

    print(f'#{tc} {ans}')

            