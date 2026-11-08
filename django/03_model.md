# Django 03 — Model

> 📎 확인문제·예상문제·암기카드: [`시험대비/03_model_시험대비.md`](시험대비/03_model_시험대비.md)

*(MTV의 M. 데이터베이스 테이블을 Python 클래스로 설계하고(Model), 그 설계를 실제 DB에 반영하는 과정(Migrations), 그리고 데이터를 바로 만져볼 수 있는 Admin 사이트까지. 다음 단원 ORM에서 이 테이블에 실제로 데이터를 넣고 뺀다.)*

## 오늘의 목차

1. Model
2. Model class
3. Model Field
4. Migrations
5. Admin site
6. 보조 명령어, SQLite, DB 초기화

---

## 1. Model

- 데이터베이스와 **Python 클래스(객체)로 추상화된 형태**로 상호작용
- DB 지식이 깊지 않아도 데이터 관리 가능, DB 변경 시 코드 수정 최소화
- 역할 분담

| 파일 | 역할 |
|---|---|
| `urls.py` | 요청의 시작점 |
| `views.py` | 요청 처리, models.py로 데이터 다룸 |
| `models.py` | DB 정의 및 DB와 상호작용 |
| `templates` | views에서 받은 데이터로 화면 구성 |

---

## 2. Model class

- DB 테이블을 **정의**하고 데이터를 조작하는 기능 제공
- 테이블 구조를 설계하는 **청사진(blueprint)**: 어떤 컬럼을, 어떤 타입·길이로 저장할지 Python 코드로 정의

```python
# articles/models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
```

- 모델 클래스 == 테이블 설계도 → `id | title | content` 테이블 생성
- **id 필드는 Django가 자동 생성** (기본키, 따로 적지 않음)
- **클래스 변수명 = 테이블의 필드(열) 이름**
- 실제 테이블 이름은 **`앱이름_모델이름소문자`** → `articles_article`

| 모델 쪽 | DB 쪽 |
|---|---|
| 모델 클래스 | 테이블 |
| 클래스 변수(필드) | 컬럼(열) |
| 인스턴스 1개 | 행(레코드) 1개 |

> ⚠️ `models.py`에 클래스를 **정의만** 해서는 DB에 테이블이 생기지 않는다. 아래 4장의 migrations 과정이 필요.

### `models.Model` 상속

- model 관련 코드가 이미 작성된 부모 클래스 → 개발자는 **테이블 구조 설계만** 작성
- 제공 기능: 테이블 자동 생성(Migrations), SQL 자동 변환, 데이터 저장·조회·수정·삭제, 유효성 검사, id 자동 생성
- 프레임워크 없이 만들면 sqlite3 연결, `CREATE TABLE` SQL 작성, commit, close를 직접 해야 함

```python
# 순수 Python으로 작성할 경우
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS article (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(10) NOT NULL,
        content TEXT NOT NULL
    )
''')
conn.commit()
conn.close()
```

- 코드 한 줄 안의 두 가지 "가져다 쓰기"
  - `models.Model` → **상속**받아 기능을 물려받음 (모델의 부모 클래스)
  - `models.CharField` → 만들어진 클래스를 **가져다 씀** (개별 컬럼의 타입 결정, 길이 검사 처리)

> 💡 사고의 전환: "어떻게 직접 만들지?"(알고리즘) → "이미 있는 기능을 어떻게 조합하지?"(프레임워크)
>
> ⚠️ `class Article():`처럼 `models.Model`을 상속하지 않으면 Django Model이 아니다.

---

## 3. Model Field

- DB 테이블의 **필드(열) 정의**, 데이터 타입과 제약 조건 명시
- 구성: `models.필드유형(필드옵션)`
  - **Field types**: 저장될 **데이터의 종류** 정의 (예: `CharField`)
  - **Field options**: 필드의 **동작과 제약 조건** 정의 (예: `max_length=10`)
- 유효성 검사: 정해진 규칙이나 조건에 따라 데이터의 정확성을 확인하는 과정

### Field types

| 구분 | CharField | TextField |
|---|---|---|
| 용도 | 제한된 길이의 문자열 | 길이 제한 없는 대용량 텍스트 (시스템에 따라 한계 있음) |
| 길이 | 짧고 예상 가능 | 길거나 예상 어려움 |
| max_length | **지정 (필수)** | 지정하지 않음 |
| 예시 | 이름, 제목, 이메일 | 게시글 본문, 상품 설명 |

