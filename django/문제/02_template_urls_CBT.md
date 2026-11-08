# Django 2단원 CBT — Template & URLs (30문항)

> 출제 범위: [`../02_template_urls.md`](../02_template_urls.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. Django Template System의 주요 목적은?

- ① HTML과 Python 코드를 분리해 작성하기 위해
- ② 모델 정의를 읽어 데이터베이스 테이블을 만들기 위해
- ③ 로그인한 사용자를 확인하는 인증 처리를 위해
- ④ startproject처럼 프로젝트 폴더 구조를 만들기 위해

---

### 2. DTL 문법과 용도의 연결로 **옳지 않은** 것은?

- ① `{{ name }}` — 변수 값 출력
- ② `{{ name|upper }}` — 출력 값 변형(필터)
- ③ `{% for x in items %}` — 반복 같은 로직 처리(태그)
- ④ `{# ... #}` — 여러 줄 주석 처리

---

### 3. view에서 `context = {'numbers': [10, 20, 30]}`를 넘겼다. 템플릿에서 `{{ numbers.1 }}`의 출력은?

- ① 20
- ② 10
- ③ [10, 20, 30]
- ④ 에러 발생 (DTL에서는 인덱스로 접근할 수 없다)

---

### 4. 앱 폴더 밖, 프로젝트 최상위의 `templates/` 폴더를 추가 템플릿 경로로 등록하는 설정은?

- ① `STATICFILES_DIRS` 리스트에 경로 추가
- ② `MEDIA_ROOT`에 templates 경로 지정
- ③ `TEMPLATE_PATH` 문자열에 경로 지정
- ④ `TEMPLATES` 설정 안의 `DIRS`

---

### 5. 상위(부모) 템플릿을 상속받을 때 사용하는 태그는?

- ① `{% include %}`
- ② `{% import %}`
- ③ `{% extends %}`
- ④ `{% template %}`

---

### 6. 템플릿 상속에 대한 설명으로 **옳지 않은** 것은?

- ① extends 태그는 자식 템플릿의 최상단에 작성한다.
- ② 하나의 템플릿에서 extends 태그는 한 번만 쓸 수 있다.
- ③ 자식은 부모와 같은 이름의 block을 재정의해 그 영역의 내용을 채운다.
- ④ endblock 뒤에 블록 이름을 반드시 적어야 오류가 나지 않는다.

---

### 7. `<form>` 태그의 `action` 속성을 생략했을 때 데이터가 전송되는 곳은?

- ① 사이트 루트 주소(`/`)
- ② 직전에 방문했던 이전 페이지
- ③ base.html 템플릿이 있는 위치
- ④ 현재 페이지의 URL

---

### 8. HTML form 제출 시 서버가 사용자 입력값을 찾는 key로 쓰이는 input 속성은?

- ① `name`
- ② `id`
- ③ `type`
- ④ `value`

---

### 9. 다음 form에 hello를 입력해 제출했을 때 요청 URL은?

```html
<form action="/catch/" method="GET">
  <input type="text" name="message">
  <input type="submit">
</form>
```

- ① `/catch/hello/`
- ② `/catch/?message=hello`
- ③ `/catch/#message=hello`
- ④ `/catch/?hello=message`

---

### 10. 위 요청을 받은 catch view에서 입력값을 꺼내는 코드로 옳은 것은?

- ① `request.POST.get('message')`
- ② `request.message`
- ③ `request.GET.get('message')`
- ④ `request.GET.get('hello')`

---

### 11. `message` 키가 **없을 때** `request.GET.get('message')`와 `request.GET['message']`의 동작으로 옳은 것은?

- ① 둘 다 None을 반환한다.
- ② get()은 None을 반환하고, 대괄호 방식은 예외가 발생한다.
- ③ get()은 예외가 발생하고, 대괄호 방식은 None을 반환한다.
- ④ 둘 다 빈 문자열을 반환한다.

---

### 12. `/articles/10/` 요청에서 10을 **정수**로 받아 detail view에 넘기는 URL 패턴은?

- ① `path('articles/<int:num>/', views.detail)`
- ② `path('articles/{num}/', views.detail)`
- ③ `path('articles/:num/', views.detail)`
- ④ `path('articles/<num:int>/', views.detail)`

---

### 13. 다음 URL 패턴에 연결할 view 함수 선언부로 옳은 것은?

```python
path('hello/<str:name>/', views.greeting)
```

- ① `def greeting(request, username):`
- ② `def greeting(request, name):`
- ③ `def greeting(name):`
- ④ `def greeting(request, str):`

---

### 14. Django가 기본 제공하는 path converter가 **아닌** 것은?

- ① `str`
- ② `float`
- ③ `slug`
- ④ `uuid`

---

### 15. `include()`에 대한 설명으로 **옳은** 것은?

- ① HTML 템플릿에서 다른 템플릿을 불러와 상속받는 함수다.
- ② 앱의 views 모듈 전체를 프로젝트로 import하는 함수다.
- ③ 일치한 부분까지 잘라내고 나머지를 앱 URL로 넘긴다.
- ④ 앱 urls.py에서 상위 프로젝트 urls.py를 불러올 때 쓴다.

---

### 16. 프로젝트 urls.py에 `path('articles/', include('articles.urls'))`가 있을 때, articles/urls.py의 `path('', views.index)`가 처리하는 요청 URL은?

- ① `/`
- ② `/index/`
- ③ `/articles/articles/`
- ④ `/articles/`

---

### 17. 프로젝트에 `path('articles/', include('articles.urls'))`가 있는데, 앱 urls.py에도 `path('articles/', views.index)`라고 쓰면 index의 최종 URL은?

- ① `/articles/articles/`
- ② `/articles/`
- ③ `/articles/index/`
- ④ 에러가 나서 서버가 실행되지 않는다.

---

### 18. URL에 이름(`name`)을 지정하는 이유로 가장 적절한 것은?

- ① URL을 암호화해서 사용자에게 숨기기 위해
- ② URL을 해석하는 처리 속도를 높이기 위해
- ③ 경로가 바뀌어도 이름으로 링크를 유지하기 위해
- ④ 앱을 INSTALLED_APPS에 자동으로 등록하기 위해

---

### 19. `path('<int:num>/', views.detail, name='detail')`일 때, 1번 글로 가는 링크를 만드는 올바른 DTL은?

- ① `{{ url 'detail' 1 }}`
- ② `{% url 'detail', 1 %}`
- ③ `{% url 'detail' 1 %}`
- ④ `{% url detail=1 %}`

---

### 20. articles 앱 urls.py에 `app_name = 'articles'`와 `name='index'`가 있을 때 올바른 url 태그는?

- ① `{% url 'index:articles' %}`
- ② `{% url 'articles:index' %}`
- ③ `{% url 'articles.index' %}`
- ④ `{% url 'articles/index' %}`

---

## 함정 문제 (21~30)

### 21. 다음 중 HTTP request method가 **아닌** 것은?

- ① `GET`
- ② `POST`
- ③ `DELETE`
- ④ `FETCH`

---

### 22. `<form>` 태그에서 `method` 속성을 **생략**하면 어떤 방식으로 전송되는가?

- ① GET
- ② POST
- ③ 전송되지 않는다
- ④ 브라우저마다 다르다

---

### 23. `/articles/?page=3` 요청에서 3을 view로 꺼내는 방법은?

- ① view 함수의 매개변수 `page`로 받는다.
- ② `request.page`로 꺼낸다.
- ③ `request.GET.get('page')`로 꺼낸다.
- ④ `<int:page>` 패턴이 자동으로 받아 준다.

---

### 24. detail 패턴이 `path('<int:pk>/', views.detail, name='detail')`인데 템플릿에서 `{% url 'articles:detail' %}`처럼 **인자 없이** 쓰면?

- ① NoReverseMatch 에러가 난다.
- ② pk 없이 `/articles/` 주소가 만들어진다.
- ③ pk 자리에 0이 자동으로 채워진 주소가 된다.
- ④ 빈 문자열이 출력되고 에러는 나지 않는다.

---

### 25. `path('articles/<int:num>/', views.detail)`만 있을 때 `/articles/abc/`로 요청하면?

- ① num='abc'로 detail view가 호출된다.
- ② num=None인 채로 detail view가 호출된다.
- ③ 일치하는 패턴이 없어 404 Not Found가 난다.
- ④ abc를 정수로 바꾸다 실패해 500 에러가 난다.

---

### 26. `app_name`에 대한 설명으로 **옳은** 것은?

- ① 앱 urls.py에 쓰는 URL 네임스페이스이며 템플릿 폴더명과 무관하다.
- ② templates 아래 앱 폴더 이름과 반드시 같아야 동작한다.
- ③ settings.py의 INSTALLED_APPS 목록 안에 선언한다.
- ④ app_name을 지정하면 실제 URL 경로 앞에도 그 이름이 자동으로 붙는다.

---

### 27. 부모 base.html에는 `{% block content %}{% endblock %}`만 있다. 자식이 `{% block main %}...{% endblock %}`으로 작성하면?

- ① 자식의 main 블록 내용이 content 자리에 대신 들어간다.
- ② 블록 이름이 달라 TemplateSyntaxError가 발생한다.
- ③ 부모에 main 블록이 없어 자식의 내용이 화면에 나오지 않는다.
- ④ 부모의 content 블록 이름이 자동으로 main으로 바뀐다.

---

### 28. 한 템플릿 안에서 `{% extends %}` 태그를 **두 번** 사용하면?

- ① 나중에 쓴 부모 템플릿만 적용된다.
- ② 두 부모 템플릿이 순서대로 합쳐진다.
- ③ 먼저 쓴 부모 템플릿만 적용된다.
- ④ 에러가 발생한다.

---

### 29. 다음 중 DTL 문법이 **올바른** 것은?

- ① `{{ if user.is_authenticated }}`
- ② `{% for article in articles %}`
- ③ `{% article.title %}`
- ④ `{{ url 'articles:index' }}`

---

### 30. 프로젝트 urls.py에 `path('pages/', include('pages.urls'))`, pages/urls.py에 `path('about/', views.about)`가 있다. about view의 URL은?

- ① `/about/`
- ② `/pages/about/`
- ③ `/pages/pages/about/`
- ④ `/about/pages/`

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ① | ④ | ① | ④ | ③ | ④ | ④ | ① | ② | ③ |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ② | ① | ② | ② | ③ | ④ | ① | ③ | ③ | ② |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ① | ③ | ① | ③ | ① | ③ | ④ | ② | ② |

- **1. ①** 템플릿은 표현(화면)을, View는 로직을 맡도록 분리한다. 강의 확인문제 1번.
- **2. ④** `{# #}`는 한 줄 주석. 여러 줄 주석은 `{% comment %} ... {% endcomment %}`.
- **3. ①** DTL은 인덱스·속성·딕셔너리 키를 모두 점(.)으로 접근한다. `numbers.1`은 두 번째 요소.
- **4. ④** `'DIRS': [BASE_DIR / 'templates']`. STATICFILES_DIRS는 정적 파일용(7단원), TEMPLATE_PATH라는 설정은 없다.
- **5. ③** 자식 템플릿 최상단에 `{% extends 'articles/base.html' %}`. 강의 확인문제 3번.
- **6. ④** `{% endblock content %}`처럼 이름을 적는 건 가독성을 위한 선택 사항이다.
- **7. ④** action 생략 = 현재 페이지로 전송. `action="/"`(사이트 루트)와 구분할 것.
- **8. ①** 서버는 name 속성 값으로만 입력 데이터에 접근한다. id는 label과 연결하는 HTML 식별자일 뿐.
- **9. ②** GET은 입력값을 쿼리 스트링으로 보낸다. 기본 URL과 `?`로 구분하고 `name=값` 형태.
- **10. ③** GET으로 온 데이터는 `request.GET`(QueryDict)에 담기고, key는 input의 name인 `'message'`.
- **11. ②** 딕셔너리와 같다. `.get()`은 기본값 None, `['key']`는 MultiValueDictKeyError.
- **12. ①** 형식은 `<path_converter:variable_name>`. 순서가 바뀐 ④와 다른 프레임워크 문법(②③)은 오답.
- **13. ②** URL 변수명과 view 매개변수 이름이 같아야 한다(키워드 인자로 전달). 첫 인자 request도 필수.
- **14. ②** 기본 5가지: str, int, slug, uuid, path. float는 없다.
- **15. ③** 프로젝트 urls.py에서 `include('articles.urls')`로 앱 URL에 나머지 처리를 위임한다. 템플릿 상속(extends)과는 무관.
- **16. ④** include가 `articles/`를 잘라낸 뒤 남은 빈 문자열이 `''`와 매칭된다. 즉 `''`는 `/articles/` 자체.
- **17. ①** 프로젝트 prefix + 앱 경로가 이어 붙는다. 앱 쪽에 prefix를 또 쓰면 중복된다.
- **18. ③** 주소를 하드코딩하면 경로가 바뀔 때 모든 곳을 고쳐야 한다. 이름만 유지하면 된다. 강의 확인문제 8번.
- **19. ③** url은 태그라 `{% %}`를 쓰고, URL 이름과 인자는 쉼표 없이 띄어쓰기로 구분한다.
- **20. ②** 형식은 `'app_name:path_name'`. app_name은 URL 이름 중복을 막는 네임스페이스다.
- **21. ④** FETCH는 JavaScript의 fetch() API 이름일 뿐 HTTP 메서드가 아니다. DELETE는 실제 HTTP 메서드지만 HTML form에서는 GET·POST만 쓸 수 있다. 강의 확인문제 4번.
- **22. ①** method 기본값은 GET이다. action 생략(현재 페이지로 전송)과 함께 짝으로 외울 것.
- **23. ③** `?page=3`은 쿼리 스트링이라 request.GET으로 받는다. view 인자로 들어오는 건 `/articles/3/`처럼 경로에 포함된 변수(Variable Routing)뿐.
- **24. ①** URL 패턴에 변수가 있으면 url 태그에도 그 인자를 넘겨야 역으로 주소를 만들 수 있다.
- **25. ③** int 컨버터는 숫자만 매칭한다. view까지 가지도 않고 URL 매칭 단계에서 실패한다.
- **26. ①** app_name은 url 태그에서 `'articles:index'`처럼 쓰는 이름 구분용이다. 실제 주소(/articles/)는 프로젝트 urls.py의 prefix가 결정한다.
- **27. ③** 자식은 부모에 있는 이름의 block만 덮어쓸 수 있다. 이름이 다르면 에러 없이 조용히 무시된다 — 그래서 더 찾기 어렵다.
- **28. ④** extends는 템플릿당 한 번만, 최상단에 쓴다. 두 번 쓰면 TemplateSyntaxError.
- **29. ②** 로직(if·for·url 등 태그)은 `{% %}`, 값 출력은 `{{ }}`. ①④는 태그를 `{{ }}`에, ③은 변수를 `{% %}`에 넣었다.
- **30. ②** 프로젝트 prefix + 앱 경로가 앞에서부터 이어 붙는다.
