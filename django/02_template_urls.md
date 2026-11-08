# Django 02 — Template & URLs

> 📎 확인문제·예상문제·암기카드: [`시험대비/02_template_urls_시험대비.md`](시험대비/02_template_urls_시험대비.md)

*(1차시의 MTV·render()에 이어, Template에 데이터를 넣는 방법(DTL·상속)과 요청을 View로 보내는 URL 설계(변수 라우팅·include·이름·네임스페이스)를 다룬다.)*

## 오늘의 목차

1. Django Template System
2. DTL 문법 4종
3. 템플릿 상속
4. 요청과 응답 — HTML form
5. Django URLs
6. Variable Routing
7. App URL 정의 (include)
8. URL 이름 지정 (Naming URL patterns)
9. URL 이름 공간 (app_name)
10. 추가 템플릿 경로와 주의사항

---

## 1. Django Template System

### 정의와 역할

- 데이터 **표현을 제어**하면서, **표현과 관련된 부분**을 담당
- HTML 콘텐츠를 변수 값에 따라 바꾸고 싶을 때 사용
- 주요 목적: **HTML과 Python 코드를 분리**해 작성하기 위함 (확인 문제 1번)

### DTL (Django Template Language)

- Template에서 조건, 반복, 변수 등의 프로그래밍적 기능을 제공하는 시스템

### context 전달 흐름

```python
# views.py
def index(request):
    context = {
        'name': 'Jane',
    }
    return render(request, 'articles/index.html', context)
```

```html
<!-- index.html -->
<h1>Hello, {{ name }}</h1>
```

- context 딕셔너리의 **key**가 템플릿에서 **변수명**이 됨

최종적으로 브라우저가 받는 HTML:

```html
<body>
  <a href="/articles/">index</a>
  <a href="/articles/dinner/">dinner</a>
  <h1>Hello, Jane</h1>
</body>
```

> 💡 브라우저는 `{{ name }}` 같은 DTL 문법을 전혀 보지 못한다. 서버(Django)가 렌더링을 끝낸 **완성된 HTML**만 받는다.

---

## 2. DTL 문법 4종

| 구분 | 기본형 | 목적 | 예 |
|---|---|---|---|
| **Variable** | `{{ variable }}` | 값 출력 | `{{ user.name }}` |
| **Filter** | `{{ variable\|filter }}` | 출력값 변형 | `{{ name\|upper }}`, `{{ 1\|add:2 }}` → 3 |
| **Tag** | `{% tag %}` | 조건·반복 등 로직, 구조 | `{% for n in nums %}...{% endfor %}` |
| **Comment** | `{# 주석 #}` | 한 줄 주석 | 여러 줄은 `{% comment %} ... {% endcomment %}` |

### Variable

- render()의 세 번째 인자로 넘긴 context의 key 이름으로 접근
- 자료구조의 **인덱스·속성·딕셔너리 키는 점(`.`)으로 접근** — `{{ numbers.0 }}`, `{{ article.title }}`
- `{{ name }}`은 변수 *정의*가 아니라 값 *출력* 표현식

### Filter

- 변수를 `|`로 연결해 표시 형태를 바꿈. 인자는 `:`로 지정 (`{{ value|truncatewords:10 }}`)
- 자주 쓰는 필터: `upper`, `lower`, `length`, `default`, `truncatewords` 등

### Tag

```html
{% if login %}
  <h1>Welcome!</h1>
{% else %}
  <h1>Please, login.</h1>
{% endif %}

<ul>
  {% for item in nums %}
    <li>{{ item }}</li>
  {% endfor %}
</ul>
```

- 일부 태그(`if`, `for`, `block`, `comment` 등)는 **시작 태그와 종료 태그**가 필요

> ⚠️ DTL은 Python 전체 문법을 템플릿으로 옮기기 위한 언어가 **아니다**. 복잡한 계산·비즈니스 로직은 **View에서 먼저 처리**하고, 템플릿은 결과를 출력만 한다.

