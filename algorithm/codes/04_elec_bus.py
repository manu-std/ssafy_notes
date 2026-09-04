import sys
sys.stdin = open('algorithm/codes/input.txt')
T = int(input())

# 현재 위치 current_idx 에서 K 만큼 우선 앞으로 이동을하고, 
# 값이 True(충전기가 있는 위치)인지 검사흘 한다 
# True이면 current_idx에 K를 더하여 이동하고, 포문을 탈출한다 
# False이라면, K-1위치를 검사한다...1까지 검사
# 위 4줄 전체를 반복하며 N에 닿을때 까지 반복하고 충전횟수 charge_count를 출력
# 만약 True에 닿지 못했다면 전체 반복을 탈출하고 즉시 0을 출력하고 다음 tc로 넘어간다 

def count_min_charges(tc, K, N, charger_list):
    road = [False] * (N+1)
    for charger_idx in charger_list:
        road[charger_idx] = True
    # 현재 인덱스를 저장하는 상태
    current_idx = 0 
    # 충전 횟수를 저장하는 상태
    charge_count = 0

    # 몇회 반복해야하는지 모르므로, 무한 반복으로 시작하고, break를 사용하여
    # while문을 탈출한다.

    while True:
        # 좋은 구현은 아니지만, 종료조건은 에러로 처리한다....
        
        try:
            
            for idx in range(K,0,-1):
                # N에 딱 닿는 경우는 인덱스 에러가 발생하지 않으므로 우선 검사한다(좋은 구현이 아님)
                if current_idx+idx == N:
                     # 종료조건에 닿았으므로 인덱스 에러를 레이즈해 except 문으로 간다
                     raise IndexError
                # 충전기를 만나면 안쪽 각 상태를 업데이트 하고 안쪽 for문을 탈출한다 
                # 이때 IndexError가 터지면 정상적으로 N에 도달 한 것이다.  
                if road[current_idx+idx]:
                    current_idx += idx
                    charge_count += 1
                    break
            else:
                # 안쪽 for 문의 break를 만나지 못하였다면 충전기를 만나지 못한것이므로,  
                # 0을 출력하고 tc를 종료한다
                print(f'#{tc} 0')
                # 이때 이 break는 바깥쪽 while문을 탈출한다
                break
        # 인덱스 에러를 만났다면, 정상 도달 한 것이므로 charge_count를 출력하고 tc를 종료한다
        except IndexError:
            print(f'#{tc} {charge_count}')
            break

for tc in range(1,T+1):
    # K 한번 충전으로 갈 수 있는 정류장 수
    # N 종점 정류장
    # M 충전기가 설치된 정류장 수
    # charger_list 충전기가 설치된 정류장 위치
    K, N, M = map(int, input().split())
    charger_list = list(map(int, input().split()))
    count_min_charges(tc, K, N, charger_list)
        
                
                
            



                   
          