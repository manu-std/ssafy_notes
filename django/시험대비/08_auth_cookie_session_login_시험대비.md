# Django 8단원 시험대비 — Authentication System 01

> 📎 개념 정리 노트: [`../08_auth_cookie_session_login.md`](../08_auth_cookie_session_login.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

출처: 사용자가 제공한 Django_Authentication_System_01.zip, 총 87개 슬라이드 이미지. 강의 확인문제: 76~79쪽(12문제). 8단원범위에 로그아웃·회원가입·회원정보수정 구현은 포함되지 않음. 아래 예상문제는 강의 기반으로 직접 제작한 연습문제이며 실제 출제는 보장되지 않습니다.

## 0. 15분 공부 전략

1. 0~3분: HTTP → Cookie → Session 개념과 흐름을 한 문장으로 설명.
2. 3~6분: AbstractUser, AUTH_USER_MODEL, 마이그레이션 시점 암기.
3. 6~10분: GET/POST에 따른 AuthenticationForm, auth_login, request.user 코드 빈칸 작성.
4. 10~13분: 강의 확인문제 12개 풀이.
5. 13~15분: 틀린 문항과 서술형 필수 키워드 복습.

## 1. 강의 목차와 출제 근거

| 슬라이드 | 내용 | 중요도 |
| --- | --- | --- |
| 7~10 | HTTP, Connectionless, Stateless | ★★★ |
| 11~23 | Cookie 정의·동작·목적 | ★★★ |
| 24~29 | Session 정의·동작·저장 구조 | ★★★ |
| 30~35 | Django 인증 시스템, 기본 User 모델 제약 | ★★★ |
| 36~44 | Custom User, AbstractUser, AUTH_USER_MODEL, DB 초기화 주의 | ★★★ |
| 45~56 | AuthenticationForm, 로그인 코드와 세션 확인 | ★★★ |
| 57~59 | 인증 사용자 템플릿 출력, Context Processors | ★★ |
| 60~74 | AbstractUser 비교, 쿠키 수명·보안, 세션 백엔드, 참고 | ★★ |
| 75 | 실습 안내 | ★ |
| 76~79 | 확인문제 12개 및 공식 정답 | ★★★ |
| 80~86 | 개념 복습 | ★★ |

## 2. 이해와 암기를 위한 핵심 개념

### 2.1 HTTP의 두 가지 특징

- Connectionless(비연결 지향): 요청·응답을 마친 후 연결을 지속하지 않을 수 있는 특성. HTTP 지속 연결(keep-alive)이 존재한다는 점과 '애플리케이션 상태가 보존되지 않는다'는 점을 구분한다.
- Stateless(무상태): 각 요청이 독립적이므로 HTTP 프로토콜 자체는 직전 요청의 로그인 여부를 기억하지 않는다.
- 이를 보완하려고 쿠키와 서버 측 세션을 조합한다.
- 시험 함정: HTTP가 사용자 정보를 자동으로 기억한다 → X.

### 2.2 Cookie

- 서버가 브라우저에 저장하도록 전달하는 작은 데이터. 응답의 Set-Cookie 헤더로 설정하고, 이후 조건이 일치하는 요청에서 브라우저가 Cookie 헤더로 전달한다.
- 용도: 세션 식별, 장바구니·개인화·추적 등의 상태 관련 기능.
- 키와 값, 만료, 도메인, 경로, 보안 속성이 있다.
- 세션 기반 로그인에서 브라우저는 통상 sessionid를 보관하며 비밀번호를 보관하는 게 아니다.
- 쿠키를 브라우저에 저장하므로 민감한 원문 정보 저장은 부적절하다.

### 2.3 Session

- 사용자의 여러 요청을 논리적으로 연결하는 서버 측 상태 관리 기법.
- 전형적인 흐름: (1) 서버에서 세션 생성 (2) 고유한 세션 ID 발급 (3) 응답 쿠키로 전달 (4) 브라우저가 이후 요청에 전송 (5) 서버가 세션을 조회하여 사용자를 판별.
- Django 기본 세션 저장 방식은 데이터베이스 백엔드로, 활성화 시 django_session 테이블에 저장된다(설정에 따라 저장 위치는 달라질 수 있다).
- 세션 ID는 쿠키로 전달될 수 있고 세션 데이터는 서버 측에 저장되는 점이 핵심.
- 세션에 사용자 관련 인증 정보가 저장되며, 브라우저에 모든 사용자 데이터가 그대로 저장되는 것은 아님.

### 2.4 Cookie vs Session 비교

| 비교 | Cookie | Session |
| --- | --- | --- |
| 기본 개념 | 브라우저에 저장되는 데이터 | 사용자 상태를 관리하는 메커니즘 |
| 저장 위치 | 브라우저 | 보통 서버 측 저장소(Django 기본 DB) |
| 연결 역할 | sessionid 등을 요청에 전송 | 세션 ID를 바탕으로 상태 정보 조회 |
| 위험 | 쿠키 탈취·노출·변조 등의 위험 | 세션 ID 탈취 시 세션 하이재킹 위험 |
| 만료 | Expires/Max-Age 등 | 설정과 세션 유효기간에 따름 |
| 비유 | 보관함 번호표 | 서버의 보관함 |

### 2.5 Django Authentication System

- 사용자 인증 및 관련 처리에 필요한 기본 기능 제공.
- 인증(Authentication): 누구인가? 본인 확인.
- 인가(Authorization): 무엇을 할 수 있는가? 권한 확인.
- django.contrib.auth: Django 인증 관련 모듈.
- django.contrib.sessions: 세션 사용과 관련된 앱.
- 시험 주의: 인증과 인가는 구별되는 개념이며, 이 강의는 주로 로그인 인증 중심.

### 2.6 Custom User 모델을 만드는 이유

- 기본 User 모델의 필드(예: username, password, email 등)를 그대로 사용하면 요구사항 확장에 제약이 있을 수 있다.
- 프로젝트 초기에 사용자 모델을 별도로 만들고 AbstractUser 상속으로 기본 인증 기능을 활용하는 방법을 권장.
- AbstractUser는 기존 Django User의 필드와 기능을 포함하고 있어 확장하기 쉽다.
- AbstractBaseUser는 더 낮은 수준에서 사용자 인증 기능을 직접 구성하는 데 쓰인다. 완전한 커스텀 인증을 설계할 때 더 많은설정이 필요.

```
# accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

# settings.py
AUTH_USER_MODEL = 'accounts.User'

# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```

- AUTH_USER_MODEL은 사용자 모델 경로를 지정하는 설정이다.
- 표기법: '앱레이블.모델클래스명'.
- 첫 마이그레이션 이전 설정이 안전하며 권장된다. 프로젝트 DB 생성 후 바꾸면 테이블·외래키·Migration 의존성 등 작업이 복잡해진다.
- 강의의 기존 db.sqlite3 및 migration 파일을 지우는 예시는 실습 초기화 맥락이다. 운영 DB에서 무작정 삭제하면 데이터 손실이 발생하므로 절대 일반화하지 않는다.
- 다른 모델에서 사용자 참조 시 settings.AUTH_USER_MODEL 또는 get_user_model() 활용이 권장된다.

### 2.7 AuthenticationForm

- django.contrib.auth.forms.AuthenticationForm은 로그인 인증 입력을 검증하기 위한 Form.
- 사용자의 계정을 새로 생성하는 ModelForm이 아니다.
- 생성 시 첫 번째 인자로 요청 객체를 전달할 수 있다.

```
# GET: 빈 로그인 폼
form = AuthenticationForm()
# POST: 제출값으로 검증
form = AuthenticationForm(request, request.POST)
```

- ArticleForm(request.POST)와 달리 로그인 AuthenticationForm은 request를 먼저 받는 방식이 대표적 함정이다.
- is_valid()는 입력의 유효성 확인 및 인증 과정을 수행한다.
- form.get_user()는 성공적으로 인증한 User 인스턴스를 가져온다.
- Form 객체 자체가 인증 처리를 마친 뒤 자동으로 로그인 세션을 만드는 것은 아니다.

### 2.8 auth.login 함수

```
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

<form action="{% url 'accounts:login' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="로그인">
</form>
```

- auth_login(request, user): Django 로그인 상태를 세션에 연결.
- form.get_user(): 검증된 사용자 객체 반환.
- auth_login이라는 별칭은 View 함수 이름 login과 충돌을 막는 데 사용.
- redirect는 로그인 뒤 다음 페이지로 이동하도록 응답을 반환. 리다이렉트 자체가 인증을 수행하지는 않는다.
- POST 폼에는 CSRF 토큰이 필요(일반적인 CSRF 미들웨어 설정 기준).
- GET은 빈 폼, POST는 바인딩된 폼, POST 유효성 검증 실패 시 오류 포함 폼을 다시 보여 준다.
- 로그인은 새 게시글 생성과 달리 사용자 객체를 새로 저장하는 작업이 아니라 인증된 사용자와 세션을 연결하는 작업이다.

### 2.9 request.user, 템플릿 인증 데이터, Context Processor

- request.user: 현재 요청과 연결된 사용자(인증되지 않으면 일반적으로 AnonymousUser).
- request.user.is_authenticated: 인증 여부 판단을 위한 속성.
- {{ user.username }}: 템플릿에 전달되는 인증 사용자 정보 출력 예시.
- django.contrib.auth.context_processors.auth가 활성화되어 있으면 템플릿에 user 등을 기본 제공.

```
{% if user.is_authenticated %}
  <p>안녕하세요, {{ user.username }}님!</p>
{% else %}
  <a href="{% url 'accounts:login' %}">로그인</a>
{% endif %}
```

- 주의: 화면에서 버튼만 숨기는 것은 서버 측 접근 권한을 통제하는 것과 다르다. 실제 보호는 View에서 인증·권한 검사를 해야한다.

### 2.10 쿠키 수명과 보안

- Session cookie: 일반적으로 브라우저 세션 종료까지 지속. 브라우저의 세션 복원 등 동작에 따라 실제 유지 여부가 달라질 수있음.
- Persistent cookie: Expires/Max-Age 등 설정에 의해 일정 기간 지속.
- HttpOnly: JavaScript의 document.cookie 접근을 막음. 네트워크 요청에 쿠키가 전송되는 것을 막는 속성은 아니다.
- Secure: HTTPS 연결에만 쿠키를 보내도록 지정.
- SameSite: 사이트 간 요청에 대한 쿠키 전송을 제한해 CSRF 위험을 낮추는 데 도움.
- 비밀번호 같은 민감 정보를 쿠키에 평문 저장하지 않는다는 원칙.

## 3. 슬라이드 원본 확인문제 12개 — 정답 및 이유

원문 문제의 의미를 유지하여 간략 재기술. 정답 표기는 강의 79쪽과 일치.

| 번호 | 확인 내용 | 공식 정답 | 해설 |
| --- | --- | --- | --- |
| 1 | HTTP의 특징이 아닌 것 | a) Stateful | HTTP는 Stateless |
| 2 | 서버가 브라우저로 보내는 작은 데이터 | b) Cookie | Set-Cookie로 설정 가능 |
| 3 | Cookie의 주된 사용 목적이 아닌 것 | d) 데이터베이스 역할 | Cookie는 DB 대체물이 아님 |
| 4 | 서버 측 사용자 상태 저장 기술 | c) Session | 상태 정보를 서버 측에 유지 |
| 5 | 세션 ID 저장 후 클라이언트에 전달 | Cookie | sessionid 쿠키 활용 |
| 6 | 기본 User에 없는 추가 필드 예시 | b) phone_number | 별도 확장 필요 |
| 7 | Custom User 설정 권장 시점 | d) 프로젝트 시작 시 | 초기 설정이 안전 |
| 8 | 로그인 인증 내장 폼 | b) AuthenticationForm | 유효성·인증 확인 |
| 9 | 인증 사용자 로그인 세션 생성 | c) login() | auth.login() 사용 |
| 10 | Custom User 설정 이름 | d) AUTH_USER_MODEL | 설정 파일에서 경로 지정 |
| 11 | HTTP Stateless 의미 | a) 이전 요청 정보를 유지하지 않음 | 독립 요청 |
| 12 | Cookie/Session 공통 목적 | d) 상태 정보 유지 및 사용자 식별 | HTTP의 Stateless 한계 보완 |

