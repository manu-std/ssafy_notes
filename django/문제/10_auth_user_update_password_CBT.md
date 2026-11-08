# Django 10단원 CBT — Auth 03 · 회원정보·비밀번호·해시 (30문항)

> 출제 범위: [`../10_auth_user_update_password.md`](../10_auth_user_update_password.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. 회원정보 수정에 사용하는 Django 내장 폼은?

- ① `AuthenticationForm`
- ② `UserCreationForm`
- ③ `PasswordChangeForm`
- ④ `UserChangeForm`

---

### 2. CustomUserChangeForm에서 Meta.fields를 지정해야 하는 이유로 가장 적절한 것은?

- ① fields를 지정하지 않으면 폼이 화면에 렌더링되지 않아서
- ② fields를 지정해야 저장할 때 비밀번호가 해시되어서
- ③ fields가 없으면 instance=request.user를 쓸 수 없어서
- ④ is_superuser 같은 관리자용 필드까지 노출되어서

---

### 3. 회원정보 수정(POST)에서 폼을 생성하는 코드로 옳은 것은?

- ① `CustomUserChangeForm(request.POST, instance=request.user)`
- ② `CustomUserChangeForm(request, request.POST)`
- ③ `CustomUserChangeForm(request.POST, user=request.user)`
- ④ `CustomUserChangeForm(data=request.user, instance=request.POST)`

---

### 4. 회원정보 수정 view에서 `instance=request.user`를 넣는 이유로 **옳지 않은** 것은?

- ① GET에서 기존 사용자 정보를 폼에 미리 채우기 위해
- ② POST에서 save() 시 새 User가 아니라 기존 User를 수정하기 위해
- ③ instance를 넣으면 유효성 검사 없이 바로 저장되기 때문에
- ④ 수정 대상을 현재 로그인한 사용자로 고정하기 위해

---

### 5. 회원정보 수정 URL(`accounts/update/`)에 pk가 없어도 되는 이유는?

- ① Django가 URL 끝에 pk를 자동으로 붙여 주기 때문에
- ② 회원정보 수정은 POST 없이 GET 요청만 사용해서
- ③ User 모델에는 기본키(pk) 필드가 존재하지 않아서
- ④ 수정 대상이 항상 request.user라서

---

### 6. PasswordChangeForm에 대한 설명으로 **옳은** 것은?

- ① 기존 비밀번호 확인이 포함된 비밀번호 변경용 Form이다.
- ② ModelForm이므로 첫 번째 인자로 data(request.POST)를 받는다.
- ③ 기존 비밀번호를 몰라도 새 비밀번호만 입력하면 변경된다.
- ④ 회원가입 시 입력한 비밀번호를 해시해 저장하는 폼이다.

---

### 7. 비밀번호 변경(POST)에서 폼을 생성하는 코드로 옳은 것은?

- ① `PasswordChangeForm(request.POST)`
- ② `PasswordChangeForm(request, request.POST)`
- ③ `PasswordChangeForm(request.POST, instance=request.user)`
- ④ `PasswordChangeForm(request.user, request.POST)`

---

### 8. 비밀번호 변경 후 아무 처리도 하지 않으면 로그아웃되는 이유는?

- ① 세션에 저장된 인증 해시가 바뀐 비밀번호와 맞지 않아 세션이 무효 처리되어서
- ② PasswordChangeForm.save()가 내부적으로 logout()을 호출해서
- ③ 비밀번호가 바뀌면 User 객체가 삭제되었다가 다시 생성되어서
- ④ 브라우저가 비밀번호 변경을 감지해 쿠키를 지워서

---

### 9. 비밀번호 변경 후 현재 세션의 로그인을 유지하기 위해 Django가 제공하는 함수로, 빈칸에 들어갈 코드는?

```python
if form.is_valid():
    user = form.save()
    _______
    return redirect('articles:index')
```

- ① `auth_logout(request)`
- ② `request.session.flush()`
- ③ `update_session_auth_user(request, user)`
- ④ `update_session_auth_hash(request, user)`

---

### 10. 인증 관련 폼과 생성자 **첫 번째 인자**의 연결로 **옳지 않은** 것은?

- ① AuthenticationForm — request
- ② PasswordChangeForm — request
- ③ UserCreationForm — data
- ④ UserChangeForm — data

---

### 11. 비밀번호를 저장할 때 해싱을 사용하는 이유로 가장 적절한 것은?

- ① 키만 있으면 언제든 원래 비밀번호로 복호화할 수 있어서
- ② Base64처럼 규칙만 알면 누구나 되돌릴 수 있어서
- ③ 역연산이 어려워 유출돼도 원문을 바로 알 수 없어서
- ④ 해시값의 길이가 비밀번호 길이에 따라 달라져 추측이 어려워서

---

### 12. 인코딩·암호화·해싱에 대한 설명으로 **옳은** 것은?

- ① 인코딩은 키가 있어야만 원래대로 복원할 수 있다.
- ② 암호화는 키를 사용하며, 올바른 키로 복호화할 수 있다.
- ③ 해싱은 키를 사용해 언제든 원문으로 되돌릴 수 있다.
- ④ Base64는 비밀번호 보호에 적합한 암호화 방식이다.

---

### 13. 암호학적 해시 함수의 특징이 **아닌** 것은?

- ① 같은 입력은 항상 같은 출력을 낸다.
- ② 해시값으로 원래 입력값을 쉽게 알아낼 수 있다.
- ③ 입력이 조금만 달라져도 출력이 크게 달라진다.
- ④ 입력 길이와 상관없이 출력 길이가 고정된다.

---

### 14. SHA-256 해시값을 16진수로 표현했을 때의 길이는?

- ① 32자리
- ② 128자리
- ③ 64자리
- ④ 256자리

---

### 15. 레인보우 테이블 공격을 무력화하는 데 핵심적인 기술은?

- ① Key Stretching
- ② CAPTCHA
- ③ Salt
- ④ Base64 인코딩

---

### 16. Salt에 대한 설명으로 **옳은** 것은?

- ① 반드시 비밀로 숨겨야 하므로 DB에는 저장하면 안 된다.
- ② 사용자마다 달라서 같은 비밀번호도 해시가 달라진다.
- ③ 해시 연산을 수천 번 반복해 계산 비용을 늘리는 기술이다.
- ④ Salt만 있으면 무차별 대입 공격도 완전히 막을 수 있다.

---

### 17. 무차별 대입(Brute-force) 공격의 효율을 낮추기 위해 해시 연산을 의도적으로 많이 반복하는 기술은?

- ① Salt
- ② Key Stretching
- ③ Encoding
- ④ Rainbow Table

---

### 18. 강의 기준 Django의 기본 비밀번호 해싱 알고리즘은?

- ① `PBKDF2`
- ② `MD5`
- ③ `Base64`
- ④ `AES`

---

### 19. Django DB의 password 값 `pbkdf2_sha256$...$...$...`의 구성 요소가 **아닌** 것은?

- ① username
- ② iterations (반복 횟수)
- ③ salt
- ④ hash

---

### 20. 비밀번호 초기화 메일을 실제로 보내지 않고 개발 서버 콘솔에 출력하려 한다. 빈칸에 들어갈 설정 항목은?

```python
# settings.py
_______ = 'django.core.mail.backends.console.EmailBackend'
```

- ① `EMAIL_HOST`
- ② `AUTH_PASSWORD_VALIDATORS`
- ③ `EMAIL_BACKEND`
- ④ `DEBUG_EMAIL`

---

## 함정 문제 (21~30)

### 21. 비밀번호 변경 후 `update_session_auth_hash(request, user)`를 호출했다. 다른 기기에 로그인되어 있던 세션은?

- ① 모든 기기의 로그인이 그대로 유지된다.
- ② 현재 기기를 포함해 모든 기기가 로그아웃된다.
- ③ 다른 기기만 유지되고 현재 기기는 로그아웃된다.
- ④ 현재 세션만 유지, 다른 기기는 끊긴다.

---

### 22. 해시 함수에 대한 설명으로 **옳지 않은** 것은?

- ① 같은 입력이면 같은 해시가 나온다.
- ② 입력이 조금만 바뀌어도 해시가 크게 바뀐다.
- ③ 해시값만 보고 원래 입력을 알아내기는 어렵다.
- ④ 다른 입력이 같은 해시가 되는 일은 절대 없다.

---

### 23. `EMAIL_BACKEND`를 console.EmailBackend로 설정하고 비밀번호 초기화를 요청했다. **옳은** 것은?

- ① 실제 발송 없이 runserver 터미널에 메일 내용이 찍힌다.
- ② 사용자의 실제 메일함으로 재설정 메일이 발송된다.
- ③ 브라우저 개발자 도구의 Console 탭에 메일 내용이 출력된다.
- ④ settings.py의 EMAIL_HOST 서버로 메일이 전송된다.

---

### 24. 비밀번호 변경 view에서 `form.is_valid()`만 호출하고 `form.save()`를 빠뜨렸다. 결과는?

- ① 비밀번호는 바뀌지 않는다.
- ② 비밀번호가 바뀌고 로그아웃된다.
- ③ 비밀번호가 바뀌고 로그인이 유지된다.
- ④ 기존 비밀번호가 삭제되어 빈 값이 된다.

---

### 25. 기존 비밀번호를 **잊어버린** 사용자를 위한 기능과 본인 확인 수단의 연결로 **옳은** 것은?

- ① 비밀번호 변경 — 기존 비밀번호 입력
- ② 비밀번호 초기화 — 이메일로 받은 재설정 링크
- ③ 회원정보 수정 — UserChangeForm 입력
- ④ 비밀번호 초기화 — 기존 비밀번호 입력

---

### 26. 프로젝트 urls.py에 `path('accounts/', include('django.contrib.auth.urls'))`를 추가했을 때 비밀번호 초기화 페이지 주소는?

- ① `/password_reset/`
- ② `/auth/password_reset/`
- ③ `/accounts/password_reset/`
- ④ `/accounts/auth/password_reset/`

---

### 27. `AUTH_PASSWORD_VALIDATORS` 설정의 역할은?

- ① 비밀번호 해시 알고리즘을 지정한다.
- ② 비밀번호 초기화 메일의 발송 방식을 지정한다.
- ③ 짧거나 흔한 비밀번호를 막는 품질 검사
- ④ 로그인 실패 횟수를 세어 계정을 잠근다.

---

### 28. 비밀번호 초기화 화면에 **가입되지 않은** 이메일을 입력하면?

- ① 계정이 있을 때와 같은 안내 화면이 나온다.
- ② "존재하지 않는 이메일입니다" 에러가 표시된다.
- ③ 입력한 이메일로 새 계정이 자동 생성된다.
- ④ 관리자에게 대신 알림 메일이 발송된다.

---

### 29. Salt와 Key Stretching의 목적을 바르게 짝지은 것은?

- ① Salt — 무차별 대입 비용 증가 / Key Stretching — 레인보우 테이블 무력화
- ② Salt — 레인보우 테이블 무력화 / Key Stretching — 무차별 대입 비용 증가
- ③ Salt — 비밀번호 암호화 키 / Key Stretching — 복호화 속도 향상
- ④ 둘 다 해시 충돌을 완전히 없애기 위한 기술

---

### 30. 기능과 사용하는 Django 내장 폼의 연결로 **옳지 않은** 것은?

- ① 회원가입 — UserCreationForm
- ② 로그인 — AuthenticationForm
- ③ 비밀번호 변경 — UserChangeForm
- ④ 회원정보 수정 — UserChangeForm

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ④ | ① | ③ | ④ | ① | ④ | ① | ④ | ② |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ③ | ② | ② | ③ | ③ | ② | ② | ① | ① | ③ |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ④ | ① | ① | ② | ③ | ③ | ① | ② | ③ |

- **1. ④** UserChangeForm은 회원정보 수정용 built-in ModelForm. 강의 확인문제 1번.
- **2. ④** 사용자가 고쳐도 되는 필드(예: first_name, last_name, email)만 명시한다.
- **3. ①** ModelForm이라 첫 인자는 data(request.POST), 수정 대상은 instance=request.user. ④는 둘을 뒤바꿨다. GET일 땐 instance만.
- **4. ③** instance는 수정 대상을 지정할 뿐이다. 검증(is_valid)과 저장(save)은 그대로 거쳐야 한다.
- **5. ④** 이미 들고 있는 request.user를 그대로 쓰면 된다. 다시 조회할 필요도 없다.
- **6. ①** SetPasswordForm을 상속하고 기존 비밀번호 확인(old_password)을 추가한 Form. 첫 인자는 user.
- **7. ④** 생성자가 `__init__(self, user, *args, **kwargs)`. 기존 비밀번호 확인·새 비밀번호 저장의 대상이 user다.
- **8. ①** Django는 세션에 비밀번호 기반 해시를 함께 저장해 두고 요청마다 비교한다.
- **9. ④** 새 비밀번호 기준으로 현재 세션의 인증 해시를 갱신한다. 비슷한 이름(③)에 주의. 강의 확인문제 4번.
- **10. ②** PasswordChangeForm은 user가 먼저. "AuthenticationForm은 요청(request), PasswordChangeForm은 사람(user)".
- **11. ③** 로그인 때는 입력값을 똑같이 해싱해 해시끼리 비교하면 되므로 원문을 보관할 필요가 없다.
- **12. ②** 인코딩(UTF-8, Base64)은 규칙만 알면 복원, 암호화(AES)는 키로 복호화, 해싱(SHA-256)은 원칙적으로 역연산 불가.
- **13. ②** 결정성·일방향성·눈사태 효과·고정 길이. 강의 확인문제 6번.
- **14. ③** 256비트 = 32바이트, 16진수 한 자리는 4비트 → 256 ÷ 4 = 64자리.
- **15. ③** 사용자마다 다른 Salt를 붙이면 미리 계산해 둔 해시표가 쓸모없어진다. 강의 확인문제 7번.
- **16. ②** Salt는 비밀이 아니라 해시와 함께 저장된다. ③은 Key Stretching. 무차별 대입 방어는 Key Stretching의 몫.
- **17. ②** 후보 하나를 검사하는 비용을 크게 늘린다. 강의 확인문제 8번.
- **18. ①** PBKDF2 + SHA-256(저장 문자열 접두사 pbkdf2_sha256). Salt와 반복(키 스트레칭)을 모두 적용한다. 강의 확인문제 9번.
- **19. ①** 형식은 algorithm$iterations$salt$hash. 사용자 식별값은 다른 필드에 있다. 강의 확인문제 10번.
- **20. ③** EMAIL_BACKEND를 console 백엔드로 지정하면 메일 내용이 runserver 터미널에 출력된다. AUTH_PASSWORD_VALIDATORS는 비밀번호 품질 검사 설정. 강의 확인문제 11번.
- **21. ④** 이 함수는 **현재 요청의 세션**만 새 비밀번호 기준으로 갱신한다. 다른 세션은 해시가 맞지 않아 끊긴다(보안상 의도된 동작).
- **22. ④** 출력 길이가 고정이라 충돌은 원리상 가능하다. 다만 좋은 해시에서는 찾기가 극히 어렵다.
- **23. ①** 여기서 콘솔은 서버를 실행 중인 터미널이다. 브라우저 콘솔과 헷갈리지 말 것. 운영에선 SMTP 등 실제 백엔드가 필요하다.
- **24. ①** is_valid()는 검증만 한다. 새 비밀번호를 해싱해 저장하는 건 save().
- **25. ②** 변경(Change)은 기존 비밀번호를 아는 경우, 초기화(Reset)는 이메일 링크(토큰)로 본인을 확인한다.
- **26. ③** 내장 URL의 password_reset/ 앞에 include 접두사 accounts/가 붙는다.
- **27. ③** 해싱(PASSWORD_HASHERS)이나 이메일(EMAIL_BACKEND)과는 다른 설정이다.
- **28. ①** 계정이 있는지 없는지를 외부에 노출하지 않으려는 것. 메일 설정이 틀려도 화면은 똑같이 나오니 주의.
- **29. ②** 목적을 뒤바꾼 ①이 대표 함정. Salt는 비밀 키도 아니다.
- **30. ③** 비밀번호 변경은 PasswordChangeForm. 이름이 비슷한 UserChangeForm(정보 수정)과 헷갈리게 내는 유형.