---

## 3. 템플릿 상속

### 필요한 이유

- 여러 템플릿에 공통 요소(ex. Bootstrap, navbar)가 반복될 때 **모든 파일을 수정**해야 하는 문제 발생
- 페이지의 **공통 요소를 포함**하고, 하위 템플릿이 **재정의할 수 있는 공간**을 정의한 기본 skeleton 템플릿을 작성 → 하위 템플릿이 상속받아 사용

### 상속 관련 DTL 태그

| 태그 | 위치 | 역할 |
|---|---|---|
| `{% extends 'path' %}` | 하위 템플릿 | 자식(하위) 템플릿이 부모 템플릿을 확장한다는 것을 알림. **반드시 템플릿 최상단에 작성**, **2개 이상 사용 불가** |
| `{% block name %}{% endblock name %}` | 상위·하위 템플릿 | 하위 템플릿에서 **재정의(override)할 수 있는 블록**을 정의. 하위 템플릿이 작성할 수 있는 공간 지정 |

```html
<!-- articles/base.html (상위) -->
<body>
  {% block content %}
  {% endblock content %}
</body>
```

```html
<!-- articles/index.html (하위) -->
{% extends 'articles/base.html' %}

{% block content %}
  <h1>Hello, {{ name }}</h1>
{% endblock content %}
```

- 자식의 block 이름과 부모의 block 이름이 **일치해야** 해당 영역이 교체됨
- endblock 뒤에 블록 이름을 적어주면 가독성이 좋아짐 (선택 사항)

> 확인 문제: 상위 템플릿 지정 태그 → **`{% extends %}`** (`include`, `import`, `template` 아님)
>
> ⚠️ `{% extends 'articles/base.html' %}`(템플릿 상속)와 `include('articles.urls')`(URL 설정 위임)는 **전혀 다른 것**이다.

---

## 4. 요청과 응답 — HTML form

### HTML form

- HTML 상에서 **HTTP 요청을 서버에 보내는 가장 편리한 방법**
- 웹에서 사용자 정보를 입력하는 여러 방식 제공 (text, password, checkbox 등)

### form 핵심 속성

| 속성 | 역할 |
|---|---|
| **action** | 입력 데이터가 전송될 **URL(목적지)** 지정. **지정하지 않으면 현재 form이 있는 페이지의 URL로 전송** |
| **method** | 데이터를 **어떤 방식**으로 보낼지 정의. HTTP request methods(**GET, POST**) 지정. 생략하면 GET |

> 확인 문제: action이 없을 때 → **현재 페이지**로 전송 (`action="/"`은 사이트 루트로 전송 — 구분할 것)
>
> 확인 문제: form에서 사용하는 HTTP 메서드가 아닌 것 → **FETCH** (form은 기본적으로 GET, POST 사용)

### input 핵심 속성: name

- 사용자 입력 데이터를 받는 요소. `type` 속성 값에 따라 동작 방식이 달라짐
- **name 속성**: input의 핵심 속성
  - 데이터를 제출했을 때 **서버는 name 속성에 설정된 값을 통해서만 사용자가 입력한 데이터에 접근** 가능
  - name 속성 값이 Query String의 **key**가 됨

> ⚠️ `id`는 `<label for="...">`과 연결하는 HTML 식별자일 뿐이다. 서버가 값을 찾는 키는 **name**.

### Query String Parameters

- 사용자 입력 데이터를 URL 주소에 파라미터로 붙여 서버로 전송하는 방법
- 형식: `&`로 연결된 `key=value` 쌍, 기본 URL과는 `?`로 구분

```text
http://host:port/path?key=value&key=value
```

### fake Naver 예시

```html
<!-- articles/search.html -->
{% extends 'articles/base.html' %}

{% block content %}
  <form action="https://search.naver.com/search.naver" method="GET">
    <label for="message">검색어</label>
    <input type="text" name="query" id="message">
    <input type="submit" value="submit">
  </form>
{% endblock content %}
```

