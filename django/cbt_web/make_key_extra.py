"""함정 문항(21~30번) 정답 위치표를 문제보다 먼저 만든다.
단원당 10문항 = 두 위치는 3개, 두 위치는 2개. 10단원 합계 ①~④ 각 25개.
같은 번호 3연속 금지 (기존 19·20번과 이어지는 구간 포함). 시드 고정."""
import json, random, sys
p = sys.argv[1]
data = json.load(open(p, encoding='utf-8'))
SEED = 20261109
rng = random.Random(SEED)
units = [f'{i:02d}' for i in range(1, 11)]
while True:  # 각 위치가 '3개짜리'가 되는 단원이 정확히 5개씩
    slots = [1, 2, 3, 4] * 5
    rng.shuffle(slots)
    pairs = [slots[i*2:i*2+2] for i in range(10)]
    if all(a != b for a, b in pairs):
        break
extra = {}
for u, (a, b) in zip(units, pairs):
    base = data['key'][u]
    while True:
        seq = []
        for pos in (1, 2, 3, 4):
            seq += [pos] * (3 if pos in (a, b) else 2)
        rng.shuffle(seq)
        full = base + seq
        if all(not (full[i] == full[i+1] == full[i+2]) for i in range(len(full) - 2)):
            break
    extra[u] = seq
data['extra_seed'] = SEED
data['extra'] = extra
json.dump(data, open(p, 'w', encoding='utf-8'), indent=1)
tot = [0]*5
for u, s in extra.items():
    for x in s: tot[x] += 1
    print(u, ' '.join(map(str, s)), [s.count(i) for i in range(1, 5)])
print('totals', tot[1:])