- 255자를 넘을 것 같으면 TextField 고려

> ⚠️ 원본 노트에는 "max_length는 SQLite에서는 선택 사항"이라고 적었는데, 두 가지가 섞인 표현이다.
> - **SQLite는 VARCHAR 길이를 DB 차원에서 강제하지 않는다** → 그래서 SQLite에서는 길이 제한을 사실상 **Django 유효성 검사가 담당**한다. (이건 맞음)
> - 하지만 **Django 쪽에서 `CharField`의 `max_length`는 PostgreSQL을 제외한 모든 내장 DB 백엔드에서 필수**다. SQLite에서도 빼면 시스템 체크 에러(`fields.E120`)가 난다.
> - 결론: **CharField엔 항상 max_length를 적는다.**

| 분류 | 주요 필드 |
|---|---|
| 문자열 | `CharField`, `TextField` |
| 숫자 | `IntegerField`, `FloatField` |
| 날짜/시간 | `DateField`(날짜), `TimeField`(시간), `DateTimeField`(날짜+시간) |
| 파일 | `FileField`, `ImageField` (7단원) |

### Field options

- **제약 조건(Constraint)**: 특정 규칙을 강제하기 위해 테이블의 열이나 행에 적용되는 제한사항 (숫자만 저장, 100자까지만 저장 등)

| 옵션 | 의미 | 적용 레벨 | 기본값 |
|---|---|---|---|
| `max_length` | 문자열 최대 길이 | 필드 정의·검증 | — |
| `null` | **DB**에서 NULL 값 허용 여부 | DB | False |
| `blank` | **form**에서 빈 값 허용 여부 (`blank=False`면 필수 입력) | 유효성 검사/Form | False |
| `default` | 필드의 기본값 설정 | — | — |

> ⚠️ **null과 blank는 서로 대체할 수 없다.**
> - `null=True, blank=False` → DB는 NULL을 허용하지만, Form 검증에서는 비워둘 수 없음
> - `blank=True, null=False` → 문자열 필드는 빈 문자열 `''`로 저장됨 (SQL NULL과는 다름)

---

## 4. Migrations

- model 클래스의 변경사항(필드 생성, 수정, 삭제 등)을 **DB에 최종 반영**하는 방법
- 변경 사항이 코드로 관리되어 협업 시 추적·공유가 쉬움

### 흐름

```text
model class (설계도 초안)
   ↓ makemigrations
migration 파일 0001_initial.py (최종 설계도)
   ↓ migrate
db.sqlite3 (DB)
```

| 명령어 | 역할 |
|---|---|
| `python manage.py makemigrations` | 모델 변경을 감지해 **migration 파일(최종 설계도)** 생성. DB는 아직 그대로 |
| `python manage.py migrate` | 아직 적용 안 된 migration 파일을 **DB에 반영** (Python 코드 → SQL로 자동 변환 → DB 실행) |

```bash
$ python manage.py makemigrations
Migrations for 'articles':
  articles/migrations/0001_initial.py
    + Create model Article

$ python manage.py migrate
```

- migration 파일: 모델 변경사항을 기록한 Python 코드, DB 테이블 변경 내역을 순차적으로 저장
- SQL: DB를 조작하는 데 사용되는 표준 질의 언어
- migrations 폴더에 자동 생성된 파일은 **직접 수정·삭제하지 않는 것이 원칙**
- 서버 실행 시 `You have 18 unapplied migration(s)` 경고 → 미적용 migration 파일이 있다는 뜻 → `migrate` 실행으로 해결
  - 처음 migrate하면 여러 개가 적용되는 이유: 기본 설치 앱(admin, auth, contenttypes, sessions)도 각자 초기 migration을 갖고 있기 때문

> ⚠️ 함정 체크
> - "makemigrations 실행 시 DB에 테이블이 즉시 만들어진다" → ❌ (파일만 생성)
> - "migrate는 migration 파일을 기준으로 DB 변경을 적용한다" → ✅
> - "모델을 한번 만든 후 수정하면 migration이 필요 없다" → ❌

### 추가 Migrations (기존 테이블에 필드 추가)