## 4. 추가 객관식 예상문제 15개

### Q1. HTTP Stateless의 의미로 가장 올바른 것은?

A. 연결을 지속할 수 없다 B. 요청 간 응용프로그램 상태를 기본적으로 기억하지 않는다 C. 암호화가 불가능하다 D. 브라우저가 쿠키를 저장하지 못한다

### Q2. 서버가 브라우저에 쿠키를 지정할 때 사용하는 HTTP 헤더는?

A. Authorization B. Content-Type C. Set-Cookie D. Accept

### Q3. Django 기본 데이터베이스 세션 설정에서 세션 데이터를 저장하는 테이블은?

A. auth_user B. django_session C. accounts_user D. auth_permission

### Q4. 사용자 정의 모델을 만드는 대표 코드로 옳은 것은?

A. class User(models.Form) B. class User(AuthenticationForm) C. class User(AbstractUser) D. class User(Session)

### Q5. AUTH_USER_MODEL = 'accounts.User'에서 accounts는 무엇인가?

A. 데이터베이스 이름 B. 앱 레이블 C. 사용자 이름 D. 세션 쿠키 이름

### Q6. AuthenticationForm의 POST 데이터를 받는 대표적인 방식은?

A. AuthenticationForm(request.POST) B. AuthenticationForm(request, request.POST) C. AuthenticationForm(instance=request.user) D. AuthenticationForm(request.FILES)

