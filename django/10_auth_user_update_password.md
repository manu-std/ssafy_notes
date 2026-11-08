# Django 10 — Authentication System 03: 회원정보 수정, 비밀번호 변경, 비밀번호 보안

> 📎 확인문제·예상문제·암기카드: [`시험대비/10_auth_user_update_password_시험대비.md`](시험대비/10_auth_user_update_password_시험대비.md)

*(인증 3부작의 마지막. 남은 User Update(회원정보 수정)와 비밀번호 변경을 만들고, Django가 비밀번호를 어떻게 안전하게 보관하는지(해시·솔트·키 스트레칭·PBKDF2)와 이메일 비밀번호 초기화까지. [08](08_auth_cookie_session_login.md)·[09](09_auth_logout_signup_access.md)와 이어진다.)*

## 오늘의 목차

1. 회원정보 수정 (UserChangeForm)
2. 비밀번호 변경 (PasswordChangeForm)
3. 인증 관련 Form 생성자 인자 총정리
4. 비밀번호 저장 — 인코딩·암호화·해싱
5. 비밀번호 공격과 방어 (Salt, Key Stretching, PBKDF2)
6. 이메일로 비밀번호 초기화 (Reset)
7. 8~10단원 연결 정리

---

## 1. 회원정보 수정

- 회원정보 수정 = **User 객체를 Update** 하는 과정

```python
# accounts/urls.py
app_name = 'accounts'
urlpatterns = [
    ...
    path('update/', views.update, name='update'),
]
```

### UserChangeForm

- 회원정보 수정 시 사용자 입력 데이터를 받는 **built-in ModelForm**
- 유효성 검사를 통과한 데이터로 기존 User 객체를 갱신·저장
- `Meta.model = User`가 기본 `auth.User`로 고정 → 회원가입 때와 똑같이 **상속 후 일부분만 재작성**

```python
# accounts/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email',)
```

- `get_user_model()`: `AUTH_USER_MODEL`에 등록된 **현재 프로젝트가 실제로 쓰는 유저 모델** 반환 (`accounts.User`)
  - `from .models import User`로 직접 import하지 않는 이유: 유저 모델이 바뀌어도 코드를 고치지 않기 위함 (공식 문서 권장)
- `class Meta(UserChangeForm.Meta):` → 부모의 fields, field_classes 등은 그대로 물려받고 model만 변경 (`class Meta:`로만 쓰면 부모 설정이 사라짐)

> ⚠️ **`fields`를 꼭 제한할 것.** UserChangeForm을 기본 그대로 쓰면 `is_superuser`, `is_staff`, `groups`, `user_permissions` 같은 **관리자용 필드까지** 일반 사용자 화면에 나온다. 사용자가 고쳐도 되는 필드만 `Meta.fields`에 명시한다 (6단원 `fields='__all__'` 주의와 같은 맥락).

### view 함수

```python
# accounts/views.py
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)
```

- `request.user`: 로그인한 사용자 객체. `AuthenticationMiddleware`가 요청마다 넣어 줌
- `instance=request.user`를 넣는 이유
  - GET: 폼에 **기존 정보가 미리 채워짐**
  - POST: `save()` 시 새 객체 생성(INSERT)이 아니라 **기존 객체 수정(UPDATE)**
- **생성과 수정의 차이 = instance 유무** (게시글 수정 `ArticleForm(request.POST, instance=article)`과 같은 원리)
- `User.objects.get(pk=request.user.pk)`처럼 다시 조회할 필요 없음 → 이미 들고 있는 객체를 다시 찾는 것, URL에 pk도 없음
- 수정 대상을 `request.user`로 고정하므로 **남의 정보는 수정할 수 없다** (로그인했다고 모든 계정을 수정할 권한이 생기는 게 아님)
- 회원정보 수정은 서버 상태를 바꾸는 요청 → form은 POST