- 결과 URL: `https://search.naver.com/search.naver?query=검색어`
- 네이버 서버가 `query`라는 key로 검색어를 받기 때문에 input의 name을 `query`로 맞춘 것

### 데이터를 보내고 받기 (throw & catch)

```python
# urls.py
path('throw/', views.throw),
path('catch/', views.catch),

# views.py
def throw(request):
    return render(request, 'articles/throw.html')

def catch(request):
    message = request.GET.get('message')
    context = {
        'message': message,
    }
    return render(request, 'articles/catch.html', context)
```

```html
<!-- articles/throw.html -->
{% extends 'articles/base.html' %}

{% block content %}
  <h1>Throw</h1>
  <form action="/catch/" method="GET">
    <input type="text" id="message" name="message">
    <input type="submit">
  </form>
{% endblock content %}
```

```html
<!-- articles/catch.html -->
{% extends 'articles/base.html' %}

{% block content %}
  <h1>{{ message }}</h1>
{% endblock content %}
```

- **request 객체**: 요청에 대한 모든 정보가 담겨 있음
- GET 방식으로 전송된 데이터는 **`request.GET`**(QueryDict)에 담김
- **`request.GET.get('key')`로** name 속성 값(key)에 해당하는 데이터 추출

| 코드 | key가 없을 때 |
|---|---|
| `request.GET.get('message')` | `None` 반환 |
| `request.GET['message']` | 예외(`MultiValueDictKeyError`) 발생 |

> ⚠️ GET 데이터는 URL에 그대로 노출되므로 비밀번호 같은 민감한 값을 보내면 안 된다. 서버 데이터를 바꾸는 요청은 POST (5단원에서 다룸).

---

## 5. Django URLs

- 요청과 응답에서 URLs의 역할: **요청 URL에 따라 실행될 view 함수가 달라짐**

### URL dispatcher

- **URL 패턴을 정의**하고, 해당 패턴이 일치하는 요청을 처리할 **view 함수를 연결(매핑)**
- 프로젝트 폴더의 `urls.py`를 이용해 설정

---

## 6. Variable Routing

### 필요한 이유

- 템플릿의 많은 부분이 중복되고 URL의 일부만 변경되는 상황
  - `articles/1/`, `articles/2/`, `articles/3/` ... 을 계속 따로 작성해야 하는 문제

### 정의

- **URL 일부에 변수를 포함**시키는 것
- 변수는 **view 함수의 인자로 전달**할 수 있음
- 작성 형식: **`<path_converter:variable_name>`**

```python
# urls.py
urlpatterns = [
    path('articles/<int:num>/', views.detail),
    path('hello/<str:name>/', views.greeting),
]

# views.py
def detail(request, num):
    context = {
        'num': num,
    }
    return render(request, 'articles/detail.html', context)

def greeting(request, name):
    context = {
        'name': name,
    }
    return render(request, 'articles/greeting.html', context)
```

- 요청 URL의 `<int:num>` 위치에 들어온 값이 변수처럼 취급됨
- 값은 view 함수에 **키워드 인자**로 전달
  - `/articles/10/` → `views.detail(request, num=10)`
  - `/hello/Jane/` → `views.greeting(request, name='Jane')`
  - 키워드 인자: 함수 호출 시 인자 순서를 무시하고 특정 매개변수에 값을 할당하는 인자
- **Path Converter의 변수명과 View 함수의 파라미터 이름은 같아야 함**

### Path Converter

- URL 변수의 타입을 지정. **5가지 타입** 지원: `str`, `int`, `slug`, `uuid`, `path` (강의에선 str/int 위주)
- `<int:num>`인데 `/articles/abc/`로 요청하면 → int 패턴에 맞지 않아 매칭 실패 (다른 패턴이 없으면 404)

