import math


def aim_direct(white_ball, target_ball):
    """수구에서 목적구 중심을 향하는 일타싸피 각도를 반환한다."""
    # TODO: 목표에서 수구를 빼서 좌표 차이를 구하세요
    # [힌트] 순서는 항상 '목표 - 수구' 입니다
    delta_x = target_ball[0]-white_ball[0]
    delta_y = target_ball[1]-white_ball[1]

    # TODO: atan2로 라디안을 구하세요
    # [힌트] 일타싸피는 +y축이 0도이므로 인자 순서를 뒤집습니다
    radians = math.atan2(delta_x,delta_y)

    # TODO: 도로 변환하고 0 ~ 360 범위로 정규화하세요
    # [힌트] math.degrees() 와 % 360
    angle = math.degrees(radians)%360

    return angle


# 검증: 아래 네 줄이 각각 0.0, 90.0, 180.0, 270.0 이 나와야 합니다
print(aim_direct((50, 50), (50, 90)))
print(aim_direct((50, 50), (90, 50)))
print(aim_direct((50, 50), (50, 10)))
print(aim_direct((50, 50), (10, 50)))