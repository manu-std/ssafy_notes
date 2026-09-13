import math

# 두 공이 맞닿았을 때 중심 사이의 거리(= 공 지름)
# 아래 값은 설명용 예시이며, 실제 공 크기에 맞춰 조정한다
BALL_DIAMETER = 10


def to_ssafy_angle(delta_x, delta_y):
    """좌표 차이를 일타싸피 각도(0 <= angle < 360)로 변환한다."""
    return math.degrees(math.atan2(delta_x, delta_y)) % 360


def aim_at(white_ball, target_ball, hole):
    """수구로 목적구를 쳐서 hole에 넣기 위한 (각도, 세기, 접점)을 반환한다."""
    # 1) 목적구 -> 홀 방향 벡터
    to_hole_x = hole[0] - target_ball[0]
    to_hole_y = hole[1] - target_ball[1]
    hole_distance = math.hypot(to_hole_x, to_hole_y)

    # 2) 길이를 1로 정규화
    unit_x = to_hole_x / hole_distance
    unit_y = to_hole_y / hole_distance

    # 3) 접점 = 목적구에서 홀 반대 방향으로 공 지름만큼 물러난 자리
    contact_x = target_ball[0] - unit_x * BALL_DIAMETER
    contact_y = target_ball[1] - unit_y * BALL_DIAMETER

    # 4) 수구 -> 접점 방향을 일타싸피 각도로 변환
    delta_x = contact_x - white_ball[0]
    delta_y = contact_y - white_ball[1]
    angle = to_ssafy_angle(delta_x, delta_y)

    # 5) 세기는 수구 -> 접점 거리를 기준으로 잡고 상황에 맞게 보정
    power = math.hypot(delta_x, delta_y)

    return angle, power, (contact_x, contact_y)


angle, power, contact = aim_at((40, 40), (120, 90), (240, 160))
print(f'접점: ({contact[0]:.2f}, {contact[1]:.2f})')
print(f'각도: {angle:.2f}도, 세기: {power:.2f}')