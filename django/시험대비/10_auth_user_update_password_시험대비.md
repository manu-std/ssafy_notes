# Django 10단원 시험대비 — Authentication System 03

> 📎 개념 정리 노트: [`../10_auth_user_update_password.md`](../10_auth_user_update_password.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

학습 근거: 제공된 Django_Authentication_System_03.zip의 슬라이드 78장(p001~p078). 강의 원본 확인문제는 p067~p069(11 문제), 강의 정답·해설은 p070~p071에 있다. 이 문서의 추가 예상문제는 강의 내용에 근거해 제작한 연습문제이며 실제 출제를 보장하지 않는다.

## 0. 15분 실전 암기 루틴

1. 0~3분: UserChangeForm / PasswordChangeForm / AuthenticationForm 생성자 인자 순서 암기.
2. 3~6분: form.is_valid() → form.save() → update_session_auth_hash(request, form.user) → redirect 흐름 손으로 쓰기.
3. 6~10분: 해싱·암호화·솔트·키 스트레칭·레인보우 테이블·무차별 대입 공격 구분.
4. 10~12분: 기본 비밀번호 저장 형태 algorithm$iterations$salt$hash와 PBKDF2 복습.
5. 12~15분: 공식 확인문제 11개와 취약점 3개(세션 유지/Meta.fields/메일 설정) 재확인.

## 1. 슬라이드 기반 학습 지도

| 슬라이드 | 핵심 주제 | 중요도 |
| --- | --- | --- |
| p004~p005 | 비밀번호 보관에 대한 보안 문제의식, 학습 목표 | ★★ |
| p006~p016 | 회원정보 수정, UserChangeForm, CustomUserChangeForm, instance=request.user, fields | ★★★ |
| p017~p024 | 비밀번호 변경, PasswordChangeForm, 기존 비밀번호 확인, 저장 | ★★★ |
| p025~p027 | 비밀번호 변경 시 세션 무효화 방지, update_session_auth_hash() | ★★★ |
| p028~p047 | 해시의 특성, SHA-256, Rainbow Table, Salt, Brute-force, Key Stretching, PBKDF2 | ★★★ |
| p049~p059 | 이메일을 통한 비밀번호 초기화, Django 내장 auth URLs, EMAIL_BACKEND | ★★~★★★ |
| p061~p065 | PasswordChangeForm의 첫 번째 인자, built-in forms 코드 비교 | ★★★ |
| p067~p071 | 강의 원본 확인문제 11개, 공식 답과 해설 | ★★★ |
| p072~p077 | 요약·암기·복습 | ★★★ |

## 2. 회원정보 수정: UserChangeForm

### 2.1 정의와 필요성

- 회원정보 수정: 이미 존재하는 사용자 객체(User)의 정보를 갱신(UPDATE) 하는 작업.
- Django 제공 UserChangeForm은 ModelForm 계열이다. Custom User를 사용하는 프로젝트에서는 모델 및 출력 필드를 맞춘 사용자 정의 폼을 만드는 것이 편리하다.
- 내 정보를 수정할 때는 instance=request.user를 전달해야 한다. instance가 없으면 수정하려는 사용자 인스턴스가 바인딩되지 않는다.
- UserChangeForm을 기본 상태로 표시하면 일반 사용자에게 불필요하거나 민감한 필드가 노출될 수 있다. Meta.fields에 허용된 필드만 명시하는 방식이 중요하다.

```
# accounts/forms.py
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .forms import CustomUserChangeForm

@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/update.html', {'form': form})

<!-- accounts/update.html -->
<h1>회원정보 수정</h1>
<form action="{% url 'accounts:update' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">저장</button>
</form>
```

핵심 구분

- GET: 기존 사용자 정보를 채운 폼을 출력 → CustomUserChangeForm(instance=request.user).
- POST: 새 입력 데이터를 현재 사용자에 연결 → CustomUserChangeForm(request.POST, instance=request.user).
- is_valid()는 입력값 검증, save()는 검증에 성공한 내용을 사용자 객체에 저장.
- UserChangeForm은 회원정보 수정 용도이지 기존 비밀번호를 안전하게 변경하는 전용 폼이 아니다. 비밀번호 변경은 별도의 PasswordChangeForm으로 처리한다.
- 로그인이 되었다고 모든 사람의 정보를 수정할 권한이 주어지는 것은 아니다. request.user로 수정 대상을 제한하는 것이 중요하다.

출제 예상 서술형: instance=request.user가 빠지면 왜 문제인가? → 기존 객체 갱신이라는 의도가 보장되지 않고 새 모델 인스턴스를 만들거나 입력 데이터와 현재 계정이 바르게 연결되지 않을 수 있다. 따라서 회원정보 수정에서는 현재 로그인 사용자 객체를 instance로 지정한다.

## 3. 비밀번호 변경: PasswordChangeForm

### 3.1 용도와 특징

- 비밀번호 변경은 단순 텍스트 필드 갱신이 아니다. 기존 비밀번호 확인 → 새 비밀번호 검증 → 안전한 해싱 → 사용자 비밀번호 갱신이 필요하다.
- Django 내장 **PasswordChangeForm**이 이 과정을 지원한다. SetPasswordForm을 기반으로 하며 기존 비밀번호 확인을 추가한다.
- 일반적으로 세 입력값: old_password, new_password1, new_password2.
- 생성자 첫 번째 인자는 request가 아니라 User 객체다.

```
# accounts/views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

@login_required
@require_http_methods(['GET', 'POST'])
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password.html', {'form': form})

<!-- accounts/password.html -->
<h1>비밀번호 변경</h1>
<form action="{% url 'accounts:password' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">비밀번호 변경</button>
</form>
```

### 3.2 코드가 하는 일

1. request.user: 현재 로그인한 사용자 객체.
2. PasswordChangeForm(request.user, request.POST): 현재 사용자와 제출 데이터를 바인딩.
3. form.is_valid(): 기존 비밀번호가 맞는지, 새 비밀번호가 일치하는지, 지정된 검증 규칙을 충족하는지 검사.
4. form.save(): 사용자의 새 비밀번호를 적절히 해싱해서 저장하고 사용자 객체를 반환.
5. update_session_auth_hash(request, user): 변경된 비밀번호와 현재 로그인 세션의 인증 해시를 맞추어 현재 사용자의 로그인상태 유지.
6. redirect(): 변경 후 다른 페이지로 이동하는 POST/Redirect/GET 패턴.

### 3.3 변경 후 로그아웃되는 이유와 방지책

- Django는 세션에 저장된 인증 해시와 현재 사용자의 인증 해시를 비교하여 세션의 유효성을 확인한다.
- 비밀번호가 바뀌면 인증 해시가 달라져 기존 세션이 무효화될 수 있다. 별도 조치 없이 현재 세션이 다음 요청에서 로그아웃될수 있다.
- update_session_auth_hash(request, user)는 현재 세션을 새로운 비밀번호 기준으로 갱신한다. 일반적으로 보안을 위해 기존의다른 세션들은 무효화될 수 있다.
- 이는 비밀번호 변경용 기능이지 사용자 생성이나 암호화 알고리즘을 설정하는 기능이 아니다.

### 3.4 생성자 인자 비교 — 시험에 매우 중요

| 목적 | 폼 | 올바른 사용 예 | 첫 번째 인자 |
| --- | --- | --- | --- |
| 게시글 생성 | ArticleForm | ArticleForm(request.POST) | data |
| 회원정보 수정 | CustomUserChangeForm | CustomUserChangeForm(request.POST, instance=request.user) | data |
| 로그인 | AuthenticationForm | AuthenticationForm(request, request.POST) | request |
| 비밀번호 변경 | PasswordChangeForm | PasswordChangeForm(request.user, request.POST) | user |
| 비밀번호 재설정(기존 암호 없이) | SetPasswordForm | SetPasswordForm(user, data=request.POST) | user |

기억 문장: AuthenticationForm은 요청(request), PasswordChangeForm은 **사람(user)이** 먼저 온다.

## 4. 비밀번호 해싱·암호화·인코딩 비교

| 용어 | 기본 성질 | 목적/예시 | 복원 여부 |
| --- | --- | --- | --- |
| 인코딩(Encoding) | 정해진 규칙으로 표현 변환 | UTF-8, Base64(이진 데이터 텍스트화) | 규칙에 따라 복원 가능 |
| 암호화(Encryption) | 키를 사용해 내용을 보호 | AES 등 | 올바른 키로 복호화 가능 |
| 해싱(Hashing) | 임의 길이 입력 → 보통 고정 길이 해시값 | SHA-256 등 | 원칙적으로 역연산이 어렵다 |

비밀번호를 평문 그대로 저장하면 안 된다. DB가 유출되면 공격자가 바로 비밀번호를 확보할 수 있고 비밀번호를 재사용한 다른 사이트까지 위험해진다. 단순히 Base64 인코딩하는 것도 비밀번호 보호가 아니다. 복호화를 전제로 하는 일반 암호화보다는 비밀번호 전용 느린 해시·KDF를 사용한다.

### 4.1 암호학적 해시 함수 주요 성질

- 결정성: 동일 입력은 동일 해시 함수에서 동일 출력(솔트 등의 추가 입력 조건도 동일할 때).
- 일방향성(역상 저항성): 해시값으로 원래 입력을 직접 복원하기 어렵다.
- 눈사태 효과(Avalanche Effect): 입력이 조금만 달라져도 출력이 크게 변할 수 있다.
- 고정 길이: 특정 해시 함수 출력은 입력 길이와 무관하게 고정 길이.
- 충돌: 서로 다른 두 입력이 같은 해시값을 갖는 경우는 원리상 가능. 해시가 완벽하게 일대일 대응하는 것은 아니다.
- SHA-256: 출력 길이 256비트 = 32바이트 = 16진수 64자리. 강의 p037 참고.

강의 확인문제 함정: '해시값으로 원래 값을 쉽게 알아낼 수 있다'는 틀림. 하지만 흔한 비밀번호는 해시 후보를 대량 계산해 맞힐 수있으므로 해시만으로 충분한 보호가 되는 것은 아니다.

## 5. 비밀번호 공격과 방어 기술

### 5.1 레인보우 테이블 공격과 Salt

- 레인보우 테이블: 공격자가 미리 계산해 둔 비밀번호 후보와 해시값들의 대응 정보를 활용하여 훔친 해시를 빠르게 역추적하려는 기법.
- Salt: 비밀번호를 해싱할 때 사용자/비밀번호마다 추가하는 임의의 값.
- 같은 비밀번호여도 서로 다른 Salt를 사용하면 해시 결과가 달라질 수 있다.
- 따라서 미리 계산한 해시표를 재활용하는 공격의 효율이 크게 떨어진다.
- Salt는 비밀이어야 하는 값이 아니며, 일반적으로 해시값과 함께 저장된다. 비밀번호 자체를 대체하거나 별도의 암호 키로 동작하지 않는다.

### 5.2 무차별 대입 공격과 Key Stretching

- Brute-force(무차별 대입): 가능한 비밀번호 후보를 반복 시험하는 공격.
- Key Stretching(키 스트레칭): 비밀번호 처리에 의도적으로 반복·비용을 부과하여 후보 하나를 검증하는 시간/비용을 늘리는기술.
- Salt만으로 모든 무차별 대입 공격을 차단할 수는 없다. 강의에서 구분하는 대표 방어 조합은 Salt → 레인보우 테이블 효율 감 소, Key Stretching → 대량 시도 비용 증가.
- CAPTCHA·로그인 제한은 온라인 로그인 시도에 도움을 줄 수 있지만, 이미 유출된 해시를 오프라인으로 시험하는 경우의 대책과는 구별해야 한다.

### 5.3 Django 기본 비밀번호 해싱 — PBKDF2

- 강의 기준 기본 해셔: PBKDF2 + SHA-256 (pbkdf2_sha256). 실제 프로젝트의 설정에 따라 다른 해셔를 선택할 수도 있다.
- PBKDF2는 Salt를 이용하며 해시 연산을 여러 번 반복해 공격 비용을 늘린다.
- Django DB의 패스워드 필드 예시는 대체로 아래와 같은 형태이다.

```
pbkdf2_sha256$iterations$salt$hash
```

- 저장되는 값의 구성 요소: algorithm(알고리즘), iterations(반복 횟수), salt(솔트), hash(파생 해시값).
- username은 이 패스워드 필드의 구성 요소가 아니다. 사용자 식별값은 다른 필드에 존재한다.
- 강의에서 설명하는 보안 기술과 다른 개념인 AUTH_PASSWORD_VALIDATORS는 비밀번호의 품질·형식 검증에 관한 설정이며, 이메일발송이나 세션 유지 설정이 아니다.

## 6. 이메일을 이용한 비밀번호 초기화(Reset)

### 6.1 변경(Change)과 초기화(Reset)의 차이

| 구분 | 비밀번호 변경 | 비밀번호 초기화 |
| --- | --- | --- |
| 상황 | 기존 비밀번호를 알고, 인증된 계정 사용 | 기존 비밀번호를 잊어버림 |
| 핵심 폼 | PasswordChangeForm | 내장 재설정 폼/뷰와 이메일 확인 흐름 |
| 기존 비밀번호 확인 | 일반적으로 필요 | 이메일의 재설정 링크·토큰 등을 통해 소유 확인 |
| 세션 유지 | update_session_auth_hash()로 현재 세션 유지 | 보통 재설정 후 다시 로그인 |

### 6.2 내장 auth URL 연결

```
# project/urls.py - 강의 실습 취지
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

- django.contrib.auth.urls를 include하면 비밀번호 초기화 등에 필요한 Django 내장 URL 패턴을 활용할 수 있다.
- 강의에서는 accounts/ 아래에서 password_reset/ 경로를 확인한다.
- 중요: 경로는 실제 include() 접두부에 따라 바뀌므로 /accounts/password_reset/이라는 절대 주소가 항상 고정인 것은 아니다.
- 템플릿 구성·이메일 설정은 서비스 구현 시 추가로 필요한 부분이 있다. 내장 URL을 연결하는 것만으로 실제 발송이 완성되는것은 아니다.
- Django는 등록되지 않은 이메일 주소에 대해서도 계정 존재 여부가 노출되지 않도록 처리하는 방식을 사용한다. 메일 발송·템플릿·설정이 올바른지 확인해야 한다.

### 6.3 이메일 백엔드

```
# settings.py - 학습·개발 환경 예
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

- 이 설정은 실제 메일을 보내기보다 개발 서버 콘솔에 이메일 내용을 출력한다.
- 테스트용 console.EmailBackend를 운영에서 실제 발송 설정으로 착각하면 안 된다.
- 운영에서는 SMTP 또는 이메일 전송 서비스 등 적절한 백엔드 설정이 필요하다.
- 흐름: 이메일 입력 → 계정이 있으면 재설정 링크가 포함된 메일 생성 → 사용자가 유효한 링크에 접속 → 새 비밀번호 설정 → 완료 후 로그인.

## 7. 8~10단원 한꺼번에 연결하기

1. 8단원: 커스텀 사용자 모델 (AUTH_USER_MODEL)을 준비 → 로그인 폼(AuthenticationForm) → auth_login(request, form.get_user())로 세션 연결.
2. 9단원: 가입(UserCreationForm / form.save()) → 필요 시 자동 로그인 → 로그아웃(auth_logout) → 회원탈퇴 (request.user.delete()) → 접근 제한.
3. 10단원: 정보 수정(UserChangeForm, instance) → 비밀번호 변경(PasswordChangeForm) → 현재 세션 유지 (update_session_auth_hash) → 분실 시 이메일 초기화 → 비밀번호 보호(Salt/PBKDF2/반복 연산).

## 8. 강의 원본 확인문제 11개 — 공식 답과 해설 (p067~p071)

원문의 선택지를 학습용으로 간결하게 정리했다. 정답은 강의 공식 답안과 대조했다.

| 번호 | 확인문제 핵심 질문 | 공식 답 | 해설 |
| --- | --- | --- | --- |
| 1 | 회원정보 수정에 사용하는 Django 내장 폼은? | c. UserChangeForm | User 정보를 갱신하는 ModelForm 계열 |
| 2 | UserChangeForm에서 출력할 필드만 지정하려면? | b. Meta.fields | 필요한 이름만 명시하여 출력·수정 범위를 제어 |
| 3 | 현재 비밀번호 확인을 포함한 비밀번호 변경 폼은? | b. PasswordChangeForm | 기존 비밀번호 검증 + 새 비밀번호 변경 |
| 4 | 변경 후 현재 세션 로그아웃을 방지하려면? | c. update_session_auth_hash(request, user) | 현재 세션의 인증 해시를 업데이트 |
| 5 | 복원이 어려운 고정 길이 문자열 변환은? | c. Hashing | 암호화·인코딩과 구분 |
| 6 | 해시 함수의 특징이 아닌 것은? | b. 해시값으로 원래 입력값을 쉽게 알 수 있다 | 일반적으로 역상 계산은 어렵다 |
| 7 | 레인보우 테이블 공격 방어에 중요한 기술은? | b. Salt 사용 | 사용자별 임의값으로 사전 계산 공격 억제 |
| 8 | 무차별 대입 공격 효율을 낮추는 기술은? | b. Key Stretching | 후보당 검증 연산 비용 증가 |
| 9 | 강의 기준 Django 기본 비밀번호 해시 알고리즘은? | c. PBKDF2 | 보통 PBKDF2-SHA256을 사용 |
| 10 | algorithm$iterations$salt$hash에 포함되지 않는 것은? | d. username | 사용자 식별명은 해시 문자열 구성요소가 아님 |
| 11 | 비밀번호 초기화 메일 출력을 위해 설정한 항목은? | b. EMAIL_BACKEND | 강의는 콘솔 백엔드로 발송 내용을 확인 |

공식 정답만 빠르게 암기: 1 C / 2 B / 3 B / 4 C / 5 C / 6 B / 7 B / 8 B / 9 C / 10 D / 11 B.

## 9. 추가 예상 객관식 15문제

Q1. 기존 사용자 이름·이메일 등을 수정할 때 적절한 폼은? A. AuthenticationForm B. UserChangeForm C. UserCreationForm D. PasswordResetForm

Q2. 회원정보 수정 POST에서 가장 적절한 폼 생성은? A. CustomUserChangeForm() B. CustomUserChangeForm(request.POST) C. CustomUserChangeForm(request.POST, instance=request.user) D. CustomUserChangeForm(request.user, request.POST)

Q3. 커스텀 폼에서 화면에 보여줄 사용자 필드를 안전하게 제한하는 위치는? A. Meta.fields B. Meta.template_name C. settings.MEDIA_URL D. AUTH_PASSWORD_VALIDATORS

Q4. 비밀번호 변경 폼의 첫 번째 위치 인자로 올바른 것은? A. request.POST B. request.user C. request D. request.FILES

Q5. 비밀번호 변경 후 현재 세션을 유지하기 위한 함수는? A. authenticate() B. get_user_model() C. update_session_auth_hash() D. set_password()

Q6. PasswordChangeForm(request.user, request.POST)에 대해 옳은 설명은? A. 저장하려면 기존 비밀번호가 필요하지 않다. B. is_valid()만으로 DB 저장이 끝난다. C. 생성자 첫 인자는 사용자 객체다. D. Form이 아닌 ModelForm의 일종이다.

Q7. 암호화와 해싱의 차이에 대한 올바른 설명은? A. 둘 다 키로 복호화할 수 있다. B. 해싱은 암호화보다 항상 안전하다. C. 암호화는 적절한 키로 복호화하지만 해싱은 일반적으로 원문 복원이 어렵다. D. 해싱은 항상 입력 길이와 같은 출력이 나온다.

Q8. 같은 비밀번호를 쓰는 두 사용자의 저장된 해시가 서로 다를 수 있는 대표 이유는? A. 각자 다른 Salt B. render() 호출 C. MEDIA_ROOT 차이 D. HTML 인코딩

Q9. 레인보우 테이블 공격에 직접 대응하는 주된 기법은? A. 쿠키 만료 B. Salt C. ForeignKey D. CSRF Token

Q10. Key Stretching의 핵심 목적은? A. 해시를 복호화 가능하게 만든다. B. 저장 공간을 줄인다. C. 비밀번호 한 개를 추측해 확인하는 계산 비용을 늘린다. D. 로그인 없이 접근하게 한다.

Q11. pbkdf2_sha256$...$...$... 값에서 pbkdf2_sha256이 나타내는 것은? A. Username B. Hash algorithm C. Email backend D. Session ID

Q12. 비밀번호 해시 문자열의 대표 구성요소가 아닌 것은? A. Salt B. Iterations C. Algorithm D. Username

Q13. Django 내장 비밀번호 초기화 경로를 포함시키는 방법은? A. include('django.contrib.auth.urls') B. models.Model() C. form.save(commit=False) D. collectstatic

Q14. EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'는 무엇을 하는가? A. 이메일을 실제 수신자에게 보냈음을보장한다. B. 파일 업로드 URL을 만든다. C. 이메일 내용을 개발 콘솔에 출력한다. D. 사용자를 로그인시킨다.

Q15. 다음 중 올바른 설명은? A. 회원정보 수정과 비밀번호 변경에 같은 기본 Form이 반드시 쓰인다. B. update_session_auth_hash()는 모든 브라우저의 세션을 일괄 유지한다. C. UserChangeForm은 비밀번호 변경 전용 폼이다. D. 회원정보 수정은 instance, 비밀번호 변경은 PasswordChangeForm과 현재 사용자 정보를 고려한다.

### 객관식 정답·해설

| 번호 | 답 | 핵심 해설 |
| --- | --- | --- |
| 1 | B | UserChangeForm은 기존 User 정보 수정을 지원 |
| 2 | C | request.POST + instance=request.user 둘 다 필요 |
| 3 | A | Meta.fields를 제한해 수정 허용 범위를 지정 |
| 4 | B | 첫 인자는 user |
| 5 | C | 현재 세션의 인증 해시를 갱신 |
| 6 | C | PasswordChangeForm은 user를 첫 번째 인자로 받는 Form 계열 |
| 7 | C | 일반 암호화는 키로 복호화 가능; 비밀번호 해싱은 원문 복원 어려움 |
| 8 | A | 서로 다른 Salt가 서로 다른 저장 해시를 만들 수 있음 |
| 9 | B | 사전 계산 해시표 활용을 어렵게 함 |
| 10 | C | 한 번의 확인 작업을 느리게 함 |
| 11 | B | 비밀번호 해싱 알고리즘 이름 |
| 12 | D | username은 별도의 사용자 필드 |
| 13 | A | Django 내장 auth URL 패턴 사용 |
| 14 | C | 테스트 환경에서 콘솔 출력 |
| 15 | D | 9·10단원 Form 역할 비교 |

## 10. 추가 예상 주관식 10문제

S1. 회원정보 수정에 사용하는 Django 기본 내장 폼 이름을 쓰시오.

S2. 회원정보 수정을 위한 CustomUserChangeForm의 POST 생성 코드를 한 줄로 쓰시오. (현재 로그인 사용자를 수정)

S3. 사용자 수정 폼에서 출력 가능한 필드를 제한할 때 Meta 내부에 사용하는 속성 이름은?

S4. 비밀번호 변경에 사용하며 기존 비밀번호를 확인하는 Django 기본 폼 이름은?

S5. PasswordChangeForm 생성자의 첫 번째 위치 인자에 들어가야 할 값은?

S6. 비밀번호 변경 후 현재 세션의 로그아웃을 방지하는 Django 함수의 이름은?

S7. 해시의 역연산이 어려운 성질을 무엇이라고 하는가? (한국어 또는 영어)

S8. 같은 비밀번호라도 사용자별 다른 해시값을 만들고 레인보우 테이블 공격을 약화시키는 임의값은?

S9. 비밀번호에 반복 연산을 가해 대량 추측 속도를 낮추는 방어 기법은?

S10. 학습용 콘솔 이메일 출력 백엔드를 지정하는 Django 설정 항목은?

### 주관식 정답

1. UserChangeForm
2. CustomUserChangeForm(request.POST, instance=request.user)
3. fields (Meta.fields)
4. PasswordChangeForm
5. request.user (현재 사용자 객체)
6. update_session_auth_hash
7. 일방향성 / 역상 저항성(Preimage resistance)
8. Salt (솔트)
9. Key Stretching (키 스트레칭)
10. EMAIL_BACKEND

## 11. 추가 예상 서술형 5문제와 만점 답안

### E1. 회원정보 수정 요청의 GET·POST 처리 흐름을 설명하시오.

모범답안: 로그인한 사용자에 대해 GET 요청에서는 CustomUserChangeForm(instance=request.user)로 현재 값을 채운 폼을 만들고화면에 렌더링한다. POST 요청에서는 CustomUserChangeForm(request.POST, instance=request.user)로 제출 데이터를 기존 사용자에 바인딩한다. form.is_valid()가 참이면 form.save()로 DB의 사용자 정보를 갱신하고 redirect()로 이동한다. 검증 실패 시 오류가 있는 폼을 다시 보여준다.

채점 키워드: GET/POST 구분, request.POST, instance=request.user, is_valid, save, redirect.

### E2. 비밀번호 변경 후 로그아웃되는 이유와 이를 방지하는 방법을 설명하시오.

모범답안: Django는 세션의 인증 해시를 현재 사용자 인증 해시와 비교한다. 사용자의 비밀번호가 바뀌면 인증 해시가 달라져 기존세션이 무효화될 수 있다. 비밀번호를 저장한 다음 update_session_auth_hash(request, user)를 호출하여 현재 로그인 세션의 인증해시를 갱신하면 해당 사용자가 로그아웃되는 현상을 방지한다.

채점 키워드: 비밀번호 변경, 세션 인증 해시 불일치, 세션 무효화, update_session_auth_hash, 현재 세션 유지.

### E3. 해싱과 암호화의 차이, 비밀번호 보관에 적절한 방식을 설명하시오.

모범답안: 암호화는 올바른 키로 복호화하는 것을 전제로 하는 데이터 보호 방식인 반면, 해싱은 보통 고정 길이 출력으로 변환하고원문을 되돌리는 역연산이 어렵다. 비밀번호는 원문이나 단순 인코딩으로 저장하면 유출 시 위험하므로, Salt와 반복 연산을 사용하는 PBKDF2 같은 비밀번호 전용 해싱 방식으로 저장하는 것이 적절하다.

채점 키워드: 암호화 복호화 가능, 해싱 단방향성, 평문 저장 금지, Salt, PBKDF2.

### E4. 레인보우 테이블 공격과 무차별 대입 공격을 구분하고 대응 기술을 설명하시오.

모범답안: 레인보우 테이블 공격은 미리 계산해 둔 비밀번호 후보와 해시 결과를 활용해 유출된 해시의 원문 후보를 알아내려는 방식이다. Salt는 사용자별 다른 해시값을 유도하여 이런 사전 계산표의 재사용을 어렵게 한다. 무차별 대입 공격은 가능한 비밀번호후보를 반복 시험하는 공격이다. Key Stretching은 후보당 검증 연산 비용을 증가시켜 대량 공격을 느리게 만든다. 두 기법은 함께사용하면 더 효과적이다.

채점 키워드: Rainbow Table / 사전 계산, Salt, Brute-force / 대량 추측, Key Stretching / 반복 비용 증가.

### E5. 비밀번호 초기화 기능을 구현하는 주요 Django 요소와 흐름을 설명하시오.

모범답안: 비밀번호를 분실한 사용자를 위해 Django 내장 비밀번호 초기화 URL을 include('django.contrib.auth.urls')로 연결할수 있다. 사용자가 이메일을 입력하면 등록된 사용자에 대해서 재설정 링크·토큰을 포함한 이메일을 생성하고, 사용자는 해당 링크에서 새 비밀번호를 설정한다. 이 과정에서 메일 전송 기능은 EMAIL_BACKEND로 지정한다. 개발 환경에서는 콘솔 이메일 백엔드를 사용해 전송 내용을 확인할 수 있으며, 운영 환경에서는 실제 이메일 발송 백엔드가 필요하다.

채점 키워드: 내장 auth.urls, 이메일 확인, 토큰/재설정 링크, 새 비밀번호 설정, EMAIL_BACKEND, 콘솔 백엔드 vs 실발송.

## 12. 추가 코드 오류·실행 흐름 문제 8개

### C1. 잘못된 폼 생성자 수정

```
form = PasswordChangeForm(request.POST, request.user)
```

정답:

```
form = PasswordChangeForm(request.user, request.POST)
```

해설: 첫 번째 위치 인자가 User 객체다.

### C2. 누락된 회원 수정 대상

```
form = CustomUserChangeForm(request.POST)
```

정답:

```
form = CustomUserChangeForm(request.POST, instance=request.user)
```

해설: 현재 사용자를 갱신하는 작업이므로 기존 객체를 바인딩해야 한다.

### C3. 비밀번호 변경 후 리다이렉트 전에 필요한 한 줄

```
if form.is_valid():
    user = form.save()
    # ______
    return redirect('articles:index')
```

정답: update_session_auth_hash(request, user). 해설: 현재 인증 세션을 갱신한다.

### C4. 회원정보 수정 시 필요한 등록 모델 지정

```
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ______
        fields = ('first_name', 'last_name', 'email')
```

정답: get_user_model(). 해설: 프로젝트에 설정된 커스텀 User 모델을 사용한다.

### C5. 변경 Form에서 GET과 POST 구분

```
if request.method == 'POST':
    form = PasswordChangeForm(_____, _____)
else:
    form = PasswordChangeForm(_____)
```

정답: 각각 request.user, request.POST, request.user. 해설: 비밀번호 변경 Form은 사용자를 먼저 받고, POST에서 데이터를 추가로 받는다.

### C6. 비밀번호 저장 형태 분석

```
pbkdf2_sha256$870000$s0m3S4lt$randomDerivedHash
```

문제: 네 부분이 나타내는 것은?

정답: algorithm / iterations / salt / hash. 숫자는 학습 예시일 뿐 버전별 기본 반복 횟수와 동일하다는 뜻이 아니다.

### C7. 내장 비밀번호 초기화 URL

```
path('accounts/', include('django.contrib.auth.urls'))
```

문제: 강의에서 확인한 초기화 시작 URL은?

정답: /accounts/password_reset/. 해설: accounts/는 접두부, Django 내장 패턴의 password_reset/이 결합된다.

### C8. 이메일 미발송 문제

```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

문제: 왜 실제 이메일 수신함에 메일이 안 보이는가?

정답: 개발용 콘솔 백엔드이므로 이메일이 개발 서버 터미널/콘솔에 출력되며 실제 발송하지 않는다.

## 13. 만점 방해하는 함정 12개

1. UserChangeForm과 UserCreationForm 혼동: 수정 vs 생성.
2. AuthenticationForm(request, data)와 PasswordChangeForm(user, data)의 첫 인자 혼동.
3. form.is_valid()만 실행하면 DB가 변경된다는 오해 → 검증과 저장은 별개.
4. instance=request.user 없이 현재 사용자 변경이라고 생각하는 오류.
5. 비밀번호 변경 후 update_session_auth_hash()를 빠뜨림 → 현재 로그인 세션 무효화 위험.
6. update_session_auth_hash()가 모든 다른 기기의 로그인도 유지한다고 생각하는 오류.
7. 일반 암호화와 해시를 같은 의미로 사용하는 오류.
8. 해시가 원리상 충돌이 절대 없다고 생각하는 오류.
9. Salt를 비밀 키 또는 해시 알고리즘이라고 오해.
10. Key Stretching과 Salt의 목적을 뒤바꿈.
11. 비밀번호 해시 문자열의 구성에 username이 들어간다고 오해.
12. 개발용 console.EmailBackend가 실제 메일을 발송한다고 오해.

## 14. 시험 직전 90초 암기 카드

```
회원정보 수정 = UserChangeForm → fields 한정 → POST + instance=request.user → is_valid() → save()
비밀번호 변경 = PasswordChangeForm(request.user, request.POST)
비밀번호 변경 후 로그인 유지 = update_session_auth_hash(request, user)
회원가입 = UserCreationForm / CustomUserCreationForm
로그인 = AuthenticationForm(request, request.POST) → auth_login(request, form.get_user())
로그아웃 = auth_logout(request)
Hash = 일방향, 고정 길이 출력, SHA-256은 256비트
Rainbow Table 방어 = Salt
Brute-force 효율 감소 = Key Stretching
Django 기본(강의) = PBKDF2-SHA256
저장 형태 = algorithm$iterations$salt$hash
비밀번호 분실 = include('django.contrib.auth.urls') + EMAIL_BACKEND
개발용 메일 = console.EmailBackend (실제 발송 X)
```

## 15. 최종 자가 점검

- CustomUserChangeForm 생성/수정 View를 손으로 쓸 수 있다.
- PasswordChangeForm의 첫 인자가 user인 이유를 말할 수 있다.
- update_session_auth_hash가 필요한 원리를 서술할 수 있다.
- 해싱·암호화·인코딩의 차이 설명 가능.
- Salt와 Key Stretching이 막는 공격/목적을 각각 구분한다.
- pbkdf2_sha256$iterations$salt$hash 네 부분을 순서대로 외웠다.
- 강의 확인문제 11개를 모두 풀 수 있다.
- 이메일 백엔드의 개발용 동작을 구분할 수 있다.

완료: 10/10단원. 본 파일은 마지막 10단원 단독 학습자료이며, 별도 문서인 Django_10단원_통합_실전모의고사.md에서 전 단원 60분모의고사를 제공한다.
