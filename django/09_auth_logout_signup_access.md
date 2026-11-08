# Django 09 — Authentication System 02: 로그아웃, 회원가입, 회원 탈퇴, 접근 제한

> 📎 확인문제·예상문제·암기카드: [`시험대비/09_auth_logout_signup_access_시험대비.md`](시험대비/09_auth_logout_signup_access_시험대비.md)

*(인증 3부작의 2편. [08](08_auth_cookie_session_login.md)에서 로그인 = 세션 Create였다면, 여기선 로그아웃 = 세션 Delete, 회원가입 = User Create, 회원 탈퇴 = User Delete. 마지막으로 로그인 여부에 따라 접근을 막는 두 가지 방법을 배운다.)*

## 오늘의 목차

1. Logout (로그아웃)
2. Signup (회원가입)
3. 회원 탈퇴
4. 로그인 사용자에 대한 접근 제한
5. 정리 — 세션 vs User 객체, 무엇을 만들고 지우나

---

## 1. Logout (로그아웃)

- 로그아웃 = **세션을 Delete** 하는 과정

```python
# accounts/urls.py
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
```

```python
# accounts/views.py
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('articles:index')
```

```html
<h3>Hello, {{ user.username }}</h3>
<a href="{% url 'accounts:login' %}">[LOGIN]</a>
<form action="{% url 'accounts:logout' %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="LOGOUT">
</form>
```

### logout(request)가 하는 일

1. **서버(DB)의 세션 데이터 삭제** (`request.session.flush()`)
2. **클라이언트 쿠키의 sessionid 삭제**

- 추가로 `request.user`를 `AnonymousUser`로 바꿈
- 로그인하지 않은 상태에서 호출해도 에러 없음
- `as` 없이 쓰면 view 함수가 자기 자신을 계속 호출 → `RecursionError` (08단원 `auth_login`과 같은 이유)

> ⚠️ `auth_logout(request)`는 **세션만** 끊는다. DB의 User 계정은 그대로 남는다 (탈퇴 `request.user.delete()`와 완전히 다름).

### 이름 구분

| 이름 | 정체 |
|---|---|
| `name='logout'` | URL의 별명 |
| `def logout` | 우리가 만든 view 함수 |
| `auth_logout` | Django가 만든 실제 로그아웃 처리 함수 |

### 로그인은 a 링크, 로그아웃은 form인 이유

| | 로그인 링크 | 로그아웃 버튼 |
|---|---|---|
| 하는 일 | 로그인 **페이지를 보여달라** 요청 | 세션을 **삭제**해 달라 요청 |
| 서버 상태 변화 | 없음 | 있음 |
| 방식 | GET → `<a>` | POST → `<form>` + `{% csrf_token %}` |

- `<a>`는 GET만 보낼 수 있음. 서버 데이터를 바꾸는 요청은 POST
- 상태를 바꾸는 요청 뒤에는 render가 아니라 **redirect**

> 📌 view 쪽에서도 POST만 받도록 막으려면 `require_POST` 데코레이터를 붙인다 (GET으로 오면 405).
>
> ```python
> from django.views.decorators.http import require_POST
>
> @require_POST
> def logout(request):
>     auth_logout(request)
>     return redirect('articles:index')
> ```

---

## 2. Signup (회원가입)

- 회원가입 = **User 객체를 Create** 하는 과정
- built-in **`UserCreationForm`** (**ModelForm**): username, password1, password2 입력
  - 저장 시 비밀번호를 **해시해서** 저장해 줌 (직접 `user.password = '평문'` 하면 안 되는 이유)

### UserCreationForm을 그대로 쓸 수 없는 이유

- `UserCreationForm`의 `Meta.model`은 기본 **`auth.User`로 고정**되어 있음
- 우리는 `AUTH_USER_MODEL = 'accounts.User'`로 유저 모델을 갈아 끼웠으므로 → 그대로 쓰면 엉뚱한 모델을 가리킴
- 해결: **상속 후 model만 재작성**

```python
# accounts/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
```

- `get_user_model()`: `AUTH_USER_MODEL`에 등록된, **현재 프로젝트가 실제로 쓰는 유저 모델**을 반환 (`accounts.User`)
- `class Meta(UserCreationForm.Meta):` → 부모 Meta의 fields 등은 물려받고 **model만 교체**

```python
# accounts/urls.py
path('signup/', views.signup, name='signup'),
```

```python
# accounts/views.py
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```

- POST, GET **양쪽 모두** CustomUserCreationForm으로 바꿔야 함
- `context`와 `render`가 if/else 바깥 → GET과 "검사 실패한 POST"가 같은 코드 공유 (에러 메시지가 담긴 폼을 다시 보여줌)
- `from .forms`의 `.` = 현재 앱(accounts) 폴더

### 회원가입 후 자동 로그인

