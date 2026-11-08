# Django 05 — ORM with View

> 📎 확인문제·예상문제·암기카드: [`시험대비/05_orm_with_view_시험대비.md`](시험대비/05_orm_with_view_시험대비.md)

*(4단원 QuerySet API를 실제 웹 기능으로 연결해 게시판 CRUD를 완성한다. 그 과정에서 GET/POST, HTTP 상태 코드, CSRF, redirect가 왜 필요한지 하나씩 등장한다. 6단원 Form은 여기서 손으로 짠 입력·저장 코드를 개선하는 내용.)*

## 오늘의 목차

1. Read (단일 게시글 조회)
2. Create
3. HTTP request methods (GET vs POST)
4. HTTP response status code
5. CSRF
6. Redirect
7. Delete
8. Update
9. 정리 — CRUD URL 한눈에 보기

```text
브라우저 요청 → urls.py 경로 매칭 → views.py 함수 실행 → ORM(Model.objects...) → DB 조회/변경
           → render() 또는 redirect() 응답 → 브라우저
```

---

## 1. Read

### 2가지 Read

1. 전체 게시글 조회 (4단원)
2. **단일 게시글 조회**

### 단일 게시글 조회

```python
# articles/urls.py
urlpatterns = [
    ...
    path('<int:pk>/', views.detail, name='detail'),
]
```

```python
# articles/views.py
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)
```

- `get(pk=pk)`: 왼쪽 `pk`는 **필드 이름**, 오른쪽 `pk`는 URL에서 넘어온 **변수**

```html
<!-- templates/articles/detail.html -->
<h2>DETAIL</h2>
<h3>{{ article.pk }} 번째 글</h3>
<hr>
<p>제목: {{ article.title }}</p>
<p>내용: {{ article.content }}</p>
<p>작성일: {{ article.created_at }}</p>
<p>수정일: {{ article.updated_at }}</p>
<hr>
<a href="{% url 'articles:index' %}">[back]</a>
```

### 단일 게시글 이동 링크 (index.html)

```html
{% for article in articles %}
  <div>
    <p>글 번호: {{ article.pk }}</p>
    <p>
      글 제목: <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
    </p>
    <p>글 내용: {{ article.content }}</p>
  </div>
  <hr>
{% endfor %}
```

> 📌 없는 pk로 요청하면 `get()`이 `DoesNotExist` 예외를 던진다 → 자동으로 404가 되는 게 아니라 **서버 에러(500)**. 실무에서는 `get_object_or_404(Article, pk=pk)`로 404 응답을 돌려준다 (심화).

---

## 2. Create

- Create 로직에는 **두 개의 view 함수** 필요

| view 함수 | 역할 |
|---|---|
| `new` | 사용자 입력 데이터를 받을 **페이지를 렌더링** (DB 저장 X) |
| `create` | 사용자가 입력한 요청 데이터를 받아 **DB에 저장** |

### new: 페이지 렌더링

```python
# articles/urls.py
path('new/', views.new, name='new'),

# articles/views.py
def new(request):
    return render(request, 'articles/new.html')
```

```html
<!-- templates/articles/new.html -->
<h1>NEW</h1>
<form action="#" method="GET">
  <div>
    <label for="title">Title: </label>
    <input type="text" name="title" id="title">
  </div>
  <div>
    <label for="content">Content: </label>
    <textarea name="content" id="content"></textarea>
  </div>
  <input type="submit">
</form>
<hr>
<a href="{% url 'articles:index' %}">[back]</a>
```

- index 페이지에 new로 이동하는 링크 추가

```html
<h1>Articles</h1>
<a href="{% url 'articles:new' %}">NEW</a>
<hr>
```

### create: 데이터 저장

```python
# articles/urls.py
path('create/', views.create, name='create'),
```

```python
# articles/views.py
def create(request):
    title = request.GET.get('title')
    content = request.GET.get('content')

    # 1. 인스턴스 생성 후 속성 할당 및 저장
    # article = Article()
    # article.title = title
    # article.content = content
    # article.save()

    # 2. 인스턴스 생성 시 속성 할당 후 저장
    article = Article(title=title, content=content)
    article.save()

    # 3. create() 메서드를 통한 인스턴스 생성 및 즉시 저장
    # Article.objects.create(title=title, content=content)

    return render(request, 'articles/create.html')
```

```html
<!-- templates/articles/create.html -->
<h1>게시글이 작성 되었습니다.</h1>
```