> 확인 문제: URL 변수 전달 올바른 방법 → **`path('user/<int:id>/', views.user_detail)`** (`{id}`, `url()`, `get()`, `:id` 형식은 오답)
>
> ⚠️ `/articles/3/`(경로 변수)와 `/articles/?num=3`(쿼리 스트링)은 다르다. 경로 변수는 view **인자**로, 쿼리 스트링은 `request.GET`으로 받는다.

---

## 7. App URL 정의

### App URL mapping

- **각 앱에 URL을 정의**하는 것
- 프로젝트와 각 앱이 URL을 나누어 관리를 편하게 하기 위함
- 앱이 늘어나도 서로 다른 앱의 URL이 섞이지 않도록 나누어 관리

### 2번째 앱(pages) 생성 후 문제

- view 함수 이름이 같거나 같은 패턴의 URL을 사용하는 경우 충돌
- `from articles import views as article_views`처럼 별칭으로 해결할 수 있으나 **권장되지 않음**
- 해결: **"URL을 각자 app에서 관리하자"**

### URL 구조 변화

- 기존: 프로젝트 `urls.py`에 모든 URL이 담겨 있음
- 변경: **각 앱의 `urls.py`에서** 각자의 URL 관리

```text
요청 → 프로젝트 urls.py → 앱 urls.py → views
```

### include 함수

- `include('app.urls')`
- **프로젝트 내부 앱들의 URL을 참조할 수 있도록 매핑**하는 함수
- URL의 **일치하는 부분까지 잘라내고**, **남은 문자열 부분은 후속 처리를 위해 include된 URL로 전달**

```python
# articles/urls.py  (앱 폴더에 직접 생성)
from django.urls import path
from . import views    # 현재 앱 폴더의 views 모듈

urlpatterns = [
    path('', views.index),
    path('dinner/', views.dinner),
    path('<int:num>/', views.detail),
]
```

```python
# firstpjt/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('pages/', include('pages.urls')),
]
```

- 요청 URL이 `http://127.0.0.1:8000/articles/dinner/`일 때
  1. `firstpjt/urls.py`에서 `articles/`까지 일치 → 잘라냄
  2. 남은 `dinner/`를 `articles/urls.py`에서 찾음
- 앱 urls.py의 `''`(빈 문자열)은 `articles/` **그 자체**를 의미
- 앱 URL 이동 후 HTML의 href 주소도 `/articles/dinner/`처럼 앞에 `articles/`가 붙도록 변경해야 함

> 확인 문제: 앱별 URL 구성을 따로 하는 설정 → **urls.py에서 `include()` 사용**
>
> ⚠️ 앱 urls.py에도 `articles/`를 또 적으면 최종 주소가 `/articles/articles/...`가 된다 (prefix 중복).

---

## 8. URL 이름 지정 (Naming URL patterns)

### URL 구조 변경에 따른 문제

- 기존 주소 앞에 `articles/`가 붙으면서 **해당 URL을 사용하는 모든 위치를 찾아가 변경**해야 함
- 해결: **"URL에 이름을 지어주면 이름만 기억하면 되지 않을까?"**

### Naming URL patterns

- **URL에 이름을 지정**하는 것
- path 함수에 **`name` 인자를 키워드 인자로** 정의해서 사용

```python
# articles/urls.py
urlpatterns = [
    path('', views.index, name='index'),
    path('dinner/', views.dinner, name='dinner'),
    path('search/', views.search, name='search'),
    path('throw/', views.throw, name='throw'),
]
```

- a 태그의 **href** 속성뿐 아니라 form의 **action** 속성 등도 변경해야 함

> 확인 문제: URL 이름 지정 이유 → **템플릿에서 링크를 쉽게 연결하기 위해** (경로가 바뀌어도 이름만 유지하면 됨 → 유지보수 편리)

### DTL url tag

- 형식: **`{% url 'url_name' arg1 arg2 %}`**
- **주어진 URL 패턴의 이름과 일치하는 절대 경로 주소를 반환**
- URL에 이름을 붙였을 때, url 태그와 이름으로 템플릿에서 실제 주소를 작성할 수 있게 해줌

