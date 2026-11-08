# Django 04 — ORM

> 📎 확인문제·예상문제·암기카드: [`시험대비/04_orm_시험대비.md`](시험대비/04_orm_시험대비.md)

*(3단원에서 만든 테이블에 Python 코드로 데이터를 넣고·읽고·고치고·지운다(CRUD). SQL 대신 QuerySet API를 쓰는 방법과, 그 결과를 View→Template으로 넘기는 첫 연결까지. 5단원에서 이걸 웹 화면 기능으로 확장한다.)*

## 오늘의 목차

1. ORM
2. QuerySet API
3. QuerySet API 실습 준비
4. Create
5. Read
6. Update
7. Delete
8. Field Lookups
9. ORM with view (전체 게시글 조회)

---

## 1. ORM

- **Object-Relational Mapping**: 객체 지향 프로그래밍 언어의 **객체(Object)와** DB의 **데이터**를 매핑하는 기술
- 매핑(Mapping): 코드 상의 '객체'와 DB의 '테이블(데이터)'이 1:1로 대응되도록 연결하는 것
- 문제 상황: Django는 **Python**, DB는 **SQL** 사용 → 언어 차이로 소통 불가
- ORM의 역할: Django와 DB 사이의 **번역자(통역사)**
  - SQL을 직접 작성하지 않고 파이썬 코드로 데이터 조작
  - 코드 작성 시간과 실수 감소
- ORM은 개발자에게 **QuerySet API**라는 도구를 제공

> 💡 SQL이 사라지는 게 아니다. ORM이 **내부적으로 SQL을 만들어서** 실행해 주는 것 — 개발자가 직접 쓸 필요가 줄어들 뿐.

---

## 2. QuerySet API

- DB의 복잡한 SQL 쿼리문을 **SQL 대신 직관적인 Python 코드로** DB에 요청할 수 있게 해주는 도구(인터페이스)
- `.filter()`, `.exclude()`, `.order_by()` 등의 메서드로 생성·조회·수정·삭제
- **Query**: DB에 특정 데이터를 보여 달라는 요청 ("쿼리문을 작성한다" = 원하는 데이터를 얻기 위해 DB에 요청을 보낼 코드를 작성한다)

### Query 처리 과정

1. 파이썬 코드 → ORM: QuerySet API(파이썬 코드)가 ORM으로 전달
2. ORM → SQL 변환: SQL 쿼리로 변환해 DB에 전달
3. DB 응답 → ORM: DB가 쿼리를 처리하고 결과를 ORM에 반환
4. ORM → QuerySet 변환: 결과를 **QuerySet 또는 Instance**(파이썬 객체)로 변환해 전달

### QuerySet

- Django ORM을 통해 만들어진 자료형
- DB에서 전달받은 **객체 목록(데이터 모음)**, 순회 가능, **0개 이상**의 데이터
- 단, `get()`처럼 **단일 객체를 조회하는 메서드는 QuerySet이 아닌 모델의 인스턴스를 반환**

### 구문 기본 구조

```python
Article.objects.all()
# Model class . Manager . QuerySet API
```

| 구성 | 역할 |
|---|---|
| `Article` (모델 클래스) | DB 테이블에 대한 Python 클래스 표현 (`articles_article` 테이블의 스키마 정의) |
| `.objects` (매니저) | DB 질의 작업을 위한 기본 인터페이스, 쿼리 작업의 **진입점**. Django가 모든 모델에 자동 추가 |
| `.all()` (QuerySet API 메서드) | 특정 DB 작업을 수행하는 명령 (테이블의 모든 레코드 조회 SQL 생성·실행) |

---

## 3. QuerySet API 실습 준비

### CRUD

- 대부분의 소프트웨어가 가지는 기본 데이터 처리 기능
- **C**reate(생성), **R**ead(조회), **U**pdate(수정), **D**elete(삭제)
- Django에서는 QuerySet API를 통해 복잡한 SQL 없이 Python 코드로 CRUD를 직관적으로 수행

### 사전 준비

```bash
$ pip install ipython
$ pip freeze > requirements.txt
```

- **IPython**: 일반 파이썬 셸보다 자동 완성 등 편리한 작업 환경을 제공하는 도구

### Django Shell

- Django 프로젝트의 코드를 명령창에서 바로 실행하고 테스트하는 특별한 파이썬 환경
- Django 환경 내에서 실행 → 입력한 QuerySet API 구문이 **실제 DB(db.sqlite3)에 그대로 반영**

```bash
$ python manage.py shell
$ python manage.py shell -v 2   # 자동으로 import된 모델 목록까지 출력
```

