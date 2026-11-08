# Django 06 — Django Form

> 📎 확인문제·예상문제·암기카드: [`시험대비/06_django_form_시험대비.md`](시험대비/06_django_form_시험대비.md)

*(5단원에서 `request.POST.get()`으로 손수 꺼내 저장하던 코드를 Form/ModelForm으로 바꾼다. 입력창 생성·검증·에러 표시·저장을 클래스 하나에 맡기고, 마지막엔 GET/POST를 view 하나로 합친다. 8~10단원의 인증 폼들도 전부 이 구조 위에 있다.)*

## 오늘의 목차

1. 왜 Form이 필요한가
2. Form class
3. Widgets
4. ModelForm
5. Meta class (fields / exclude)
6. ModelForm을 적용한 create — is_valid()
7. save()와 commit=False
8. ModelForm을 적용한 update — instance
9. HTTP 요청 다루기 — GET/POST를 하나의 view로
10. Form 렌더링 옵션과 필드 커스터마이징

---

## 1. 왜 Form이 필요한가

**Django Form은 사용자 입력을 받는 일 전체를 한 클래스에 맡기는 도구**
(HTML 입력창 만들기, 값 꺼내기, 검증하기, 에러 보여주기)

```python
# Form class 사용 전 코드
title = request.POST.get('title')
content = request.POST.get('content')
article = Article(title=title, content=content)
article.save()
```

1. 검증이 없음
2. 모델 제약과 화면이 따로 논다
3. 에러를 사용자에게 알려줄 방법이 없음
4. HTML 입력창을 손으로 써야 함

→ Form 클래스는 이 네 가지를 각각 해결할 수 있음

| 문제 | Form이 해주는 일 |
|---|---|
| 검증 없음 | 필드 규칙에 따라 자동 검사 |
| 모델 제약 미반영 | 모델 필드 정의를 그대로 가져와 규칙으로 사용 (ModelForm) |
| 에러 전달 불가 | 필드별 에러 메시지를 모아 템플릿에 출력 |
| HTML 수작업 | 필드 정의로 `<input>` 태그 자동 생성 |

> 📌 브라우저의 `required`, `maxlength` 속성은 편의 기능일 뿐이다. 개발자 도구로 지우면 그냥 통과되므로, **진짜 검증은 서버(Django Form)에서** 해야 한다.

---

## 2. Form class

- **Django Form**: 사용자 입력 데이터를 **수집하고, 처리 및 유효성 검사**를 수행하기 위한 도구

### Form class 정의

Form 클래스는 모델 클래스와 생김새가 거의 같다. 모델이 'DB 테이블의 설계도'라면, Form은 **입력 양식의 설계도**이다. 앱 폴더(`articles/`)에 `forms.py` 파일을 새로 만들고 그 안에 작성한다.

```python
# articles/forms.py
from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=10)
    content = forms.CharField(widget=forms.Textarea)
```

- `forms.Form` 상속: 모델과 무관하게 입력 폼을 구성
- `forms.CharField`는 **폼 입력값 검증용** 필드 — DB 컬럼을 정의하는 `models.CharField`와는 다른 클래스
- `created_at`, `updated_at`이 없는 이유: 사용자로부터 입력받는 값이 아니기 때문 (Form은 사용자 입력을 받기 위한 것)

> ⚠️ `forms.Form`에는 **save() 메서드가 없다**. DB 저장 기능은 ModelForm에만 있다.

### Form class를 적용한 new 로직

```python
# articles/views.py
from .forms import ArticleForm

def new(request):
    form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/new.html', context)
```

- `ArticleForm()`은 괄호 안에 데이터가 없으므로 **unbound form**(빈 양식) → 빈 입력창을 보여주는 것이 목적이므로 맞음
- 클래스를 만들어 두기만 해서는 화면에 나오지 않는다. **인스턴스를 만들고 context로 템플릿에 넘겨야** 템플릿에서 `form`이라는 이름으로 쓸 수 있다 (`Article.objects.all()`을 context로 넘기던 것과 같은 원리)
- `from .forms import ArticleForm`의 `.`은 `admin.py`의 `.models`와 같은 **명시적 상대 경로**

