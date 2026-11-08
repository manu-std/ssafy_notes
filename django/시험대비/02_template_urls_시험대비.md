# Django 2단원 시험대비 — Template & URLs

> 📎 개념 정리 노트: [`../02_template_urls.md`](../02_template_urls.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

SSAFY 강의 Django_Template_Urls.zip (슬라이드 119장) 기반. 객관식·주관식·서술형 60분 시험 대비. 2단원 자료이며 1단원의 MTV, views.py, render()와 연동됨. 중요도는 강의 강조·실습·확인문제에 따른 학습 우선순위 추정이지 실제 출제를 보장하지 않는다.

## 0. 3분 핵심 요약

- Template system = 데이터(context)와 HTML 표현을 결합하여 동적 페이지를 만드는 기능.
- DTL = Variable {{ name }}, Filter {{ name|upper }}, Tag {% if ... %}, Comment {# ... #} 또는 {% comment %}...{% endcomment %}.
- 상속 = 부모 base.html에 {% block content %}{% endblock %}, 자식 첫 부분에 {% extends 'articles/base.html' %}, 같은 이름의 block 재정의.
- form = action은 요청 목적지, method는 HTTP 방식, input name은 데이터의 키. GET의 값은 URL Query String에 표현된다.
- GET 수신 = request.GET.get('message'), HTML의 &lt;input name="message"&gt;와 키 일치.
- Variable Routing = path('articles/&lt;int:num&gt;/', views.detail)에서 num을 detail(request, num)으로 전달. &lt;str:name&gt; 등 converter.
- App URL = 프로젝트 urls.py에서 path('articles/', include('articles.urls')), 앱 urls.py에서 나머지 경로만 매칭.
- URL 이름 = path('index/', views.index, name='index'), 템플릿에서 {% url 'index' %}.
- Namespace = 앱 urls.py에 app_name = 'articles', 템플릿에서 {% url 'articles:index' %}.
- 추가 템플릿 경로 = settings.py의 TEMPLATES[...]['DIRS']에 BASE_DIR / 'templates'.

## 1. 슬라이드별 학습 지도

| 슬라이드 | 내용 | 중요도 | 헷갈리는 지점 |
| --- | --- | --- | --- |
| 1–12 | 목표·Django Template system·context | ★★★ | 정적 HTML vs 동적 HTML, render(context) |
| 13–23 | DTL Variables / Filters / Tags / Comments | ★★★ | {{ }} vs {% %}; dot 접근, ` |
| 24–32 | 템플릿 상속, extends/block | ★★★ | 부모/자식 역할, 같은 block 이름, extends 상단 |
| 33–60 | HTML form, GET, request, throw/catch | ★★★ | action/method/name, query string, request.GET |
| 61–71 | URL dispatcher, variable routing | ★★★ | &lt;int:num&gt;, view 인자 및 URL 매칭 |
| 72–82 | 앱별 URL, include | ★★★ | 접두 경로 + 앱 경로 결합 |
| 83–93 | URL naming, DTL url tag | ★★★ | name=, {% url ... %}, 전달 인자 |
| 94–99 | app_name namespace | ★★★ | 이름 충돌, articles:index |
| 100–108 | DIRS, BASE_DIR, DTL 주의, trailing slash | ★★ | 템플릿 위치·Python 로직을 뷰에서 처리 |
| 109–118 | 실습·확인문제 12개·활동 정리 | ★★★ | 강의의 직접 확인 항목 |

## 2. 완전 개념 정리

### A. Django Template System과 context

Template은 화면 구조/표현을 맡고 View는 요청을 처리하고 데이터를 준비한다. Python 코드와 HTML 표시를 분리하여 유지보수를 쉽게 한다. render(request, 'articles/index.html', context)는 템플릿에 context를 전달해 HTML 응답을 만든다. context는키/값 딕셔너리다.

```
# articles/views.py
from django.shortcuts import render

def index(request):
    context = {'name': 'Jane', 'numbers': [1, 2, 3]}
    return render(request, 'articles/index.html', context)

<h1>Hello, {{ name }}!</h1>
<p>{{ numbers.0 }}</p>
```

예상 출력 Hello, Jane! 및 1. {{ name }}은 Python 변수 정의문이 아니라 컨텍스트 값 출력 표현식이다. 자료구조의 인덱스/속성/딕셔너리 키는 DTL에서 점(.)으로 접근할 수 있다.

### B. DTL 문법 4종

| 구분 | 기본형 | 목적 | 예 |
| --- | --- | --- | --- |
| Variable | `{{ variable }}` | 값 출력 | `{{ user.name }}` |
| Filter | `{{ variable\|filter }}` | 출력값 변형 | `{{ name\|upper }}` |
| Tag | `{% tag %}` | 조건·반복·구조 | `{% for n in nums %}...{% endfor %}` |
| Comment | `{# 주석 #}` | 한 줄 주석 | `{% comment %}` 여러 줄 `{% endcomment %}` |

필터는 `|`로 연결하며 인자 지정에는 `:`가 쓰인다. `{{ 1|add:2 }}`의 출력은 3이다. 자주 쓰는 예로 upper, lower, length, default, truncatewords 등이 있다(지원 여부·작동은 필터 정의에 따라 다름).

```
{% if login %}
  <h1>Please, login.</h1>
{% else %}
  <h1>Please, login.</h1>
{% endif %}

<ul>
{% for item in nums %}
  <li>{{ item }}</li>
{% endfor %}
</ul>
```

주의: 위 조건문은 분기 문법 예시다. 양쪽 출력이 동일한 예시는 조건에 따라 결과가 달라지는 실습으로 적절하지 않다. 차이를 보려면 if/else의 텍스트를 다르게 써야 한다. DTL은 Python 전체 문법을 그대로 사용할 수 없으며 복잡한 데이터 계산·비즈니스 로직은 View에서 처리한다.

### C. 템플릿 상속 (p25–32)

여러 페이지에서 공통 HTML(navbar, Bootstrap 등)을 반복하지 않고 부모 템플릿의 공통 부분 + 자식 템플릿의 고유 부분을 합성한다.

```
<!-- articles/base.html: 부모 -->
<!doctype html>
<html><body>
  <nav>공통 메뉴</nav>
  {% block content %}{% endblock content %}
</body></html>

<!-- articles/index.html: 자식 -->
{% extends 'articles/base.html' %}
{% block content %}
  <h1>메인 화면</h1>
{% endblock content %}
```

- {% extends '...' %} = 어떤 부모 템플릿을 상속할지 지정. 일반적으로 자식 템플릿의 첫 템플릿 태그로 작성해야 한다.
- {% block content %} = 부모가 자식에 재정의를 허용하는 영역을 지정하고 자식이 내용을 채운다.
- 자식의 block 이름과 부모 block 이름이 일치해야 한다. 다른 이름을 쓰면 의도한 영역을 덮어쓰지 못한다.
- include('articles.urls')와 {% extends 'articles/base.html' %}는 전혀 다르다: URL 모듈 포함 vs HTML 템플릿 상속.

### D. HTML form과 HTTP 요청 (p33–60)

```
<form action="/catch/" method="GET">
  <label for="message">메시지</label>
  <input type="text" name="message" id="message">
  <input type="submit" value="보내기">
</form>
```

입력 안녕을 제출하면 URL은 예컨대 /catch/?message=%EC%95%88%EB%85%95 형태가 된다(URL 인코딩). action=목적지, method=GET/POST 등의 전송 방식, name=전달되는 키, id=label과 연결 등에 사용하는 HTML 식별자. 핵심은 id가 아닌 name 으로 서버 측 입력을 찾아온다는 점.

```
# urls.py
path('throw/', views.throw, name='throw'),
path('catch/', views.catch, name='catch'),

# views.py
def catch(request):
    message = request.GET.get('message')
    return render(request, 'articles/catch.html', {'message': message})
```

request.GET은 쿼리 문자열의 입력 데이터를 담는 QueryDict. request.GET.get('message')는 한 값을 얻고, 키가 없을 때 기본값은 None이다. request.GET['message']는 해당 키가 없으면 예외가 난다. GET 요청 자체가 쿼리 문자열에서만 값을 가진다는 뜻은 아니며, 강의의 GET form 예제에서 이렇게 읽는다.

GET과 POST 구분: GET은 주로 조회 요청, POST는 서버 상태를 변경하거나 데이터를 제출할 때 많이 쓴다. GET 데이터는 URL에노출될 수 있으므로 비밀번호 등의 민감한 값을 GET 쿼리로 전송하면 안 된다. POST는 주소창에 데이터가 표시되지 않지만, 그 자체로 암호화나 보안이 보장되는 건 아니다. HTTPS가 중요하다. Django 내부 POST 폼에는 일반적으로 {% csrf_token %}이 필요하다(이번 강의의 중심은 GET).

action 생략 시 브라우저는 현재 문서 URL로 제출한다. 이와 구별해 action을 /로 지정하면 사이트 루트 URL로 전송된다. method 생략 시 기본은 GET.

### E. URL dispatcher와 Variable Routing (p61–71)

```
# urls.py
path('articles/<int:num>/', views.detail, name='detail'),
path('hello/<str:name>/', views.greeting, name='greeting'),

# views.py
def detail(request, num):
    return render(request, 'articles/detail.html', {'num': num})

def greeting(request, name):
    return render(request, 'articles/greeting.html', {'name': name})
```

- /articles/486/ → detail(request, num=486); num은 정수.
- /hello/Jane/ → greeting(request, name='Jane').
- &lt;converter:variable_name&gt;에서 변수명이 view의 매개변수명과 맞아야 한다.
- 기본 path converter: str, int, slug, uuid, path (강의에서는 특히 str/int 강조).
- &lt;int:num&gt;은 URL의 일부(경로 매개변수)를 뽑는다. ?num=486의 쿼리 문자열과 다름.
- path('articles/&lt;int:num&gt;/')에서 /articles/abc/는 int 패턴에 부합하지 않는다.

### F. 앱별 URL 정의, include (p72–82)

```
# project/urls.py
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
]

# articles/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('<int:num>/', views.detail, name='detail'),
]
```

- /articles/index/ = 프로젝트 prefix articles/ + 앱 index/.
- /articles/12/ = prefix + 앱 &lt;int:num&gt;/.
- include('articles.urls')는 앱 URL 설정으로 나머지 경로 처리를 위임한다.
- 두 URLconf에 같은 prefix를 중복해서 적으면 의도하지 않은 /articles/articles/index/가 될 수 있다.
- 프로젝트의 URLconf는 '어느 앱으로' 나눠 보내는 입구가 되고 앱 URLconf는 자기 앱의 뷰를 연결한다.

### G. URL 이름, DTL URL 태그, 동적 인자 (p83–93)

```
path('index/', views.index, name='index')
path('<int:num>/', views.detail, name='detail')

<a href="{% url 'index' %}">홈</a>
<a href="{% url 'detail' 1 %}">1번 상세</a>
{% for num in nums %}
  <a href="{% url 'detail' num %}">Article {{ num }}</a>
{% endfor %}
```

URL 경로 문자열을 HTML에 직접 박아 두면 경로를 바꾸는 순간 여러 템플릿을 동시에 고쳐야 할 수 있다. **이름에 의한 역참조 (reverse URL resolution)를** 쓰면 실제 path 변경에 강하다. name='detail'의 이름을 {% url 'detail' num %}로 참조한다. DTL URL 태그는 {{ }}가 아니라 {% %}! 동적 URL에 필요한 인자를 빠뜨리면 reverse 오류가 발생할 수 있다.

### H. URL namespace와 app_name (p94–99)

```
# articles/urls.py
app_name = 'articles'
urlpatterns = [path('index/', views.index, name='index')]

# pages/urls.py
app_name = 'pages'
urlpatterns = [path('index/', views.index, name='index')]

<a href="{% url 'articles:index' %}">articles 홈</a>
<a href="{% url 'pages:index' %}">pages 홈</a>
```

다른 앱에서도 index라는 URL 이름을 쓸 수 있기 때문에 namespace로 구분한다. 형식은 app_name:path_name. app_name은 템플릿 파일의 폴더명이 아니라 해당 앱의 urls.py에 선언하는 URL namespace 식별자다. name=은 각 path(...)에 설정하는 개별 URL 패턴 이름이다.

### I. 추가 템플릿 경로, BASE_DIR, DTL 주의점, slash (p100–108)

```
# settings.py
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': []},
    },
]
```

이 코드는 핵심 설정 키를 보여주기 위한 축약 예제다. 실제 프로젝트에서 OPTIONS의 기존 기본값을 임의로 삭제하면 안 된다. DIRS 는 별도로 추가한 템플릿 검색 경로를 지정한다. BASE_DIR은 기준 디렉터리를 가리키는 Path 객체이다. APP_DIRS=True면 설치된 앱내부의 templates/ 폴더도 찾도록 설정한다.

- DTL은 파이썬 로직을 모두 템플릿으로 옮기기 위한 언어가 아니다. 중요한 계산·처리는 view에서 먼저 수행하고 결과를 출력한다.
- URL 끝의 /는 Django에서 일반적으로 쓰는 관례지만 모든 프레임워크의 강제 규칙은 아니다.
- /foo와 /foo/는 기술적으로 서로 다른 URL. APPEND_SLASH 및 middleware 등의 설정에 따라 slash를 붙인 URL로 리다이렉트될 수 있지만, 항상 자동 수정되는 것은 아니다.

## 3. 반드시 구분할 12쌍 — 시험 함정

1. {{ name }} 값 출력 vs {% if ... %} 제어/태그.
2. {{ name|upper }} 필터 vs {% url ... %} URL 태그.
3. {% extends %} 템플릿 상속 vs include() URL 설정 위임.
4. {% block %} 교체 영역 vs {% for %} 반복.
5. form action 목적지 vs method HTTP 방식.
6. input name 데이터 키 vs id HTML 식별자.
7. request.GET.get('key') 값 조회 vs request.GET['key'] 키 없을 때 예외.
8. /article/3/ path 매개변수 vs ?id=3 query string.
9. path('article/&lt;int:num&gt;/') URL 선언 vs detail(request, num) View 인자.
10. name='index' 패턴 이름 vs app_name='articles' 네임스페이스.
11. TEMPLATES['DIRS'] 템플릿 경로 vs STATICFILES_DIRS 정적 파일 경로.
12. action 생략(현재 URL) vs action='/'(사이트 루트).

## 4. 강의 확인문제 원문 12문제 (p110–114)

다음은 강의 끝의 선택지를 뜻을 유지해 전사한 핵심 문제다. 정답은 강의 해설 슬라이드(p113–114)와 대조했다.

1. 템플릿 시스템 주요 목적? (a DB 관리 / b HTML-Python 코드 분리 / c 인증 / d 프로젝트 폴더 생성) → b. 표시와 처리를 분리.
2. DTL 변수 출력 문법? (a {{ 변수명 }} / b {% 변수명 %} / c (( 변수명 )) / d [ 변수명 ]) → a.
3. 상위 템플릿 지정 태그? (a include / b import / c extends / d template) → c.
4. HTML form을 통한 데이터 전송에 쓰는 HTTP 메서드가 아닌 것은? (a GET / b POST / c DELETE / d FETCH) → d. FETCH는 HTTP 메서드가 아님. 주의: DELETE는 표준 HTTP 메서드지만 일반 네이티브 HTML form method의 유효값은 GET/POST/dialog이다.
5. form의 action 생략 시 제출 경로? (a 루트 / b 이전 페이지 / c 현재 페이지 / d 부모 템플릿) → c.
6. 동적 URL 경로 표기? (a path('user/&lt;int:id&gt;/', views.user_detail) / b {id} / c url(...) / d get(...)) → a.
7. 앱 URL 분리 설정? (a urls.py에서 include() / b view import / c models 연결 / d settings에 form 작성) → a.
8. URL 이름 지정 이유? (a 암호화 / b 숨기기 / c 템플릿에서 링크 쉽게 연결 / d URL 길게 만들기) → c.
9. URL 태그 문법? (a {{ url 'home' }} / b [[ url 'home' ]] / c {% url 'home' %} / d &lt;% url 'home' %&gt;) → c.
10. app_name 목적? (a 암호화 / b 렌더 / c namespace 지정해 이름 중복 구분 / d 앱 등록) → c.
11. 추가 템플릿 검색 경로 설정 변수? (a STATICFILES_DIRS / b MEDIA_ROOT / c TEMPLATES / d TEMPLATE_PATH) → c. 정확히는 TEMPLATES 설정 안의 DIRS.
12. DTL 변수 출력 방식이 아닌 것? (a {{ title }} / b {% title %} / c {{ user.name }} / d {{ 1|add:2 }}) → b.

## 5. 추가 예상문제 30개

### 객관식 15문제

Q1. DTL {{ profile.name }}의 설명으로 적절한 것은? ① 부모 템플릿 선언 ② 변수/속성값 표시 ③ URL 앱 등록 ④ POST 요청수행

Q2. 다음 중 필터를 올바르게 사용하는 코드는? ① {% username|upper %} ② {{ username|upper }} ③ {{ username:upper }} ④ {# username|upper #}

Q3. 부모의 {% block content %}를 자식에서 바꾸는 올바른 표현은? ① {% render content %} ② {% include content %} ③ {% block content %}새 내용{% endblock content %} ④ {{ content }}

Q4. input type="text" name="keyword" id="search"인 GET 폼의 값을 읽는 코드? ① request.GET.get('search') ② request.GET.get('keyword') ③ request.POST['search'] ④ request.id

Q5. method="GET"인 폼 제출의 일반적인 특징은? ① 입력 데이터를 경로 변수로만 전달 ② URL의 query string에 입력값을 표현 ③ 언제나 데이터 암호화 ④ 서버 요청 없음

Q6. /hello/Amy/와 path('hello/&lt;str:name&gt;/', views.hello)가 매칭되면 View의 매개변수는? ① name='hello' ② name='Amy' ③ name=None ④ name=0

Q7. path('item/&lt;int:pk&gt;/', views.detail)과 일치하지 않는 주소? ① /item/3/ ② /item/004/ ③ /item/abc/ ④ /item/999/

Q8. path('blog/', include('blog.urls')) + 앱 path('new/', views.new)의 최종 경로는? ① /new/ ② /blog/new/ ③ /blog/blog/ new/ ④ /urls/new/

Q9. name='detail'인 URL pattern에 인자 7을 보내는 DTL 코드는? ① {{ url 'detail' 7 }} ② {% url detail, 7 %} ③ {% url 'detail' 7 %} ④ {% path 'detail' 7 %}

Q10. app_name이 articles이고 개별 URL name이 index일 때? ① {% url 'index:articles' %} ② {% url 'articles:index' %} ③ {{ articles.index }} ④ {% include 'articles:index' %}

Q11. render(request, 'articles/index.html', {'x': 3})의 템플릿에서 3을 출력하려면? ① {% x %} ② {{ 3:x }} ③ {{ x }} ④ {{ request.x }}

Q12. URL 변경에 대비한 권장 링크 작성법? ① &lt;a href="/articles/index/"&gt;만 고정 ② &lt;a href="{% url 'articles:index' %}"&gt; ③ &lt;a href="{{ index }}"&gt; ④ &lt;a href="{% extends 'index' %}"&gt;

Q13. 템플릿 추가 검색 경로를 지정할 곳은? ① settings.py TEMPLATES 내 DIRS ② models.py ③ STATIC_URL ④ admin.py

Q14. HTML form의 action을 생략했을 때 기본 제출 대상은? ① 무조건 / ② 현재 문서 URL ③ 가장 최근 방문 URL ④ Django admin/

Q15. DTL에 관한 가장 옳은 설명은? ① 완전한 Python 프로그램 실행을 목적으로 설계 ② 데이터 처리 로직은 가능하면 View에, 출력은 Template에 ③ 모든 템플릿에 같은 HTML 코드를 복붙해야 함 ④ {{ }}로 if문을 작성

### 주관식 10문제

Q16. DTL에서 값을 출력하는 구분자 두 쌍을 쓰시오.

Q17. 변수를 대문자로 변환하는 필터를 포함해 {{ name }}을 수정하시오.

Q18. base.html을 상속받을 때 쓰는 DTL 태그를 작성하시오. (articles/base.html)

Q19. form의 제출 URL을 결정하는 속성과 HTTP 방식을 결정하는 속성을 순서대로 쓰시오.

Q20. &lt;input name="query"&gt;의 GET 입력값을 view에서 안전하게 조회하는 코드를 쓰시오.

Q21. path('posts/&lt;int:post_id&gt;/', views.detail)의 View 함수 선언부를 쓰시오.

Q22. project/urls.py에서 앱 posts.urls에 /posts/ prefix로 위임하는 path 코드를 쓰시오.

Q23. DTL에서 posts app의 detail URL에 숫자 5를 전달하는 태그를 작성하시오.

Q24. 앱별 URL 이름 충돌을 피하기 위한 urls.py의 변수명을 쓰시오.

Q25. 추가 전역 템플릿 디렉터리 경로를 지정하는 TEMPLATES 내부 설정 키를 쓰시오.

### 서술형 5문제

Q26. Django Template System이 필요한 이유를 View와 Template 역할의 차이를 포함해 3문장 이내로 서술하시오.

Q27. 부모/자식 템플릿 상속의 작동을 extends와 block의 역할을 포함해 설명하고 유지보수상의 장점을 쓰시오.

Q28. 사용자가 /throw/의 &lt;form action="/catch/" method="GET"&gt;&lt;input name="message"&gt;&lt;/form&gt;에 Hello를 입력할 때, 브라우저요청부터 catch view를 거쳐 결과 화면까지 전체 흐름을 4단계 이상으로 쓰시오.

Q29. project/urls.py의 path('articles/', include('articles.urls'))와 앱 urls.py의 path('&lt;int:num&gt;/', views.detail, name='detail')가 있을 때 /articles/7/ 요청이 처리되는 과정을 설명하시오. URL 변수·뷰 인자를 포함하시오.

Q30. articles와 pages 앱이 각각 name='index'를 가진다. app_name과 URL 태그로 충돌을 해결하는 방법을 예시 코드로 제시하고, 하드코딩 URL보다 이름을 이용할 때의 장점을 설명하시오.

## 6. 추가문제 정답·해설

### 객관식

| 문제 | 답 | 해설 |
| --- | --- | --- |
| 1 | ② | 점 접근으로 context 객체/딕셔너리 관련 값을 출력. |
| 2 | ② | `{{ 값 |
| 3 | ③ | 같은 이름의 block을 자식에서 재정의. |
| 4 | ② | 서버 전송 키는 id가 아닌 name. |
| 5 | ② | GET form 입력은 대체로 query string 형태. |
| 6 | ② | str converter는 문자열을 View 인자에 전달. |
| 7 | ③ | int converter는 숫자 패턴 매칭. |
| 8 | ② | 프로젝트 prefix와 앱 세부 경로를 결합. |
| 9 | ③ | url은 DTL 태그; 필요한 경로 인자 제공. |
| 10 | ② | app_name:path_name. |
| 11 | ③ | context의 키 x를 DTL 변수로 사용. |
| 12 | ② | URL 역참조로 하드코딩을 줄임. |
| 13 | ① | TEMPLATES → DIRS. |
| 14 | ② | action 미설정은 현재 페이지 주소. |
| 15 | ② | 로직/출력을 분리하는 설계. |

### 주관식 모범답안

1. {{ 와 }} (즉, {{ 변수명 }}).
2. {{ name|upper }}.
3. {% extends 'articles/base.html' %}.
4. action, method.
5. request.GET.get('query').
6. def detail(request, post_id):.
7. path('posts/', include('posts.urls')) (상단에서 include import).
8. {% url 'posts:detail' 5 %} (app_name='posts', name='detail' 가정).
9. app_name.
10. DIRS.

### 서술형 모범답안 및 채점 키워드

26. Template System은 View가 준비한 데이터(context)를 HTML 템플릿에 주입하여 동적인 화면을 생성한다. View는 요청 처리와 데이터·비즈니스 로직을 담당하고 Template은 표시를 담당한다. 이를 분리하면 가독성과 재사용성, 유지보수가 향상된다. 키워드: context / 동적 페이지 / 역할 분리.
27. 부모 base.html은 공통 마크업과 {% block content %} 같은 변경 지점을 정의한다. 자식은 {% extends 'articles/base.html' %}로 부모를 상속하고 동일한 block 이름을 재정의하여 페이지별 내용을 채운다. 공통 UI를 한 곳에서 수정하여 중복을 줄인다. 키워드: extends=상속 / block=교체 영역 / 공통 구조 재사용.
28. (1) /throw/ 화면에서 사용자가 Hello를 입력해 제출한다. (2) method='GET'이므로 브라우저가 /catch/?message=Hello를 요청한다. (3) Django URLconf가 catch view를 호출한다. (4) View의 request.GET.get('message')는 Hello를 읽고 context를 만든다. (5) render로 템플릿에 전달하고 응답 HTML을 반환한다. 키워드: name → query string → request.GET → context → render.
29. 프로젝트 URLconf는 articles/를 매칭하고 남은 7/ 처리를 articles.urls로 위임한다. 앱 URLconf의 &lt;int:num&gt;/가 7을 정수로 변환해 views.detail(request, num=7)을 호출한다. View는 템플릿을 렌더링해 응답한다. 키워드: include / 접두 경로 / 정수변환 / View 전달.
30. articles/urls.py에 app_name='articles', pages/urls.py에 app_name='pages'를 선언하고 두 파일에서 각각 path('', views.index, name='index')를 둔다. 템플릿에서 {% url 'articles:index' %}와 {% url 'pages:index' %}로 구분한다. URL 패턴의실제 주소가 바뀌어도 URL 이름과 namespace가 유지되면 링크 코드를 고칠 필요가 적다. 키워드: 이름 중복 / namespace / app_name:path_name / reverse.

## 7. 코드 추론 초단기 실전 5개

A. context={'values':[10,20]}일 때 {{ values.1 }} 결과 → 20.

B. {{ 'abc'|upper }} → ABC (일반적인 DTL 문자열 리터럴 필터 적용 예시).

C. path('hello/&lt;str:name&gt;/', views.greeting)에서 def greeting(request, username): → 매개변수명 불일치로 오류. name을 받도록 수정한다.

D. project path('articles/', include('articles.urls')) + app path('search/', views.search) → /articles/search/.

E. 앱이 app_name='articles'일 때 {% url 'index' %}만 쓰면? → 이름을 못 찾거나 의도와 다르게 해석될 수 있으므로 강의 예제에서는 {% url 'articles:index' %}로 적는다.

## 8. 시험 실전 운영 전략

- 15분 암기: DTL 4문법 → extends/block → form(action/method/name) → request.GET → path converter → include → name/url → app_name.
- 15분 코드 읽기: HTML form을 주고 주소창 query string을 예측, URLconf를 주고 실제 접근 경로와 view 인자를 찾기.
- 10분 강의 확인 12문항: 답만 외우지 말고 오답 선택지가 왜 틀렸는지 설명하기.
- 20분 문제풀이: 추가 객관식 15 + 단답형 10 + 서술형 5 중 취약 파트 집중.
- 서술형 규칙: 구성요소의 정의와 역할 → 코드 또는 전달 흐름 → 장점/결과 순서로 쓰기. 2~4문장에 채점 키워드 포함.
- 시험장 60분: 쉬운 객관식/단답형부터 점수 확보(약 20분), 서술·응용에 30분, 남은 10분에 URL 슬래시·quote·중괄호·인자명검토. 실제 배점과 문항 수에 맞춰 조정.

## 9. 시험 직전 60초 암기장

```
{{ x }}                  값 출력
{{ x|upper }}            필터
{% if x %} ... {% endif %} 조건
{% for x in xs %} ... {% endfor %} 반복
{# ... #}                주석
{% extends 'base.html' %} 부모 상속
{% block content %} ... {% endblock content %} 자식의 교체 영역
<form action='/catch/' method='GET'> 목적지와 방식
<input name='message'> 서버에 전송되는 키
request.GET.get('message') GET 데이터 추출
path('<int:num>/', views.detail) URL 정수 변수
include('articles.urls') 앱 URLconf 연결
name='index'             URL 패턴 이름
{% url 'articles:index' %} app namespace 포함 역참조
app_name='articles'      앱 URL 이름 공간
TEMPLATES → DIRS         추가 템플릿 디렉터리
```

최종 셀프체크: 누군가 request.GET.get()과 &lt;int:num&gt;의 차이, extends와 include의 차이, name과 app_name의 차이를 물으면 코드 1줄씩 예시를 들어 즉답할 수 있어야 한다.