### Q7. 검증된 AuthenticationForm에서 사용자 인스턴스를 가져오는 메서드는?

A. save() B. get() C. get_user() D. create_user()

### Q8. auth_login(request, user)의 역할은?

A. 새 User 레코드 생성 B. 로그인 상태를 세션에 연결 C. 쿠키 전체 삭제 D. DB 마이그레이션 수행

### Q9. Django 템플릿에 현재 사용자 변수를 기본 공급하는 설정은?

A. django.contrib.auth.context_processors.auth B. STATIC_URL C. AUTH_USER_MODEL D. MEDIA_ROOT

### Q10. HttpOnly 쿠키의 올바른 설명은?

A. HTTPS로만 전송 B. 절대 만료되지 않음 C. JavaScript의 document.cookie 접근 제한 D. 서버 저장소에만 존재

### Q11. Secure 쿠키의 기본 의미는?

A. 암호 해싱을 수행 B. HTTPS에 전송 제한 C. 사용자를 자동 생성 D. 쿠키 값 자동 암호화

### Q12. 프로젝트 중간에 AUTH_USER_MODEL을 바꾸면 복잡해지는 주요 이유는?

A. Python 문법 오류 B. 기존 DB 테이블·Migration 관계 C. 정적 파일 검색 실패 D. 템플릿 상속 오류

