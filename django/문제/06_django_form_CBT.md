# Django 6단원 CBT — Django Form (30문항)

> 출제 범위: [`../06_django_form.md`](../06_django_form.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. `forms.Form`을 상속한 일반 Form이 해주는 일로 **옳지 않은** 것은?

- ① 입력받은 데이터를 DB 테이블에 자동으로 저장한다.
- ② 필드 정의를 바탕으로 input 태그를 자동 생성한다.
- ③ 필드 규칙에 따라 입력값을 검증한다.
- ④ 필드별 에러 메시지를 모아 템플릿에 출력할 수 있게 한다.

---

### 2. content 필드를 여러 줄 입력창(textarea)으로 표시하려면 빈칸에 무엇을 써야 하는가?

```python
class ArticleForm(forms.Form):
    title = forms.CharField(max_length=10)
    content = forms.CharField(_______)
```

- ① `type='textarea'`
- ② `widget=forms.Textarea`
- ③ `field=forms.TextField`
- ④ `attrs={'textarea': True}`

---

### 3. new view에서 빈 입력 양식을 템플릿에 넘기는 코드로 옳은 것은?

- ① `form = ArticleForm()` 후 `context = {'form': form}`
- ② `form = ArticleForm(request.POST)` 후 `context = {'form': form}`
- ③ `form = ArticleForm` 후 `context = {'form': form.save()}`
- ④ `context = {'form': 'ArticleForm'}`

---

### 4. 템플릿에 `{{ form }}`을 쓸 때, Form이 만들어 주지 않아 **직접 작성해야 하는 것**은?

- ① form 태그, csrf_token, 제출 버튼
- ② 각 필드의 `<label>`과 `<input>` 태그
- ③ 필드별 에러 메시지와 도움말(help text)
- ④ input의 name·id·required 속성

---

### 5. Form을 템플릿에 적용했는데 create view를 고치지 않아도 글 작성이 되던 이유는?

- ① Form이 내부적으로 DB 저장까지 자동으로 처리하기 때문에
- ② create view가 Form의 save()를 자동으로 호출하기 때문에
- ③ Form이 만든 input의 name이 기존 POST 키와 같아서
- ④ Form이 GET 요청을 POST로 바꿔서 보내 주기 때문에

---

### 6. Form과 ModelForm의 선택으로 **옳은** 것은?

- ① 로그인 폼 — ModelForm / 게시글 작성 — Form
- ② 검색 폼 — Form / 회원가입 — ModelForm
- ③ 게시글 작성 — Form / 회원가입 — Form
- ④ 검색 폼 — ModelForm / 로그인 — ModelForm

---

### 7. ModelForm이 필요한 이유로 가장 적절한 것은?

- ① Form보다 HTML 입력창을 더 보기 좋게 만들어 주기 때문에
- ② 일반 Form에서는 유효성 검사를 할 수 없기 때문에
- ③ 모델과 폼에 필드 정보를 중복 작성하는 문제를 없애려고
- ④ ModelForm을 쓰면 CSRF 토큰 없이도 POST를 보낼 수 있어서

---

### 8. ModelForm의 `class Meta`에 대한 설명으로 **옳지 않은** 것은?

- ① 어떤 모델과 연결할지(model)를 지정한다.
- ② 사용할 필드(fields) 또는 제외할 필드(exclude)를 지정한다.
- ③ 폼을 어떻게 만들지에 대한 설정 공간이다.
- ④ ModelForm이 Meta 클래스를 상속받아 기능을 물려받는 구조다.

---

### 9. Article 필드가 title, content, created_at(auto_now_add), updated_at(auto_now)일 때, 다음 ModelForm이 렌더링하는 입력 칸은?

```python
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('title',)
```

- ① title
- ② title, content
- ③ content, created_at, updated_at
- ④ content

---

### 10. `fields = '__all__'` 사용 시 보안상 주의할 점으로 옳은 것은?

- ① id 같은 자동 생성 필드도 입력 칸으로 함께 나온다.
- ② 나중에 추가된 모델 필드까지 폼에 자동 노출된다.
- ③ '__all__'을 쓰면 is_valid() 검사가 생략된다.
- ④ exclude와 함께 써야만 정상적으로 동작한다.

---

### 11. `is_valid()`에 대한 설명으로 **옳지 않은** 것은?

- ① 유효성 검사를 실행하고 결과를 Boolean으로 반환한다.
- ② 통과하면 검증된 값을 cleaned_data로 쓸 수 있다.
- ③ 실패하면 form.errors에 필드별 에러가 담긴다.
- ④ 실패해도 일단 DB에 저장된 뒤 에러 메시지만 표시된다.

---

### 12. ModelForm create view에서 유효성 검사에 **실패**했을 때 올바른 처리는?

- ① `ArticleForm()`을 새로 만들어 render한다.
- ② `redirect('articles:index')`로 목록에 보낸다.
- ③ 에러가 담긴 기존 form 객체를 그대로 render한다.
- ④ `form.save()`로 일단 저장한다.

---

### 13. 제목 input에 스페이스바로 공백만 입력하고 제출했을 때 일어나는 일은?

- ① 브라우저의 required 검사에 걸려 제출되지 않는다.
- ② 공백 문자열이 그대로 제목으로 저장되고 detail로 이동한다.
- ③ Django가 공백을 '제목 없음'으로 바꿔 저장한다.
- ④ 브라우저는 통과시키지만 Django가 빈 값 에러를 낸다.

---

### 14. `article = form.save(commit=False)`에 대한 설명으로 옳은 것은?

- ① DB에 저장한 뒤 반환값 없이 None을 돌려준다.
- ② DB에 저장하지 않은 모델 인스턴스를 반환한다.
- ③ 유효성 검사를 건너뛰고 곧바로 DB에 저장한다.
- ④ 저장을 취소하고 form의 입력값을 초기화한다.

---

### 15. `commit=False`를 쓰는 대표적인 상황은?

- ① 폼에 없는 필드(예: 작성자)를 코드로 채워 저장할 때
- ② 유효성 검사를 건너뛰고 빠르게 저장하고 싶을 때
- ③ GET 요청에서 기존 값이 채워진 빈 폼을 보여줄 때
- ④ 저장된 데이터를 DB에서 삭제하기 전에 확인할 때

---

### 16. 수정 페이지(GET)에서 기존 값이 채워진 폼을 만드는 코드는?

- ① `ArticleForm(article)`
- ② `ArticleForm(request.POST)`
- ③ `ArticleForm(instance=article)`
- ④ `ArticleForm(data=article)`

---

### 17. 수정 처리(POST)에서 `instance=article`을 빠뜨리고 `ArticleForm(request.POST)`로 저장하면?

- ① 기존 글의 제목과 내용이 정상적으로 수정된다.
- ② pk가 없어 IntegrityError가 발생하고 저장되지 않는다.
- ③ 기존 글은 그대로이고 새 글이 생긴다.
- ④ 기존 글이 삭제되고 같은 pk로 다시 저장된다.

---

### 18. GET/POST를 하나로 합친 create view에서 빈칸에 들어갈 조건은?

```python
def create(request):
    if _______:
        form = ArticleForm(request.POST)
        ...
```

- ① `request.POST`
- ② `request.method == 'POST'`
- ③ `request.method == POST`
- ④ `form.is_valid()`

---

### 19. 다음 통합 create view에 대한 설명으로 **옳지 않은** 것은?

```python
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)
```

- ① GET 요청이면 빈 폼을 render한다.
- ② POST에서 검증에 성공하면 detail로 redirect한다.
- ③ POST에서 검증에 실패하면 에러가 담긴 폼을 render한다.
- ④ 마지막 context와 render는 GET 요청일 때만 실행된다.

---

### 20. Form 렌더링 옵션에 대한 설명으로 **옳은** 것은?

- ① `{{ form.as_p }}`는 각 필드를 `<p>` 태그로 감싸 출력한다.
- ② `{{ form.as_table }}`은 `<table>` 태그까지 자동으로 만들어 준다.
- ③ `{{ form.as_ul }}`은 각 필드를 `<p>` 태그로 출력한다.
- ④ `{{ form.title.errors }}`는 title 필드의 input 태그를 출력한다.

---

## 함정 문제 (21~30)

### 21. 입력창에 placeholder나 class 같은 **HTML 속성**을 지정하는 곳은?

- ① widget의 `attrs`
- ② Meta의 `fields`
- ③ Meta의 `exclude`
- ④ 모델 필드의 `default`

---

### 22. widget과 attrs에 대한 설명으로 **옳지 않은** 것은?

- ① widget은 필드를 어떤 HTML 입력 요소로 그릴지 정한다.
- ② attrs는 그 입력 요소에 붙일 HTML 속성을 정한다.
- ③ widget을 바꿔도 DB 컬럼의 자료형은 바뀌지 않는다.
- ④ attrs는 ModelForm의 Meta 안에 반드시 작성해야 한다.

---

### 23. 일반 Form(forms.Form)에 대한 설명으로 **옳은** 것은?

- ① 유효성 검사는 ModelForm에서만 할 수 있다.
- ② 일반 Form에는 is_valid() 메서드가 없다.
- ③ is_valid()로 검증할 수 있지만 save()는 없다.
- ④ 검증 없이 입력값을 바로 DB에 저장한다.

---

### 24. ModelForm Meta의 fields·exclude에 대한 설명으로 **옳은** 것은?

- ① exclude에 넣은 필드는 DB 테이블에서도 삭제된다.
- ② fields에 적지 않은 필드는 모델 정의에서 사라진다.
- ③ exclude에 넣으면 그 필드의 유효성 검사만 꺼진다.
- ④ 모델 필드 중 무엇을 폼의 입력 칸으로 둘지만 정한다.

---

### 25. `form = ArticleForm(request.POST)`로 만든 form에 대한 설명으로 **옳은** 것은?

- ① 데이터가 없는 unbound form이라 빈 입력창만 보여준다.
- ② 사용자 입력이 담긴 bound form이다.
- ③ 이미 DB에 저장된 모델 인스턴스다.
- ④ instance를 넘기지 않아 생성 시 에러가 난다.

---

### 26. `form.is_valid()`가 True를 반환한 **직후**의 DB 상태는?

- ① 이미 새 글이 저장되어 있다.
- ② 아직 아무것도 저장되지 않았다.
- ③ 임시 테이블에 저장되어 있다.
- ④ commit=False 상태로 저장되어 있다.

---

### 27. is_valid()를 통과한 뒤 **검증된** title 값을 꺼내는 코드는?

- ① `form.title`
- ② `form.validated_data['title']`
- ③ `form.errors['title']`
- ④ `form.cleaned_data['title']`

---

### 28. 통합 update view에서 GET 요청일 때 `form = ArticleForm()`으로 instance 없이 만들면?

- ① 기존 값이 채워진 수정 폼이 나온다.
- ② 빈 폼이 나와 기존 내용이 보이지 않는다.
- ③ 수정 대상이 없어 에러가 발생한다.
- ④ 새 글 작성 페이지로 redirect된다.

---

### 29. `{{ form.as_table }}`로 폼을 출력할 때 필요한 것은?

- ① 아무것도 없다. table 태그까지 자동으로 만들어진다.
- ② Meta에 `table = True`를 설정해야 한다.
- ③ `<table>` 태그로 직접 감싸야 한다.
- ④ 각 필드의 widget을 Table로 바꿔야 한다.

---

### 30. 통합 create view에서 POST 요청이 is_valid()에서 **False**가 나왔다. 다음에 일어나는 일은?

- ① if를 빠져나와 에러가 담긴 form으로 render한다.
- ② else 블록으로 넘어가 빈 폼을 새로 만든다.
- ③ redirect로 detail 페이지에 이동한다.
- ④ 반환값이 없어 view가 None을 반환하며 에러가 난다.

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ① | ② | ① | ① | ③ | ② | ③ | ④ | ④ | ② |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ③ | ④ | ② | ① | ③ | ③ | ② | ④ | ① |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ① | ④ | ③ | ④ | ② | ② | ④ | ② | ③ | ① |

- **1. ①** 일반 Form에는 save()가 없다. DB 저장은 모델과 연결된 ModelForm의 기능이다.
- **2. ②** widget은 필드가 HTML에서 어떤 입력 요소로 그려질지 정한다. 겉모습만 바꿀 뿐 검증 규칙은 그대로.
- **3. ①** 데이터 없이 만든 unbound form을 context로 넘겨야 템플릿에서 `{{ form }}`으로 쓸 수 있다.
- **4. ①** `{{ form }}`은 필드(label·input·에러)만 그린다. form 태그·CSRF 토큰·submit 버튼은 그대로 직접 쓴다.
- **5. ③** 이 단계의 Form은 "HTML 대신 써주기"만 한다. 서버 검증은 is_valid()부터 시작된다.
- **6. ②** 기준은 "DB에 저장하는가". 검색·로그인은 저장하지 않으니 Form, 게시글·회원가입은 레코드가 생기니 ModelForm.
- **7. ③** 모델의 max_length를 바꾸고 폼 수정을 잊으면 둘이 어긋난다. ModelForm은 모델 정의를 보고 폼을 알아서 만든다.
- **8. ④** 클래스 안에 클래스가 있지만 상속 관계가 아니다. Meta는 설정 값을 적는 곳일 뿐.
- **9. ④** title은 제외했고, auto_now·auto_now_add 필드는 editable=False라 처음부터 폼 대상이 아니다. id도 마찬가지.
- **10. ②** 그래서 허용할 필드를 명시하는 쪽이 안전하다. 10단원 UserChangeForm에서 실제 문제가 된다.
- **11. ④** 검증에 실패하면 저장하지 않는다. 에러가 담긴 form을 다시 보여줄 뿐이다.
- **12. ③** 새 폼을 만들면 사용자가 입력한 값과 에러 메시지가 다 사라진다.
- **13. ④** 아예 비우면 브라우저 required가 먼저 막고, 공백만 넣으면 Django가 앞뒤 공백을 제거한 뒤 빈 값으로 판단한다.
- **14. ②** 객체만 만들어 두고 값을 더 채운 뒤 `article.save()`로 저장한다.
- **15. ①** 예: `article.user = request.user` 후 `article.save()`.
- **16. ③** instance로 수정 대상을 넘기면 기존 값이 채워진다. 손으로 value를 넣던 작업을 대신해 준다.
- **17. ③** save()는 instance가 없으면 생성(INSERT), 있으면 수정(UPDATE).
- **18. ②** 요청 메서드는 `request.method`에 문자열('GET', 'POST')로 담긴다.
- **19. ④** context·render는 if/else 바깥이라 GET과 "검증 실패한 POST"가 함께 쓴다.
- **20. ①** as_table은 `<tr>`만, as_ul은 `<li>`만 출력하므로 table·ul은 직접 감싸야 한다. `.errors`는 에러 메시지.
- **21. ①** `forms.TextInput(attrs={'class': 'my-title', 'placeholder': '...'})`. 강의 확인문제 9번.
- **22. ④** attrs는 widget에 넘기는 딕셔너리다. Meta의 필수 속성은 model과 fields(또는 exclude).
- **23. ③** 검증은 Form과 ModelForm 공통 기능. 모델과 연결된 save()만 ModelForm에 있다.
- **24. ④** fields/exclude는 폼 구성 설정일 뿐, 모델이나 DB 구조에는 영향이 없다.
- **25. ②** 데이터가 들어간(bound) 폼이라 is_valid()로 검사할 수 있다. 저장은 save()를 해야 일어난다.
- **26. ②** 검증과 저장은 별개다. is_valid()는 검사만 하고, 저장은 form.save()가 한다.
- **27. ④** 검증을 통과한 값은 cleaned_data에 담긴다. validated_data는 Django REST Framework(serializer)의 이름이라 헷갈리기 쉽다. form.errors는 에러 메시지.
- **28. ②** 수정 페이지는 GET에서도 `ArticleForm(instance=article)`이어야 기존 값이 채워진다.
- **29. ③** as_table은 `<tr>`만, as_ul은 `<li>`만 출력한다. 바깥 table·ul 태그는 직접 쓴다.
- **30. ①** else는 GET일 때만 실행된다. 검증 실패한 POST는 if 바깥의 context/render로 내려가 에러 메시지를 보여준다.