- `-v` 옵션(기본값 1): 출력 상세도(verbosity level) 설정
- Django 5.2부터 shell이 **설치된 앱의 모델을 자동 import** → `from articles.models import Article`을 따로 안 써도 됨. `-v 2`로 무엇이 import됐는지 확인 가능

> 📌 `-v 2`는 "자동 import 목록"을 보여주는 것이지, ORM이 실행하는 **SQL을 보여주는 옵션이 아니다**.

---

## 4. Create

### 데이터 객체를 생성하는 3가지 방법

**① 빈 객체 생성 후 값 할당 및 저장**

```python
>>> article = Article()          # Article(class)로부터 article(instance) 생성
>>> article
<Article: Article object (None)>

>>> article.title = 'first'      # 인스턴스 변수에 값 할당
>>> article.content = 'django!'

# save를 하지 않으면 아직 DB에 저장되지 않음
>>> Article.objects.all()
<QuerySet []>

>>> article.save()
>>> article
<Article: Article object (1)>
>>> article.id    # 1
>>> article.pk    # 1
>>> Article.objects.all()
<QuerySet [<Article: Article object (1)>]>
```

**② 초기 값과 함께 객체 생성 및 저장**

```python
>>> article = Article(title='second', content='django!')
>>> article                       # 아직 저장 안 됨
<Article: Article object (None)>
>>> article.save()
>>> article
<Article: Article object (2)>
```

- ①, ② 모두 **save 메서드를 호출해야 DB에 저장됨** (테이블에 한 행(레코드)이 쓰여진 것)
- pk는 **save() 이후에** 배정됨 (그 전엔 `None`)

**③ create() 메서드로 한 번에 생성 및 저장**

```python
>>> Article.objects.create(title='third', content='django!')
<Article: Article object (3)>
```

- 생성과 동시에 저장되고, **생성된 객체가 반환**됨
- create()는 객체 생성과 DB 저장을 한 번에 처리하는 **단축 메서드** → 뒤에 save() 필요 없음

### save()

- 객체를 DB에 저장하는 **인스턴스 메서드**
- 저장 전에 값을 더 채우거나 바꿔야 할 때 생성과 저장을 나눠서 사용
- 입력값이 올바른지 **검사하지 않고** 그대로 저장 (입력값 검사는 Form에서 — 6단원)
- 반환값은 `None` (저장된 객체를 돌려주는 게 아님)

---

## 5. Read

| 구분 | 메서드 | 설명 |
|---|---|---|
| QuerySet 반환 | `all()` | 전체 데이터 조회 |
| QuerySet 반환 | `filter()` | 주어진 매개변수와 일치하는 객체를 포함하는 QuerySet 반환 |
| QuerySet 반환 X | `get()` | 주어진 매개변수와 일치하는 **객체(인스턴스)** 반환 |

```python
>>> Article.objects.all()
<QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>]>

>>> Article.objects.filter(content='django!')   # 3개 모두
>>> Article.objects.filter(title='abc')
<QuerySet []>                                    # 없으면 빈 QuerySet (에러 아님)
>>> Article.objects.filter(title='first')
<QuerySet [<Article: Article object (1)>]>

>>> Article.objects.get(pk=1)
<Article: Article object (1)>
>>> Article.objects.get(pk=100)
DoesNotExist: Article matching query does not exist.
>>> Article.objects.get(content='django!')
MultipleObjectsReturned: get() returned more than one Article -- it returned 3!
```

### 결과 개수별 비교

| 결과 | `all()` / `filter()` | `get()` |
|---|---|---|
| 0건 | 빈 QuerySet | **DoesNotExist** 예외 |
| 1건 | 1개 든 QuerySet | 모델 인스턴스 |
| 2건 이상 | 여러 개 든 QuerySet | **MultipleObjectsReturned** 예외 |

### get()의 특징

- 객체가 없으면 **DoesNotExist**, 둘 이상이면 **MultipleObjectsReturned** 예외 발생
- 따라서 **primary key처럼 고유성(uniqueness)을 보장하는 조회**에서 사용
- Primary key(pk): DB 테이블에서 각 행을 고유하게 식별할 수 있는 속성

---

## 6. Update

- 인스턴스 변수를 변경한 후 save 메서드 호출

```python
>>> article = Article.objects.get(pk=1)   # 수정할 인스턴스 조회
>>> article.title = 'byebye'              # 인스턴스 변수 변경
>>> article.save()                        # 저장
```

- save()는 **pk가 없으면 새로 생성(INSERT), pk가 있으면 수정(UPDATE)** → Create와 Update 모두 save() 사용
- 값만 대입하고 save()를 안 하면 **메모리 속 객체만 바뀌고 DB는 그대로**