### Q13. form.is_valid()가 False라면 강의의 로그인 View는 일반적으로 무엇을 하나?

A. auth_login 호출 B. 인증 실패 정보가 담긴 폼 다시 렌더링 C. 관리자 생성 D. 사용자 자동 가입

### Q14. 화면에 로그인 여부에 따라 다른 문구를 출력할 때 사용하는 속성은?

A. user.is_authenticated B. user.is_admin() C. request.sessionid() D. request.POST.is_valid()

### Q15. Custom User를 비교적 손쉽게 확장하고 기본 User 기능을 유지하려면?

A. AbstractBaseUser만 무조건 사용 B. AbstractUser 상속 C. HttpResponse 상속 D. BaseForm 상속

정답: 1-B, 2-C, 3-B, 4-C, 5-B, 6-B, 7-C, 8-B, 9-A, 10-C, 11-B, 12-B, 13-B, 14-A, 15-B.

오답 함정 해설: Q1은 Stateless와 Connectionless 구분. Q3은 User 테이블과 Session 테이블 구분. Q6은 첫 인자로 request 전달. Q7은 ModelForm.save와 AuthenticationForm.get_user 구분. Q8은 로그인과 가입 구분. Q10/11은 HttpOnly와 Secure 구분. Q12는 프로젝트 초기 설정 이유. Q14는 화면 표시와 실제 View의 권한 검사 차이를 기억.

## 5. 주관식 예상문제 10개

1. HTTP가 이전 요청 상태를 기억하지 않는 특성을 영어로 쓰시오.
2. 서버가 브라우저에 쿠키를 전달할 때 사용하는 응답 헤더명을 쓰시오.
3. 세션 ID를 브라우저가 보관하는 대표적인 수단을 쓰시오.
4. Django 기본 DB 기반 Session의 저장 테이블을 쓰시오.
5. 기존 Django User 모델을 쉽게 확장하기 위한 상속 클래스를 쓰시오.
6. 프로젝트의 사용자 모델을 지정하는 settings.py 설정명을 쓰시오.
7. 로그인 인증용 내장 Form 클래스명을 쓰시오.
8. 검증된 AuthenticationForm에서 인증 사용자 객체를 반환하는 메서드를 쓰시오.
9. 로그인 세션을 연결하는 Django 함수 호출을 쓰시오(request, user 존재).
10. 템플릿에서 사용자가 로그인했는지 검사할 때 확인하는 속성명을 쓰시오.

정답: 1. Stateless, 2. Set-Cookie, 3. Cookie, 4. django_session, 5. AbstractUser, 6. AUTH_USER_MODEL, 7. AuthenticationForm, 8. get_user(), 9. auth_login(request, user) 또는 django.contrib.auth.login(request, user), 10. is_authenticated.

