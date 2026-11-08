# Django 08 — Authentication System 01: 쿠키·세션, Custom User, 로그인

> 📎 확인문제·예상문제·암기카드: [`시험대비/08_auth_cookie_session_login_시험대비.md`](시험대비/08_auth_cookie_session_login_시험대비.md)

*(인증 3부작의 1편. HTTP가 사용자를 기억하지 못하는 문제를 쿠키·세션으로 푸는 원리, 프로젝트 초기에 Custom User를 깔아 두는 이유, 그리고 로그인(=세션 생성)까지. 로그아웃·회원가입은 [09](09_auth_logout_signup_access.md), 회원정보 수정·비밀번호는 [10](10_auth_user_update_password.md).)*

## 오늘의 목차

1. HTTP의 특징
2. 쿠키 (Cookie)
3. 세션 (Session)
4. 쿠키 vs 세션, 로그인 상태 유지 흐름
5. Django Authentication System
6. Custom User Model
7. Login (로그인)
8. 템플릿에서 로그인 사용자 출력하기
9. 테스트용 유저 만들기

---

## 1. HTTP의 특징

| 특징 | 의미 |
|---|---|
| **비연결 지향 (connectionless)** | 요청에 대한 응답을 보내고 나면 연결을 끊음 |
| **무상태 (stateless)** | 각 요청이 독립적. 서버는 이전 요청을 **기억하지 못함** |

- 그래서 요청이 끝나면 서버는 클라이언트를 기억하지 못한다 → "방금 로그인한 그 사람"인지 다음 요청에서 알 길이 없음
- 로그인 상태를 유지하기 위해 **쿠키(브라우저 쪽)와** **세션(서버 쪽)을** 함께 사용

> ⚠️ 함정: "HTTP가 사용자 정보를 자동으로 기억한다" → ❌

---

## 2. 쿠키 (Cookie)

- 서버가 브라우저에 **저장하도록 전달하는 작은 데이터** (key-value)
- 동작
  1. 서버가 응답의 **`Set-Cookie`** 헤더로 쿠키를 내려줌
  2. 브라우저는 쿠키를 저장해 두고
  3. 이후 같은 서버에 요청할 때마다 **`Cookie`** 헤더에 담아 **자동으로** 함께 보냄
- 용도: 세션 관리(로그인), 개인화(테마·언어), 트래킹 등

### 쿠키의 수명

| 종류 | 언제까지 |
|---|---|
| Session cookie | 브라우저를 닫으면(세션 종료) 삭제 |
| Persistent cookie | `Expires` / `Max-Age`로 정한 기간 동안 유지 |

### 쿠키 보안 속성

| 속성 | 효과 |
|---|---|
| `HttpOnly` | JavaScript(`document.cookie`)로 **읽지 못하게** 함. 요청에 실려 가는 건 막지 않음 |
| `Secure` | **HTTPS** 연결에서만 전송 |
| `SameSite` | 다른 사이트에서 시작된 요청에 쿠키를 보내지 않도록 제한 → CSRF 위험 감소 |

> ⚠️ 쿠키는 브라우저(사용자 PC)에 저장되므로 **비밀번호 같은 민감 정보를 넣으면 안 된다**. 세션 로그인에서 브라우저가 들고 있는 건 비밀번호가 아니라 **sessionid**(보관함 번호표)뿐이다.

---

## 3. 세션 (Session)

- 서버 쪽에서 사용자의 상태를 기억하고 여러 요청을 **논리적으로 연결**하는 기법
- 흐름
  1. 서버가 세션 생성 → 고유한 **세션 ID** 발급
  2. 세션 ID를 **쿠키**에 담아 브라우저로 보냄
  3. 브라우저가 이후 요청마다 세션 ID 쿠키를 함께 보냄
  4. 서버가 세션 ID로 세션 데이터를 찾아 **누구인지 판별**
- Django 기본 세션 저장소는 **DB** → `django_session` 테이블

---

## 4. 쿠키 vs 세션, 로그인 상태 유지 흐름