- new.html의 form action 수정: `<form action="{% url 'articles:create' %}" method="GET">`
- 결과 URL: `/articles/create/?title=제목&content=내용` → GET이라 **데이터가 URL에 노출**됨 → 다음 장에서 POST로 바꾼다

---

## 3. HTTP request methods

### HTTP

- 네트워크 상에서 **데이터(리소스)를 주고받기 위한 약속**

### HTTP request methods

- 데이터에 대해 **수행을 원하는 작업(행동)을** 나타내는 것
- 서버에게 원하는 작업의 종류를 알려주는 역할

### GET vs POST

| 구분 | GET | POST |
|---|---|---|
| 의미 | 서버로부터 데이터를 요청하고 받아오는 데(**조회**) 사용 | 서버에 데이터를 제출해 리소스를 **변경(생성, 수정, 삭제)하는** 데 사용 |
| 사용 예 | 검색 쿼리 전송, 웹 페이지 요청, API 데이터 조회 | 로그인 정보 제출, 파일 업로드, 새 게시글 작성, API 데이터 변경 |
| 데이터 전송 | URL의 **쿼리 문자열(Query String)** | **HTTP Body** |
| Django에서 꺼내기 | `request.GET.get('title')` | `request.POST.get('title')` |
| 데이터 크기 제한 | 브라우저가 허용하는 URL 최대 길이 → 대량 데이터 부적합 | HTTP 규격상 제한 없음 (서버 설정에 따라 제한) |
| 브라우저 히스토리 | 요청 URL이 **남음** | **남지 않음** |
| 캐싱 | **가능** (같은 URL 재요청 시 저장된 결과 사용 → 로딩 시간 단축) | 기본적으로 **불가** (서버 상태를 변경하는 작업이기 때문) |

- **캐싱**: 자주 사용하는 데이터나 결과를 임시로 저장해두고 재활용해 처리 속도를 높이는 기술
  - 장점: 서버 부하·DB 조회 감소, 응답 속도 향상
  - 단점: 원본 데이터가 바뀌면 캐시를 갱신·무효화해야 함 (일관성 관리 필요)
- 정리: **GET은 데이터 조회**, **POST는 데이터 생성이나 수정**에 주로 사용
- HTML form은 **GET과 POST만 지원** → 지금은 생성·수정·삭제 모두 POST로 처리 (PUT, DELETE는 REST API 시간에 학습)

> ⚠️ POST라고 데이터가 **암호화되는 건 아니다**. 주소창에 안 보일 뿐, 전송 중 보호는 HTTPS가 담당한다.

### POST method로 변경

- new.html의 form 요청은 새로운 데이터를 생성하는 요청 → POST가 적절

```html
<!-- templates/articles/new.html -->
<form action="{% url 'articles:create' %}" method="POST">
```

```python
# articles/views.py
def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    ...
```

- 변경 후 게시글 작성 시 **403 Forbidden** 응답 발생 → 왜?

---

## 4. HTTP response status code

- 서버가 클라이언트의 요청에 대한 **처리 결과를 나타내는 3자리 숫자**
- 클라이언트는 이 코드로 요청이 성공했는지, 실패했는지, 추가 조치가 필요한지 즉시 파악 → 브라우저는 적절한 메시지를 표시하고, 개발자는 문제 해결 단서를 얻음

| 범위 | 의미 | 강의에 나온 예 |
|---|---|---|
| 2xx | 성공 | 200 OK |
| 3xx | 리다이렉션 | 302 Found (redirect) |
| 4xx | 클라이언트 측 오류 | 403 Forbidden, 404 Not Found |
| 5xx | 서버 측 오류 | 500 Internal Server Error |

### 403 Forbidden

- 서버에 요청이 전달되었지만, **권한 때문에 거절**되었다는 의미
- 거절 이유: **CSRF token 누락** (`CSRF verification failed`, `CSRF cookie not set.`)

> 📌 403(서버가 이해했지만 거부) ≠ 404(요청한 리소스를 찾지 못함).

---

## 5. CSRF

### CSRF (Cross-Site-Request-Forgery, 사이트 간 요청 위조)

- 사용자가 **자신의 의지와 무관하게** 공격자가 의도한 행동(글쓰기, 정보 수정, 송금 등)을 특정 웹사이트에 요청하게 만드는 해킹 방식

