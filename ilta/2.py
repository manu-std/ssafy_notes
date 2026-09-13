import math


def nearest_point(origin, points):
    """origin에서 가장 가까운 점의 좌표를 반환한다."""
    # TODO: min()의 key 인자에 '기준점까지의 거리'를 계산하는 람다를 넘기세요
    return min(points, key = lambda  x : math.dist(origin, x))


candidates = [(12, 80), (95, 25), (140, 60), (30, 15)]

print(nearest_point((60, 50), candidates))   # (95, 25)
print(nearest_point((130, 70), candidates))  # (140, 60)