```python
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

| 옵션 | 동작 | 기억법 |
|---|---|---|
| `auto_now_add` | 데이터가 **처음 생성될 때만** 현재 날짜시간 저장 (생성 시점) | add = 최초 추가 |
| `auto_now` | 데이터가 **저장될 때마다** 현재 날짜시간 저장 (수정 시점) | now = 저장할 때마다 지금 |

> 📌 `auto_now`는 `save()`할 때 갱신된다. `QuerySet.update()`처럼 save()를 거치지 않는 경로에서는 자동 갱신되지 않는다 (시험 기본 범위는 "수정 시각 기록"으로 기억).

- 기존 레코드가 있는 테이블에 필드를 추가하면 **기존 행들에 채울 값이 필요** → makemigrations 시 기본값 프롬프트 표시
  - `1) Provide a one-off default now`: 지금 기본값 직접 입력 → 기존 모든 행에 적용
  - `2) Quit and manually define a default value in models.py`
  - 1 선택 후 아무것도 입력하지 않고 Enter → Django 제안값 `timezone.now` 적용

```bash
$ python manage.py makemigrations
Migrations for 'articles':
  articles/migrations/0002_article_created_at_article_updated_at.py
    + Add field created_at to article
    + Add field updated_at to article

$ python manage.py migrate
```

- 결과: `0002_article_created_at_article_updated_at.py` 생성 → `migrate` 후 테이블에 created_at, updated_at 컬럼 추가
- 설계도를 쌓아가며 문제 시 복구·되돌리기 가능 (git commit과 유사)

> 💡 여기서 입력한 일회성 기본값은 **기존 행을 채우기 위한 것**일 뿐, 모델 필드의 영구적인 `default=` 옵션과는 다르다.

### ⭐ 반드시 기억

```text
model class 변경 → makemigrations → migrate
```

---

## 5. Admin site

- **Automatic admin interface**: Django가 추가 설치·설정 없이 자동 제공하는 웹 기반 관리 도구
- 등록된 모델의 **CRUD(생성, 읽기, 업데이트, 삭제)를** 간편하게 수행
- 활용: 빠른 프로토타이핑, 비개발자 데이터 관리, 내부 시스템 구축

### 사용 순서

**① 관리자 계정 생성** (manage.py 위치에서, `migrate`로 기본 테이블이 만들어진 뒤)

```bash
python manage.py createsuperuser
```

- username, email(선택), password(입력 시 화면에 안 보임), password 확인
- DB의 `auth_user` 테이블에 계정 저장

**② 접속** — `http://127.0.0.1:8000/admin/` 접속 후 로그인 (처음엔 Groups, Users만 보임, 정상)

**③ 모델 등록**

```python
# articles/admin.py
from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

**④ 데이터 조작** — Articles 항목에서 데이터 생성(ADD), 수정(SAVE), 삭제(Delete) 가능 → DB `articles_article` 테이블에서도 확인 가능

> ⚠️ 관리자 계정 생성(`createsuperuser`)과 모델의 Admin 등록(`admin.site.register`)은 **별개의 작업**이다. 모든 모델이 자동으로 Admin에 나오지 않는다.

---

## 6. 보조 명령어, SQLite, DB 초기화

### 보조 명령어

| 명령어 | 역할 |
|---|---|
| `python manage.py showmigrations` | migration 파일 목록과 적용 여부 확인 (`[X]` = 적용됨) |
| `python manage.py sqlmigrate articles 0001` | 해당 migration이 실행할 **SQL을 출력만** (실행하지 않음) |

### SQLite

- Django 기본 설정에서 사용하는 **가벼운 관계형 DB 엔진**
- 파일 하나(`db.sqlite3`)에 저장 → 개발·학습에 편리
- SQLite = DBMS, `db.sqlite3` = 그 DB의 파일

### DB 초기화 (학습용 로컬 환경 한정)

1. 앱의 `migrations/` 폴더 안 번호 붙은 migration 파일 삭제 (**`__init__.py`는 남김**)
2. `db.sqlite3` 삭제
3. 다시 `makemigrations` → `migrate`

> ⚠️ 실제 데이터가 있는 DB에서 이렇게 하면 **데이터가 전부 날아간다**. 팀 프로젝트·운영 환경에서는 절대 그대로 하지 말 것. 로컬 학습용 `db.sqlite3`는 `.gitignore`로 저장소에서 제외하는 경우가 많다.