### 위조된 인감도장 비유

1. **로그인**: 은행에 로그인하면 은행이 세션 쿠키(인감도장)를 브라우저에 발급
2. **악성 링크**: 해커가 "무료 경품 이벤트!" 같은 미끼 링크 전송 (실제 내용은 "100만원 송금" 위임장)
3. **요청 전송**: 링크를 클릭하면 브라우저가 은행에 위조된 요청을 보내면서 세션 쿠키를 **자동으로 첨부**
4. **공격 성공**: 은행은 정상 인감도장이 찍혀 있으니 진짜 요청이라 믿고 송금 실행

### CSRF 방어

- Django는 **CSRF 토큰**이라는 안전장치 사용
- 중요한 요청에 "Django가 직접 내려준 페이지에서 보낸 요청이 맞다"는 **비밀 값(토큰)을** 함께 보내도록 해 위조된 요청을 막음

### CSRF Token 적용

- DTL의 **`csrf_token` 태그**로 사용자에게 토큰 값 부여 → 요청 시 토큰도 함께 서버로 전송

```html
<!-- templates/articles/new.html -->
<form action="{% url 'articles:create' %}" method="POST">
  {% csrf_token %}
  ...
</form>
```

- 렌더링 결과: `<input type="hidden" name="csrfmiddlewaretoken" value="...">`
- 요청 형태 변화: 요청 데이터 → 게시글 작성 ⇒ **요청 데이터 + CSRF 토큰** → 게시글 작성

### 토큰을 함께 보내야 하는 이유

- DB에 영향을 주는 요청에 대해 "**Django가 직접 제공한 페이지에서 데이터를 작성하고 있는 것인지**" 확인하는 수단이 필요
- 겉모습이 똑같은 위조 사이트나 비정상 요청에 대한 방어 수단

### 왜 POST일 때만 토큰을 확인할까?

- POST는 리소스의 **변경(생성, 수정, 삭제)을** 요청하는 의미와 기술적 특성을 지님
- DB를 조작하는 요청은 "우리 사이트에서 보낸 요청인지" 확인 필요 → 토큰으로 **요청의 출처를 확인**
- GET은 원래 서버 데이터를 바꾸지 않는 요청으로 약속되어 있어 보호 대상이 아님
- ⚠️ **GET으로 데이터를 바꾸도록 만들면 CSRF 보호를 받을 수 없음**

> ⚠️ CSRF 토큰은 데이터를 **암호화하는 기능이 아니다** (출처 확인용). 403이 난다고 CSRF 보호를 꺼버리는 건 올바른 해결이 아님.

### 게시글 작성 결과

- URL에 Query String이 더 이상 표시되지 않음
- 개발자 도구 Network > Payload에서 Form Data(`csrfmiddlewaretoken`, `title`, `content`) 전송 확인

---

## 6. Redirect

### 문제 상황

- 게시글 작성(POST) 후 "게시글이 작성되었습니다" 페이지를 **직접 반환** → POST 요청에 대한 적절한 응답이 아님
- HTTP 표준 관점: POST는 동일 요청이 반복되면 안 됨. 완료 페이지에서 **새로고침하면 중복 게시물 작성** 위험
- 사용자 경험(UX) 관점: 직관적이지 않고, 브라우저 기록·상태 관리에 혼란

### 해결

- 서버는 데이터 저장 후 페이지를 응답하는 것이 아니라 **사용자를 적절한 기존 페이지로 보내야 함**
- 실제로는 서버가 직접 보내는 것이 아니라, **클라이언트가 GET 요청을 한 번 더 보내도록 응답**하는 것

### redirect()

- 클라이언트가 **인자에 작성된 주소로 다시 요청을 보내도록** 하는 함수

```python
# articles/views.py
from django.shortcuts import render, redirect

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    article = Article(title=title, content=content)
    article.save()
    return redirect('articles:detail', article.pk)
```

| 응답 | 하는 일 |
|---|---|
| `render(...)` | 지금 요청에 대한 결과를 **HTML로 바로** 응답. 주소 변경·재요청 유도 없음 |
| `redirect(...)` | **302** 응답 + 이동할 주소(Location)를 보내 클라이언트가 그 주소로 **GET 재요청**하게 함 |

### 동작 원리 (POST → Redirect → GET, PRG 패턴)