```html
<!-- accounts/update.html -->
<h1>회원정보 수정</h1>
<form action="{% url 'accounts:update' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```

> ⚠️ UserChangeForm은 회원정보 수정용이다. 비밀번호는 여기서 바꾸는 게 아니라 **PasswordChangeForm**으로 따로 처리한다.

---

## 2. 비밀번호 변경

- (강의 기준) 수정 페이지의 비밀번호 영역에 있는 `Set password` 링크는 상대 경로 `../password/` → **`/accounts/password/`**
  - 현재 `/accounts/update/` → `../`로 한 단계 위 `/accounts/` → `password/`
  - 그래서 비밀번호 변경 URL을 `password/`로 맞춰 둔다

```python
# accounts/urls.py
path('password/', views.change_password, name='change_password'),
```

```python
# accounts/views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)
```

> 📌 view·URL 이름은 자유다. 학습자료에서는 `password` / `accounts:password`로 쓰기도 한다. 중요한 건 **URL 경로가 `password/`라는** 점.

### PasswordChangeForm

- 비밀번호 변경용 built-in **Form** (`SetPasswordForm` 상속 + 기존 비밀번호 확인 추가)
- 입력 필드 3개: `old_password`, `new_password1`, `new_password2`
- **첫 번째 인자가 user**: 생성자가 `__init__(self, user, *args, **kwargs)`
  - 헷갈리면 `PasswordChangeForm(user=request.user, data=request.POST)`
  - user가 필요한 이유: 기존 비밀번호 확인(`check_password`) 대상, 새 비밀번호 저장(`set_password`) 대상
- `@login_required` 필수: 비로그인 상태면 `request.user`가 AnonymousUser라 바꿀 비밀번호가 없음

### 코드가 하는 일 (순서)

1. `PasswordChangeForm(request.user, request.POST)`: 현재 사용자 + 제출 데이터 바인딩
2. `form.is_valid()`: 기존 비밀번호가 맞는지, 새 비밀번호 두 개가 일치하는지, 비밀번호 규칙을 충족하는지 검사
3. `form.save()`: 새 비밀번호를 **해싱해서** 저장하고 user 객체 반환
4. `update_session_auth_hash(request, user)`: 현재 세션을 새 비밀번호에 맞게 갱신 → 로그인 유지
5. `redirect()`: PRG 패턴

### update_session_auth_hash(request, user)

- 문제: 비밀번호가 바뀌면 **로그인이 풀린다**
  - Django는 세션에 **비밀번호 기반 인증 해시**를 함께 저장해 두고, 요청마다 현재 사용자의 해시와 비교해 세션이 유효한지 확인
  - 비밀번호가 바뀌면 해시가 달라져 → 기존 세션이 무효 처리됨
- 해결: 이 함수가 **새 비밀번호 기준으로 현재 세션의 해시를 갱신** → 로그인 상태 유지
- 다른 기기의 기존 세션들은 그대로 무효화된다 (보안상 의도된 동작)

> ⚠️ 이 함수는 "비밀번호 변경 후 세션 유지"용이다. 사용자 생성이나 해시 알고리즘 설정과는 무관.

---

## 3. 인증 관련 Form 생성자 인자 총정리

| 목적 | 폼 | 종류 | 올바른 사용 | 첫 번째 인자 |
|---|---|---|---|---|
| 게시글 생성 | ArticleForm | ModelForm | `ArticleForm(request.POST)` | data |
| 로그인 | AuthenticationForm | Form | `AuthenticationForm(request, request.POST)` | **request** |
| 회원가입 | (Custom)UserCreationForm | ModelForm | `CustomUserCreationForm(request.POST)` | data |
| 회원정보 수정 | (Custom)UserChangeForm | ModelForm | `CustomUserChangeForm(request.POST, instance=request.user)` | data |
| 비밀번호 변경 | PasswordChangeForm | Form | `PasswordChangeForm(request.user, request.POST)` | **user** |