```html
<!-- articles/new.html -->
<form action="{% url 'articles:create' %}" method="POST">
  {% csrf_token %}
  {{ form }}
  <input type="submit">
</form>
```

- 손으로 쓰던 `<label>`과 `<input>`이 `{{ form }}` 한 줄로 바뀌었다
- `<form>` 태그, `{% csrf_token %}`, 제출 버튼은 **Form이 만들지 않으므로 그대로 남는다**
- `action`이 여전히 `create`를 가리킨다 → 이 단계에서는 아직 함수가 둘로 나뉘어 있음

### 왜 create view를 안 고쳤는데도 동작할까?

Form이 만든 입력창의 `name`이 `title`, `content`로, 기존 `request.POST.get('title')`의 키와 **정확히 같기 때문**이다.

다시 말해 이 단계에서 Form은 **"HTML 대신 써주기"만** 하고 있고, 서버 쪽 검증은 아직 일어나지 않는다. 진짜 검증은 6장의 `is_valid()`에서 시작된다.

---

## 3. Widgets

- **Widget**: Form 필드가 **HTML에서 어떻게 표현될지**(어떤 입력 요소로 그려질지) 지정
- `forms.CharField`의 기본 위젯은 `TextInput`(한 줄 `<input type="text">`) → 긴 글엔 `Textarea`로 교체

```python
content = forms.CharField(widget=forms.Textarea)
```

| 위젯 | 렌더링 결과 |
|---|---|
| `forms.TextInput` | 한 줄 입력 `<input type="text">` |
| `forms.Textarea` | 여러 줄 입력 `<textarea>` |

> ⚠️ 위젯은 **겉모습(HTML 표현)만** 바꾼다. 유효성 검사 규칙이나 DB 자료형이 바뀌는 게 아니다.

---

## 4. ModelForm

### Form과 ModelForm: 기준은 'DB에 저장하는가'

| Form | ModelForm |
|---|---|
| 사용자 입력 데이터를 **DB에 저장하지 않을 때** | 사용자 입력 데이터를 **DB에 저장해야 할 때** |
| 예: 검색, 로그인 | 예: 게시글 작성, 회원가입 |

둘 다 사용자 입력을 받는 폼을 만들고, 입력값을 검증하는 도구이다. 차이는 **입력받은 데이터를 어디까지 가져가는가**이다.

- **Form**: 입력을 받고 검증하고 끝난다. 검색어는 검색에 한 번 쓰고 버리고, 로그인 아이디·비밀번호는 기존 정보와 비교만 한다. DB에 새로 저장할 것이 없으므로 모델과 연결될 필요가 없다.
- **ModelForm**: 입력받은 데이터가 그대로 DB의 record가 된다. 게시글을 쓰면 Article 테이블에 한 줄이 추가되고, 회원가입을 하면 User 테이블에 한 줄이 추가된다. 그래서 특정 모델과 연결된 폼이 필요하다.

> 💡 **ModelForm = Form의 기능 전부 + '모델과 연결'(필드 자동 생성, save()) 기능**

### 왜 ModelForm이 필요할까: 기존 Form의 중복 문제

```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()

# forms.py (일반 Form 방식)
class ArticleForm(forms.Form):
    title = forms.CharField(max_length=10)
    content = forms.CharField(widget=forms.Textarea)
```

→ 같은 정보를 **두 번** 적고 있다. "title은 최대 10글자, content는 긴 글"이라는 정보가 모델에 이미 있는데 폼에 또 적었다.

나중에 모델에서 `max_length=10`을 `50`으로 바꾸고 폼 수정을 잊어버리면, DB는 50글자를 받을 수 있는데 폼은 10글자에서 막아 버린다. **두 곳의 정보가 어긋나는 것.**