> 📌 조건에 맞는 여러 행을 한 번에 바꾸려면 QuerySet의 `update()`를 쓸 수도 있다. 이건 save()를 거치지 않고 바로 UPDATE SQL을 실행하며, **영향받은 행 수**를 반환한다.
>
> ```python
> Article.objects.filter(title='old').update(title='new')
> ```

---

## 7. Delete

- 삭제할 데이터를 조회한 후 delete 메서드 호출

```python
>>> article = Article.objects.get(pk=1)
>>> article.delete()
(1, {'articles.Article': 1})     # (삭제된 총 개수, 모델별 삭제 개수) 튜플 반환

>>> Article.objects.get(pk=1)
DoesNotExist: Article matching query does not exist.
```

- QuerySet에도 `.delete()` 가능 → `Article.objects.filter(title='old').delete()` (전체 삭제 `all().delete()`는 주의)
- 1번 글 삭제 후 새 글을 만들면 1번이 아니라 4번 → **한 번 쓴 pk는 재사용하지 않음**

> 📌 pk 재사용 안 하는 건 Django가 SQLite에 테이블을 만들 때 `AUTOINCREMENT`를 붙이기 때문이다. 정확히는 DB 엔진/설정에 따른 동작이지만, 강의 환경(SQLite)에서는 "재사용 안 함"으로 기억하면 된다.

---

## 8. Field Lookups

- 조회 조건을 세밀하게 지정하는 문법: **`필드명__lookup=값`** (언더스코어 **2개**)
- `filter()`, `exclude()`, `get()`에서 사용

```python
Article.objects.filter(title__exact='Django')       # 정확히 일치 (title='Django'와 같음)
Article.objects.filter(title__contains='jang')      # 문자열 포함
Article.objects.filter(title__icontains='JANG')     # 대소문자 무시하고 포함
Article.objects.filter(title__startswith='Dja')     # 시작 문자열 일치
Article.objects.filter(title__istartswith='dja')    # 대소문자 무시하고 시작 일치
Article.objects.filter(pk__gt=10)                   # 초과 (>)
Article.objects.filter(pk__gte=10)                  # 이상 (>=)
Article.objects.filter(pk__lt=10)                   # 미만 (<)
Article.objects.filter(pk__lte=10)                  # 이하 (<=)

Article.objects.exclude(title='abc')                # 제목이 abc인 행을 '제외'
```

| lookup | 의미 | 기억법 |
|---|---|---|
| `exact` | 정확히 일치 | 생략하면 기본값 |
| `contains` / `icontains` | 포함 / 대소문자 무시 포함 | `i` = case-**i**nsensitive |
| `startswith` | 앞부분 일치 | 포함이 아니라 **시작** |
| `gt` / `gte` / `lt` / `lte` | > / >= / < / <= | greater / less + equal |

---

## 9. ORM with view (전체 게시글 조회)

### View에서의 QuerySet API

- 웹 페이지에 보여줄 데이터를 DB에서 **가져올 때** 사용
- 사용자가 입력한 새로운 데이터를 DB에 **저장할 때** 사용
- 2가지 Read: 전체 게시글 조회(이번 단원), 단일 게시글 조회(5단원)

### 전체 게시글 조회

```text
http://127.0.0.1:8000/articles/ → 프로젝트 urls → 앱 urls → views ↔ models(DB) / templates
```

```python
# crud/urls.py  (crud는 프로젝트 이름)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
]
```

```python
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
]
```

- 앱 URL의 빈 문자열(`''`): include로 `articles/` 부분은 잘려나가고 나머지만 앱 urls.py로 전달 → `''`는 **`articles/` 자체**를 의미

```python
# articles/views.py
from django.shortcuts import render
from .models import Article

def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)
```

```html
<!-- templates/articles/index.html -->
<h1>Articles</h1>
<hr>
{% for article in articles %}
  <div>
    <p>글 번호: {{ article.pk }}</p>
    <p>글 제목: {{ article.title }}</p>
    <p>글 내용: {{ article.content }}</p>
  </div>
  <hr>
{% empty %}
  <p>게시글이 없습니다.</p>
{% endfor %}
```

- `{{ articles }}`를 그대로 찍으면 `<QuerySet [<Article: Article object (1)>, ...]>` 문자열이 나옴 → **for 태그로 하나씩 꺼내서** 필드에 접근해야 함
- `{% empty %}`: 순회할 데이터가 0개일 때 출력할 내용

> ⚠️ 흔한 실수: QuerySet을 만들어 놓고 **context에 안 넣음** / 템플릿 변수명 오타 / render의 템플릿 경로 오타
