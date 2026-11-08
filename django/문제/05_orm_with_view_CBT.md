# Django 5단원 CBT — ORM with View (30문항)

> 출제 범위: [`../05_orm_with_view.md`](../05_orm_with_view.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. 단일 게시글 조회 코드에서 빈칸에 알맞은 것은?

```python
# urls.py
path('<int:pk>/', views.detail, name='detail')

# views.py
def detail(request, pk):
    article = _______
```

- ① `Article.objects.get(pk=pk)`
- ② `Article.objects.all(pk)`
- ③ `Article.objects.filter(pk)`
- ④ `Article.get(pk=pk)`

---

### 2. index.html에서 각 글 제목을 상세 페이지로 링크하는 코드로 옳은 것은? (app_name = 'articles')

- ① `<a href="{% url 'articles:detail' %}">{{ article.title }}</a>`
- ② `<a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>`
- ③ `<a href="{{ url 'articles:detail' article.pk }}">{{ article.title }}</a>`
- ④ `<a href="/articles/article.pk/">{{ article.title }}</a>`

---

### 3. Create 기능의 new와 create view 역할로 **옳은** 것은?

- ① new는 입력 페이지를 보여주고, create는 DB에 저장한다.
- ② new는 DB에 저장하고, create는 입력 페이지를 보여준다.
- ③ 둘 다 사용자가 입력한 데이터를 DB에 저장한다.
- ④ new는 전체 글 목록을, create는 상세 페이지를 보여준다.

---

### 4. GET과 POST의 비교로 **옳지 않은** 것은?

- ① GET은 주로 조회, POST는 주로 생성·수정·삭제에 쓴다.
- ② POST로 보낸 데이터는 자동으로 암호화되어 안전하다.
- ③ GET 데이터는 URL의 쿼리 스트링에 담긴다.
- ④ POST 데이터는 HTTP Body에 담긴다.

---

### 5. GET 방식의 특징으로 **옳은** 것은?

- ① HTTP 규격상 데이터 크기 제한이 없다.
- ② 요청 URL이 브라우저 히스토리에 남지 않는다.
- ③ 서버 상태를 변경하는 요청이라 캐싱이 불가능하다.
- ④ 같은 URL을 다시 요청하면 캐싱된 결과를 쓸 수 있다.

---

### 6. 강의 기준, HTML form의 method로 지정할 수 있는 HTTP 메서드는?

- ① GET, PUT
- ② GET, POST
- ③ POST, DELETE
- ④ GET, POST, PUT, DELETE

---

### 7. form을 POST로 바꾼 뒤 게시글을 작성하자 403 Forbidden이 발생했다. 이유는?

- ① URL 패턴이 존재하지 않아서
- ② view 함수에 문법 오류가 있어서
- ③ CSRF 토큰이 누락되어서
- ④ DB에 테이블이 없어서

---

### 8. HTTP 상태 코드와 의미의 연결로 **옳지 않은** 것은?

- ① 200 — 요청 성공
- ② 302 — 리다이렉션
- ③ 404 — 요청한 리소스를 찾을 수 없음
- ④ 403 — 서버 내부 오류

---

### 9. CSRF에 대한 설명으로 **옳은** 것은?

- ① 사용자 의도와 무관한 요청을 대신 보내게 만드는 공격이다.
- ② 입력창에 악성 SQL을 넣어 DB의 데이터를 탈취하는 공격이다.
- ③ 서버에 대량의 요청을 한꺼번에 보내 서비스를 마비시키는 공격이다.
- ④ 가능한 비밀번호를 하나씩 대입해 계정을 알아내는 공격이다.

---

### 10. `{% csrf_token %}`에 대한 설명으로 **옳지 않은** 것은?

- ① hidden input(`csrfmiddlewaretoken`)으로 토큰을 렌더링한다.
- ② 요청이 Django가 제공한 페이지에서 왔는지 확인하는 데 쓰인다.
- ③ POST form 안에 작성한다.
- ④ 전송되는 form 데이터를 암호화한다.

---

### 11. Django가 GET 요청에는 CSRF 토큰을 검사하지 않는 이유는?

- ① GET은 항상 HTTPS로만 전송되기 때문에
- ② GET 요청에는 쿠키가 전송되지 않기 때문에
- ③ GET은 서버 데이터를 바꾸지 않기로 약속된 요청이라서
- ④ GET은 CSRF 토큰을 쿼리 스트링에 자동으로 붙이기 때문에

---

### 12. 게시글 저장 후 render 대신 redirect를 쓰는 이유로 가장 적절한 것은?

- ① render는 POST 요청에서 사용할 수 없기 때문에
- ② redirect가 render보다 HTML을 더 빠르게 만들기 때문에
- ③ redirect를 쓰면 CSRF 토큰이 필요 없어지기 때문에
- ④ 완료 화면에서 새로고침했을 때 같은 POST가 다시 전송되는 것을 막기 위해

---

### 13. redirect()의 동작으로 **옳은** 것은?

- ① 서버가 detail view를 직접 호출해 HTML을 바로 응답한다.
- ② 클라이언트에게 HTML 없이 200 응답만 보낸다.
- ③ 클라이언트가 지정한 주소로 GET 요청을 다시 보내도록 응답한다.
- ④ 브라우저 히스토리를 모두 삭제한다.

---

### 14. 게시글 작성 후 개발자 도구 Network 탭에 보이는 요청 순서로 옳은 것은?

- ① detail/(200) → create/(302)
- ② create/(302) → 새 글의 detail/(200)
- ③ create/(200) → index/(200)
- ④ create/(403) → detail/(302)

---

### 15. 게시글 삭제 기능의 구현으로 가장 적절한 것은?

- ① POST form + `{% csrf_token %}`으로 요청하고, 삭제 후 index로 redirect
- ② `<a href="{% url 'articles:delete' article.pk %}">`로 요청하고 delete.html을 render
- ③ GET form으로 요청하고 삭제 후 detail로 redirect
- ④ POST form으로 요청하되 csrf_token 없이 보낸다.

---

### 16. 강의 초반의 다음 delete view가 가진 문제점은?

```python
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')
```

- ① 주소창에 URL을 직접 입력(GET)해도 삭제된다.
- ② 삭제 후 이미 지워진 글의 detail로 이동해 에러가 난다.
- ③ delete()는 QuerySet에서만 동작하므로 AttributeError가 난다.
- ④ form에 CSRF 토큰이 있으면 오히려 삭제되지 않는다.

---

### 17. 수정 페이지에서 기존 내용을 textarea에 출력하는 올바른 코드는?

- ① `<textarea name="content" value="{{ article.content }}"></textarea>`
- ② `<textarea name="content">{{ article.content }}</textarea>`
- ③ `<textarea name="content" placeholder="{{ article.content }}"></textarea>`
- ④ `<textarea name="{{ article.content }}"></textarea>`

---

### 18. 다음 update view가 실행된 후 DB에 저장된 제목은?

```python
def update(request, pk):
    article = Article.objects.get(pk=pk)
    article.title = request.POST.get('title')
    return redirect('articles:detail', article.pk)
```

- ① 새로 입력한 제목으로 바뀐다.
- ② 제목이 빈 값이 된다.
- ③ 새 글이 하나 더 생성된다.
- ④ 기존 제목 그대로다.

---

### 19. 없는 pk로 detail 요청이 왔을 때(`Article.objects.get(pk=pk)` 사용) 설명으로 옳은 것은?

- ① Django가 자동으로 404 Not Found 페이지를 응답한다.
- ② 빈 detail 페이지가 에러 없이 정상 출력된다.
- ③ DoesNotExist 예외가 난다. 404는 직접 처리해야 한다.
- ④ index 페이지로 자동 redirect되어 목록을 보여준다.

---

### 20. 캐싱에 대한 설명으로 **옳지 않은** 것은?

- ① 자주 쓰는 데이터나 결과를 임시 저장해 재사용하는 기술이다.
- ② 응답 속도를 높이고 서버 부하를 줄인다.
- ③ 원본 데이터가 바뀌어도 캐시는 자동으로 항상 최신 상태를 유지한다.
- ④ GET 요청의 결과는 캐싱할 수 있다.

---

## 함정 문제 (21~30)

### 21. form은 `method="POST"`인데 create view에서 `title = request.GET.get('title')`로 꺼냈다. title의 값은?

- ① POST 데이터가 GET으로 자동 변환되어 입력값이 들어간다.
- ② `None`
- ③ KeyError가 즉시 발생한다.
- ④ CSRF 검증에 실패해 403이 발생한다.

---

### 22. Update 기능의 edit와 update view 역할로 **옳은** 것은?

- ① edit는 DB를 수정하고, update는 기존 값이 채워진 페이지를 보여준다.
- ② 둘 다 DB에 저장된 데이터를 직접 수정한다.
- ③ edit는 기존 값이 채워진 페이지를 보여주고, update는 DB를 수정한다.
- ④ edit가 GET·POST를 모두 처리하므로 update는 필요 없다.

---

### 23. 삭제 요청을 보내려고 `<form method="DELETE">`로 작성했다. 실제로 어떻게 전송되는가?

- ① 브라우저가 지원하지 않는 값이라 GET으로 전송된다.
- ② DELETE 요청이 정상 전송되어 삭제된다.
- ③ Django가 DELETE를 POST로 바꿔 처리한다.
- ④ CSRF 토큰과 함께 DELETE 메서드로 전송된다.

---

### 24. 게시글 저장 후 `return redirect('articles:detail')`처럼 **pk 없이** 쓰면?

- ① pk를 생략했으니 `/articles/` 목록으로 이동한다.
- ② NoReverseMatch 에러가 난다.
- ③ 가장 최근에 작성한 글의 상세로 이동한다.
- ④ 같은 create 페이지를 다시 렌더링한다.

---

### 25. redirect()에 대한 설명으로 **옳지 않은** 것은?

- ① URL 이름과 인자를 받아 이동할 주소를 만들 수 있다.
- ② 기본적으로 302 상태 코드와 이동할 주소로 응답한다.
- ③ 클라이언트가 새 주소로 GET 요청을 다시 보내게 한다.
- ④ 그 전에 만든 객체를 DB에 자동 저장해 준다.

---

### 26. `{% csrf_token %}`을 빼먹은 POST form을 제출했을 때의 응답 상태 코드는?

- ① 403
- ② 404
- ③ 302
- ④ 500

---

### 27. POST로 게시글을 작성한 뒤, 전송된 title·content 값을 개발자 도구에서 확인할 수 있는 곳은?

- ① 주소창 URL 뒤의 쿼리 스트링
- ② 브라우저의 방문 기록(History)
- ③ Application 탭의 Cookies
- ④ Network 탭의 Payload

---

### 28. POST 방식의 특징으로 **옳은** 것은?

- ① 요청 URL과 데이터가 브라우저 히스토리에 남는다.
- ② 데이터가 HTTP Body에 담겨 URL에 드러나지 않는다.
- ③ 같은 요청은 캐싱된 결과로 빠르게 응답된다.
- ④ URL 길이 제한 때문에 대량 데이터 전송에 부적합하다.

---

### 29. CSRF 공격이 성공할 수 있는 핵심 원리는?

- ① 사용자가 비밀번호를 공격자에게 직접 알려 줘서
- ② 서버가 HTTPS를 쓰지 않고 HTTP로 통신해서
- ③ 공격자가 서버의 DB에 직접 접속할 수 있어서
- ④ 브라우저가 세션 쿠키를 자동으로 붙여서

---

### 30. 게시글 저장 후 `render(request, 'articles/create.html')`로 완료 페이지를 보여줬다. 이 페이지에서 새로고침(F5)하면?

- ① 화면만 다시 그려지고 아무 일도 없다.
- ② detail 페이지로 자동 이동한다.
- ③ 같은 POST가 다시 전송될 수 있다.
- ④ CSRF 토큰이 만료되어 항상 403이 난다.

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ① | ② | ① | ② | ④ | ② | ③ | ④ | ① | ④ |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ③ | ④ | ③ | ② | ① | ① | ② | ④ | ③ | ③ |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ② | ③ | ① | ② | ④ | ① | ④ | ② | ④ | ③ |

- **1. ①** 왼쪽 pk는 필드 이름, 오른쪽 pk는 URL에서 넘어온 변수. 매니저(objects)를 거쳐야 한다.
- **2. ②** detail URL에는 pk 변수가 있으므로 인자로 article.pk를 넘겨야 한다. url은 `{% %}` 태그.
- **3. ①** Create에는 view 두 개가 필요하다: 입력 페이지(new) + 저장 처리(create).
- **4. ②** POST는 주소창에 안 보일 뿐 암호화되지 않는다. 전송 중 보호는 HTTPS의 역할.
- **5. ④** ①②③은 POST의 특징. GET은 URL 길이 제한이 있고, 히스토리에 남고, 캐싱이 가능하다.
- **6. ②** HTML form은 GET과 POST만 지원한다. 그래서 지금은 생성·수정·삭제를 모두 POST로 처리한다(PUT·DELETE는 REST API에서).
- **7. ③** 403 = 요청은 전달됐지만 권한 때문에 거절. 메시지: CSRF verification failed. `{% csrf_token %}`을 넣으면 해결.
- **8. ④** 403은 Forbidden(권한 거부, 4xx 클라이언트 측 오류). 서버 내부 오류는 500(5xx).
- **9. ①** Cross-Site Request Forgery(사이트 간 요청 위조). 브라우저가 세션 쿠키를 자동으로 첨부하는 점을 악용한다.
- **10. ④** CSRF 토큰은 요청 출처 확인용이지 암호화 기능이 아니다.
- **11. ③** 그래서 GET으로 데이터를 바꾸도록 만들면 CSRF 보호를 받을 수 없다.
- **12. ④** 저장 후 GET 페이지로 보내면(PRG 패턴) 새로고침해도 GET만 다시 간다. 중복 게시물 방지.
- **13. ③** 서버가 직접 이동시키는 게 아니라 302 + 이동할 주소를 보내 클라이언트가 다시 요청하게 한다.
- **14. ②** [POST] create → 302 redirect → [GET] 새 글 상세 → 200.
- **15. ①** 삭제는 DB를 바꾸는 요청 → POST + CSRF. 삭제된 글의 detail로는 갈 수 없으니 목록으로.
- **16. ①** 요청 메서드를 확인하지 않아서다. 이후 `if request.method == 'POST':`로 POST일 때만 삭제하도록 고친다.
- **17. ②** textarea에는 value 속성이 없다. 여닫는 태그 사이에 값을 넣는다. (input은 value 속성 사용)
- **18. ④** save()가 빠졌다. 대입만으로는 메모리 속 객체만 바뀌고 DB는 그대로다.
- **19. ③** get()의 DoesNotExist는 자동으로 404가 되지 않는다(처리 안 하면 서버 에러).
- **20. ③** 원본이 바뀌면 캐시를 갱신·무효화해야 한다. 일관성 관리는 캐시의 단점이다.
- **21. ②** POST 데이터는 request.POST에 있다. request.GET에는 해당 키가 없으니 get()은 None. 그대로 저장하면 NOT NULL 제약 에러로 이어질 수 있다.
- **22. ③** new/create와 같은 구조. 보여주기(edit, GET) + 저장(update, POST).
- **23. ①** HTML form은 GET·POST만 지원한다. 잘못된 method 값은 기본값인 GET으로 처리된다.
- **24. ②** detail URL에는 `<int:pk>`가 있으므로 redirect에도 인자가 필요하다: `redirect('articles:detail', article.pk)`.
- **25. ④** 저장은 view가 save()로 먼저 해야 한다. redirect는 이동 응답을 만들 뿐.
- **26. ①** 403 Forbidden — CSRF verification failed. 요청은 도착했지만 거부된 것.
- **27. ④** POST 데이터는 HTTP Body에 담겨 URL에 안 보인다. Payload에서 csrfmiddlewaretoken, title, content를 확인할 수 있다.
- **28. ②** ①③④는 모두 GET의 특징이다.
- **29. ④** 위조된 요청에도 정상 인감도장(세션 쿠키)이 자동으로 찍혀 가는 게 문제. 그래서 페이지 출처를 증명하는 CSRF 토큰을 따로 요구한다.
- **30. ③** POST 결과를 render로 보여준 페이지에서 새로고침하면 같은 POST가 재전송되어 글이 중복 생성될 수 있다. 그래서 저장 후에는 redirect(POST-Redirect-GET).