ModelForm은 **"모델에 이미 적어 둔 정보를 보고 폼을 알아서 만들어라"라고** 지시해서 이 문제를 해결한다.

### ModelForm 정의

```python
# articles/forms.py
from django import forms
from .models import Article

# 상속받는 부모가 forms.Form → forms.ModelForm 으로 바뀜
# 모델을 읽어서 필드를 자동으로 생성하는 능력, save() 기능을 물려받게 됨
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
```

---

## 5. Meta class

- **ModelForm의 정보를 작성하는 곳**
- ModelForm 내부에서 **어떤 모델과 연결할지, 어떤 필드를 사용할지** 등을 정의하는 설정 공간 → 폼의 동작 방식을 제어하는 핵심 역할
- `class Meta:` — 클래스 안에 또 클래스가 있지만 **상속과는 관계가 없다**. 그저 ModelForm의 설정 값을 작성하는 곳일 뿐

### 전제: ModelForm이 하는 일

```python
# articles/models.py
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

`forms.ModelForm`을 상속하면 Django가 **모델을 보고 입력 칸을 자동으로 만들어 준다.** `CharField`는 한 줄 입력창, `TextField`는 큰 textarea가 되는 식이다. 폼 필드를 손으로 하나씩 다시 정의하지 않아도 된다.

다만 Django는 두 가지를 알아야 한다.

1. **어떤 모델**을 기반으로 만들지 → `model = Article`
2. 그 모델의 필드 중 **어떤 것을 입력 칸으로 보여줄지** → `fields` 또는 `exclude`

이 정보를 담는 곳이 Meta다. Meta는 폼의 입력 칸 자체가 아니라 "이 폼을 어떻게 만들지"에 대한 **설정표**다.

### fields: 포함할 필드를 직접 나열

```python
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title',)
```

- "Article 모델에서 **title만** 폼에 넣어라" → 화면에는 **title 입력 칸 하나만** 나옴
- 여러 개: `fields = ('title', 'content')` / 전부: `fields = '__all__'`

### exclude: 뺄 필드를 나열

```python
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('title',)
```

- "Article 모델의 필드 중 **title만 빼고 나머지 전부** 폼에 넣어라" → 화면에는 **content 입력 칸**이 나옴
- `fields`와 `exclude`는 방향만 반대. 보통 **둘 중 하나만** 쓴다

> 💡 그러면 `created_at`, `updated_at`도 나와야 하지 않을까?
>
> 나오지 않는다. `auto_now`, `auto_now_add`가 붙은 필드는 Django가 자동으로 값을 채우는 **수정 불가(`editable=False`) 필드**라서, 처음부터 폼 대상에서 빠진다. `id`도 마찬가지.
>
> 📌 `fields = '__all__'`은 나중에 모델에 필드가 추가되면 그것까지 자동으로 노출된다. 보안상 **허용할 필드를 명시**하는 쪽이 안전하다 (10단원 회원정보 수정에서 실제로 문제가 됨).

---

## 6. ModelForm을 적용한 create — is_valid()

```python
# articles/views.py
from .forms import ArticleForm

def create(request):
    # 1. 사용자 입력을 폼에 담기 (모델 폼이라 데이터를 통째로 받아도 알아서 필드에 매칭)
    form = ArticleForm(request.POST)
    # 2. 저장 전에 유효성 검사
    if form.is_valid():
        # 3-1. 통과하면 DB에 저장
        article = form.save()
        # 3-2. 저장 후 리다이렉트
        return redirect('articles:detail', article.pk)
    # 4. 통과 못 하면 입력 페이지를 에러 메시지와 함께 다시 보여줌
    context = {
        'form': form,
    }
    return render(request, 'articles/new.html', context)
