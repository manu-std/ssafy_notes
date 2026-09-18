# SWEA A형 기출

A형(Advanced) 실제 기출 문제 모음. 문제별로 폴더 하나씩 사용한다.

## 폴더 구성

| 파일 | 설명 |
|---|---|
| `prob.md` | 문제 정리 (조건 / 제약 / 예제 설명) |
| `input.txt` | 샘플 입력 |
| `output.txt` | 샘플 정답 출력 |
| `solve.py` | 정리된 풀이 |
| `main.py` | 직접 푼 코드 (있는 경우) |

풀이는 `sys.stdin = open('input.txt')` 로 입력을 읽으므로 **해당 문제 폴더에서 실행**한다.

```bash
cd 01_robot_harvest
python solve.py
```

## 문제 목록

| # | 폴더 | 문제 | 유형 | 제약 |
|---|---|---|---|---|
| 1 | [01_robot_harvest](01_robot_harvest/) | 개척자 로봇 곡식 수확 | 시뮬레이션 + 완전탐색 | N 6 ~ 9, M 10 ~ 50 |
| 2 | [02_ev_charging_station](02_ev_charging_station/) | 전기 자동차 충전소 | 좌표 완전탐색 (비트마스크) | N 2 ~ 20, 좌표 -15 ~ 15 |