> 💡 기억 문장: **AuthenticationForm은 요청(request)이, PasswordChangeForm은 사람(user)이 먼저 온다.** 나머지 ModelForm들은 전부 data가 먼저.

---

## 4. 비밀번호 저장 — 인코딩·암호화·해싱

| 방식 | 하는 일 | 예 | 원래대로 되돌리기 |
|---|---|---|---|
| **인코딩 (Encoding)** | 정해진 규칙으로 **표현 형식만** 변환 | UTF-8, Base64 | 규칙만 알면 누구나 복원 |
| **암호화 (Encryption)** | **키**를 사용해 내용을 보호 | AES | 올바른 키가 있으면 복호화 가능 |
| **해싱 (Hashing)** | 임의 길이 입력 → **고정 길이** 해시값 | SHA-256 | 원칙적으로 **역연산이 어렵다** |

- 비밀번호를 **평문**으로 저장하면 DB가 유출되는 순간 그대로 털림 + 같은 비밀번호를 쓰는 다른 사이트까지 위험
- Base64 인코딩은 보호가 아님 (누구나 디코딩)
- 그래서 비밀번호는 **해싱**한다 — 서버도 원래 비밀번호를 몰라도 되고, 로그인 때는 입력값을 똑같이 해싱해서 **해시끼리 비교**하면 된다

### 암호학적 해시 함수의 성질

| 성질 | 의미 |
|---|---|
| **결정성** | 같은 입력 → 항상 같은 출력 |
| **일방향성** (역상 저항성) | 해시값으로 원래 입력을 알아내기 어렵다 |
| **눈사태 효과** (Avalanche) | 입력이 조금만 달라져도 출력이 완전히 달라짐 |
| **고정 길이** | 입력 길이와 상관없이 출력 길이가 같음 |
| 충돌 가능성 | 다른 입력이 같은 해시가 될 수는 있음 (완벽한 1:1이 아님) — 다만 찾기 매우 어려움 |

- SHA-256: 출력 **256비트** = 32바이트 = 16진수 **64자리**

> ⚠️ 확인문제 함정: "해시값으로 원래 입력값을 쉽게 알 수 있다" → **틀림**. 다만 `1234`처럼 흔한 비밀번호는 후보를 미리 잔뜩 해싱해 두면 맞춰볼 수 있다 → 그래서 해시만으로는 부족하고 아래 5장의 방어 기술이 필요하다.

---

## 5. 비밀번호 공격과 방어

### 레인보우 테이블 공격 ↔ Salt

- **레인보우 테이블**: 자주 쓰는 비밀번호 후보와 그 해시값을 **미리 계산해 둔 표**. 유출된 해시를 표에서 찾아 바로 원래 비밀번호를 알아냄
- **Salt(솔트)**: 해싱할 때 비밀번호에 덧붙이는 **사용자마다 다른 임의의 값**
  - 같은 비밀번호라도 솔트가 다르면 해시 결과가 달라짐
  - 공격자의 미리 계산해 둔 표가 **쓸모없어짐** (솔트마다 표를 새로 만들어야 하므로)
- 솔트는 비밀 값이 아니다 → 보통 해시값과 **함께 저장**된다

### 무차별 대입 공격 ↔ Key Stretching

- **무차별 대입 (Brute-force)**: 가능한 비밀번호 후보를 **하나씩 전부** 대입해 보는 공격
- **키 스트레칭 (Key Stretching)**: 해시 연산을 **일부러 수천~수십만 번 반복**해서, 후보 하나를 검사하는 데 드는 시간·비용을 크게 늘림
  - 정상 사용자는 로그인 1번에 아주 잠깐 느려질 뿐이지만, 수십억 개를 시험해야 하는 공격자에겐 치명적

| 공격 | 방어 | 원리 |
|---|---|---|
| 레인보우 테이블 | **Salt** | 미리 계산한 표를 무력화 |
| 무차별 대입 | **Key Stretching** | 후보 1개당 검사 비용 증가 |