## 6. 서술형 예상문제 5개와 만점 모범답안

### S1. HTTP의 Stateless 특성과 Cookie·Session을 이용한 로그인 상태 유지 과정을 설명하시오.

모범답안: HTTP는 각 요청이 독립적이라 이전 요청 상태를 기본적으로 기억하지 않는다. 사용자가 로그인을 완료하면 Django는서버 측에 로그인 관련 세션 상태를 생성하고 클라이언트에 세션 식별 정보를 쿠키로 전달한다. 브라우저는 이후 요청에 해당 쿠키를 첨부하고, 서버는 쿠키의 세션 ID를 바탕으로 세션 정보를 확인하여 사용자 로그인 상태를 유지한다.

채점 키워드: Stateless / 서버 측 세션 / 세션 ID / Cookie / 후속 요청 / 사용자 판별.

### S2. Cookie와 Session의 차이점 및 보안상 주의점을 설명하시오.

모범답안: Cookie는 브라우저에 저장되는 작은 데이터이며 요청에 함께 전송된다. Session은 서버 측에서 사용자 상태를 유지·조회하기 위한 메커니즘으로 일반적으로 쿠키에 담긴 세션 ID를 이용해 연결된다. 쿠키에 비밀번호 같은 민감 데이터를 직접 저장하지않아야 하며, Secure, HttpOnly, SameSite 설정을 적절히 사용하고 HTTPS를 적용해 위험을 낮춰야 한다.

채점 키워드: 브라우저/서버 저장 위치, 세션 ID, HttpOnly, Secure, 민감정보.

### S3. Custom User 모델을 프로젝트 시작 시 지정해야 하는 이유와 기본 설정 과정을 설명하시오.

모범답안: Django 기본 User 모델만으로는 추가 필드와 사용자 요구사항의 확장이 불편할 수 있다. 따라서 프로젝트 초기 accounts 앱에 AbstractUser를 상속한 User 모델을 만들고, settings.py에 AUTH_USER_MODEL = 'accounts.User'를 지정한다. 이미 기본 User 모델을 기준으로 Migration이 적용된 이후 바꾸면 기존 테이블과 관계, Migration 의존성 처리가 복잡하므로첫 마이그레이션 이전에 설정하는 것이 권장된다.

채점 키워드: AbstractUser / accounts.User / AUTH_USER_MODEL / 첫 Migration 이전 / DB 관계.

### S4. AuthenticationForm과 ModelForm의 차이 및 로그인 View 처리 과정을 설명하시오.

모범답안: ModelForm은 모델과 연계해 데이터 유효성 검사 및 생성·수정 저장을 지원한다. 반면 AuthenticationForm은 인증용로그인 폼으로 사용자가 제출한 계정 정보의 유효성을 확인한다. GET에서는 빈 AuthenticationForm을 보여주고 POST에서는 AuthenticationForm(request, request.POST)로 데이터를 바인딩한다. is_valid()가 True이면 get_user()로 인증 사용자를 얻고 auth_login(request, user)로 세션에 로그인 상태를 연결한 뒤 redirect한다. 실패하면 오류를 포함한 폼을 다시 렌더링한다.

채점 키워드: request 첫 인자 / is_valid / get_user / auth_login / redirect / 오류 재출력.

### S5. Django 템플릿에서 현재 로그인 사용자의 이름이 출력되는 이유를 설명하시오.

모범답안: Django는 세션과 인증 미들웨어를 통해 요청에 연결된 사용자를 request.user로 제공한다. 인증 Context Processor가 설정되어 있으면 사용자 정보가 템플릿의 user 변수로 제공되어 {{ user.username }}과 같이 출력할 수 있다. 비로그인 시에는 AnonymousUser가 제공될 수 있으므로 user.is_authenticated로 분기하는 것이 적절하다.

채점 키워드: request.user / AuthenticationMiddleware / Context Processor / user.username / is_authenticated.

## 7. 코드 추론·빈칸 8문제

### C1

```
form = AuthenticationForm(____, request.POST)
```

정답: request.

### C2

```
if form.is_valid():
    auth_login(request, form.____())
```

정답: get_user.

### C3

```
# settings.py
____ = 'accounts.User'
```

정답: AUTH_USER_MODEL.

### C4

```
from django.contrib.auth.models import ____
class User(____):
    pass
```

정답: AbstractUser 두 곳.