1. [POST] 게시글 작성 요청 (+입력 데이터)
2. create view 함수 호출
3. redirect 응답 (detail 주소로 요청을 보내라)
4. [GET] detail 페이지 요청
5. detail view 함수 호출
6. detail 페이지 응답

- 사용자는 작성 후 detail 페이지로 이동한 것처럼 느낌
- 개발자 도구 Network에서 `create/`(**302**) → `8/`(200) 순서로 요청 확인
- 이제 detail 페이지에서 새로고침해도 GET만 다시 보내질 뿐 → 중복 작성 위험 감소

---

## 7. Delete

```python
# articles/urls.py
path('<int:pk>/delete/', views.delete, name='delete'),
```

```python
# articles/views.py
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')
```

```html
<!-- articles/detail.html -->
<form action="{% url 'articles:delete' article.pk %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="DELETE">
</form>
<a href="{% url 'articles:index' %}">[back]</a>
```

- 삭제는 DB를 바꾸는 요청 → `<a>` 링크(GET)가 아니라 **POST form**으로

> ⚠️ 현재 코드는 주소창에 `/articles/1/delete/`를 직접 입력(GET)해도 삭제된다. 6단원 "HTTP 요청 다루기"에서 `request.method`로 POST일 때만 삭제하도록 고친다.
>
> ```python
> def delete(request, pk):
>     if request.method == 'POST':
>         article = Article.objects.get(pk=pk)
>         article.delete()
>     return redirect('articles:index')
> ```

---

## 8. Update

- Update 로직에도 **두 개의 view 함수** 필요

| view 함수 | 역할 |
|---|---|
| `edit` | 사용자 입력 데이터를 받을 **페이지를 렌더링** (기존 값이 채워진 폼) |
| `update` | 사용자가 입력한 요청 데이터를 받아 **DB에 저장** |

### edit: 페이지 렌더링

```python
# articles/urls.py
path('<int:pk>/edit/', views.edit, name='edit'),
```

```python
# articles/views.py
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/edit.html', context)
```

- 수정 시 **이전 데이터가 출력**되도록 작성
  - `input`: 한 줄 텍스트, **value 속성**으로 기존 데이터 입력
  - `textarea`: 여러 줄 텍스트, **value 속성이 없고** 태그 여닫는 사이에 값을 넣음
- detail.html에 edit 페이지로 이동하는 링크 추가

```html
<a href="{% url 'articles:edit' article.pk %}">EDIT</a><br>
```

### update: 데이터 저장

```python
# articles/urls.py
path('<int:pk>/update/', views.update, name='update'),
```

```python
# articles/views.py
def update(request, pk):
    article = Article.objects.get(pk=pk)
    article.title = request.POST.get('title')
    article.content = request.POST.get('content')
    article.save()
    return redirect('articles:detail', article.pk)
```

```html
<!-- articles/edit.html -->
<h1>EDIT</h1>
<form action="{% url 'articles:update' article.pk %}" method="POST">
  {% csrf_token %}
  <div>
    <label for="title">Title: </label>
    <input type="text" name="title" id="title" value="{{ article.title }}">
  </div>
  <div>
    <label for="content">Content: </label>
    <textarea name="content" id="content">{{ article.content }}</textarea>
  </div>
  <input type="submit">
</form>
<hr>
<a href="{% url 'articles:index' %}">[back]</a>
```

> ⚠️ `<textarea value="{{ article.content }}">`로 쓰면 기존 내용이 **안 나온다**. textarea는 시작·종료 태그 **사이**에 값을 넣는다.
>
> ⚠️ update에서 값을 대입만 하고 `save()`를 빼먹으면 DB는 그대로다.

---

## 9. 정리 — CRUD URL 한눈에 보기

| 기능 | URL | view | 메서드 | 응답 |
|---|---|---|---|---|
| 전체 조회 | `''` | index | GET | render |
| 상세 조회 | `<int:pk>/` | detail | GET | render |
| 작성 페이지 | `new/` | new | GET | render |
| 작성 처리 | `create/` | create | POST | redirect → detail |
| 삭제 | `<int:pk>/delete/` | delete | POST | redirect → index |
| 수정 페이지 | `<int:pk>/edit/` | edit | GET | render |
| 수정 처리 | `<int:pk>/update/` | update | POST | redirect → detail |

> 💡 규칙: **보여주기(GET)는 render, 바꾸기(POST)는 redirect.** 6단원에서는 new+create, edit+update를 각각 하나의 view로 합친다.
