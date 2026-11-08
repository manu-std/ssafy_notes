# Django 3단원 CBT — Model (30문항)

> 출제 범위: [`../03_model.md`](../03_model.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. Django Model 클래스가 반드시 상속해야 하는 부모 클래스는?

- ① `models.Model`
- ② `models.CharField`
- ③ `forms.ModelForm`
- ④ `django.db.Table`

---

### 2. articles 앱의 models.py에 다음 모델이 있다. 설명으로 **옳은** 것은?

```python
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
```

- ① id 필드를 적지 않았으므로 기본키가 없는 테이블이 만들어진다.
- ② 클래스를 정의하고 저장하는 즉시 DB에 테이블이 생성된다.
- ③ migrate하면 `articles_article` 테이블이 만들어진다.
- ④ title과 content는 각각 테이블의 행(row) 하나에 해당한다.

---

### 3. 모델과 DB의 대응으로 **옳지 않은** 것은?

- ① 모델 클래스 — 테이블
- ② 클래스 변수(필드) — 컬럼(열)
- ③ 모델 인스턴스 1개 — 테이블 1개
- ④ id 필드 — 자동 생성되는 기본키

---

### 4. 게시글 제목처럼 길이가 짧고 예상 가능한 문자열에 적합한 필드는?

- ① `TextField`
- ② `CharField`
- ③ `IntegerField`
- ④ `FileField`

---

### 5. 빈칸에 들어갈, 문자열의 최대 길이를 지정하는 필드 옵션은?

```python
title = models.CharField(_______=10)
```

- ① `max_value`
- ② `length`
- ③ `size`
- ④ `max_length`

---

### 6. 필드 타입과 저장 데이터의 연결로 **옳지 않은** 것은?

- ① `DateField` — 날짜
- ② `TimeField` — 날짜와 시간
- ③ `DateTimeField` — 날짜와 시간
- ④ `FloatField` — 실수

---

### 7. `null`과 `blank` 옵션에 대한 설명으로 **옳은** 것은?

- ① null은 form의 빈 값 허용, blank는 DB의 NULL 허용 여부다.
- ② 두 옵션의 기본값은 모두 True다.
- ③ blank=True만 지정하면 DB에도 NULL이 저장된다.
- ④ null은 DB 레벨, blank는 유효성 검사(form) 레벨의 설정이다.

---

### 8. `content = models.TextField(blank=True)`로 정의했을 때의 설명으로 옳은 것은?

- ① form에서 content를 비워도 유효성 검사를 통과한다.
- ② DB에 SQL NULL 값이 저장된다.
- ③ content 컬럼이 테이블에서 제외된다.
- ④ content는 반드시 입력해야 하는 필수 항목이 된다.

---

### 9. makemigrations와 migrate에 대한 설명으로 **옳지 않은** 것은?

- ① makemigrations는 모델 변경을 감지해 migration 파일을 만든다.
- ② migrate는 아직 적용되지 않은 migration을 DB에 반영한다.
- ③ migration 파일은 모델 변경 내역을 순서대로 기록한 Python 코드다.
- ④ makemigrations만 실행해도 DB에 테이블이 즉시 생성된다.

---

### 10. 모델 클래스를 수정한 뒤 DB에 반영하는 올바른 순서는?

- ① migrate → makemigrations
- ② makemigrations → migrate
- ③ runserver → migrate
- ④ makemigrations → runserver

---

### 11. 객체가 **처음 생성될 때만** 현재 시각을 자동 저장하는 옵션은?

- ① `auto_now=True`
- ② `default=now`
- ③ `auto_now_add=True`
- ④ `auto_create=True`

---

### 12. `updated_at = models.DateTimeField(auto_now=True)`의 동작은?

- ① 객체가 처음 생성될 때만 시각을 저장한다.
- ② 사용자가 form에서 직접 시각을 입력해야 한다.
- ③ DB에 NULL이 저장된다.
- ④ 객체가 save()될 때마다 현재 시각으로 갱신된다.

---

### 13. 데이터가 이미 있는 테이블에 NULL을 허용하지 않는 새 필드를 추가하고 makemigrations를 실행하면?

- ① 기존 데이터가 모두 자동으로 삭제된 뒤 필드가 추가된다.
- ② 새 필드는 기존 행에서 NULL 값으로 자동 채워진다.
- ③ 기존 행에 채울 기본값을 묻는 프롬프트가 나온다.
- ④ 에러가 발생하며 해당 필드는 더 이상 추가할 수 없다.

---

### 14. Migrations에 대한 설명으로 **옳지 않은** 것은?

- ① 변경 사항이 코드로 남아 협업 시 추적·공유가 쉽다.
- ② 처음 migrate하면 admin, auth 같은 기본 앱의 migration도 함께 적용된다.
- ③ `showmigrations`로 각 migration의 적용 여부를 확인할 수 있다.
- ④ migrations 폴더의 자동 생성 파일은 필요할 때 직접 수정하는 것이 원칙이다.

---

### 15. `python manage.py sqlmigrate articles 0001`의 역할은?

- ① 해당 migration이 실행할 SQL을 출력만 한다.
- ② 해당 migration을 DB에 적용한다.
- ③ 0001 migration 파일을 삭제한다.
- ④ articles 앱의 모든 데이터를 SQL 파일로 백업한다.

---

### 16. Admin 사이트에서 사용할 관리자 계정을 만드는 명령어는?

- ① `python manage.py createsuperuser`
- ② `python manage.py createadmin`
- ③ `django-admin createsuperuser`
- ④ `python manage.py adduser`

---

### 17. Article 모델을 Admin 사이트에 표시하기 위한 admin.py 코드는?

- ① `admin.register(Article)`
- ② `admin.site.register(Article)`
- ③ `admin.site.add(Article)`
- ④ `Article.objects.register(admin)`

---

### 18. Django Admin에 대한 설명으로 **옳은** 것은?

- ① 별도 패키지를 설치해야 사용할 수 있다.
- ② 프로젝트의 모든 모델이 자동으로 Admin 화면에 나타난다.
- ③ 등록된 모델의 데이터를 웹 화면에서 생성·조회·수정·삭제할 수 있다.
- ④ createsuperuser를 실행하면 모델 등록도 함께 이루어진다.

---

### 19. Django 기본 설정에서 사용하는 데이터베이스와 그 파일의 연결로 옳은 것은?

- ① MySQL — db.mysql
- ② SQLite — db.sqlite3
- ③ PostgreSQL — db.psql
- ④ SQLite — manage.py

---

### 20. 학습용 로컬 DB를 초기화하는 방법으로 옳은 것은?

- ① 번호 붙은 migration 파일과 db.sqlite3 삭제 후 makemigrations, migrate
- ② `__init__.py`까지 포함해 migrations 폴더를 통째로 삭제한 뒤 migrate만 실행
- ③ models.py의 클래스를 모두 지우고 runserver를 다시 실행해 테이블을 비운다
- ④ 같은 방법으로 운영 서버의 데이터도 초기화해 맞춘다

---

## 함정 문제 (21~30)

### 21. `title = models.CharField(max_length=10, null=True)`로 정의하고, form에서 title을 **비운 채** 제출하면?

- ① DB에 NULL로 저장된다.
- ② 빈 문자열 ''로 저장된다.
- ③ blank 기본값이 False라 유효성 검사에서 막힌다.
- ④ max_length 검사만 통과하면 그대로 저장된다.

---

### 22. Model에 대한 설명으로 **옳지 않은** 것은?

- ① DB 테이블 구조를 정의하는 Python 클래스다.
- ② Model 클래스가 곧 데이터베이스 그 자체다.
- ③ 클래스 변수 하나가 테이블 컬럼 하나에 대응한다.
- ④ models.Model을 상속해 테이블 생성·CRUD 기능을 물려받는다.

---

### 23. `migrate`에 대한 설명으로 **옳은** 것은?

- ① migration 파일을 바탕으로 DB에 변경 사항을 적용한다.
- ② 모델 변경을 감지해 migration 파일을 새로 만든다.
- ③ 모델이 바뀌지 않았어도 매번 새 migration 파일을 만든다.
- ④ migration 파일이 없으면 models.py를 직접 읽어 테이블을 만든다.

---

### 24. 기존 데이터가 있는 테이블에 created_at을 추가하다 makemigrations 프롬프트에서 `1) Provide a one-off default now`를 고르고 timezone.now를 입력했다. **옳은** 것은?

- ① models.py의 필드에 default=timezone.now가 자동으로 추가된다.
- ② 앞으로 새로 만드는 글에도 이 값이 기본값으로 계속 쓰인다.
- ③ 이미 있던 행들을 채우는 데만 한 번 쓰인다.
- ④ 기존 행은 비워 두고 새로 만드는 행에만 적용된다.

---

### 25. 생성일·수정일 필드와 옵션의 연결로 **옳은** 것은?

- ① created_at — auto_now=True / updated_at — auto_now_add=True
- ② created_at — auto_now_add=True / updated_at — auto_now=True
- ③ created_at, updated_at 모두 auto_now=True
- ④ created_at, updated_at 모두 auto_now_add=True

---

### 26. superuser를 만들고 admin에 로그인했는데 Article 메뉴가 보이지 않는다. 가장 직접적인 원인은?

- ① superuser에게는 Article을 볼 권한이 없어서
- ② migrate를 하지 않아 Article 테이블이 없어서
- ③ runserver를 다시 실행하지 않아서
- ④ admin.py에 Article을 등록하지 않아서

---

### 27. `python manage.py showmigrations` 결과에서 `[ ] 0002_article_created_at...`의 의미는?

- ① 0002 migration 파일이 손상되었다.
- ② 0002 migration이 아직 DB에 적용되지 않았다.
- ③ 0002 migration이 이미 DB에 적용되었다.
- ④ 0002 migration 파일이 아직 만들어지지 않았다.

---

### 28. accounts 앱에 `class Profile(models.Model)`을 만들고 migrate했다. 생성되는 테이블 이름은?

- ① `profile`
- ② `Profile`
- ③ `profile_accounts`
- ④ `accounts_profile`

---

### 29. 다음 중 makemigrations가 **필요 없는** 변경은?

- ① views.py의 함수 내용을 수정했다.
- ② 모델에 새 필드를 추가했다.
- ③ 필드의 max_length 값을 바꿨다.
- ④ 모델에서 필드 하나를 삭제했다.

---

### 30. Admin 사이트에서 게시글 내용을 수정하고 SAVE를 눌렀다. 옳은 것은?

- ① Admin 화면에서만 바뀌고 DB에는 반영되지 않는다.
- ② 다음 migrate를 실행할 때 DB에 반영된다.
- ③ DB의 articles_article 테이블에 바로 반영된다.
- ④ Admin 수정은 superuser의 개인 복사본에만 적용된다.

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ① | ③ | ③ | ② | ④ | ② | ④ | ① | ④ | ② |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ③ | ④ | ③ | ④ | ① | ① | ② | ③ | ② | ① |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ③ | ② | ① | ③ | ② | ④ | ② | ④ | ① | ③ |

- **1. ①** `models.Model`을 상속해야 테이블 생성·CRUD 등 모델 기능을 물려받는다. CharField는 개별 컬럼 타입.
- **2. ③** 테이블 이름은 `앱이름_모델이름소문자`. id는 자동 생성되고, 필드는 컬럼에 해당하며, 테이블은 migrations 이후에 생긴다.
- **3. ③** 인스턴스 1개는 테이블의 **행(레코드) 1개**에 해당한다.
- **4. ②** 길이가 제한된 짧은 문자열은 CharField, 본문처럼 긴 글은 TextField.
- **5. ④** CharField에는 max_length를 항상 적는다. 10자를 넘으면 유효성 검사에서 걸린다.
- **6. ②** TimeField는 시간만 저장한다. 날짜와 시간을 함께 저장하는 건 DateTimeField.
- **7. ④** null=DB에 NULL 허용, blank=form에서 빈 값 허용. 기본값은 둘 다 False이고 서로 대체할 수 없다.
- **8. ①** blank=True는 form 검증에서 빈 값을 허용한다. 문자열 필드는 빈 문자열 `''`로 저장되며 SQL NULL과는 다르다.
- **9. ④** makemigrations는 설계도 파일만 만든다. 실제 DB 반영은 migrate.
- **10. ②** model 변경 → makemigrations(설계도 생성) → migrate(DB 반영).
- **11. ③** add = 최초 추가 시점. created_at에 쓴다.
- **12. ④** auto_now는 저장할 때마다 갱신 → 수정 시각 기록용.
- **13. ③** 기존 행에 채울 값이 없기 때문. 1) 지금 일회성 기본값 입력(빈 Enter 시 timezone.now) 또는 2) 종료 후 models.py에 default 지정.
- **14. ④** 자동 생성된 migration 파일은 직접 수정·삭제하지 않는 것이 원칙이다.
- **15. ①** sqlmigrate는 migration이 어떤 SQL로 변환되는지 보여줄 뿐 실행하지 않는다.
- **16. ①** manage.py 위치에서 createsuperuser. migrate로 기본 테이블이 먼저 있어야 한다.
- **17. ②** `from .models import Article` 후 `admin.site.register(Article)`.
- **18. ③** Admin은 기본 제공되며, 등록(register)한 모델만 보인다. 계정 생성과 모델 등록은 별개 작업.
- **19. ②** 기본 DB 엔진은 가벼운 관계형 DB인 SQLite, 데이터는 db.sqlite3 파일 하나에 저장된다.
- **20. ①** `__init__.py`는 남겨야 한다. 이 방법은 데이터가 전부 사라지므로 로컬 학습 환경에서만 쓴다.
- **21. ③** null=True는 DB 레벨 설정일 뿐이다. form에서 비워도 되게 하려면 blank=True가 따로 필요하다.
- **22. ②** Model은 DB를 다루기 위한 설계도이자 인터페이스다. 실제 데이터는 db.sqlite3 같은 DB에 있다.
- **23. ①** ②는 makemigrations의 설명이다. 둘의 역할을 뒤바꾼 보기가 단골 함정.
- **24. ③** one-off(일회성) 기본값은 기존 행을 채우기 위한 것이다. 모델 필드의 영구 `default=` 옵션과는 다르다.
- **25. ②** add = 처음 추가될 때 한 번(생성일), now = 저장할 때마다(수정일). 뒤바꾼 ①이 대표 함정.
- **26. ④** 계정 생성과 모델 등록은 별개. `admin.site.register(Article)`을 해야 메뉴가 나온다.
- **27. ②** `[X]`는 적용됨, `[ ]`는 파일은 있지만 미적용. migrate를 실행하면 [X]가 된다.
- **28. ④** `앱이름_모델이름소문자`. Article이 articles_article이 되는 것과 같은 규칙.
- **29. ①** migration은 모델(테이블 구조) 변경만 기록한다. view 코드는 DB 구조와 무관.
- **30. ③** Admin의 CRUD는 실제 DB 데이터를 바로 바꾼다. migrate는 데이터가 아니라 구조 변경용.