| 구분 | 쿠키 (Cookie) | 세션 (Session) |
|---|---|---|
| 저장 위치 | 클라이언트(브라우저) | 서버(DB, `django_session` 테이블) |
| 내용 | `sessionid` (세션을 찾는 열쇠) | "이 세션 키 = 이 유저" 기록 |
| 비유 | 보관함 **번호표** | 서버의 **보관함** |
| 위험 | 탈취·노출·변조 | 세션 ID가 털리면 세션 하이재킹 |

### 로그인 상태 유지 흐름

1. 로그인 성공 → 서버가 세션 생성 후 DB에 저장
2. 응답에 `sessionid` 쿠키를 담아 브라우저로 전송
3. 브라우저는 이후 모든 요청에 `sessionid` 쿠키를 자동으로 함께 보냄
4. 서버는 `sessionid`로 세션을 찾아 "누구인지" 확인 → **`request.user`에 User 객체를 넣어 줌**

- 확인: 개발자 도구 → Application → Cookies에서 `sessionid` 생성 여부

---

## 5. Django Authentication System

- 사용자 인증과 관련된 기능을 모아 놓은 시스템
- `django.contrib.auth` (인증), `django.contrib.sessions` (세션) — 둘 다 `INSTALLED_APPS`에 기본 포함

| 개념 | 질문 | 예 |
|---|---|---|
| **인증 (Authentication)** | 누구인가? (본인 확인) | 로그인 |
| **인가 (Authorization)** | 무엇을 할 수 있는가? (권한 확인) | 내 글만 수정 가능 |

> 📌 이번 인증 3부작은 주로 **인증(로그인 여부)** 중심이다. "로그인했다 = 모든 권한이 있다"가 아니라는 점은 구분해 둘 것.

---

## 6. Custom User Model

- 수업에서는 Django 기본 `auth.User` 대신 **`accounts.User`(커스텀 유저 모델)** 사용
- 이유: 기본 User는 필드가 정해져 있어 나중에 요구사항(필드 추가 등)이 생기면 확장이 어렵다 → **처음부터 내 User 모델로 갈아 끼워 두면** 나중에 바꾸기 쉬움

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```

```python
# settings.py
AUTH_USER_MODEL = 'accounts.User'
```

```python
# accounts/admin.py — 커스텀 User는 admin에 직접 등록해야 보임
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```

- `AUTH_USER_MODEL`: 프로젝트가 실제로 사용할 유저 모델 지정 (기본값 `'auth.User'`)
  - 형식: `'앱이름.모델클래스명'` → `accounts`는 **앱 이름**
- 유저 모델은 **프로젝트 초기(첫 migrate 전)에** 설정하는 것이 원칙
  - 중간에 바꾸면 테이블·외래키·migration 의존성이 꼬여서 매우 복잡 → 학습 환경에서는 `db.sqlite3`와 migration 파일을 지우고 다시 하는 식으로 초기화 (운영 DB에선 절대 금지)

### AbstractUser vs AbstractBaseUser

| 클래스 | 특징 | 언제 |
|---|---|---|
| **AbstractUser** | 기본 User의 필드(username, email, first_name ...)와 기능을 **전부 포함** | 기본 기능은 그대로 쓰고 필드만 조금 추가할 때 → **수업에서 사용** |
| **AbstractBaseUser** | 비밀번호·인증 등 **최소 기능만** 제공. 필드·매니저를 직접 설계 | 인증 방식을 완전히 새로 짤 때 |

> 💡 다른 모델에서 User를 참조할 땐 `User`를 직접 import하지 말고 `settings.AUTH_USER_MODEL`이나 `get_user_model()`을 쓴다 (9·10단원에서 등장).

---

## 7. Login (로그인)

- 로그인 = **세션을 Create** 하는 과정 ("이 브라우저(요청) = 이 유저"로 연결)

| 요청 | 언제 | 할 일 |
|---|---|---|
| GET | 로그인 페이지에 처음 들어올 때 | 빈 로그인 폼 보여주기 |
| POST | 아이디/비번 입력 후 로그인 버튼 클릭 | 입력값 검사 후 로그인 처리 |

```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
]
```

```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
```

```html
<!-- accounts/login.html -->
<h1>Login</h1>
<form action="{% url 'accounts:login' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```

