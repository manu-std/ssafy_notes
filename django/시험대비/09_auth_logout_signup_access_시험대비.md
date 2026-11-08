# Django 9단원 시험대비 — Authentication System 02

> 📎 개념 정리 노트: [`../09_auth_logout_signup_access.md`](../09_auth_logout_signup_access.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

학습 근거: 업로드한 SSAFY Django_Authentication_System_02.zip 전체 69장(p001~p069). 강의 확인문제 p058~p062, 공식 해설 p061~p062. 출제 중요도는 슬라이드 강조·실습·확인문제에 근거한 추정이며 실제 시험의 확정 출제 예측은 아님.

## 0. 한눈에 보기

- 최우선(★★★): logout(request), UserCreationForm, 커스텀 유저와 get_user_model(), 회원탈퇴 request.user.delete(), is_authenticated 속성, @login_required, POST 및 CSRF, 회원가입 후 자동 로그인.
- 중요(★★): AuthenticationForm과 UserCreationForm 비교, login(request,user), auth_logout과 logout View 이름충돌, 익명 사용자, 회원탈퇴 후 세션 정리, AbstractUser와 AbstractBaseUser.
- 연결 개념: 8단원 Session/Cookie 및 Custom User Model, 6단원 ModelForm/유효성 검사, 5단원 GET/POST 및 PRG, 3 단원 Model.

## 1. 인증 상태 이해 — AnonymousUser와 request.user (p004, p039~p043)

**인증(Authentication)은** 사용자가 누구인지 확인하는 과정이다. **인가(Authorization)는** 특정 동작 수행 권한을 부여하거나 검사하는 과정이다. 이 강의에서 is_authenticated는 로그인 여부를 구분하는 데 사용한다. 단, 로그인됨이 곧 모든 데이터에 대한 권한을 가진다는 뜻은 아니다.

- 로그아웃 사용자: request.user는 보통 AnonymousUser, request.user.is_authenticated == False.
- 로그인 사용자: request.user는 인증된 사용자 모델의 객체, request.user.is_authenticated == True.
- is_authenticated는 속성(property): request.user.is_authenticated (일반적인 Django 코드에서 괄호 없음).
- 템플릿: {% if request.user.is_authenticated %} 혹은 컨텍스트 프로세서로 제공되는 user.is_authenticated.
- 접근 제한 예: 로그인·회원가입은 이미 로그인한 사용자가 다시 진입하지 않도록 리다이렉트 가능. 로그인과 회원가입을 요구하는 접근 제한이 모든 시스템의 필수 규칙은 아니며 프로젝트 요구사항에 따른 설계다.

## 2. 로그인 복습 (p006~p016)

HTTP는 Stateless(각 요청이 독립적)하므로 로그인 상태를 계속 기억하기 위한 Session·Cookie가 필요하다.

```
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
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
```

- AuthenticationForm은 기본 로그인 폼이며 forms.Form 기반이다. 모델을 직접 저장하는 ModelForm이 아니다.
- AuthenticationForm(request, request.POST)의 첫 번째 인자가 request인 점이 중요하다.
- form.is_valid()는 검증, form.get_user()는 인증된 사용자 객체를 반환, auth_login(request, user)는 로그인 처리.
- form.is_valid()만으로 로그인 세션이 생성되지 않는다.
- 로그인 페이지 POST 폼에 {% csrf_token %}을 삽입.

## 3. Logout (p017~p021)

로그아웃은 로그인 상태를 유지하기 위해 연결된 세션을 종료하는 동작이다. Django의 django.contrib.auth.logout(request)는 해당 요청의 세션 데이터를 정리한다. 브라우저 측 세션 쿠키도 응답 처리에서 삭제·무효화되도록 한다. 강의의 핵심은 서버 세션과 브라우저 쿠키의 연결 해제이다.

```
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('articles:index')
```

HTML 예:

```
<form action="{% url 'accounts:logout' %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="Logout">
</form>
```

시험 함정: auth_logout(request)는 사용자 계정을 삭제하지 않으며, request.user.delete()와 완전히 다르다. 로그아웃은 서버 상태 변경이므로 GET 링크보다는 POST 방식이 적절하다. 강의 실습은 3단계로 URL 작성 → 뷰 작성 → POST 폼 작성.

## 4. 회원가입(UserCreationForm) (p022~p033)

회원가입은 새로운 사용자 계정을 DB에 생성하는 과정이다.

- Django 제공 UserCreationForm: 사용자 생성용 ModelForm. AuthenticationForm은 로그인용 Form.
- 기본 제공 폼은 기본 User 모델과 결합된 방식일 수 있다. 프로젝트에서 AUTH_USER_MODEL = 'accounts.User'로 User를 교체하면 기본 UserCreationForm을 그대로 사용했을 때 모델 참조 관련 문제가 날 수 있다.
- get_user_model()은 현재 프로젝트에서 활성화된 사용자 모델 클래스를 반환한다.
- 폼의 Meta 안에서 model = get_user_model()로 재지정하는 것이 강의 핵심.

```
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

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
    return render(request, 'accounts/signup.html', {'form': form})
```

- get_user_model()의 목적: 현재 사용 중인 커스텀 User 모델을 안전하게 참조.
- form.save()가 새 사용자 객체를 생성·저장한다.
- UserCreationForm은 저장 시 비밀번호를 올바른 방식으로 해시 처리한다. 직접 User.password = '평문'을 대입해 저장하는방식과 구분.
- 가입 시 자동 로그인은 기본으로 수행되지 않는다. 아래와 같이 별도로 로그인 함수 호출 필요.

```
if form.is_valid():
    user = form.save()
    auth_login(request, user)
    return redirect('articles:index')
```

## 5. 회원탈퇴 (p034~p037, p053~p054)

```
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST

@login_required
@require_POST
def delete(request):
    user = request.user
    auth_logout(request)  # 로그인 세션 먼저 정리
    user.delete()         # 해당 사용자 객체 삭제
    return redirect('articles:index')
```

강의 초기 구현은 request.user.delete()이고 개선 흐름은 계정 삭제와 세션 정리의 순서를 올바르게 고려한다. 세션 정리 후에는 request.user를 다시 참조하여 삭제 대상을 구하지 않는 것이 안전하다. 강의 확인문제의 정답은 계정 삭제 후 로그아웃으로 설명되어 있으나, 일반적인 Django 구현에서는 삭제 대상 User 객체를 먼저 확보한 뒤 로그아웃하고 해당 객체를 삭제하는 방법도 적절하다. 핵심 원칙은 삭제할 계정을 명확히 확보하고 세션을 정리하는 것이다. 실제 보안상 이유로 상태 변경은 POST+CSRF가 적절하다.

중요 구분

- auth_logout(request) → 로그인 상태 종료; User 레코드는 남는다.
- request.user.delete() → DB의 사용자 계정 삭제; 현재 요청의 로그인 상태 처리는 별도 고려.

## 6. 인증된 사용자만 접근 — 2가지 방식 (p038~p047)

A. is_authenticated 속성

```
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    ...
```

템플릿에서도 사용 가능.

```
{% if request.user.is_authenticated %}
  <p>로그인 완료</p>
{% else %}
  <a href="{% url 'accounts:login' %}">로그인</a>
{% endif %}
```

B. @login_required 데코레이터

```
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    ...
```

- 로그인이 필요한 뷰 함수를 감싼다.
- 비로그인 사용자가 접근할 경우 로그인 페이지로 리다이렉트한다. 설정된 LOGIN_URL을 사용하며 next 파라미터가 붙을 수 있다.
- @login_required는 해당 사용자에게 해당 게시물 편집권한까지 자동 부여하지 않는다. 소유권 검사는 별도로 필요.
- 강의 함정: is_authenticated와 login_required는 함수나 속성의 종류부터 다르다. 전자는 속성, 후자는 데코레이터.

## 7. AbstractUser와 AbstractBaseUser (p060~p062 및 8단원 연결)

- AbstractUser: Django 기본 사용자 필드·기능이 준비된 추상 사용자 모델. 추가 필드를 붙여 확장하기 편리.
- AbstractBaseUser: 인증을 위한 더 기본적인 기능을 제공하며 사용자 필드, 매니저 등을 보다 직접 설계할 때 사용.
- 커스텀 User 모델은 프로젝트 초기에 AUTH_USER_MODEL로 지정하는 것이 바람직하다.

## 8. 코드 오류 찾아내기 — 출제 함정 12가지

1. AuthenticationForm(request.POST) → 첫 positional 인자를 request로 해석할 수 있으므로 AuthenticationForm(request, request.POST) 사용.
2. UserCreationForm()과 AuthenticationForm()의 역할 혼동.
3. Custom User 모델을 활성화했는데 기본 UserCreationForm의 Meta.model을 바꾸지 않음.
4. is_authenticated()처럼 함수 호출 → 속성이므로 보통 is_authenticated.
5. @login_required()와 @login_required는 사용 형태가 다를 수 있지만 이 강의의 기본은 @login_required.
6. 로그아웃을 &lt;a href&gt; GET으로 처리 → POST 폼 권장.
7. POST 폼에 {% csrf_token %} 누락 → 기본 CSRF 보호 환경에서 403 가능.
8. form.is_valid()만 호출하고 auth_login() 누락 → 로그인 안 됨.
9. 회원가입 form.save() 후 자동 로그인된다고 착각 → 별도 auth_login 필요.
10. auth_logout()을 회원 탈퇴와 동일하게 취급 → DB User는 남음.
11. @login_required만으로 본인 글만 수정 가능하다고 착각 → 별도 객체 권한 검사 필요.
12. 삭제 전후 request.user의 상태에만 의존해 삭제할 객체를 찾음 → User 객체를 미리 확보하여 안전하게 처리.

## 9. 강의 원본 확인문제 10개 (p058~p062, 문제의 취지를 재서술)

1. 로그아웃 시 다루는 대상은? 정답 c: 세션 데이터와 쿠키 모두. 세션 연결을 종료하고 관련 브라우저 쿠키를 무효화한다.
2. 회원가입용 기본 Django Form은? 정답 b: UserCreationForm.
3. get_user_model()의 목적은? 정답 c: 현재 활성 User 모델 참조.
4. 로그인한 사용자의 탈퇴에 활용하는 호출은? 정답 a: request.user.delete().
5. 로그인 여부 확인에 쓰는 속성은? 정답 d: is_authenticated.
6. login_required의 목적은? 정답 b: 비인증 사용자 접근 제한.
7. 회원가입 직후 자동 로그인 구현은? 정답 a: form.save() 후 login() 호출.
8. 탈퇴 후 세션 정리와 관련한 강의 정답은? 정답 b: 계정 삭제 후 로그아웃. 단, 일반 구현에서는 삭제 대상을 미리 확보한 다음로그아웃 후 삭제해도 된다. 특정 순서 자체보다 대상과 세션의 올바른 처리가 중요.
9. AbstractUser와 AbstractBaseUser 비교의 올바른 설명은? 정답 c: AbstractUser가 기본 필드를 포함.
10. 로그아웃처럼 서버 상태를 변경하는 요청에 권장되는 메서드는? 정답 b: POST.

## 10. 추가 객관식 15문제

Q1. 로그인 후 인증 상태를 유지할 수 있도록 돕는 것은? A CSS B Session/Cookie C Template D Static → B. HTTP의 무상태성을 보완한다.

Q2. 사용자 인증 상태를 Boolean으로 확인할 수 있는 속성은? A is_staff() B is_authenticated C login_required D get_user_model → B. 괄호 없는 속성.

Q3. 가입 완료만으로 자동 로그인을 실행하는 코드는? A form.save() B auth_login(request, form.save()) C form.is_valid() D redirect() → B (전제: 유효성 검사를 통과한 ModelForm). 반환된 사용자를 login에 넘긴다.

Q4. 활성 User 모델을 얻는 함수는? A get_user_model() B User.objects.all() C login() D get_object_or_404() → A.

Q5. 커스텀 User 모델과 UserCreationForm을 연결할 적절한 Meta 선언은? A model = User 고정 B model = get_user_model() C fields = request.POST D instance = User → B.

Q6. 로그아웃의 올바른 설명은? A 계정을 삭제 B 세션을 종료 C 새로운 사용자 생성 D 게시물 삭제 → B.

Q7. 비로그인자가 보호 View로 접근할 때 리다이렉트를 지원하는 데코레이터는? A @csrf_exempt B @login_required C @property D @staticmethod → B.

Q8. 회원가입과 로그인 Form 설명 중 옳은 것은? A 둘 다 같은 ModelForm B UserCreationForm은 가입, AuthenticationForm은 로그인 C AuthenticationForm은 계정 저장 D UserCreationForm은 인증 세션 생성 → B.

Q9. 탈퇴 요청에서 DB 사용자 계정을 삭제하는 메서드는? A auth_logout(request) B request.user.delete() C request.session.get() D form.get_user() → B.

Q10. request.user.is_authenticated 값이 False인 상황은? A 모든 관리자 B 익명 사용자 C 활성 사용자 D 로그인 완료 사용자 → B.

Q11. 로그아웃 요청 방식으로 적절한 것은? A GET이 필수 B POST + CSRF 토큰 C DELETE 링크만 허용 D HTTP Method 무관 → B.

Q12. @login_required의 보호 기능 한계는? A 로그인 확인도 못함 B 해당 데이터의 소유권을 자동 검사하지 않음 C 쿠키 제거 D POST 차단 → B.

Q13. 사용자 객체를 생성·저장하는 일반적인 가입 코드 위치는? A CustomUserCreationForm(request.POST) 뒤 form.is_valid() 확인 후 form.save() B get_user_model().delete() C auth_logout() D AuthenticationForm().save() → A.

Q14. 다음 중 AnonymousUser에게 일반적으로 성립하는 것은? A is_authenticated == True B is_authenticated == False C 자동 계정 생성 D 슈퍼유저 → B.

Q15. AbstractUser를 이용한 커스텀 User의 대표 장점은? A DB 기능 삭제 B 기본 필드를 상속하면서 확장 가능 C 로그인 금지 D 세션 불필요 → B.

## 11. 추가 주관식 10문제

1. 현재 활성 사용자 모델 클래스를 반환하는 함수는? → get_user_model().
2. 회원가입용 Django 기본 ModelForm 이름은? → UserCreationForm.
3. 로그인용 Django 기본 Form 이름은? → AuthenticationForm.
4. 현재 사용자를 인증된 상태로 설정하는 함수는? → login(request, user) (auth_login 별칭 가능).
5. 현재 요청의 인증 세션을 종료하는 함수는? → logout(request) (auth_logout 별칭 가능).
6. 사용자 로그인 여부를 검사하는 속성은? → is_authenticated.
7. 비로그인 사용자의 View 접근을 막는 데코레이터는? → @login_required.
8. 현재 로그인 사용자를 DB에서 삭제하는 메서드는? → request.user.delete().
9. 기본 User 필드를 포함해 확장하기 쉬운 추상 클래스는? → AbstractUser.
10. 가입 후 자동 로그인에 필요한 두 핵심 호출을 순서대로 쓰시오. → user = form.save() → auth_login(request, user).

## 12. 서술형 예상문제 5개 (모범답안과 채점 키워드)

S1. 로그아웃과 회원탈퇴의 차이점을 설명하시오.

- 모범답안: 로그아웃은 사용자의 DB 계정을 유지한 채 서버의 인증 세션을 종료하여 로그인 상태를 해제한다. 회원탈퇴는 현재사용자의 DB 사용자 레코드를 삭제하는 것으로, 로그인 세션도 함께 적절히 정리해야 한다.
- 채점 키워드: 계정 유지/계정 삭제, 세션 종료, auth_logout, user.delete.

S2. 커스텀 사용자 모델이 적용된 프로젝트에서 UserCreationForm을 재정의해야 하는 이유를 쓰시오.

- 모범답안: 기본 UserCreationForm은 기본 User 모델을 참조할 수 있어 커스텀 User 모델을 활성화한 프로젝트와 충돌할 수있다. UserCreationForm을 상속받아 Meta.model에 get_user_model()을 지정하면 현재 활성화된 User 모델에 맞는 회원가입 폼을 제공할 수 있다.
- 채점 키워드: 커스텀 User, UserCreationForm 상속, Meta.model, get_user_model().

S3. 회원가입 직후 자동 로그인을 구현하는 절차를 설명하시오.

- 모범답안: POST 데이터로 CustomUserCreationForm을 생성하고 is_valid()로 검증한다. 유효하면 user = form.save()로 User 객체를 저장한 다음 auth_login(request, user)로 세션에 로그인 상태를 설정하고 redirect로 이동한다.
- 채점 키워드: POST, is_valid, save 반환 User, auth_login, redirect.

S4. is_authenticated와 login_required의 차이를 설명하시오.

- 모범답안: is_authenticated는 request.user가 인증된 사용자인지를 나타내는 Boolean 속성으로 View나 Template의 분기 조건에 활용한다. login_required는 View를 보호하는 데코레이터이며 비로그인자가 접근하면 로그인 URL로 이동하도록한다.
- 채점 키워드: 속성/데코레이터, True/False, View 보호, 로그인 페이지 리다이렉트.

S5. HTTP GET 대신 POST로 로그아웃을 구현하는 이유를 설명하시오.

- 모범답안: GET은 원칙적으로 서버의 상태를 변경하지 않는 조회 요청에 사용해야 한다. 로그아웃은 인증 세션 상태를 변경하는 작업이므로 POST로 처리하는 것이 적절하며, CSRF 토큰을 함께 사용해 교차 사이트 요청 위조로 인한 의도치 않은 로그아웃을 방지할 수 있다.
- 채점 키워드: GET 안전성, POST 상태 변경, 세션, CSRF.

## 13. 코드 추론 8문제

1. form = AuthenticationForm(request.POST)에서 문제점은? → request.POST가 첫 번째 request 위치로 해석될 수 있으므로 AuthenticationForm(request, request.POST) 사용.
2. user = form.save(); return redirect(...) 직후 로그인 상태인가? → 기본적으로 아니다. auth_login 별도 호출.
3. auth_logout(request) 직후 DB 사용자 레코드는? → 유지된다.
4. request.user.delete() 뒤 동일 세션을 유지해도 되는가? → 권장되지 않는다. 인증 세션 정리 필요.
5. @login_required가 붙은 수정 View에 로그인한 타인이 접근하면 자동으로 본인 글만 수정 가능한가? → 아니다. 소유권 검사필요.
6. request.user.is_authenticated()는 올바른가? → 속성이므로 request.user.is_authenticated.
7. 기본 UserCreationForm으로 AUTH_USER_MODEL='accounts.User'를 사용하면? → 모델 참조 문제 가능; Meta.model을 get_user_model()로 지정한 커스텀 폼 사용.
8. &lt;a href="{% url 'accounts:logout' %}"&gt;로 로그아웃을 구현하면? → GET 요청이 되므로 POST Form과 csrf_token이 바람직.

## 14. 1~9단원 통합 연결 문제

- 2단원 URLconf: path('logout/', views.logout, name='logout') → 템플릿 {% url 'accounts:logout' %}.
- 5단원 POST/CSRF: 로그인·로그아웃·가입·탈퇴 등 처리 폼에 POST와 CSRF 적용.
- 6단원 Form: AuthenticationForm은 Form, UserCreationForm은 ModelForm; 둘 다 is_valid() 사용.
- 3단원 Model: AUTH_USER_MODEL 사용자 스키마를 처음 migrate 전에 지정하는 이유.
- 8단원 로그인: auth_login으로 세션 연결; 9단원 로그아웃: auth_logout으로 세션 연결 해제.

## 15. 시험 직전 3분 암기장

```
login : AuthenticationForm(request, request.POST) → is_valid() → get_user() → auth_login(request,user)
logout: auth_logout(request) / POST + csrf_token
signup: CustomUserCreationForm(request.POST) → is_valid() → user=form.save()
자동 로그인: signup 저장 다음 auth_login(request,user)
CustomUserCreationForm(UserCreationForm): Meta.model=get_user_model()
회원탈퇴: 삭제할 User 확보 → 세션 정리 + User 삭제 (POST)
로그인 여부: request.user.is_authenticated (속성)
뷰 보호: @login_required (데코레이터)
AbstractUser: 기본 필드 포함 / AbstractBaseUser: 기본 인증 구성 요소
get_user_model(): 활성 User 모델 클래스 반환
```

### 최종 자가 체크 (모두 '예'가 되어야 만점권)

- 로그인·로그아웃·회원탈퇴 각각 DB 계정 및 세션에 미치는 영향 설명 가능
- AuthenticationForm과 UserCreationForm 구분 가능
- CustomUserCreationForm의 Meta.model을 암기함
- get_user_model()이 무엇을 반환하는지 정확히 설명 가능
- is_authenticated와 @login_required의 차이를 설명 가능
- 가입 후 자동 로그인 코드 순서를 외움
- POST·CSRF 사용 이유를 서술할 수 있음
- 8단원 내용과 연계해 세션·쿠키를 설명할 수 있음

학습 전략: 개념서 12분 → 확인문제 10개 4분 → 추가 객관식/주관식 12분 → 서술형 10분 → 오답 및 코드 빈칸 7분. 실제 시험범위가 10단원 전체이면 이후 누적 모의고사로 재점검.