- `form.save()`는 유저를 **만들기만** 한다. 로그인까지 시켜주지 않음
- 바로 로그인 상태로 만들려면 save()가 돌려준 유저로 `auth_login` 호출

```python
if form.is_valid():
    user = form.save()
    auth_login(request, user)
    return redirect('articles:index')
```

---

## 3. 회원 탈퇴

- 회원 탈퇴 = **User 객체를 Delete** 하는 과정

```python
# accounts/urls.py
path('delete/', views.delete, name='delete'),
```

```python
# accounts/views.py
def delete(request):
    request.user.delete()
    return redirect('articles:index')
```

```html
<form action="{% url 'accounts:delete' %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="회원탈퇴">
</form>
```

- `request.user`: 지금 요청을 보낸 로그인한 사람의 User 객체
- `.delete()`: 그 객체에 해당하는 DB 행 삭제 (`article.delete()`와 같은 메서드)
- URL에 pk가 없는 이유: 탈퇴 대상은 언제나 **"지금 로그인한 나"라서** `request.user`로 충분

### 탈퇴 후 세션 정리

- 계정만 지우면 브라우저에는 이미 지워진 유저의 세션이 남는다 → 탈퇴 시 **로그아웃까지** 처리하는 게 깔끔함
- 강의 확인문제 정답 순서: **계정 삭제 → 로그아웃**

```python
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('articles:index')
```

> 📌 반대로 로그아웃을 먼저 하면 `request.user`가 `AnonymousUser`로 바뀌어 지울 대상을 잃는다. 순서를 바꾸고 싶다면 `user = request.user`로 **미리 잡아 두고** 로그아웃 → `user.delete()`.

---

## 4. 로그인 사용자에 대한 접근 제한

### ① is_authenticated 속성

- 사용자가 인증되었는지 여부를 알 수 있는 **속성** (User는 True, AnonymousUser는 False)
- 메서드가 아니라 속성 → **괄호 없이** `request.user.is_authenticated`

```html
<!-- articles/index.html -->
{% if request.user.is_authenticated %}
  <h3>Hello, {{ user.username }}</h3>
  <a href="{% url 'articles:create' %}">[NEW]</a>
  <form action="{% url 'accounts:logout' %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="Logout">
  </form>
  <form action="{% url 'accounts:delete' %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="회원탈퇴">
  </form>
{% else %}
  <a href="{% url 'accounts:login' %}">[Login]</a>
  <a href="{% url 'accounts:signup' %}">[Signup]</a>
{% endif %}
```

- `if ~ else`: 회원 전용 / `else ~ endif`: 비회원 전용 / `endif` 바깥: 공통
- view에서도 사용: 이미 로그인한 사용자는 login, signup 함수를 못 쓰게 처리

```python
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    ...

def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    ...
```

### ② login_required 데코레이터

- **인증된 사용자에 대해서만 view 함수를 실행**시키는 데코레이터
- 비로그인 사용자는 `/accounts/login/` 주소로 redirect (`settings.LOGIN_URL` 기본값)
  - 이때 `?next=/articles/create/`처럼 원래 가려던 주소가 붙음

```python
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    ...
```

| | is_authenticated | login_required |
|---|---|---|
| 정체 | User 객체의 **속성** | view 함수에 붙이는 **데코레이터** |
| 쓰는 곳 | 템플릿 분기, view 안 if문 | view 함수 위 |
| 비로그인 시 | 직접 분기 처리 | 로그인 페이지로 자동 redirect |

> ⚠️ `@login_required`는 "로그인했는가"만 본다. **남의 글을 수정하지 못하게 막는 것(소유권 검사)은** 별도 로직이 필요하다.
>
> ⚠️ 템플릿에서 [NEW] 버튼만 숨기면 주소창에 `/articles/create/`를 직접 쳐서 들어올 수 있다. 화면 분기(①)와 view 보호(②)를 **같이** 써야 한다.

---

## 5. 정리 — 세션 vs User 객체, 무엇을 만들고 지우나

| 기능 | 대상 | CRUD | 핵심 코드 | 사용 폼 |
|---|---|---|---|---|
| 로그인 | 세션 | Create | `auth_login(request, form.get_user())` | AuthenticationForm (Form) |
| 로그아웃 | 세션 | Delete | `auth_logout(request)` | — |
| 회원가입 | User | Create | `form.save()` | UserCreationForm (ModelForm) |
| 회원 탈퇴 | User | Delete | `request.user.delete()` | — |
| 회원정보 수정 | User | Update | `form.save()` (instance=request.user) | UserChangeForm → [10단원](10_auth_user_update_password.md) |

| | AuthenticationForm | UserCreationForm |
|---|---|---|
| 용도 | 로그인 (이미 있는 유저 확인) | 회원가입 (새 유저 생성) |
| 종류 | Form | **ModelForm** |
| 생성자 첫 인자 | `request` | `data` (`request.POST`) |
| save() | 없음 | 있음 (비밀번호 해시 저장) |