### C5

```
form = AuthenticationForm(request, request.POST)
if form.is_valid():
    return redirect('articles:index')
```

문제: 코드에 빠진 핵심 단계는? 정답: auth_login(request, form.get_user()). 단순 redirect는 로그인 상태를 만들지 않는다.

### C6

```
# GET 요청일 때
form = AuthenticationForm(request, request.POST)
```

문제: GET에서 빈 폼을 보여 주기 위한 더 적절한 코드? 정답: form = AuthenticationForm().

### C7

```
{% if user.is_authenticated %}
  {{ user.username }}
{% else %}
  게스트
{% endif %}
```

문제: 로그인하지 않은 경우 어떤 글자가 표시되는가? 정답: 게스트.

### C8

```
from django.contrib.auth import login

def login(request):
    ...
    login(request, user)
```

문제: 이 코드의 문제와 해결책은? 정답: 같은 이름의 View 함수와 인증 login 함수가 충돌한다. from django.contrib.auth import login as auth_login 후 auth_login(request, user)를 호출한다.

## 8. 헷갈리는 개념 TOP 10

1. Stateful / Stateless: HTTP는 Stateless.
2. Connectionless / Stateless: 연결 특성과 요청 상태 보존은 다른 개념.
3. Cookie / Session: 브라우저의 식별 정보 vs 서버 측 상태 관리.
4. sessionid / 사용자 비밀번호: 보통 세션 식별값을 쿠키로 전달.
5. AbstractUser / AbstractBaseUser: 기본 사용자 기능 포함 확장 vs 직접 설계할 항목이 더 많은 기반 클래스.
6. AUTH_USER_MODEL / INSTALLED_APPS: 사용자 모델 지정 vs 앱 등록.
7. AuthenticationForm / ModelForm: 로그인 인증 vs DB 객체 생성·수정.
8. form.get_user() / auth_login(): 인증 사용자 반환 vs 로그인 세션 연결.
9. redirect() / login(): 페이지 이동 vs 로그인 상태 생성.
10. HttpOnly / Secure: JS 접근 차단 vs HTTPS 전송 제한.

## 9. 시험 직전 90초 암기 카드

- HTTP = Stateless, Connectionless(교재 표현 기준; 지속 연결과 구별).
- Cookie = 브라우저 저장, 세션 ID 전달.
- Session = 서버 측 상태 저장, Django 기본 DB 세션: django_session.
- Custom User = class User(AbstractUser): pass.
- 설정 = AUTH_USER_MODEL = 'accounts.User'.
- 시점 = 첫 migrate 이전에 설정 권장.
- 로그인 폼 = AuthenticationForm(request, request.POST).
- 인증 검증 = form.is_valid().
- 검증된 사용자 = form.get_user().
- 실제 세션 로그인 = auth_login(request, form.get_user()).
- 현재 사용자 = request.user, 템플릿 user.username.
- 인증 확인 = user.is_authenticated.
- 보안: HttpOnly / Secure / SameSite를 구별.

## 10. 1~8단원 연결 학습

- 1단원 MTV: Login View는 요청 처리와 응답 구성 담당.
- 2단원 URL: accounts:login 이름으로 로그인 URL 역참조.
- 3단원 Model: Custom User는 모델이며 Migration 이전 설정 중요.
- 4단원 ORM: get_user()는 로그인 인증 사용자 반환; ORM의 get()와 다름.
- 5단원 ORM with View: POST 폼, CSRF 토큰, redirect 재활용.
- 6단원 Form: AuthenticationForm은 일반 게시글 ModelForm과 역할 다름.
- 7단원 Staticfiles: 인증 사용자에 연결된 업로드 파일에는 별도 접근 통제가 필요할 수 있음.
- 8단원 Authentication: 사용자 인증 상태는 Cookie + Session 조합으로 유지.

### 실전 자기 점검

- HTTP Stateless를 1문장으로 설명할 수 있다.
- 세션 ID의 브라우저 전달과 서버 측 조회 흐름을 순서대로 설명할 수 있다.
- AbstractUser와 AUTH_USER_MODEL 코드를 백지에서 쓸 수 있다.
- ModelForm과 AuthenticationForm의 생성 인자 차이를 안다.
- auth_login을 빼먹은 코드의 버그를 찾을 수 있다.
- 공식 확인문제 12개를 모두 설명하면서 풀 수 있다.
- 서술형 5개를 필수 키워드 중심으로 3~5문장에 요약할 수 있다.
