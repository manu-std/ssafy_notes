import sys

sys.stdin = open('input.txt')

LIM = 15  # 마을 좌표 범위: -15 ~ 15


def solve(N, houses):
    house_pos = {(x, y) for x, y, d in houses}
    full = (1 << N) - 1

    # 충전소를 지을 수 있는 모든 칸에 대해
    #   dist : 각 집까지의 맨해튼 거리
    #   mask : 허용 거리 안에 들어오는 집들의 비트마스크
    spots = []
    for cx in range(-LIM, LIM + 1):
        for cy in range(-LIM, LIM + 1):
            if (cx, cy) in house_pos:   # 집이 있는 자리에는 못 짓는다
                continue
            dist = []
            mask = 0
            for i, (hx, hy, d) in enumerate(houses):
                t = abs(hx - cx) + abs(hy - cy)
                dist.append(t)
                if t <= d:
                    mask |= 1 << i
            spots.append((dist, mask))

    # 1) 1개로 모든 집을 커버할 수 있으면 반드시 1개만 짓는다
    #    (2개가 거리 합이 더 작더라도 개수가 우선)
    one = [sum(dist) for dist, mask in spots if mask == full]
    if one:
        return min(one)

    # 2) 2개짜리
    #    커버 가능한 칸이 가장 적은 집(pivot)을 고르면,
    #    두 충전소 중 하나는 반드시 그 집을 커버해야 한다 -> 한쪽 후보를 확 줄인다
    cover = [[] for _ in range(N)]
    for idx, (dist, mask) in enumerate(spots):
        for i in range(N):
            if mask >> i & 1:
                cover[i].append(idx)

    pivot = min(range(N), key=lambda i: len(cover[i]))
    if not cover[pivot]:        # 아예 커버 못 하는 집이 있으면 2개로도 불가능
        return -1

    best = -1
    for p in cover[pivot]:
        dp, mp = spots[p]
        need = full & ~mp       # 나머지 한 곳이 반드시 커버해야 하는 집들
        for q, (dq, mq) in enumerate(spots):
            if q == p:
                continue
            if mq & need != need:
                continue
            # 각 집은 두 충전소 중 더 가까운 쪽까지의 거리로 계산
            cost = sum(map(min, dp, dq))
            if best < 0 or cost < best:
                best = cost

    return best


T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    houses = [tuple(map(int, input().split())) for _ in range(N)]
    print(f'#{tc} {solve(N, houses)}')