```html
<a href="{% url 'index' %}">index</a>
<a href="{% url 'dinner' %}">dinner</a>
```

- 브라우저에서 실제 링크는 `/articles/`, `/articles/dinner/`처럼 렌더링됨
- **태그 이름, URL 이름, 인자 등은 콤마(,)로 구분하지 않음** (띄어쓰기로 구분)
- URL 패턴에 변수가 있으면 `'url_name'` 뒤에 인자 추가 — 빠뜨리면 reverse 에러
  - `{% url 'detail' 1 %}` → `/articles/1/`
- DTL for 태그에서 사용한 변수 이름도 인자로 사용 가능

```html
{% for num in nums %}
  <a href="{% url 'detail' num %}">Article {{ num }}</a>
{% endfor %}
```

> 확인 문제: URL 태그 올바른 문법 → **`{% url 'home' %}`** (`{{ }}`, `[[ ]]`, `<% %>` 오답)

---

## 9. URL 이름 공간 (app_name)

### URL 이름 지정 후 남은 문제

- articles 앱과 pages 앱 모두 `name='index'`가 있으면 **이름만으로는 완벽하게 분리 불가**
- 해결: **"이름에 성(key)을 붙이자"**

### app_name 속성 지정

```python
# articles/urls.py
app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
]

# pages/urls.py
app_name = 'pages'
urlpatterns = [
    path('', views.index, name='index'),
]
```

- app_name이 추가되거나 수정되면 **url 태그에도 반영**해야 함
  - `{% url 'url_name' %}` → **`{% url 'app_name:path_name' %}`**

```html
<a href="{% url 'articles:index' %}">index</a>
<a href="{% url 'articles:dinner' %}">dinner</a>
<a href="{% url 'pages:index' %}">pages 홈</a>
```

- 최종 링크(`/articles/`, `/articles/dinner/`)는 변하지 않음

| 구분 | 어디에 쓰나 | 의미 |
|---|---|---|
| `name='index'` | 각 `path(...)` | 개별 URL 패턴 이름 |
| `app_name = 'articles'` | 앱의 `urls.py` 최상단 | URL **네임스페이스** (템플릿 폴더명과 무관) |

> 확인 문제: app_name 사용 목적 → **URL 이름이 중복되지 않도록 네임스페이스를 지정하기 위해**

---

## 10. 추가 템플릿 경로와 주의사항

### 추가 템플릿 경로 (DIRS)

- 앱 폴더 밖(프로젝트 최상위)의 `templates/`에 공통 템플릿(예: `base.html`)을 두고 싶을 때

```python
# settings.py
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # 추가 템플릿 검색 경로
        'APP_DIRS': True,                   # 각 앱의 templates/ 폴더도 검색
        # 'OPTIONS': { ... 기존 기본값 유지 ... },
    },
]
```

- **BASE_DIR**: 프로젝트 기준 디렉토리를 가리키는 `Path` 객체 → `BASE_DIR / 'templates'`처럼 `/`로 경로 결합
- **DIRS**: 앱 폴더 외에 추가로 템플릿을 찾을 경로 목록
- **APP_DIRS=True**: 설치된 앱 내부의 `templates/`도 찾음

> 확인 문제: 추가 템플릿 검색 경로 설정 → **`TEMPLATES` 설정 안의 `DIRS`** (`STATICFILES_DIRS`는 정적 파일용 — 7단원)

### 주의사항

- DTL에서 복잡한 로직을 짜지 말고, 계산은 View에서 끝내고 결과만 넘길 것
- URL 끝의 `/`(trailing slash)는 Django의 관례. 기술적으로 `/foo`와 `/foo/`는 서로 다른 URL이며, `APPEND_SLASH` 설정에 따라 슬래시를 붙인 주소로 리다이렉트될 수 있다
