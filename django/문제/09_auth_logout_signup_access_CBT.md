# Django 9단원 CBT — Auth 02 · 로그아웃·회원가입·접근 제한 (30문항)

> 출제 범위: [`../09_auth_logout_signup_access.md`](../09_auth_logout_signup_access.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. 로그아웃을 '세션' 관점에서 표현한 것은?

- ① 세션 Create
- ② User 객체 Delete
- ③ 세션 Delete
- ④ User 객체 Update

---

### 2. `auth_logout(request)`가 하는 일로 **옳은** 것은?

- ① 서버의 세션과 쿠키의 sessionid를 삭제한다.
- ② DB의 User 테이블에서 사용자 계정을 삭제한다.
- ③ 사용자의 비밀번호를 초기값으로 재설정한다.
- ④ 로그인하지 않은 상태에서 호출하면 에러가 발생한다.

---

### 3. 로그인 링크는 `<a>`로, 로그아웃은 POST form으로 만드는 이유는?

- ① `<a>` 태그로는 accounts 앱 URL에 접근할 수 없어서
- ② 로그아웃은 세션을 삭제하는, 서버 상태를 바꾸는 요청이라서
- ③ 로그인 페이지는 CSRF 공격 대상이 될 수 없어서
- ④ form이 a 태그보다 빠르게 동작해서

---

### 4. logout view가 POST 요청만 받도록 제한하는 데코레이터는?

- ① `@require_POST`
- ② `@login_required`
- ③ `@csrf_exempt`
- ④ `@post_only`

---

### 5. 회원가입을 CRUD 관점에서 표현한 것은?

- ① 세션 Create
- ② User 객체 Update
- ③ 세션 Delete
- ④ User 객체 Create

---

### 6. UserCreationForm에 대한 설명으로 **옳은** 것은?

- ① 회원가입용 ModelForm이며, 비밀번호를 해시해 저장한다.
- ② 로그인 확인용 Form이라 save() 메서드가 아예 없다.
- ③ Custom User를 쓰는 프로젝트에서도 수정 없이 그대로 쓸 수 있다.
- ④ 생성자의 첫 번째 인자로 request 객체를 받는다.

---

### 7. Custom User를 쓰는 프로젝트에서 UserCreationForm을 상속해 재정의하는 이유는?

- ① 비밀번호 입력 칸을 2개에서 3개로 늘려야 해서
- ② Meta.model이 기본 auth.User로 고정되어 있어서
- ③ UserCreationForm에는 is_valid() 메서드가 없어서
- ④ 상속해야 회원가입 직후 자동으로 로그인되어서

---

### 8. 다음 CustomUserCreationForm의 빈칸으로 가장 적절한 것은?

```python
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = _______
```

- ① `User`
- ② `get_user_model()`
- ③ `'auth.User'`
- ④ `settings.AUTH_USER_MODEL`

---

### 9. `get_user_model()`에 대한 설명으로 **옳은** 것은?

- ① 설정과 관계없이 항상 Django 기본 auth.User를 반환한다.
- ② 현재 요청을 보낸 로그인 사용자 객체를 반환한다.
- ③ AUTH_USER_MODEL에 지정된 유저 모델 클래스를 반환한다.
- ④ 새로운 유저 객체를 생성해 DB에 저장하고 반환한다.

---

### 10. `class Meta(UserCreationForm.Meta):`처럼 부모 Meta를 상속하는 이유는?

- ① Meta를 상속해야 ModelForm 기능이 동작해서
- ② 부모의 fields 설정은 두고 model만 바꾸려고
- ③ 부모 Meta에 정의된 model을 그대로 쓰기 위해
- ④ Meta는 반드시 부모를 상속받아야 문법 오류가 나지 않아서

---

### 11. 회원가입 직후 자동으로 로그인되게 하려면?

- ① `form.save()`만 호출해도 저장과 동시에 자동으로 로그인된다.
- ② `form.save(commit=False)`로 저장을 미루면 로그인 세션이 생긴다.
- ③ 가입 후 `redirect('accounts:login')`으로 보내면 자동 로그인된다.
- ④ save()가 돌려준 user로 auth_login()을 호출한다.

---

### 12. 회원 탈퇴 view에서 계정을 삭제하는 코드는?

- ① `auth_logout(request)`
- ② `User.objects.all().delete()`
- ③ `request.user.save()`
- ④ `request.user.delete()`

---

### 13. 로그아웃과 회원 탈퇴의 차이로 **옳은** 것은?

- ① 둘 다 세션을 지우고 DB에서 User 계정도 삭제한다.
- ② 로그아웃은 User를 삭제하고, 탈퇴는 세션만 삭제한다.
- ③ 로그아웃은 세션만 끊고, 탈퇴는 User를 삭제한다.
- ④ 둘 다 세션만 삭제하므로 DB의 User는 그대로 남는다.

---

### 14. 다음처럼 탈퇴 view에서 로그아웃을 **먼저** 하면 생기는 문제는?

```python
def delete(request):
    auth_logout(request)
    request.user.delete()
    return redirect('articles:index')
```

- ① request.user가 AnonymousUser가 돼 대상을 잃는다.
- ② 세션을 두 번 지우게 되어 KeyError가 발생한다.
- ③ 로그아웃 직후 CSRF 토큰이 무효가 되어 403이 발생한다.
- ④ 순서와 무관하게 계정 삭제와 로그아웃이 정상 처리된다.

---

### 15. `is_authenticated`에 대한 설명으로 **옳은** 것은?

- ① User 객체의 속성이라 괄호 없이 `request.user.is_authenticated`로 쓴다.
- ② 메서드이므로 `request.user.is_authenticated()`로 호출해야 한다.
- ③ view 함수 위에 붙이는 데코레이터다.
- ④ 로그인하지 않은 사용자(AnonymousUser)에서는 True다.

---

### 16. 템플릿에서 로그인한 사용자에게만 로그아웃 버튼을 보여주는 조건은?

- ① `{% if request.user.is_superuser %}`
- ② `{% if request.user.is_login %}`
- ③ `{% if request.user.is_authenticated %}`
- ④ `{% if request.user.is_authenticated() %}`

---

### 17. 이미 로그인한 사용자가 login, signup 페이지에 다시 들어오지 못하게 하는 view 코드는?

- ① login view에 `@login_required`를 붙인다.
- ② `if not request.user.is_authenticated: return redirect('articles:index')`
- ③ `if request.user.is_authenticated: return redirect('articles:index')`
- ④ `if request.method == 'GET': return redirect('accounts:login')`

---

### 18. `@login_required`에 대한 설명으로 **옳지 않은** 것은?

- ① 인증된 사용자에 대해서만 view 함수를 실행한다.
- ② 비로그인 사용자는 로그인 페이지(기본 /accounts/login/)로 redirect된다.
- ③ redirect 시 원래 가려던 주소가 next 파라미터로 붙을 수 있다.
- ④ 붙이면 해당 게시글의 작성자인지까지 자동으로 확인해 준다.

---

### 19. 템플릿에서 [NEW] 버튼만 숨기고 create view에는 아무 처리도 하지 않았을 때의 문제는?

- ① 버튼이 숨겨져 로그인한 사용자도 글을 쓸 수 없게 된다.
- ② 비로그인 사용자도 URL을 직접 입력해 접근할 수 있다.
- ③ 템플릿 분기 때문에 CSRF 토큰이 생성되지 않는다.
- ④ if 태그 안에서는 user 변수를 쓸 수 없어 에러가 난다.

---

### 20. AuthenticationForm과 UserCreationForm의 비교로 **옳지 않은** 것은?

- ① AuthenticationForm은 로그인용, UserCreationForm은 회원가입용이다.
- ② AuthenticationForm은 Form, UserCreationForm은 ModelForm이다.
- ③ AuthenticationForm은 첫 인자로 request를, UserCreationForm은 data를 받는다.
- ④ 두 폼 모두 save()로 새 User를 DB에 저장한다.

---

## 함정 문제 (21~30)

### 21. 비로그인 상태로 `@login_required`가 붙은 `/articles/create/`에 접근하면 이동하는 주소는?

- ① `/articles/?next=/articles/create/`
- ② `/accounts/signup/?next=/articles/create/`
- ③ `/admin/login/?next=/articles/create/`
- ④ `/accounts/login/?next=/articles/create/`

---

### 22. view에서 `if request.user.is_authenticated():`처럼 **괄호를 붙이면**?

- ① bool을 호출해 TypeError가 난다.
- ② 정상 동작한다. 괄호는 있어도 그만이다.
- ③ 괄호 때문에 항상 False를 반환한다.
- ④ 로그인 페이지로 redirect된다.

---

### 23. `AUTH_USER_MODEL = 'accounts.User'`인 프로젝트에서 **기본 UserCreationForm을 그대로** 회원가입에 쓰면?

- ① 정상적으로 accounts.User에 가입된다.
- ② auth.User 테이블에 따로 가입된다.
- ③ auth.User가 교체돼 있어 에러가 난다.
- ④ username 없이 이메일만으로 가입된다.

---

### 24. 회원 탈퇴 view에 `@login_required` 없이, **비로그인** 사용자가 POST로 요청하면?

- ① DB의 아무 계정 하나가 삭제된다.
- ② AnonymousUser라 에러가 난다.
- ③ 정상적으로 index로 redirect된다.
- ④ 가장 최근에 가입한 계정이 삭제된다.

---

### 25. 템플릿에서 `{{ user }}`와 `{{ request.user }}`에 대한 설명으로 **옳은** 것은?

- ① user만 쓸 수 있고 request.user는 템플릿에서 쓸 수 없다.
- ② request.user만 쓸 수 있고 user는 context로 넘겨야 한다.
- ③ 둘 다 현재 사용자를 가리키며 템플릿에서 바로 쓸 수 있다.
- ④ user는 로그인 사용자, request.user는 비로그인 사용자를 뜻한다.

---

### 26. 다음 코드로 로그아웃 버튼을 누르면 어떻게 되는가?

```python
from django.contrib.auth import logout

def logout(request):
    logout(request)
    return redirect('articles:index')
```

- ① 자기 자신을 계속 호출해 RecursionError
- ② 정상적으로 로그아웃되고 index로 이동한다.
- ③ 인자 개수가 맞지 않아 TypeError가 난다.
- ④ 세션은 지워지지만 sessionid 쿠키는 남는다.

---

### 27. signup view에서 POST 요청이 유효성 검사에 **실패**하면 사용자가 보게 되는 화면은?

- ① 입력값이 모두 지워진 빈 회원가입 폼
- ② 입력값과 에러가 담긴 회원가입 폼
- ③ redirect된 index(메인) 페이지
- ④ 가입 정보로 채워진 로그인 페이지

---

### 28. UserCreationForm이 기본으로 보여주는 입력 필드는?

- ① username, password1, password2
- ② username, password, email
- ③ email, password1, password2
- ④ username, old_password, new_password1

---

### 29. `@login_required`가 붙은 게시글 update view에서 **남의 글** 수정을 막으려면?

- ① @login_required를 한 번 더 붙인다.
- ② @require_POST를 추가로 붙인다.
- ③ 템플릿에서 수정 버튼을 숨겨 접근을 막는다.
- ④ request.user가 작성자인지 view에서 확인한다.

---

### 30. accounts/views.py의 `from .forms import CustomUserCreationForm`에서 `.`이 가리키는 곳은?

- ① 프로젝트 최상위 폴더
- ② Django 내장 forms 모듈
- ③ settings.py가 있는 설정 폴더
- ④ 현재 앱(accounts) 폴더

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ③ | ① | ② | ① | ④ | ① | ② | ② | ③ | ② |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ④ | ③ | ① | ① | ③ | ③ | ④ | ② | ④ |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ① | ③ | ② | ③ | ① | ② | ① | ④ | ④ |

- **1. ③** 로그아웃은 세션만 지운다. User 객체 Delete는 회원 탈퇴.
- **2. ①** request.user도 AnonymousUser로 바뀐다. 비로그인 상태에서 호출해도 에러는 없다.
- **3. ②** 로그인 링크는 "페이지를 보여달라"(GET, 상태 변화 없음), 로그아웃은 "세션을 지워달라"(POST + CSRF).
- **4. ①** `from django.views.decorators.http import require_POST`. GET으로 오면 405 응답.
- **5. ④** 회원가입 = DB에 User 레코드를 새로 만드는 일.
- **6. ①** 입력 필드는 username, password1, password2. ②④는 AuthenticationForm 설명, ③은 Meta.model 문제로 불가.
- **7. ②** AUTH_USER_MODEL을 accounts.User로 바꿨으니 폼도 그 모델을 가리켜야 한다.
- **8. ②** Meta.model에는 모델 **클래스**가 와야 한다. get_user_model()은 현재 유저 모델 클래스를 반환하고, settings.AUTH_USER_MODEL은 'accounts.User'라는 **문자열**이라 여기엔 맞지 않다.
- **9. ③** 객체(인스턴스)가 아니라 모델 **클래스**를 반환한다. 현재 로그인한 사용자는 request.user.
- **10. ②** `class Meta:`로만 쓰면 부모 설정이 사라진다.
- **11. ④** save()는 유저를 만들기만 한다. 로그인은 save()가 돌려준 user로 auth_login을 따로 호출해야 한다.
- **12. ④** request.user = 지금 요청을 보낸 로그인 사용자. 탈퇴 대상이 항상 "나"라서 URL에 pk가 필요 없다.
- **13. ③** auth_logout ≠ request.user.delete().
- **14. ①** 강의 순서는 삭제 → 로그아웃. 순서를 바꾸려면 `user = request.user`로 미리 잡아 둔다.
- **15. ①** User는 True, AnonymousUser는 False. 데코레이터는 login_required.
- **16. ③** is_authenticated는 속성이라 괄호 없이 쓴다(DTL에선 괄호 호출 자체가 문법 오류). is_superuser는 관리자 여부, is_login이라는 속성은 없다.
- **17. ③** 로그인 상태(True)면 메인으로 돌려보낸다. ①은 비로그인 사용자를 로그인 페이지에 못 들어가게 만드는 꼴.
- **18. ④** login_required는 로그인 여부만 본다. 소유권(인가) 검사는 별도 로직이 필요하다.
- **19. ②** 화면 분기는 접근 제한이 아니다. view에 @login_required를 함께 붙여야 한다.
- **20. ④** AuthenticationForm에는 save()가 없다. 로그인은 기존 유저 확인 + auth_login.
- **21. ④** 기본 LOGIN_URL은 /accounts/login/이고, 원래 가려던 주소가 next 파라미터로 붙는다.
- **22. ①** is_authenticated는 True/False 값을 가진 속성이다. `True()`를 호출하는 꼴이라 'bool' object is not callable.
- **23. ③** 기본 폼의 Meta.model은 auth.User인데, 그 모델은 accounts.User로 교체되어 쓸 수 없다. 그래서 CustomUserCreationForm으로 model을 바꾼다.
- **24. ②** request.user가 AnonymousUser라 `delete()`가 NotImplementedError를 낸다. 탈퇴·수정 같은 기능에도 접근 제한이 필요한 이유.
- **25. ③** 기본 context processor(auth, request)가 둘 다 모든 템플릿에 넣어 준다.
- **26. ①** 아래의 def logout이 import한 logout을 덮어쓴다. 로그인 view는 인자가 2개라 TypeError, 로그아웃은 인자가 1개로 맞아서 무한 재귀 — 짝으로 기억.
- **27. ②** context·render가 if/else 바깥이라 실패한 form이 그대로 렌더링된다(6단원 통합 view 구조).
- **28. ①** password2는 확인용. old_password는 PasswordChangeForm의 필드다.
- **29. ④** login_required는 "로그인했는가"(인증)만 본다. "이 글을 고칠 수 있는가"(인가)는 직접 검사해야 한다.
- **30. ④** 명시적 상대 경로. admin.py의 `from .models import Article`과 같은 원리.