```

### is_valid()

- **여러 유효성 검사를 실행하고, 데이터가 유효한지 여부를 Boolean으로 반환**
- 성공(True): 검증된 값을 `form.cleaned_data`로 쓸 수 있고 저장 가능
- 실패(False): `form.errors`에 필드별 에러가 담김 → 그 form을 그대로 템플릿에 넘기면 에러 메시지가 출력됨

### 공백 데이터가 유효하지 않은 이유와 에러 메시지가 출력되는 과정

- 모델 필드에는 별도로 명시하지 않아도 **기본적으로 빈 값을 허용하지 않는 제약 조건**(`blank=False`)이 설정되어 있음
- 빈 값은 `is_valid()`에 의해 False로 평가되고, form 객체에는 그에 맞는 에러 메시지가 포함되어 다음 코드(render)로 진행됨

> 📌 **TIP**: 아무것도 입력하지 않고 제출하면 Django보다 **브라우저가 먼저** "이 입력란을 작성하세요"라고 막는다 — Form이 input에 `required` 속성을 자동으로 붙여주기 때문. 반면 **스페이스바로 공백만** 입력하면 브라우저 검사는 통과하지만, Django가 앞뒤 공백을 제거한 뒤 빈 값으로 판단해 에러를 돌려준다.
>
> ⚠️ 검증 실패 시 `ArticleForm()`을 **새로 만들어 넘기면** 사용자가 입력한 값과 에러가 다 사라진다. 실패한 **그 form 객체**를 그대로 render해야 한다.

---

## 7. save()와 commit=False

- **save()**: 유효성 검사를 통과한 ModelForm 데이터를 **DB에 저장하고, 저장된 모델 인스턴스를 반환**
  - 그래서 `article = form.save()` 후 `article.pk`로 redirect할 수 있음
- ModelForm 생성 시 `instance`가 **없으면 생성(INSERT)**, **있으면 수정(UPDATE)** (8장)

### 제외한 필드의 값은 어떻게 채우는가? — commit=False

폼에서 뺀 필드라도 모델에서 필수(빈 값 불가)라면 저장할 때 값이 있어야 한다. 이 경우 `commit=False`로 **일단 객체만 만들고(DB 저장 X)**, 값을 직접 넣은 뒤 저장한다.

```python
form = ArticleForm(request.POST)
if form.is_valid():
    article = form.save(commit=False)  # DB에 아직 저장 안 함
    article.title = '자동 제목'         # 폼에서 뺀 필드를 코드로 채움
    article.save()                     # 이제 저장
```

> 💡 나중에 게시글 작성자(`user`)를 폼에서 입력받지 않고 **로그인한 사용자로 자동 지정**할 때 바로 이 패턴을 쓴다 (`article.user = request.user`).

---

## 8. ModelForm을 적용한 update — instance

```python
# articles/views.py
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm(instance=article)       # 기존 값이 채워진 폼
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/edit.html', context)


