"""문제은행(txt) → 검증 → questions.json / 단원별 마크다운 / CBT HTML.

usage: python -I build.py <cbt_dir> <repo_problem_dir>
검증: 단원당 20문항, 보기 4개, 정답 번호 == answer_key.json(문제보다 먼저 생성한 위치표)
"""
import json, re, sys
from pathlib import Path

UNITS = {
    '01': ('01_intro_design_pattern', 'Intro & Design Pattern'),
    '02': ('02_template_urls', 'Template & URLs'),
    '03': ('03_model', 'Model'),
    '04': ('04_orm', 'ORM'),
    '05': ('05_orm_with_view', 'ORM with View'),
    '06': ('06_django_form', 'Django Form'),
    '07': ('07_static_media', 'Static & Media'),
    '08': ('08_auth_cookie_session_login', 'Auth 01 · 쿠키·세션·로그인'),
    '09': ('09_auth_logout_signup_access', 'Auth 02 · 로그아웃·회원가입·접근 제한'),
    '10': ('10_auth_user_update_password', 'Auth 03 · 회원정보·비밀번호·해시'),
}
CIRCLE = '①②③④'


def parse(text):
    units, unit, q, mode, fence = {}, None, None, None, False
    for raw in text.splitlines():
        line = raw.rstrip('\n')
        if line.startswith('@@ '):
            unit = line[3:].strip(); units.setdefault(unit, []); continue
        if re.match(r'^# \d+$', line) and not fence:
            q = {'n': int(line[2:]), 'stem': [], 'opts': [], 'ans': None, 'exp': ''}
            units[unit].append(q); mode = None; continue
        if q is None:
            continue
        if line.startswith('```'):
            fence = not fence
            q['stem'].append(line); continue
        if fence:
            q['stem'].append(line); continue
        if line.startswith('Q '):
            q['stem'].append(line[2:]); mode = 'Q'; continue
        m = re.match(r'^([1-4]) (.*)$', line)
        if m and mode in ('Q', 'O'):
            q['opts'].append(m.group(2)); mode = 'O'; continue
        if line.startswith('A '):
            q['ans'] = int(line[2:].strip()); continue
        if line.startswith('E '):
            q['exp'] = line[2:].strip(); continue
        if line.strip() == '':
            continue
        if mode == 'Q':
            q['stem'].append(line); continue
        raise ValueError(f'unparsed line in {unit}#{q["n"]}: {line!r}')
    for u in units.values():
        for q in u:
            q['stem'] = '\n'.join(q['stem']).strip()
    return units


def validate(units, key):
    errs = []
    for u, (slug, _) in UNITS.items():
        qs = units.get(u, [])
        if [q['n'] for q in qs] != list(range(1, 31)):
            errs.append(f'{u}: numbering {[q["n"] for q in qs]}')
            continue
        for q in qs:
            tag = f'{u}#{q["n"]}'
            if len(q['opts']) != 4: errs.append(f'{tag}: {len(q["opts"])} options')
            if not q['exp']: errs.append(f'{tag}: no explanation')
            if q['ans'] != key[u][q['n'] - 1]:
                errs.append(f'{tag}: answer {q["ans"]} != key {key[u][q["n"]-1]}')
            if len(set(q['opts'])) != 4: errs.append(f'{tag}: duplicate options')
    return errs


def longest_bias(units):
    hit = tot = 0
    for qs in units.values():
        for q in qs:
            lens = [len(o) for o in q['opts']]
            if lens.count(max(lens)) == 1:
                tot += 1
                hit += lens.index(max(lens)) + 1 == q['ans']
    return hit, tot


def to_markdown(u, qs, seed, seed2):
    slug, title = UNITS[u]
    out = [f'# Django {int(u)}단원 CBT — {title} (30문항)', '',
           f'> 출제 범위: [`../{slug}.md`](../{slug}.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제',
           '>',
           f'> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`{seed}`) ①~④ 각 5개, '
           f'함정(`{seed2}`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.',
           '', '---', '', '## 기본 문제 (1~20)', '']
    for q in qs:
        if q['n'] == 21:
            out += ['## 함정 문제 (21~30)', '']
        lines = q['stem'].split('\n')
        out.append(f'### {q["n"]}. {lines[0]}')
        rest = lines[1:]
        if rest:
            out.append('')
            out.extend(rest)
        out.append('')
        for i, o in enumerate(q['opts']):
            out.append(f'- {CIRCLE[i]} {o}')
        out += ['', '---', '']
    out += ['## 정답 및 해설', '']
    for a in range(0, len(qs), 10):
        chunk = qs[a:a + 10]
        out += ['| ' + ' | '.join(str(q['n']) for q in chunk) + ' |',
                '|' + '---|' * len(chunk),
                '| ' + ' | '.join(CIRCLE[q['ans'] - 1] for q in chunk) + ' |', '']
    for q in qs:
        out.append(f'- **{q["n"]}. {CIRCLE[q["ans"] - 1]}** {q["exp"]}')
    return '\n'.join(out) + '\n'


def main():
    cbt, repo = Path(sys.argv[1]), Path(sys.argv[2])
    keyfile = json.loads((cbt / 'answer_key.json').read_text(encoding='utf-8'))
    seed, seed2 = keyfile['seed'], keyfile['extra_seed']
    key = {u: keyfile['key'][u] + keyfile['extra'][u] for u in keyfile['key']}
    text = ''.join((cbt / f).read_text(encoding='utf-8') + '\n'
                   for f in ('bank_01_05.txt', 'bank_06_10.txt', 'bank_traps.txt'))
    units = parse(text)
    errs = validate(units, key)
    if errs:
        print('VALIDATION FAILED'); print('\n'.join(errs)); sys.exit(1)
    hit, tot = longest_bias(units)
    print(f'ok: {sum(len(v) for v in units.values())} questions, answer == pre-made key for all')
    print(f'"정답이 가장 긴 보기" 비율: {hit}/{tot} = {hit/tot:.0%} (무작위 기대값 25%)')

    data = {'seed': seed, 'seed2': seed2, 'units': [
        {'id': u, 'slug': UNITS[u][0], 'title': UNITS[u][1],
         'questions': [{'n': q['n'], 'stem': q['stem'], 'opts': q['opts'], 'ans': q['ans'], 'exp': q['exp'],
                        'trap': q['n'] > 20}
                       for q in units[u]]}
        for u in UNITS]}
    (cbt / 'questions.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')

    repo.mkdir(parents=True, exist_ok=True)
    for u in UNITS:
        (repo / f'{UNITS[u][0]}_CBT.md').write_text(to_markdown(u, units[u], seed, seed2), encoding='utf-8')

    tpl = (cbt / 'template.html').read_text(encoding='utf-8')
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    (cbt / 'django_cbt.html').write_text(tpl.replace('__BANK_JSON__', blob), encoding='utf-8')
    print('written: questions.json, markdown x10, django_cbt.html')


if __name__ == '__main__':
    main()