> 📌 솔트만으로 무차별 대입을 막을 수는 없다 — 둘은 막는 대상이 다르다. 로그인 시도 횟수 제한·CAPTCHA는 *온라인* 시도엔 도움이 되지만, 이미 유출된 해시를 *오프라인*으로 돌리는 공격엔 소용없다.

### Django 기본 비밀번호 해싱 — PBKDF2

- Django 기본 해셔: **PBKDF2 + SHA-256** (`pbkdf2_sha256`)
- 솔트 사용 + 해시를 매우 많이 반복(키 스트레칭) → 위 두 방어를 모두 적용
- DB에 저장된 password 필드 형태:

```text
pbkdf2_sha256$<iterations>$<salt>$<hash>
  알고리즘    $  반복 횟수  $ 솔트  $ 해시값
```

- 구성 요소 4개: **algorithm, iterations, salt, hash** → **username은 포함되지 않음** (확인문제 단골)
- 반복 횟수는 Django 버전이 올라갈 때마다 늘려 왔다 (컴퓨터가 빨라지는 만큼 비용을 올리는 것)

> 📌 `AUTH_PASSWORD_VALIDATORS`는 "너무 짧다/너무 흔하다" 같은 비밀번호 **품질 검사** 설정이다. 해싱 방식이나 이메일 설정과는 무관.

---

## 6. 이메일로 비밀번호 초기화 (Reset)

### 변경(Change) vs 초기화(Reset)

| 구분 | 비밀번호 변경 | 비밀번호 초기화 |
|---|---|---|
| 상황 | 기존 비밀번호를 **알고**, 로그인한 상태 | 기존 비밀번호를 **잊어버림** |
| 본인 확인 | 기존 비밀번호 입력 | 이메일로 받은 **재설정 링크(토큰)** |
| 핵심 | `PasswordChangeForm` | Django 내장 재설정 뷰/폼 + 이메일 |
| 세션 | `update_session_auth_hash()`로 유지 | 보통 재설정 후 다시 로그인 |

### 내장 auth URL 연결

```python
# 프로젝트 urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

- `django.contrib.auth.urls`를 include하면 `password_reset/` 등 **비밀번호 초기화에 필요한 URL과 뷰를 통째로** 쓸 수 있다
- 강의에서는 `/accounts/password_reset/`에서 확인 (앞의 `accounts/`는 include 접두사에 따라 달라짐)
- 등록되지 않은 이메일을 넣어도 "메일을 보냈다"고 똑같이 응답 → **계정 존재 여부를 노출하지 않음**

### 이메일 백엔드 (개발용)

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

- 실제 메일을 보내지 않고 **runserver 터미널(콘솔)에 메일 내용을 출력** → 재설정 링크를 콘솔에서 복사해 확인
- 운영에서는 SMTP 등 실제 발송 백엔드를 설정해야 한다

```text
이메일 입력 → (계정이 있으면) 재설정 링크가 담긴 메일 생성 → 링크 접속 → 새 비밀번호 설정 → 완료 → 다시 로그인
```

---

## 7. 8~10단원 연결 정리

1. **08단원**: Custom User(`AUTH_USER_MODEL`) 준비 → 로그인(`AuthenticationForm` → `auth_login(request, form.get_user())`) = 세션 Create
2. **09단원**: 로그아웃(`auth_logout`) = 세션 Delete / 회원가입(`UserCreationForm` → `form.save()`) = User Create / 탈퇴(`request.user.delete()`) = User Delete / 접근 제한(`is_authenticated`, `@login_required`)
3. **10단원**: 회원정보 수정(`UserChangeForm` + `instance=request.user`) = User Update / 비밀번호 변경(`PasswordChangeForm` + `update_session_auth_hash`) / 비밀번호 보관(Salt + Key Stretching = PBKDF2) / 분실 시 이메일 초기화
