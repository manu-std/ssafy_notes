# Django 8단원 CBT — Auth 01 · 쿠키·세션·로그인 (30문항)

> 출제 범위: [`../08_auth_cookie_session_login.md`](../08_auth_cookie_session_login.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. HTTP의 무상태(stateless) 특징에 대한 설명으로 **옳은** 것은?

- ① 서버가 이전 요청의 로그인 정보를 자동으로 기억한다.
- ② 각 요청이 독립적이라 서버가 이전 요청을 기억하지 못한다.
- ③ 응답 후에도 연결을 계속 유지한다.
- ④ 클라이언트와 서버가 상태 정보를 HTTP 헤더에 영구 저장한다.

---

### 2. 서버가 브라우저에 쿠키를 저장하도록 지시할 때 사용하는 응답 헤더는?

- ① `Cookie`
- ② `Set-Cookie`
- ③ `Session-Id`
- ④ `Authorization`

---

### 3. 쿠키에 대한 설명으로 **옳은** 것은?

- ① 브라우저에 저장되고, 이후 요청에 자동으로 함께 전송된다.
- ② 서버의 DB 테이블에 저장되는 사용자 데이터다.
- ③ 브라우저에 저장되므로 비밀번호를 보관하기에 안전하다.
- ④ 만료 설정과 무관하게 브라우저를 닫아도 영구 유지된다.

---

### 4. 쿠키 속성과 효과의 연결로 **옳지 않은** 것은?

- ① Secure — HTTPS 연결에서만 전송
- ② HttpOnly — JavaScript(document.cookie)로 읽지 못하게 함
- ③ HttpOnly — 네트워크 요청에 쿠키가 실려 가는 것을 막음
- ④ SameSite — 다른 사이트에서 시작된 요청에 쿠키 전송을 제한

---

### 5. Django 기본 설정에서 세션 데이터가 저장되는 곳은?

- ① 브라우저의 localStorage 저장소
- ② DB의 `django_session` 테이블
- ③ settings.py의 SESSION 설정 값
- ④ 브라우저의 sessionid 쿠키 값 안

---

### 6. 세션 기반 로그인에서 브라우저가 쿠키로 보관하는 것은?

- ① sessionid (세션을 찾는 키)
- ② 사용자의 비밀번호
- ③ 사용자 정보 전체
- ④ django_session 테이블

---

### 7. 로그인 상태 유지 흐름을 순서대로 나열한 것은?

```text
가. 브라우저가 이후 요청마다 sessionid 쿠키를 함께 보낸다.
나. 로그인 성공 시 서버가 세션을 생성해 DB에 저장한다.
다. 서버가 sessionid로 세션을 찾아 request.user에 User 객체를 넣는다.
라. 응답에 sessionid 쿠키를 담아 브라우저로 보낸다.
```

- ① 가 → 나 → 다 → 라
- ② 나 → 라 → 가 → 다
- ③ 나 → 다 → 라 → 가
- ④ 라 → 나 → 가 → 다

---

### 8. 인증(Authentication)과 인가(Authorization)에 대한 설명으로 **옳은** 것은?

- ① 인증은 권한 확인, 인가는 본인 확인이다.
- ② 둘은 같은 개념을 부르는 다른 이름이다.
- ③ 로그인에 성공하면 모든 데이터에 대한 인가가 자동으로 주어진다.
- ④ 인증은 '누구인가', 인가는 '무엇을 할 수 있는가'를 확인한다.

---

### 9. 프로젝트 초기에 Custom User 모델을 만드는 이유로 가장 적절한 것은?

- ① 기본 User 모델만으로는 로그인 기능을 구현할 수 없어서
- ② Custom User를 쓰면 비밀번호를 해싱할 필요가 없어져서
- ③ 나중에 유저 모델을 확장하기 쉽게 하려고
- ④ Custom User를 쓰면 이후 migrate를 하지 않아도 되어서

---

### 10. 기본 User의 필드와 기능을 그대로 유지하면서 Custom User를 만들 때 상속하는 클래스는?

- ① `models.Model`
- ② `AbstractBaseUser`
- ③ `AbstractUser`
- ④ `UserCreationForm`

---

### 11. `AUTH_USER_MODEL = 'accounts.User'`에 대한 설명으로 **옳은** 것은?

- ① accounts는 앱 이름, User는 모델 클래스 이름이다.
- ② accounts는 모델 이름, User는 앱 이름이다.
- ③ 이 설정의 기본값이 'accounts.User'다.
- ④ 첫 migrate 이후에도 언제든 자유롭게 바꿔도 문제없다.

---

### 12. AUTH_USER_MODEL을 첫 migrate 전에 설정해야 하는 이유는?

- ① settings.py는 migrate 후 수정할 수 없어서
- ② 첫 migrate 전에만 createsuperuser를 쓸 수 있어서
- ③ migrate 후에는 accounts 앱을 만들 수 없어서
- ④ 중간에 바꾸면 테이블·외래키·migration 의존성이 꼬여 매우 복잡해져서

---

### 13. 로그인을 '세션' 관점에서 표현한 것으로 옳은 것은?

- ① User 객체를 Create
- ② 세션을 Delete
- ③ User 객체를 Update
- ④ 세션을 Create

---

### 14. AuthenticationForm에 대한 설명으로 **옳지 않은** 것은?

- ① 로그인 입력을 받는 built-in Form이다.
- ② 이미 있는 유저인지 확인하는 용도라 save()가 없다.
- ③ ModelForm이라 save()로 로그인 세션을 만든다.
- ④ 생성자의 첫 번째 인자로 request를 받는다.

---

### 15. 로그인 POST 처리에서 AuthenticationForm을 생성하는 코드로 옳은 것은?

- ① `AuthenticationForm(request, request.POST)`
- ② `AuthenticationForm(request.POST)`
- ③ `AuthenticationForm(request.POST, request)`
- ④ `AuthenticationForm(instance=request.user)`

---

### 16. `AuthenticationForm(request.POST)`로 잘못 작성했을 때 일어나는 일은?

- ① 정상적으로 로그인되고 index로 redirect된다.
- ② request 인자가 없다는 TypeError가 나서 500 에러 페이지가 뜬다.
- ③ "아이디나 비밀번호가 틀렸다"는 에러 메시지가 폼에 표시된다.
- ④ unbound form이 되어 is_valid()가 항상 False다.

---

### 17. 로그인 view에서 빈칸에 들어갈 코드는?

```python
if form.is_valid():
    auth_login(request, _______)
    return redirect('articles:index')
```

- ① `form.save()`
- ② `request.user`
- ③ `form.get_user()`
- ④ `form.cleaned_data`

---

### 18. `from django.contrib.auth import login as auth_login`처럼 별칭을 쓰는 이유는?

- ① view 이름도 login이라 view가 자기 자신을 호출하게 되어서
- ② auth_login이 login보다 세션을 더 빠르게 만들어 주어서
- ③ Django 5.x부터 login이라는 이름이 deprecated되어서
- ④ 별칭을 써야 세션이 DB에 저장되기 때문에

---

### 19. view에서 context로 넘기지 않았는데 템플릿에서 `{{ user.username }}`을 쓸 수 있는 이유는?

- ① AUTH_USER_MODEL 설정이 템플릿에 user를 자동으로 넣어 주어서
- ② login() 함수가 모든 템플릿 파일에 user 변수를 써 넣어서
- ③ DTL이 렌더링할 때마다 DB에서 user를 직접 조회해서
- ④ auth context processor가 모든 템플릿에 user를 넣어 줘서

---

### 20. 로그인하지 않은 상태에서 `request.user`의 값은?

- ① `None`
- ② `AnonymousUser`
- ③ 빈 User 객체(pk=0)
- ④ 에러 발생

---

## 함정 문제 (21~30)

### 21. HTTP의 특징이 **아닌** 것은?

- ① Stateful
- ② Stateless
- ③ Connectionless
- ④ 요청-응답 구조

---

### 22. 쿠키의 주된 사용 목적이 **아닌** 것은?

- ① 데이터를 영구 보관하는 DB 역할
- ② 로그인 상태를 유지하는 세션 관리
- ③ 테마·언어 같은 사용자 개인화 설정
- ④ 사이트 방문 기록 같은 행동 트래킹

---

### 23. Django 기본 User 모델에 **없는** 필드는?

- ① `username`
- ② `is_superuser`
- ③ `date_joined`
- ④ `phone_number`

---

### 24. "응답을 보낸 뒤 연결을 끊는" HTTP의 특성을 뜻하는 것은?

- ① Stateless
- ② Connectionless
- ③ Stateful
- ④ Persistent cookie

---

### 25. `AUTH_USER_MODEL = 'accounts.User'`만 설정하고 accounts 앱을 INSTALLED_APPS에 **등록하지 않으면**?

- ① 등록되지 않은 모델을 가리켜 에러가 난다.
- ② AUTH_USER_MODEL이 앱 등록을 대신해 정상 동작한다.
- ③ 자동으로 기본 auth.User가 대신 쓰인다.
- ④ migrate할 때 accounts 앱이 자동으로 등록된다.

---

### 26. 로그인 view 코드 중 **로그인 세션을 실제로 만드는** 것은?

- ① `form.is_valid()`
- ② `form.get_user()`
- ③ `auth_login(request, user)`
- ④ `redirect('articles:index')`

---

### 27. 쿠키와 세션의 **공통 목적**은?

- ① 비밀번호를 암호화해 저장하기 위해
- ② 서버 부하를 여러 서버로 분산하기 위해
- ③ 상태 정보를 유지하고 사용자를 식별하기 위해
- ④ 데이터베이스를 백업하기 위해

---

### 28. Custom User를 Django 기본 사용자 관리 화면(UserAdmin)으로 Admin에 등록하는 코드는?

- ① `admin.site.register(User)`
- ② `admin.site.register(User, UserAdmin)`
- ③ `admin.site.register(UserAdmin)`
- ④ `admin.register(User, AUTH_USER_MODEL)`

---

### 29. Expires나 Max-Age 없이 발급된 쿠키는 언제 사라지는가?

- ① 서버가 삭제할 때까지 영구히 유지된다.
- ② 발급 1시간 뒤 자동으로 삭제된다.
- ③ 다음 요청부터는 전송되지 않는다.
- ④ 브라우저를 닫으면(세션 종료) 삭제된다.

---

### 30. 크롬에서 로그인한 상태로 같은 사이트를 시크릿 창으로 열면 로그인되어 있지 않다. 이유는?

- ① 서버가 브라우저 종류별로 세션을 금지해서
- ② Django가 한 계정당 하나의 세션만 허용해서
- ③ CSRF 토큰이 창마다 달라 403이 나서
- ④ 새 창에는 sessionid 쿠키가 없어서

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ② | ② | ① | ③ | ② | ① | ② | ④ | ③ | ③ |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ① | ④ | ④ | ③ | ① | ④ | ③ | ① | ④ | ② |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ① | ① | ④ | ② | ① | ③ | ③ | ② | ④ | ④ |

- **1. ②** 그래서 로그인 상태를 유지하려면 쿠키와 세션이 필요하다. ③은 비연결 지향(connectionless)과 반대.
- **2. ②** 서버는 Set-Cookie로 내려주고, 브라우저는 이후 요청에 Cookie 헤더로 함께 보낸다.
- **3. ①** 쿠키는 클라이언트(브라우저) 쪽 저장소라 민감 정보를 넣으면 안 된다. 세션 쿠키는 브라우저를 닫으면 사라진다.
- **4. ③** HttpOnly는 스크립트 접근만 막는다. 요청에는 정상적으로 실려 간다.
- **5. ②** 세션은 서버 쪽(기본 DB) 저장소, 브라우저는 그 세션을 찾는 열쇠(sessionid)만 쿠키로 들고 있다.
- **6. ①** 쿠키 = 보관함 번호표, 세션 = 서버의 보관함.
- **7. ②** 세션 생성 → 쿠키 발급 → 브라우저가 매 요청에 첨부 → 서버가 세션 조회로 사용자 판별.
- **8. ④** 로그인 = 인증. 로그인했다고 남의 글을 수정할 권한(인가)까지 생기는 건 아니다.
- **9. ③** 기본 User는 필드가 정해져 있어 확장이 어렵다. 처음부터 내 User로 갈아 끼워 두는 것이 권장된다.
- **10. ③** AbstractUser는 기본 User 기능 전체를 포함. AbstractBaseUser는 최소 기능만 있어 필드·매니저를 직접 설계해야 한다.
- **11. ①** 형식은 '앱이름.모델클래스명'. 기본값은 'auth.User'이며 첫 migrate 전에 설정해야 한다.
- **12. ④** 학습 환경에서는 db.sqlite3와 migration 파일을 지우고 다시 하는 식으로 초기화하지만, 운영 DB에서는 금지.
- **13. ④** 로그인 = 세션 Create, 로그아웃 = 세션 Delete, 회원가입 = User Create.
- **14. ③** AuthenticationForm은 ModelForm이 아니다. 세션은 auth_login()이 만든다.
- **15. ①** 생성자가 `__init__(self, request=None, *args, **kwargs)`. 첫 인자가 request, 그다음이 data.
- **16. ④** 에러 메시지도 없이 로그인이 안 되는 게 특징이라 찾기 어렵다. 헷갈리면 `AuthenticationForm(request, data=request.POST)`.
- **17. ③** get_user()는 is_valid()를 통과한 유저 객체를 반환한다. 반드시 is_valid() 다음에 호출.
- **18. ①** 같은 이름을 다시 정의하면 마지막 것만 남는다 → TypeError: login() takes 1 positional argument but 2 were given.
- **19. ④** settings.py TEMPLATES의 context_processors에 `django.contrib.auth.context_processors.auth`가 기본 포함되어 있다.
- **20. ②** 그래서 템플릿에서 `Hello, {{ user.username }}`이 `Hello,`만 보인다.
- **21. ①** HTTP는 무상태(Stateless)·비연결 지향(Connectionless). 강의 확인문제 1번.
- **22. ①** 쿠키는 작은 데이터 조각이다. DB를 대신하지 않는다. 강의 확인문제 3번.
- **23. ④** 이런 필드가 필요해질 수 있어서 처음부터 Custom User로 시작한다. 강의 확인문제 6번.
- **24. ②** Connectionless = 연결을 유지하지 않음, Stateless = 이전 요청 상태를 기억하지 않음. 비슷해 보여도 다른 개념.
- **25. ①** AUTH_USER_MODEL은 유저 모델 지정, INSTALLED_APPS는 앱 등록 — 둘 다 해야 한다. 빠지면 ImproperlyConfigured.
- **26. ③** is_valid는 검증, get_user는 유저 꺼내기, redirect는 이동. 세션 생성은 login() 함수.
- **27. ③** 둘 다 Stateless한 HTTP의 한계를 보완한다. 강의 확인문제 12번.
- **28. ②** `from django.contrib.auth.admin import UserAdmin` 후 모델과 함께 등록한다.
- **29. ④** 이런 쿠키를 session cookie라 한다. 기간을 지정하면 persistent cookie.
- **30. ④** 서버는 sessionid 쿠키로 사용자를 알아본다. 쿠키 저장소가 분리된 창에서는 보낼 sessionid가 없다.