def update(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm(request.POST, instance=article)   # 입력값 + 수정 대상
    if form.is_valid():
        form.save()                                     # 기존 article을 UPDATE
        return redirect('articles:detail', article.pk)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/edit.html', context)
```

| 코드 | 의미 |
|---|---|
| `ArticleForm()` | 빈 폼 (작성 페이지) |
| `ArticleForm(request.POST)` | 입력값만 바인딩 → save() 시 **새 객체 생성** |
| `ArticleForm(instance=article)` | 기존 값이 채워진 폼 (수정 페이지) — 아직 바인딩 X |
| `ArticleForm(request.POST, instance=article)` | 입력값으로 **기존 객체 수정** → save() 시 UPDATE |

- `request.POST`는 첫 번째 위치 인자(`data`)라서 `ArticleForm(data=request.POST, instance=article)`과 같은 뜻
- edit 페이지에서 손으로 `value="{{ article.title }}"` 넣던 작업을 `instance`가 대신해 준다

> ⚠️ 수정할 때 `instance=article`을 **빼먹으면** save()가 기존 글을 고치는 게 아니라 **새 글을 하나 더 만든다**.

---

## 9. HTTP 요청 다루기 — GET/POST를 하나의 view로

### 문제

- new와 create, edit와 update는 **같은 데이터를 다루는 한 쌍**인데 함수와 URL이 둘씩 있다
- 그리고 5단원의 delete처럼 GET으로 접근해도 DB가 바뀌는 문제가 남아 있다

### 해결: 요청 메서드에 따라 분기

- **같은 URL**이라도 GET이면 "페이지 보여주기", POST면 "데이터 처리"
- `request.method`로 분기 (`'GET'`, `'POST'` 문자열)

### create 통합 (new + create)

```python
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)
```

| 요청 | 흐름 |
|---|---|
| GET `/articles/create/` | else → 빈 폼 → render |
| POST + 검증 성공 | 저장 → redirect |
| POST + 검증 실패 | if를 빠져나와 **에러가 담긴 form**으로 render |

> 💡 `context`와 `render`가 if/else **바깥**에 있는 이유: "GET"과 "검증에 실패한 POST"가 같은 코드(폼 페이지 보여주기)를 공유하기 때문. 이 구조는 로그인·회원가입 등 8~10단원에서 그대로 반복된다.

### update 통합 (edit + update)

```python
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)
```

- GET 수정: `instance=article`만 → 기존 값 표시
- POST 수정: `request.POST`와 `instance=article`을 **둘 다**

### URL·템플릿 변경

- `new/`, `edit/` URL 패턴과 view 제거 → `create/`, `<int:pk>/update/` 하나씩만 남김
- 링크·form action도 `articles:create`, `articles:update`로 수정, 템플릿 이름도 `create.html`, `update.html`로 정리

```python
# articles/urls.py
app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
]
```

---

## 10. Form 렌더링 옵션과 필드 커스터마이징

### 렌더링 옵션

| 문법 | 출력 형태 |
|---|---|
| `{{ form }}` | 기본 렌더링 |
| `{{ form.as_p }}` | 각 필드를 `<p>`로 감싸 출력 |
| `{{ form.as_ul }}` | 각 필드를 `<li>`로 출력 (`<ul>`은 직접 감싸야 함) |
| `{{ form.as_table }}` | 각 필드를 `<tr>`로 출력 (`<table>`은 직접 감싸야 함) |

### 필드 수동 렌더링

```html
<form method="POST">
  {% csrf_token %}
  <label for="{{ form.title.id_for_label }}">제목</label>
  {{ form.title }}
  {{ form.title.errors }}
  <label for="{{ form.content.id_for_label }}">내용</label>
  {{ form.content }}
  {{ form.content.errors }}
  <button type="submit">제출</button>
</form>
```

- `{{ form.필드명 }}`, `{{ form.필드명.label_tag }}`, `{{ form.필드명.errors }}`로 필드·레이블·에러를 따로 배치 가능

### 필드 재정의 — label, widget attrs, error_messages

```python
class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'my-title',
                'placeholder': 'Enter the title',
            }
        ),
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'cols': 50,
            }
        ),
        error_messages={'required': '내용을 입력해주세요.'},
    )

    class Meta:
        model = Article
        fields = '__all__'
```

| 구분 | 역할 |
|---|---|
| `widget` | 어떤 HTML 입력 요소로 그릴지 (TextInput, Textarea ...) |
| `attrs` | 그 요소에 붙일 HTML 속성 (class, placeholder, rows ...) |
| `label` | 화면에 보일 레이블 텍스트 |
| `error_messages` | 검증 실패 시 보여줄 메시지 |

> ⚠️ ModelForm에서 필드를 직접 재정의하면 모델에서 자동으로 가져오던 설정을 **그대로 물려받지 않는다**. 그래서 위처럼 `max_length=10` 같은 검증 조건을 다시 적어 줘야 할 수 있다.
