# Django 5단원 시험대비 — ORM with View

> 📎 개념 정리 노트: [`../05_orm_with_view.md`](../05_orm_with_view.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

분석 대상: Django_ORM_With_View.zip — 이미지 슬라이드 83장 (p001~p083). 강의 확인문제 p076~p079, 공식 정답 p079. 1~4 단원 연결 학습용. 출제 중요도는 강의의 실습 분량과 반복 설명을 바탕으로 한 예상이다. 실제 출제문항을 보장하지 않는다.

## 0. 1분 전체 구조

브라우저 요청 → urls.py 경로 매칭 → views.py 함수 실행 → ORM (Model.objects...) → DB 조회/변경 → render() 또는 redirect() 응답 → 브라우저

- Read: index 목록, detail 단일 레코드 조회.
- Create: new 입력 화면(GET) + create DB 저장(POST).
- Update: edit 수정 화면(GET, 기존 값 표시) + update DB 갱신(POST).
- Delete: delete DB 삭제(POST) + 목록으로 redirect.
- HTTP: GET은 조회, POST는 상태 변화에 사용. POST 폼에는 {% csrf_token %}.
- POST → redirect → GET (PRG): 성공 후 새 URL로 GET을 유도하여 새로고침 중복 제출 위험을 줄임.

## 1. 출제 우선순위

| 중요도 | 개념 | 강의 위치 | 시험에서 확인할 질문 |
| --- | --- | --- | --- |
| ★★★ | Detail 조회와 동적 URL | 7~11 | &lt;int:pk&gt;, .get(pk=pk), context와 링크 |
| ★★★ | Create: new/create 분리 | 13~19 | 입력 페이지와 저장 로직 구분 |
| ★★★ | GET/POST | 20~33, 68~72 | 쿼리스트링, Body, 목적, request.GET/POST |
| ★★★ | CSRF와 HTTP 403 | 34~45 | CSRF 뜻, csrf_token, POST에서 차단 이유 |
| ★★★ | Redirect/PRG | 46~54 | render와 redirect 차이, 두 번째 GET |
| ★★★ | Delete/Update 구현 | 55~66 | save(), delete(), pk, POST 폼 |
| ★★ | HTTP 상태코드 | 34~37, 75~79 | 403 vs 404, 3xx |
| ★★ | 캐시 | 73~74 | 이점과 무효화/일관성 문제 |
| ★★★ | 마지막 강의 확인문제 | 76~79 | 공식 답과 변형 문제 |

## 2. 핵심 개념 완전 정리

### 2-1. ORM을 View에서 쓰는 이유

- views.py는 클라이언트 요청을 처리하는 함수(또는 클래스)를 정의한다.
- ORM API (Article.objects.all(), .get(), .create())로 SQL을 직접 쓰지 않고 모델 데이터를 다룬다.
- 처리 결과를 render(request, 'articles/detail.html', context)로 화면에 보내거나 redirect('articles:detail', pk)로 다른 URL에 재요청하게 한다.
- 기본 구조: URLconf에서 View를 연결하고 View는 Model(ORM)과 Template을 사용한다.

### 2-2. Read — 전체 조회 / 상세 조회

```
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
]

# articles/views.py
from django.shortcuts import render
from .models import Article

def index(request):
    articles = Article.objects.all()
    return render(request, 'articles/index.html', {'articles': articles})

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, 'articles/detail.html', {'article': article})

{# templates/articles/index.html #}
{% for article in articles %}
  <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
{% endfor %}
```

변형 주의: 강의는 .get(pk=pk)를 사용한다. 없는 PK면 Article.DoesNotExist 예외가 생길 수 있다. 실무에서 get_object_or_404(Article, pk=pk)를 사용하면 적절한 404 응답을 만들 수 있다. .get()이 자동으로 404를 반환한다는 설명은 틀림.

### 2-3. Create — new와 create의 역할

- new(request): 사용자 입력 폼이 있는 HTML을 render한다. DB 저장은 하지 않는다.
- create(request): 입력값을 읽고 DB에 새 레코드를 저장한다.
- 강의 초기 예제는 GET으로 입력값을 보내고, 이후 안전한 설계를 위해 POST 방식으로 수정한다.

```
# urls.py
path('new/', views.new, name='new'),
path('create/', views.create, name='create'),

# views.py
from django.shortcuts import render, redirect

def new(request):
    return render(request, 'articles/new.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    article = Article(title=title, content=content)
    article.save()
    return redirect('articles:detail', article.pk)
{# templates/articles/new.html #}
<form action="{% url 'articles:create' %}" method="POST">
  {% csrf_token %}
  <input type="text" name="title">
  <textarea name="content"></textarea>
  <input type="submit" value="작성">
</form>
```

암기: Article.objects.create(title=..., content=...)는 생성과 저장을 한 번에 수행한다. 반면 Article(...)만 하면 DB에는 아직 저장되지 않는다. article.save() 필수.

### 2-4. GET vs POST (p022~p030 / p069)

| 비교 | GET | POST |
| --- | --- | --- |
| 통상적인 용도 | 읽기/조회 | 생성·수정·삭제 등 상태 변경 |
| HTML 폼 데이터 | URL Query String (?title=...) | HTTP Request Body |
| Django에서 접근 | request.GET.get('title') | request.POST.get('title') |
| URL에 값이 드러나는가 | 쿼리스트링 값이 노출될 수 있음 | 폼 데이터가 URL 쿼리스트링으로 직접 표시되지 않음 |
| 새로고침/캐시 | 조회에 적합, 캐시 가능 | 중복 제출 위험, 일반적으로 변경 요청 |

주의 1: POST라고 해서 자동으로 암호화되는 건 아니다. HTTPS를 함께 사용해야 전송 중 노출을 막을 수 있다.

주의 2: GET/POST라는 HTTP 메서드만으로 DB 동작이 결정되는 것은 아니다. 서버의 View 구현이 실제 동작을 결정한다. 다만웹 설계 원칙상 GET이 상태를 바꾸지 않도록 작성해야 한다.

주의 3: HTTP POST로 DELETE 같은 메서드를 표현할 수도 있지만, 이 강의에서는 일반 HTML 폼에서 method="POST"로 삭제를 구현한다.

### 2-5. 403 Forbidden과 CSRF (p033~p044)

- HTTP 상태 코드: 서버가 요청 처리 결과를 숫자로 표현. 403은 요청을 이해했지만 접근/처리가 금지된 상태.
- CSRF(Cross-Site Request Forgery): 사용자의 인증된 상태 등을 악용하여 의도하지 않은 요청을 보내게 만드는 공격.
- Django는 CSRF 보호가 활성화된 상태에서 토큰이 필요한 POST 요청에 토큰이 없거나 유효하지 않으면 일반적으로 403 Forbidden 응답을 보낸다.
- Django 템플릿에서 같은 사이트의 POST 폼에는 {% csrf_token %}을 넣는다.
- csrf_token은 폼에 숨겨진 토큰 입력 필드 생성과 연결된다. 서버는 토큰을 검증한다.
- 오답 함정: CSRF 토큰은 POST 데이터를 암호화하는 기능이 아니다. CSRF 검증을 우회하기 위해 보호 기능을 무작정 끄는 것은 올바른 해결이 아니다.

### 2-6. redirect와 POST-Redirect-GET (p046~p054)

```
return render(request, 'articles/create.html')
# 현재 요청 처리 결과를 HTML로 응답한다. 주소 변경/재요청을 유도하지 않는다.

return redirect('articles:detail', article.pk)
# 대개 HTTP 302 응답과 Location 정보를 보내 클라이언트가 상세 URL로 GET 요청하게 한다.
```

POST → Redirect → GET 순서:

1. 브라우저가 /articles/create/에 POST로 폼 데이터를 제출한다.
2. View가 article.save()로 DB에 저장한다.
3. 서버가 redirect('articles:detail', article.pk)로 3xx 응답을 보낸다.
4. 브라우저가 /articles/새pk/에 GET 요청을 보낸다.
5. detail View가 새 글을 읽고 HTML을 반환한다.

왜 필요한가? POST 처리 결과 페이지에서 새로고침하면 동일 POST가 다시 전송될 수 있으므로 저장 이후 GET 페이지로 이동시켜중복 요청 위험을 줄이기 위해서다. 단, PRG만으로 네트워크 재시도 등을 포함한 모든 중복 저장을 완전히 방지하는 것은 아니다.

### 2-7. Delete (p055~p057)

```
# urls.py
path('<int:pk>/delete/', views.delete, name='delete'),

# views.py
from django.shortcuts import redirect

def delete(request, pk):
    if request.method == 'POST':
        article = Article.objects.get(pk=pk)
        article.delete()
    return redirect('articles:index')

<form action="{% url 'articles:delete' article.pk %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="DELETE">
</form>
```

시험 포인트: article.delete()는 해당 인스턴스 삭제. redirect('articles:index')는 삭제 직후 목록 조회를 유도한다. 강의의 초기 삭제 예제는 메서드 제한이 없지만, 올바른 확장 예제에서는 POST 여부를 검증한다. GET 요청으로 삭제가 일어나게 하면 안 된다.

### 2-8. Update — edit와 update의 역할 (p058~p066)

- edit(request, pk): 기존 데이터를 조회해서 값이 미리 채워진 폼을 보여준다.
- update(request, pk): 사용자가 보낸 새 값을 DB에 반영하고 상세 페이지로 이동한다.

```
# urls.py
path('<int:pk>/edit/', views.edit, name='edit'),
path('<int:pk>/update/', views.update, name='update'),

# views.py
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, 'articles/edit.html', {'article': article})

def update(request, pk):
    if request.method == 'POST':
        article = Article.objects.get(pk=pk)
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
        return redirect('articles:detail', article.pk)
    return redirect('articles:index')

<form action="{% url 'articles:update' article.pk %}" method="POST">
  {% csrf_token %}
  <input name="title" value="{{ article.title }}">
  <textarea name="content">{{ article.content }}</textarea>
  <button type="submit">수정</button>
</form>
```

함정: input의 초기값은 value="{{ article.title }}"처럼, textarea는 시작 태그와 종료 태그 사이에 {{ article.content }}를 넣는다. textarea value="..."는 기존 내용을 표시하는 올바른 방식이 아니다.

### 2-9. 캐시(Cache), HTTP 상태 코드 (p068~p074)

- 캐시: 자주 쓰는 데이터를 일시적으로 저장해 서버 부하/DB 조회량 감소, 응답 속도 향상에 도움.
- 단점: 데이터가 바뀌면 캐시 무효화·갱신·일관성 관리가 필요.
- HTTP 상태 코드: 2xx 성공 / 3xx 리다이렉션 / 4xx 클라이언트 측 오류 / 5xx 서버 오류.
- 403 Forbidden: 서버가 요청을 이해했으나 허용하지 않음(예: CSRF 검증 실패).
- 404 Not Found: 요청한 리소스를 찾지 못함. 단, .get()의 DoesNotExist는 자동으로 404가 아니고, 404를 응답하도록 처리해야 한다.

## 3. 1~4단원과 연결 (서술형 대비)

1단원 MTV의 View가 요청을 받고 → 2단원에서 정리한 URL 변수 &lt;int:pk&gt;와 Template 문법을 활용하고 → 3단원 Model이 정의한 테이블에 → 4단원 QuerySet API로 CRUD를 수행한다. 5단원에서는 폼 제출과 HTTP 메서드, CSRF, redirect가 결합되어실제 게시판이 된다.

### 파일별 역할 한 줄 답안

- models.py: DB 테이블과 필드 구조를 Python 클래스로 정의.
- urls.py: HTTP URL 경로와 View 연결, URL 이름 관리.
- views.py: HTTP 요청 처리와 ORM 동작, 응답 생성.
- templates/articles/*.html: 데이터 표시, 폼 입력, URL 생성(DTL).

## 4. 강의 원본 확인문제 12개 — 공식 정답 및 핵심 해설 (p076~p079)

강의 확인문제의 핵심 질문을 간추려 정리. 공식 정답의 선택지는 p079와 대조했다.

| 번호 | 원본 질문 핵심 | 공식 정답 | 왜 맞는가 |
| --- | --- | --- | --- |
| 1 | GET 방식의 장점 | c | GET 응답은 캐시 활용 가능 |
| 2 | POST의 대표적 사용 사례 | b | 새 게시글 생성 |
| 3 | 403 Forbidden 의미 | c | 권한/접근 문제로 거절됨 |
| 4 | Django CSRF 토큰의 주요 목적 | b | 사이트 간 요청 위조 방지 |
| 5 | redirect() 실행 시 브라우저 동작 | b | 다른 URL로 재요청 유도 |
| 6 | Article.objects.create() | b | 객체 생성과 DB 저장을 함께 수행 |
| 7 | URL에서 데이터가 보일 수 있는 메서드 | a | GET 쿼리 문자열 |
| 8 | 캐시 활용 시 고려할 점이 아닌 것 | c | 자동 무결성 보장은 캐시의 성질이 아님 |

| 번호 | 원본 질문 핵심 | 공식 정답 | 왜 맞는가 |
| --- | --- | --- | --- |
| 9 | &lt;int:pk&gt;의 기능 | b | URL 경로의 정수 부분을 View 인자로 전달 |
| 10 | 모든 Article을 QuerySet으로 얻는 메서드 | c | Article.objects.all() |
| 11 | 404 Not Found의 의미 | c | 요청 리소스를 찾을 수 없음 |
| 12 | objects.get()에 대한 옳은 설명 | b | 단일 객체, 일치 항목 0개면 DoesNotExist |

## 5. 추가 예상 객관식 15문제 (강의 기반 변형)

각 문제는 정답 1개. 먼저 풀고 아래 해설을 확인할 것.

Q1. 상세 조회 View가 def detail(request, pk)일 때 URL 패턴으로 알맞은 것은? A. path('detail/', views.detail) B. path('&lt;int:pk&gt;/', views.detail, name='detail') C. path('&lt;str:request&gt;/', views.detail) D. path('pk/', views.detail)

Q2. Article.objects.get(pk=10)에서 10번 게시글이 없을 경우 기본적으로 발생하는 것은? A. 빈 QuerySet B. None C. Article.DoesNotExist D. 무조건 HTTP 404

Q3. 새 글 입력 화면만 보여주는 View의 이름으로 강의에서 사용한 것은? A. new B. create C. update D. delete

Q4. &lt;form method="POST"&gt;의 입력값을 받는 코드로 맞는 것은? A. request.GET.get('title') B. request.POST.get('title') C. request.URL['title'] D. request.HTML.title

Q5. POST 폼에 CSRF 토큰이 누락되면, 보호 설정이 활성화된 Django에서 일반적으로 볼 수 있는 상태 코드는? A. 200 B. 301 C. 403 D. 500

Q6. return redirect('articles:detail', article.pk)의 가장 정확한 설명은? A. Template을 바로 렌더링 B. 브라우저의 새 URL 요청을 유도 C. Model 삭제 D. DB 마이그레이션 실행

Q7. 다음 중 DB 저장을 실제로 완료하는 코드는? article = Article(title='A', content='B') A. article.title B. render(request, 'x.html') C. article.save() D. Article.objects.all()

Q8. 게시글 수정 페이지에서 현재 제목을 input에 채우는 방식으로 적절한 것은? A. &lt;input value="{{ article.title }}"&gt; B. &lt;input content="{{ article.title }}"&gt; C. &lt;input&gt;{{ article.title }}&lt;/input&gt; D. &lt;input value="{% article.title %}"&gt;

Q9. textarea의 기존 본문 표시 방식으로 적절한 것은? A. &lt;textarea value="{{ article.content }}"&gt;&lt;/textarea&gt; B. &lt;textarea&gt;{{ article.content }}&lt;/textarea&gt; C. &lt;textarea src="{{ article.content }}"&gt;&lt;/textarea&gt; D. &lt;textarea&gt;{% article.content %}&lt;/textarea&gt;

Q10. 게시글 삭제를 수행할 때 가장 안전한 HTML 폼 설계는? A. &lt;a href="/delete/1/"&gt; B. GET 폼으로 삭제 C. POST 폼과 CSRF 토큰 D. CSS 버튼만 사용

Q11. POST-Redirect-GET 패턴의 주된 이점은? A. DB 테이블 자동 생성 B. POST 재제출 위험 완화 C. CSRF 검사 완전 제거 D. 모든 서버 오류 제거

Q12. POST 요청 데이터에 관한 옳은 설명은? A. 무조건 암호화됨 B. HTTP Body를 사용할 수 있음 C. URL에 항상 노출 D. 항상캐시됨

Q13. 같은 URL 경로로 GET과 POST 요청이 들어왔을 때 올바른 것은? A. HTTP 메서드와 관계없이 응답이 항상 같음 B. URL 패턴은 반드시 달라야 함 C. View가 request.method에 따라 분기 가능 D. POST는 Django에서 금지됨

Q14. Article.objects.get(pk=1) 객체의 title을 변경했지만 save()를 생략한 경우? A. 일반적으로 DB 변경 반영 안 됨 B. 항상 DB에 자동 반영 C. 게시글 삭제 D. 새 테이블 생성

Q15. 캐시의 단점으로 가장 적절한 것은? A. 응답 시간을 무조건 늦춤 B. 정보를 저장하지 못함 C. 원본 변경 후 오래된 데이터가 남을 수 있음 D. 반드시 트랜잭션 삭제

### 객관식 정답 및 해설

1. B — 동적 정수 경로 pk를 View 인자로 전달.
2. C — .get()은 DoesNotExist; 404를 직접 처리하려면 별도 코드.
3. A — new는 화면, create는 DB 저장.
4. B — POST 폼은 request.POST 접근.
5. C — 일반적으로 CSRF 실패 시 403.
6. B — redirect는 새 요청을 유도.
7. C — Article(...) 구성만으로는 저장되지 않음.
8. A — input은 value 속성.
9. B — textarea는 태그 내부에 값.
10. C — DB 변경은 POST + CSRF 보호.
11. B — POST 이후 GET 페이지로 이동.
12. B — POST 데이터는 HTTP Body에 담길 수 있음. HTTPS와 별개.
13. C — 같은 URL이라도 메서드에 따른 View 분기 가능.
14. A — ORM 객체 변경 후 save() 필요.
15. C — 캐시 무효화와 최신성 문제가 중요.

## 6. 추가 주관식 10문제

1. HTTP 403 상태코드의 이름을 영문으로 쓰시오.
2. Cross-Site Request Forgery의 약어를 쓰시오.
3. Django 템플릿에서 POST 폼에 삽입하는 보안 태그를 쓰시오.
4. request.____.get('title'): POST 폼의 title 수신 시 빈칸은?
5. Article.objects.____(pk=pk): 단일 객체 조회 메서드는?
6. 모델 인스턴스의 변경값을 DB에 저장하는 메서드는?
7. DB 저장 후 URL 이름 articles:detail로 이동시키는 Django shortcut 함수는?
8. 사용자가 입력한 내용을 저장하지 않고 입력 화면을 보여주는 View 이름은? (강의 예제)
9. URL 패턴 path('&lt;int:pk&gt;/', views.detail)에서 pk는 어떤 자료형으로 전달되는가?
10. POST 요청 후 다른 URL로 GET 요청을 유도하는 패턴의 약어는?

정답: 1. Forbidden / 2. CSRF / 3. {% csrf_token %} / 4. POST / 5. get / 6. save() / 7. redirect() / 8. new / 9. 정수(int) / 10. PRG(Post/Redirect/Get).

## 7. 추가 서술형 5문제 — 만점용 모범답안과 채점 키워드

### S1. new와 create를 분리하는 이유와 각 View 역할을 설명하시오.

모범답안: new View는 GET 요청을 처리해 사용자가 제목·내용을 입력할 HTML 폼을 렌더링한다. create View는 POST 요청에서 request.POST로 입력값을 읽어 모델 객체를 생성하고 save() 또는 objects.create()로 DB에 저장한다. 생성이 끝나면 상세 페이지등으로 redirect()한다. 따라서 화면 제공과 데이터 변경의 책임을 구분할 수 있다.

채점 키워드: new=폼 렌더링, create=POST 수신, DB 저장, redirect.

### S2. GET과 POST의 용도와 데이터 전달 방식, Django 코드 차이를 비교하시오.

모범답안: GET은 리소스 조회에 쓰이고 HTML 폼의 입력값이 보통 URL 쿼리스트링에 들어간다. Django에서는 request.GET으로읽는다. POST는 주로 리소스 생성·수정·삭제처럼 서버 상태 변경이 필요한 요청에 쓰며 폼 데이터가 요청 Body에 담긴다. Django에서는 request.POST로 읽는다. POST가 암호화를 보장하는 것은 아니므로 HTTPS 사용이 필요하다.

채점 키워드: 조회/변경, Query String/Body, request.GET/POST, HTTPS와 구분.

### S3. CSRF 공격 및 Django의 방어 방식과 403 오류가 발생하는 이유를 설명하시오.

모범답안: CSRF는 공격자가 사용자의 인증된 브라우저 상태를 악용하여 사용자가 의도하지 않은 요청을 보내도록 만드는 공격이다. Django는 보호가 필요한 요청에 대해 CSRF 토큰을 검증하며, 템플릿의 POST 폼에는 {% csrf_token %}을 넣어 토큰을 전송한다. 토큰이 누락되거나 유효하지 않으면 일반적으로 403 Forbidden으로 요청이 거절될 수 있다.

채점 키워드: 사이트 간 요청 위조, 사용자 의도와 무관, 토큰 검증, 403.

### S4. 게시글 생성 후 render 대신 redirect를 사용하는 이유와 HTTP 요청 흐름을 설명하시오.

모범답안: 사용자가 POST로 게시글을 생성하면 서버는 DB에 저장한 후 3xx 리다이렉션 응답을 보낸다. 브라우저는 상세 URL로새로운 GET 요청을 보내고 상세 View가 그 데이터를 조회하여 페이지를 렌더링한다. 이 PRG 패턴은 사용자가 결과 화면을 새로고침하면서 같은 POST를 다시 제출하는 위험을 줄이고, 결과 페이지의 URL을 명확하게 만든다.

채점 키워드: POST → 3xx → GET, 브라우저 재요청, 중복 제출 감소.

### S5. 게시글 수정 처리에서 edit와 update의 차이, 기존 값 표기 및 저장 과정을 설명하시오.

모범답안: edit는 pk로 기존 글을 ORM 조회하고 해당 데이터를 템플릿에 전달하여 제목을 &lt;input value="{{ article.title }}"&gt; 에, 내용을 &lt;textarea&gt;{{ article.content }}&lt;/textarea&gt;에 채워 사용자에게 보여준다. update는 POST 입력값을 읽고 Article.objects.get(pk=pk)로 조회한 객체의 속성을 수정해 save()로 반영한 뒤 상세 페이지로 리다이렉트한다.

채점 키워드: edit/조회·기존값, input value, textarea 본문, update/POST, save(), redirect.

## 8. 코드 추론 고난도 퀴즈 8개

C1. article = Article(title='X'); print(article.pk) (아직 저장하지 않고 PK 직접 할당하지 않음) → 일반적으로? 정답: None. DB에 저장되지 않았기 때문.

C2. Article.objects.create(title='A', content='B') 다음 save()가 반드시 필요한가? 정답: 아니오. 생성·저장 동시 처리.

C3. &lt;form method="POST"&gt; 내부에 {% csrf_token %}이 없으면? 정답: 일반적으로 CSRF 보호 활성 상태에서 403. 예외적 설정은별개.

C4. &lt;textarea value="{{ article.content }}"&gt;&lt;/textarea&gt;에서 기존 내용이 나타나는가? 정답: 아니다. 시작·종료 태그 사이 텍스트로 넣어야 함.

C5. def detail(request, pk) / path('&lt;int:pk&gt;/', views.detail) / 요청 /articles/abc/ →? 정답: 정수 변환이 불가능해 패턴 매칭 실패(다른 패턴 없으면 404).

C6. 저장 후 return render(request, 'articles/create.html')로 끝내고 화면을 새로고침하면? 정답: POST 재전송 가능성이 있음. redirect 유도 권장.

C7. article.title='바뀐 글'; return redirect('articles:index') → DB 제목? 정답: 일반적으로 바뀌지 않음. save()가 빠짐.

C8. Article.objects.get(pk=9999)에서 결과가 없으면? 정답: Article.DoesNotExist 예외. 직접 404 처리 코드를 추가해야 함.

## 9. 반드시 피할 오답 12개

1. ❌ new가 DB에 저장한다 → ✅ create가 저장.
2. ❌ edit가 수정 저장한다 → ✅ update가 저장.
3. ❌ POST는 무조건 암호화된 데이터 → ✅ HTTPS가 필요.
4. ❌ POST 폼에서 request.GET → ✅ request.POST.
5. ❌ CSRF 토큰은 비밀번호 암호화 → ✅ 요청 위조 방지 검증.
6. ❌ 403=페이지 없음 → ✅ 403 거부, 404 리소스 없음.
7. ❌ render는 새로운 URL로 GET 요청 유도 → ✅ redirect.
8. ❌ redirect가 DB 저장 → ✅ View가 저장 후 redirect.
9. ❌ .get()은 빈 QuerySet을 준다 → ✅ 없으면 DoesNotExist.
10. ❌ Article(...)만으로 DB에 저장 → ✅ save() 필요.
11. ❌ textarea에 value 속성으로 내용 표시 → ✅ 태그 사이 내용.
12. ❌ 캐시가 최신 데이터 유지 자동 보장 → ✅ 무효화/일관성 관리 필요.

## 10. 15분 벼락치기 플랜

- 0~3분: URL → View → ORM → 응답 흐름을 빈 종이에 적기.
- 3~6분: new/create, edit/update, delete 세 과정과 각 요청 메서드 구분.
- 6~9분: GET/POST, CSRF/403, render/redirect, 403/404 비교 암기.
- 9~12분: 강의 원본 12문제 풀고 공식 답 확인.
- 12~15분: 서술형 S2·S3·S4를 3~4문장으로 소리 내어 말하기.

### 30초 암기 카드

detail: get(pk) | new: render 폼 | create: POST → save → redirect | edit: 기존값 채운 폼 | update: POST → 변경 → save → redirect | delete: POST → delete → redirect | GET: 조회·URL 쿼리 | POST: 변경·Body·CSRF | 403: 거부 | 404: 없음 | 3xx: 이동 | Cache: 속도↑, 무효화 필요

### 범위 구분

강의 예제의 핵심 흐름을 유지하되, 응용·함정 문제에서는 실전 웹 개발에 맞게 POST 메서드 검증, .get()과 404의 차이, HTTPS의 필요성 같은 보충 사항을 별도로 설명했다. 시험에서는 강의 원문의 표현을 우선 확인하되 이 보충사항으로 지나친 일반화를 피하자.