> 💡 6단원 "GET/POST를 하나의 view로" 구조 그대로다. GET → 빈 폼, POST 성공 → 로그인 후 redirect, POST 실패 → 에러 담긴 폼 다시 render.

### AuthenticationForm

- 로그인 시 사용자 입력 데이터를 받는 **built-in Form** (**ModelForm 아님**)
- ModelForm이 아닌 이유: 로그인은 유저를 새로 만드는 게 아니라 **이미 있는 유저인지 확인**만 하는 작업 → `form.save()` 없음
- **첫 번째 인자가 `request`**: 생성자가 `__init__(self, request=None, *args, **kwargs)`
  - `AuthenticationForm(request.POST)`로 쓰면 POST 데이터가 request 자리로 들어가 **unbound form**이 되고, `is_valid()`가 항상 False (에러 메시지도 없음)
  - 헷갈리면 `AuthenticationForm(request, data=request.POST)`
  - request가 필요한 이유: 내부에서 `authenticate(self.request, ...)`를 호출할 때 인증 백엔드가 요청 정보를 참고

```python
ArticleForm(request.POST)                  # ModelForm: 첫 인자가 data
AuthenticationForm(request, request.POST)  # 첫 인자가 request, 두 번째가 data
```

### login(request, user)

- 인증된 사용자를 **로그인시키는 함수** (세션에 유저의 id(pk) 저장)
- `request`: 세션은 요청에 붙어 다님(`request.session`), 응답에 `sessionid` 쿠키를 실어 보내기 위해 필요
- `user`: 누가 로그인했는지 기록할 대상

### get_user()

- `AuthenticationForm`의 **인스턴스 메서드**, 유효성 검사를 통과한 유저 객체를 반환
- 유저 정보는 `is_valid()` 실행 중 폼 객체 안에 저장됨 → 반드시 **`is_valid()` → `get_user()`** 순서

> ⚠️ `form.is_valid()`만으로는 로그인되지 않는다. 검증은 "아이디·비번이 맞다"까지고, **세션을 만드는 건 `auth_login()`이다**.

### 왜 `login as auth_login`으로 가져오는가

- view 함수 이름도 `login` → 파이썬은 같은 이름을 다시 정의하면 마지막 것만 남음
- 그대로 쓰면 `login(request, user)`가 view 함수 자기 자신을 호출 → `TypeError: login() takes 1 positional argument but 2 were given`
- import 쪽에 별명을 붙여 이름을 분리 (view 이름을 바꾸면 urls.py도 고쳐야 해서 보통 import 쪽을 바꿈)

---

## 8. 템플릿에서 로그인 사용자 출력하기

```html
<!-- articles/index.html -->
<h3>Hello, {{ user.username }}</h3>
<a href="{% url 'accounts:login' %}">[LOGIN]</a>
```

- view에서 context로 `user`를 넘긴 적이 없는데 쓸 수 있는 이유
  - `settings.py`의 `TEMPLATES` → `context_processors`에 `django.contrib.auth.context_processors.auth`가 **기본 포함** → **모든 템플릿에 현재 사용자(`user`) 자동 제공**
- `request.user`: 현재 요청과 연결된 사용자. 로그인 안 했으면 **`AnonymousUser`** → username이 빈 값이라 `Hello,`만 보임

> ⚠️ 템플릿에서 버튼을 숨기는 건 **화면 처리**일 뿐, 접근 제한이 아니다. 진짜 보호는 view에서 해야 한다 (9단원 `login_required`).

---

## 9. 테스트용 유저 만들기

```bash
python manage.py createsuperuser
```

- 먼저 `migrate`로 유저 테이블이 있어야 함 (없으면 `no such table: ...`)
- Email은 선택, Password 입력 시 화면에 아무것도 안 보이는 것은 정상
- 짧은 비밀번호는 경고 후 `y` 입력 시 생성 가능
- 비밀번호는 평문이 아니라 `pbkdf2_sha256$...` **해시값**으로 저장 (해시 원리는 10단원)
