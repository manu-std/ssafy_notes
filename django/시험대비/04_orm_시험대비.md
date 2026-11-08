# Django 4단원 시험대비 — ORM

> 📎 개념 정리 노트: [`../04_orm.md`](../04_orm.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

출처: 업로드된 SSAFY Django ORM 강의 이미지 62장(p001~p062). 중요도는 강의 내용과 확인문제에 근거한 예측이며 실제 출제를 보장하지 않습니다. 학습시간 권장 70~100분 + 오답 복습.

## 0. PPT 구조 및 시험 범위 매핑

| 슬라이드 | 내용 | 우선도 |
| --- | --- | --- |
| 3~9 | ORM 정의, Python과 DB 사이 중개 | ★★★ |
| 11~16 | QuerySet API, QuerySet, 기본 구조 Article.objects.all() | ★★★ |
| 18~29 | CRUD, Shell, 생성 3가지 방식, save, create | ★★★ |
| 30~35 | all, filter, get, 예외 | ★★★ |
| 36~39 | 수정 및 삭제 | ★★★ |
| 40~46 | View 연동, 전체 게시글 페이지 | ★★★ |
| 48~51 | Field Lookups (exact, contains, icontains, 접두 검색) | ★★★ |
| 52~54 | ORM의 장점, 과제 | ★★ |
| 55~58 | 강의 확인문제 12개와 해답 | ★★★ |
| 59~61 | 정리 | ★★ |

## 1. ORM과 QuerySet API

ORM(Object-Relational Mapping): 객체 지향 언어의 객체와 관계형 데이터베이스의 테이블 사이에서 매핑하고 DB 작업을 처리하는 기술. Django에서는 모델 클래스를 이용해 Python 코드로 데이터베이스를 조회·수정할 수 있다. 내부적으로 적절한 SQL을 생성하고 결과를 모델 인스턴스나 QuerySet 등으로 변환한다. SQL이 완전히 사라지는 게 아니라 직접 작성할 필요가 줄어든다.

QuerySet API: 모델과 Manager를 통해 DB 쿼리를 작성하는 Django API. 기본 예시 Article.objects.all()에서 Article=모델클래스, objects=기본 Manager, all()=QuerySet API 메서드. QuerySet은 DB 조회 결과를 나타내는 객체로 추가 필터링·정렬 가능하며 일반적으로 지연 평가(lazy evaluation)된다. 모든 QuerySet이 단순한 Python list는 아니다.

주의: get()은 QuerySet이 아니라 모델 인스턴스 한 개 반환. all() / filter()는 QuerySet 반환. filter() 결과가 없어도 예외대신 빈 QuerySet 반환.

ORM 작업 흐름: Python의 QuerySet API → ORM이 SQL 생성 → DB 실행 → 결과를 QuerySet 또는 모델 인스턴스 등으로 제공.

## 2. CRUD 요약

CRUD = Create(생성), Read(조회), Update(수정), Delete(삭제).

실습 준비: python manage.py shell 실행, from articles.models import Article로 모델 import. python manage.py shell -v 2는실행한 SQL을 확인하려는 shell verbosity 설정이 아니라, shell의 verbosity를 조정하는 플래그이므로 SQL 출력은 Django DB 로깅 설정이나 connection.queries 같은 방식으로 확인해야 한다. ※ 강의의 p22 그림은 셸 -v 2 예시이며 SQL 확인 용도로 오해하지 않기.

### Create — 반드시 세 가지 비교

```
from articles.models import Article

# 1) 빈 인스턴스 생성 → 값 할당 → save
article = Article()
article.title = 'first'
article.content = 'django'
article.save()

# 2) 인스턴스 생성 때 값 지정 → save
article = Article(title='second', content='django')
article.save()

# 3) objects.create: 생성과 DB 저장을 한 번에
article = Article.objects.create(title='third', content='django')
```

- Article(...)만 실행하면 Python 객체만 생성; save() 이전에는 신규 레코드가 DB에 저장되지 않음.
- 일반적인 자동 생성 PK는 최초 save() 또는 create() 후 배정된다. article.pk, article.id로 확인.
- save()는 반환값이 None이며, 저장된 객체 자체가 반환되는 것이 아님.
- objects.create()는 저장까지 완료하고 생성된 인스턴스를 반환.
- article.created_at 등 날짜 필드는 3단원에서 배운 auto_now_add, auto_now와 연결해서 이해.

### Read

```
Article.objects.all()                   # 전체 QuerySet
Article.objects.filter(title='first')  # 조건 일치 QuerySet (0개 이상)
Article.objects.get(pk=1)              # 딱 하나의 Article 인스턴스
```

| 구분 | all() | filter() | get() |
| --- | --- | --- | --- |
| 반환 | QuerySet | QuerySet | 모델 인스턴스 |
| 0건 | 빈 QuerySet | 빈 QuerySet | DoesNotExist |
| 1건 | 1개 포함 QuerySet | 1개 포함 QuerySet | 모델 인스턴스 |
| 2건 이상 | 여러 개 포함 QuerySet | 여러 개 포함 QuerySet | MultipleObjectsReturned |
| 용도 | 전체 | 조건에 맞는 복수 | 정확히 한 객체 |

예외: Article.DoesNotExist, Article.MultipleObjectsReturned (Django 모델별 예외). PK는 일반적으로 유일한 값이므로 get(pk=1)로 여러 객체가 동시에 일치하지 않는다. filter(pk=999)는 빈 QuerySet; get(pk=999)는 DoesNotExist.

### Update

```
article = Article.objects.get(pk=1)
article.title = 'updated'
article.save()                    # DB 반영
Article.objects.filter(title='old').update(title='new')  # 조건 일괄 수정
```

- 인스턴스 필드에 새로운 값을 대입하기만 하면 메모리 객체만 바뀜. DB 반영은 save().
- QuerySet.update(...)는 직접 UPDATE 실행. save()를 호출하지 않으며 save() 기반 모델 동작이나 signals가 동일하게 실행된다고 생각하지 않기.
- .update() 반환값은 영향을 받은 행 수(매칭된 행 수).

### Delete

```
article = Article.objects.get(pk=1)
article.delete()                             # 한 객체 삭제
Article.objects.filter(title='old').delete() # 해당 조건의 객체 삭제
Article.objects.all().delete()              # 전체 삭제 — 주의
```

- 인스턴스 .delete()와 QuerySet .delete() 모두 가능.
- 반환값은 보통 (삭제된 객체 총 개수, 모델별 삭제 개수 dict) 형태. 연관 객체의 CASCADE 삭제가 있으면 총 건수에 포함될 수있음.
- 삭제된 객체를 다시 get(pk=1) 조회하면 DoesNotExist; 새로운 create 시 ID가 이전 값과 연속되거나 재사용되는지는 DB/설정에 따라 다를 수 있음.

## 3. Field Lookups

패턴: field__lookup=value — 언더스코어 2개. filter, exclude, get 등에서 사용.

```
Article.objects.filter(title__exact='Django')       # 정확히 일치
Article.objects.filter(title__contains='jang')      # 문자열 포함
Article.objects.filter(title__icontains='JANG')     # 대소문자 무시 포함
Article.objects.filter(title__startswith='Dja')     # 시작 문자열 일치
Article.objects.filter(title__istartswith='dja')    # 대소문자 무시 시작
Article.objects.filter(pk__gt=10)                   # 초과
Article.objects.filter(pk__gte=10)                  # 이상
Article.objects.filter(pk__lt=10)                   # 미만
Article.objects.filter(pk__lte=10)                  # 이하
```

- title='Django'는 일반적으로 title__exact='Django'의 축약.
- contains와 icontains: i는 case-insensitive. 다만 실제 DB 백엔드/Collation에 따른 대소문자 민감도 차이가 있을 수 있어시험에서는 Django API의 의도된 의미로 답하기.
- startswith는 포함 여부가 아니라 앞부분 일치.
- filter(title__contains='Django'): 제목(title)에 'Django'가 포함되는 게시물.
- exclude(title='abc'): 제목이 abc인 행을 제외.

## 4. ORM + View + Template 연결 (앞 단원과 연결)

```
# 프로젝트 urls.py
from django.urls import path, include
urlpatterns = [path('articles/', include('articles.urls'))]

# 앱 urls.py
from django.urls import path
from . import views
app_name = 'articles'
urlpatterns = [path('', views.index, name='index')]

# articles/views.py
from django.shortcuts import render
from .models import Article

def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

<!-- articles/templates/articles/index.html -->
{% for article in articles %}
  <p>{{ article.pk }} - {{ article.title }} - {{ article.content }}</p>
{% empty %}
  <p>게시글이 없습니다.</p>
{% endfor %}
```

요청 /articles/ → 프로젝트 URL에서 include → 앱 URL에서 index로 연결 → View에서 QuerySet 조회 → context로 Template 전달 → HTML 응답. 앞 단원에서 다룬 render, include, DTL 반복문의 합성 문제 출제 가능.

흔한 실수: View에서 articles = Article.objects.all()만 만들고 context에 넣지 않음; 템플릿에서 articles라는 변수명을 잘못씀; return render(request, 'articles/index.html', context)의 템플릿 경로 오기.

## 5. 강의 확인문제 12개 (p55~58) — 핵심 정답과 해설

아래는 강의 확인문제의 출제 의도를 간단히 재구성한 것이며, 정답은 p58의 공식 정답표에 맞췄다.

1. Django ORM을 사용하면 SQL을 직접 작성하지 않고 Python 코드로 DB를 조작할 수 있는가? → O. ORM이 SQL을 생성한다.
2. 새 레코드 생성 + 저장을 한 번에 수행하는 메서드는? → Post.objects.create(title='New Post').
3. 전체 게시글 객체를 반환하는 기본 메서드는? → Post.objects.all().
4. 단일 객체 조회 후 제목 수정 및 저장 코드는? → post = Post.objects.get(id=1); post.title='수정됨!'; post.save().
5. 특정 게시글(id=1) 삭제는? → Post.objects.get(id=1).delete().
6. 제목이 'Welcome'으로 정확히 같은 데이터 조회는? → Post.objects.filter(title='Welcome').
7. 제목에 'Django' 포함 문자열 검색은? → Post.objects.filter(title__contains='Django').
8. ORM의 이점은 쿼리를 자동 생성해 직접 작성 부담을 줄이는 것인가? → O.
9. 작성자가 'anonymous'인 모든 글 삭제는? → Post.objects.filter(author='anonymous').delete().
10. 여러 레코드 필드 값을 한꺼번에 바꾸는 메서드는? → update().
11. 모든 Post 삭제는? → Post.objects.all().delete().
12. all()과 get() 반환 타입 차이는? → all()=QuerySet, get()=단일 모델 인스턴스.

## 6. 추가 예상 객관식 15문제

정답은 뒤에 있으니 먼저 풀어보기.

O1. Article.objects.all()에서 objects 역할은? ① 템플릿 변수 ② Manager ③ 기본 키 ④ HTTP 객체

O2. 아직 저장하지 않은 신규 Article(title='A')에 대한 설명으로 옳은 것은? ① DB에 즉시 저장 ② 생성과 동시에 migration 실행 ③ 파이썬 인스턴스만 생성 ④ 무조건 pk=1

O3. Article.objects.filter(pk=999)가 일치하는 행이 없을 때? ① 빈 QuerySet ② DoesNotExist ③ None ④ TypeError

O4. Article.objects.get(pk=999)가 일치하는 행이 없을 때? ① 빈 QuerySet ② DoesNotExist ③ None ④ 빈 리스트

O5. Article.objects.get(title='A')의 검색 결과가 3개면? ① 첫 번째 반환 ② 리스트 반환 ③ MultipleObjectsReturned ④ 빈 QuerySet

O6. 새 레코드 생성·저장을 동시에 하는 코드는? ① Article(title='A') ② Article.objects.create(title='A', content='B') ③ Article.objects.filter(title='A') ④ Article.objects.all()

O7. article.save()의 일반적인 반환값은? ① 저장된 객체 ② 1 ③ None ④ QuerySet

O8. article.title='B'만 실행하고 save를 하지 않았을 때? ① 해당 메모리 객체 값만 변경 ② DB도 즉시 수정 ③ 객체 자동 삭제 ④ 새 레코드 삽입

O9. Article.objects.filter(title__icontains='Django')의 의도된 조건은? ① 제목 정확히 Django ② 제목에 Django 포함, 대소문자 무시 ③ 제목이 Django로 시작 ④ 제목에서 Django 제외

O10. Article.objects.filter(title__startswith='Hi')는? ① Hi가 포함되는 모든 위치 ② Hi로 끝남 ③ Hi로 시작 ④ Hi와 정확히일치

O11. Article.objects.filter(pk__gte=5)의 의미? ① pk가 5 초과 ② pk가 5 이상 ③ pk가 5 이하 ④ pk가 5 미만

O12. Article.objects.all().delete()의 의미? ① 단일 객체만 삭제 ② 모든 Article 객체 삭제 ③ migrations 삭제 ④ 데이터베이스 파일 삭제

O13. View에서 조회한 QuerySet을 템플릿으로 전달할 올바른 방법은? ① render(request, 'articles/index.html', {'articles': articles}) ② render('articles/index.html') ③ Article.render(articles) ④ path(articles)

O14. QuerySet.update()에 대한 옳은 설명은? ① 모든 객체의 save를 호출 ② QuerySet 조건에 맞는 레코드 일괄 수정 ③ 새로운테이블 생성 ④ QuerySet만 리턴

O15. get()과 filter() 비교로 옳은 것은? ① 둘 다 list ② get은 모델 인스턴스, filter는 QuerySet ③ get은 QuerySet, filter는인스턴스 ④ 둘 다 반드시 하나만 반환

### 객관식 정답과 해설

O1 ② Manager를 통해 API 호출.

O2 ③ save() 전 DB 미반영.

O3 ① 0건도 빈 QuerySet.

O4 ② get() 예외.

O5 ③ get()은 반드시 딱 1건.

O6 ② create는 즉시 저장.

O7 ③ save는 None 반환.

O8 ① save가 DB 반영.

O9 ② icontains 대소문자 무시 부분일치.

O10 ③ 접두어.

O11 ② gte는 greater than or equal.

O12 ② 전체 레코드 삭제.

O13 ① context 전달.

O14 ② QuerySet 조건 일괄 수정.

O15 ② 반환 타입이 다름.

## 7. 추가 주관식 10문제

S1. ORM의 영문 풀네임을 작성하라.

S2. Article.objects.all()에서 objects의 역할을 쓰라.

S3. Article(title='A', content='B')로 만든 신규 인스턴스를 DB에 저장하는 메서드를 쓰라.

S4. get() 결과가 0건일 때 발생하는 예외명을 쓰라.

S5. get() 결과가 2건 이상일 때 발생하는 예외명을 쓰라.

S6. title 필드에 문자열 'python'이 포함된 객체를 조회하는 코드를 작성하라.

S7. pk가 3인 Article의 제목을 '수정'으로 바꾸고 DB에 저장하는 코드를 작성하라.

S8. title이 'old'인 객체들을 모두 삭제하는 코드를 작성하라.

S9. title에 'AI'가 포함된 레코드의 content를 모두 'updated'로 바꾸는 코드를 작성하라.

S10. get()과 filter()의 반환 타입을 각각 쓰라.

### 주관식 정답

S1 Object-Relational Mapping. S2 Manager(모델의 QuerySet API 호출 인터페이스). S3 article.save() (변수명을 article이라고 가정). S4 Article.DoesNotExist 또는 DoesNotExist. S5 Article.MultipleObjectsReturned 또는 MultipleObjectsReturned. S6 Article.objects.filter(title__contains='python'). S7 a=Article.objects.get(pk=3);

a.title='수정'; a.save(). S8 Article.objects.filter(title='old').delete(). S9 Article.objects.filter(title__contains='AI').update(content='updated'). S10 get()=모델 인스턴스, filter()=QuerySet.

## 8. 추가 서술형 5문제 + 만점 모범답안

D1. Django ORM의 정의와 장점 및 한계를 설명하라.

모범: ORM은 객체 지향 프로그래밍 언어의 객체와 관계형 데이터베이스를 매핑하는 기술이다. Django의 ORM은 Python의 모델과 QuerySet API를 통해 SQL을 직접 작성하지 않고도 데이터베이스에 접근하도록 지원한다. 데이터베이스별 SQL 차이를 일부 추상화하여 생산성과 유지보수성을 높일 수 있다. 다만 SQL이 내부적으로 생성되므로 쿼리의 성능을 고려해야 하며 복잡한 작업은 최적화가 필요할 수 있다.

채점 키워드: 객체-관계 매핑 / Python 코드 / SQL 생성 / 추상화 / 성능 유의.

D2. all(), filter(), get()의 차이를 반환 타입·0건·다건 중심으로 비교하라.

모범: all()은 전체 객체를 표현하는 QuerySet을 반환한다. filter()는 지정한 조건에 맞는 QuerySet을 반환하며 결과가 없더라도 빈 QuerySet이다. 반면 get()은 조건에 일치하는 단일 모델 인스턴스를 반환하며 0개면 DoesNotExist, 2개 이상이면 MultipleObjectsReturned 예외가 발생한다.

채점 키워드: QuerySet vs instance / 빈 QuerySet / 두 예외.

D3. 모델 인스턴스 생성 세 가지 방식과 DB 저장 시점의 차이를 설명하라.

모범: (1) 빈 인스턴스를 만들고 필드를 할당한 후 save(), (2) 생성자 인자로 필드 값을 넣고 save(), (3) Article.objects.create(...)를 실행한다. 앞의 두 방식은 save() 호출 시 DB에 INSERT하고, 세 번째는 create()가 생성과 저장을 함께 수행한다.

채점 키워드: 3방식 / 저장 시점 / create()에 save 불필요.

D4. 기존 레코드 수정과 삭제 절차를 예시 코드로 설명하라.

모범: article = Article.objects.get(pk=1)로 객체를 얻고 article.title='새 제목', article.save()로 수정 내용을 반영한다. 삭제는 article.delete()로 수행한다. 다수 레코드에는 Article.objects.filter(...).update(...)와 .delete()를 사용할 수 있다.

채점 키워드: 조회 / 대입 / save / delete / QuerySet 일괄 처리.

D5. 사용자가 /articles/에 접속했을 때 ORM에서 HTML 화면까지의 흐름을 설명하라.

모범: 사용자의 요청 URL은 프로젝트 urls.py와 앱 urls.py에서 해당 View 함수로 라우팅된다. View는 Article.objects.all()을호출해 DB에서 게시글을 조회하고, 조회한 QuerySet을 context={'articles': articles}로 구성한다. render(request, 'articles/ index.html', context)로 템플릿에 전달하며, DTL의 {% for article in articles %} 반복문으로 게시글 HTML을 만들고 응답한다.

채점 키워드: URLconf / View / ORM / QuerySet / context / render / Template.

## 9. 코드 추론 실전 8문제

아래 문제는 Article의 title과 content가 필수 필드이며, 레코드는 ID 1:('Django','web'), ID 2:('django ORM','db'), ID 3: ('Python','db')인 상황을 가정. DB는 대소문자 구별 비교를 지원하도록 설정했다고 가정한다.

1. Article.objects.filter(title__contains='ORM').count() → 1.
2. Article.objects.filter(title__icontains='django').count() → 2.
3. Article.objects.filter(content='db').count() → 2.
4. Article.objects.filter(content='db').get() → MultipleObjectsReturned (get()은 QuerySet의 메서드로 호출 가능하며 2개 일치).
5. Article.objects.get(pk=100) → DoesNotExist.
6. Article.objects.filter(pk=100) → 빈 QuerySet, 예외 아님.
7. Article.objects.filter(content='db').update(content='database') → 2 (매칭 행 수), 해당 두 행의 content 변경.
8. Article.objects.filter(title__startswith='Py').delete() → 해당 행 삭제, 반환은 (삭제 개수, 모델별 개수 dict). 관련 CASCADE 등 없다면 삭제 수 1.

## 10. 고득점 함정 12가지

1. get() → QuerySet ❌, 인스턴스 ✅.
2. filter() 결과 0건 → 예외 ❌, 빈 QuerySet ✅.
3. get() 결과 다건 → 첫 번째 자동 선택 ❌, MultipleObjectsReturned ✅.
4. Article(...) → DB 즉시 저장 ❌, save() 필요 ✅.
5. objects.create() 다음 save() 반드시 필요 ❌, 이미 저장됨 ✅.
6. article.title='x' → DB 자동 수정 ❌, save 필요 ✅.
7. save() 반환 → 객체 ❌, None ✅.
8. delete() 반환 → 항상 1 ❌, 튜플(삭제 수, 모델별 개수) ✅.
9. filter()와 get()을 바꿔 사용 가능 ❌, 반환 타입/예외 다름 ✅.
10. title_contains ❌, title__contains ✅ (언더스코어 2개).
11. startswith와 contains는 동의어 ❌, 접두 vs 포함 ✅.
12. makemigrations 후 DB에서 조회 가능 ❌, 3단원의 migrate 필요 ✅.

## 11. 시험 직전 90초 암기장

- ORM = Object-Relational Mapping. Python 객체 ↔ 관계형 DB.
- Article.objects.all() = Model.Manager.QuerySet API.
- C: Article(...).save() 또는 Article.objects.create(...).
- R: all() 전체 QuerySet, filter() 조건 QuerySet, get() 단일 instance.
- get() 0건=DoesNotExist, 다건=MultipleObjectsReturned.
- U: a = Article.objects.get(pk=1); a.title='x'; a.save().
- 일괄 수정 Article.objects.filter(...).update(...).
- D: a.delete() 또는 Article.objects.filter(...).delete().
- title__contains='a' 포함, title__icontains='a' 대소문자 무시 포함, title__startswith='a' 접두.
- View: ORM 조회 → context → render → Template {% for %}.

## 12. 15분 복습 플랜

- 0~4분: CRUD 핵심 메서드와 반환 타입 표를 보지 않고 써보기.
- 4~7분: get()의 0/1/2건, save()와 create() 비교 암기.
- 7~10분: Field Lookups 6개를 예시로 직접 작성.
- 10~13분: 실전 코드 추론 8문제 풀이.
- 13~15분: 서술형 D2·D5를 4문장 이내로 말하기.

## 13. 1~4단원 누적 연결

- 1단원: MTV에서 Model은 DB 구조/데이터, View는 요청 처리, Template은 출력.
- 2단원: URLconf, render, DTL를 활용하여 화면을 만든다.
- 3단원: **Model / makemigrations / migrate**로 테이블 생성.
- 4단원: QuerySet API로 모델 데이터를 CRUD하고 View→Template으로 전달.

결합 서술형 예시: "Model 정의부터 전체 게시글 페이지 출력까지 설명" → 모델 작성 → 마이그레이션 파일 생성 → 적용 → QuerySet 조회 → URL과 View 연결 → context → Template 렌더링.

### 체크리스트

- ORM 영문명과 역할을 쓸 수 있다.
- all·filter·get 반환 타입과 예외를 설명할 수 있다.
- save와 create의 저장 시점을 구분한다.
- Update·Delete 코드를 빈칸 없이 작성한다.
- Field Lookup의 이중 언더스코어를 기억한다.
- URL → View → ORM → Template 과정을 5문장으로 설명한다.
- 원본 12문제와 추가 30문제 중 틀린 문항을 재풀이했다.
