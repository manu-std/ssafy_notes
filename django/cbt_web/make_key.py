"""정답 위치표를 문제보다 먼저 만든다 (정답 위치 편향 방지).
단원당 20문항, ①~④ 각 5개 균등, 같은 번호 3연속 금지. 시드 고정으로 재현 가능."""
import json, random, sys
SEED = 20261108
rng = random.Random(SEED)
key = {}
for unit in range(1, 11):
    while True:
        seq = [1]*5 + [2]*5 + [3]*5 + [4]*5
        rng.shuffle(seq)
        if all(not (seq[i] == seq[i+1] == seq[i+2]) for i in range(18)):
            break
    key[f'{unit:02d}'] = seq
json.dump({'seed': SEED, 'key': key}, open(sys.argv[1], 'w'), indent=1)
for u, s in key.items():
    print(u, ' '.join('①②③④'[x-1] for x in s), '| counts', [s.count(i) for i in range(1,5)])
