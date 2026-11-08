# Django 6단원 시험대비 — Django Form

> 📎 개념 정리 노트: [`../06_django_form.md`](../06_django_form.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

대상: SSAFY Django Form 강의 78장 (p001~p078) | 시험: 60분, 객관식·주관식·서술형 | 출제 가능성은 강의 강조도에 따른 추정이며 실제 시험 확정 범위는 아님.

## 0. 가장 먼저 보는 1분 요약

1. Form = 사용자 입력 수집·렌더링·유효성 검사. forms.Form 상속. 일반 Form에는 기본 save() 메서드가 없다.
2. ModelForm = Model과 연계된 Form. forms.ModelForm 상속, Meta.model과 Meta.fields 또는 Meta.exclude 설정. 기본 save() 가능.
3. is_valid() = 바인딩된 폼의 유효성 검사를 수행하여 True/False 반환. 검증 실패 시 form.errors에 오류가 남고, 저장되지 않는다.
4. form.save() = 유효성 검사를 통과한 ModelForm 데이터를 DB에 저장하고 모델 인스턴스를 반환(강의의 일반적인 흐름). **commit=False**는 아직 DB에 저장하지 않은 모델 인스턴스를 반환한다.
5. 수정은 instance=가 핵심: ArticleForm(request.POST, instance=article)가 기존 객체 변경에 해당. 생략하면 새 객체 생성 흐름이 될 수 있다.
6. 폼 표시 GET, 변경 저장 POST: request.method == 'POST'로 분기. POST에서는 request.POST를 입력으로 전달하고 검증한다.
7. widget ≠ attrs: widget은 입력 HTML 요소 표현 유형, attrs는 class·placeholder 등 HTML 속성을 지정.
8. **{{ form.as_p }}는** 각 필드를 &lt;p&gt;에 배치. {% csrf_token %}과 submit 버튼은 템플릿에서 별도로 작성한다.

## 1. 슬라이드별 핵심 지도

| 슬라이드 | 주제 | 출제 포인트 |
| --- | --- | --- |
| 1~5 | 학습 목표·도입 | 입력 데이터 검증 필요성 |
| 6~16 | Django Form, Form class | Form 상속, 필드 정의, new에서 Form 사용 |
| 17~19 | Widgets | forms.Textarea와 widget= |
| 20~29 | ModelForm·Meta | Form과 차이, model, fields, exclude |
| 30~36 | 생성·수정, is_valid() | request.POST, 오류 복원, instance |
| 37~40 | save() | 모델 저장, 생성/수정 결정 |
| 41~60 | HTTP 요청별 View 결합 | GET/POST, 생성·수정 단일 View, URL 수정 |
| 61~68 | 키워드 인자·위젯 응용 | data, instance, attrs, 필드 수동 렌더링 |
| 69 | 실습 | Form/ModelForm 실습 |
| 70~74 | 강의 확인문제 10개, 정답·해설 | 우선 복습 |
| 75~77 | 요약 | 필수 용어 |

## 2. 개념 정복

### 2-1. 왜 HTML form만으로 부족할까? ★★★

HTML form은 사용자가 내용을 입력해 서버로 제출할 수 있게 해주지만 서버 측 유효성 검사까지 자동 보장하지 않는다. 공백, 길이, 형식, 필수값 등의 검사를 서버에서 수행해야 한다. Django Form은 이를 위한 필드 정의, 검증, 오류 메시지와 HTML 렌더링기능을 제공한다. 브라우저의 required 속성은 편의 기능일 뿐 서버 검증의 대체가 아니다.

### 2-2. Form 클래스 정의 ★★★

```
# articles/forms.py
from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=10)
    content = forms.CharField(widget=forms.Textarea)
```

- forms.Form 상속: Model과 무관하게 입력 폼을 구성.
- forms.CharField: 폼 입력 필드의 검증을 담당한다. models.CharField는 DB 컬럼 정의에 사용하는 다른 클래스.
- max_length=10: 10자를 넘으면 유효성 검사에서 실패.
- widget=forms.Textarea: 기본 텍스트 입력 대신 &lt;textarea&gt;로 표현.
- forms.Form은 그 자체로 DB 자동 저장 기능을 제공하지 않는다.

```
# articles/views.py
from .forms import ArticleForm

def new(request):
    form = ArticleForm()
    return render(request, 'articles/new.html', {'form': form})

<!-- articles/new.html -->
<form action="{% url 'articles:create' %}" method="POST">
  {% csrf_token %}
  {{ form }}
  <input type="submit" value="저장">
</form>
```

꼭 구분: {{ form }}은 필드를 그려줄 뿐 &lt;form&gt; 태그, CSRF 토큰, 전송 버튼까지 모두 대신 만들어 주는 것은 아니다.

### 2-3. Widgets ★★

- Widget은 Django Form 필드가 HTML에서 어떻게 표현될지 지정한다.
- forms.TextInput: 보통 한 줄 입력 / forms.Textarea: 여러 줄 입력.
- Widget의 attrs로 class, placeholder, rows, cols 등 HTML 속성을 지정.

```
content = forms.CharField(
    widget=forms.Textarea(attrs={'class': 'my-content', 'rows': 5})
)
```

widget=forms.Textarea와 widget=forms.Textarea(attrs={...})의 차이를 인지한다. HTML 표현을 바꿨다고 DB의 자료형까지 바뀌는 것은 아니다.

### 2-4. ModelForm ★★★

```
# articles/forms.py
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
```

- forms.ModelForm: 모델을 바탕으로 Form 필드를 자동 구성 가능.
- Meta.model: 어떤 Model을 기반으로 하는지 지정.
- Meta.fields: 포함할 필드. 예: ('title', 'content'), ['title', 'content'], '__all__'.
- Meta.exclude: 제외할 필드. 예: ('created_at',).
- fields와 exclude는 일반적으로 하나의 방식을 택해 사용한다.
- 보안·데이터 무결성을 위해 가능한 한 허용할 필드를 명시하는 편이 안전하다. fields='__all__'은 새 모델 필드까지 노출할 수있다.

Form과 ModelForm의 선택: DB 모델과 관계없이 입력만 검증하는 검색 폼에는 Form이 적합하고, 게시글 생성·수정처럼 DB 모델과 연결된 입력에는 ModelForm이 편리하다.

### 2-5. is_valid()와 오류 처리 ★★★

```
form = ArticleForm(request.POST)
if form.is_valid():
    article = form.save()
    return redirect('articles:detail', article.pk)
return render(request, 'articles/create.html', {'form': form})
```

- request.POST: 제출된 폼 데이터의 QueryDict (파일은 별도 request.FILES).
- 바인딩된 Form에 is_valid() 호출 시 유효성 검사를 수행.
- 성공: True; cleaned_data 사용 가능.
- 실패: False; form.errors 및 렌더링된 필드 오류를 통해 사용자에게 사유 표시.
- 유효하지 않아도 Form 객체 자체가 생성되지 않는 것은 아니다.
- 실패 시 새 ArticleForm()을 만드는 대신, 기존 **바인딩된 form**을 그대로 render해야 입력값과 오류를 보존한다.
- Django Form 검증은 DB의 모든 제약을 보장하는 것과 동일하지 않다.

### 2-6. save()와 commit=False ★★★

```
form = ArticleForm(request.POST)
if form.is_valid():
    article = form.save()  # DB 저장, 모델 인스턴스 반환

if form.is_valid():
    article = form.save(commit=False)  # 미저장 객체
    article.author = request.user
    article.save()  # 이 시점에 DB 저장
```

commit=False는 나중에 직접 채워야 하는 값을 설정할 때 유용하다. ManyToMany 필드가 포함된 경우 commit=False 후 article.save()와 함께 필요한 경우 form.save_m2m() 호출까지 고려한다(강의 범위 확장).

### 2-7. 수정 시 instance ★★★

```
article = Article.objects.get(pk=pk)
form = ArticleForm(request.POST, instance=article)
if form.is_valid():
    article = form.save()  # 기존 article 수정
```

- ArticleForm(request.POST): 기존 객체 지정 없음 → 일반적인 생성 흐름.
- ArticleForm(instance=article): 기존 값을 채운 수정 화면의 미바인딩 Form.
- ArticleForm(request.POST, instance=article): 제출된 데이터로 기존 인스턴스 수정.
- data가 첫 번째 위치 인자라 ArticleForm(request.POST, instance=article)과 ArticleForm(data=request.POST, instance=article)은 동일한 뜻.
- instance=article 자체가 DB 저장 동작을 하는 것은 아니다. 유효성 검사·저장이 뒤따라야 한다.

### 2-8. GET/POST를 하나의 View로 결합 ★★★

생성:

```
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()

    return render(request, 'articles/create.html', {'form': form})
```

- GET /articles/create/ → 비어 있는 폼 화면.
- POST /articles/create/ → 데이터 검사 후 저장. 성공하면 상세 화면으로 redirect.
- POST 검증 실패 → 같은 폼을 오류와 함께 다시 화면에 출력.

수정:

```
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'articles/update.html', {'form': form, 'article': article})
```

- GET 수정: instance=article로 기존 값 표시.
- POST 수정: request.POST와 instance=article을 둘 다 사용.
- 실무에서는 404 대응을 위해 get_object_or_404(Article, pk=pk)를 많이 사용한다(심화).

### 2-9. URL과 Template 변경 ★★

강의에서는 new+create를 create View 하나로, edit+update를 update View 하나로 통합한다. 따라서 예전 new, edit URL 패턴을 제거하고 링크/폼의 action도 articles:create, articles:update로 조정한다. HTTP 메서드에 따라 같은 URL이 서로 다른 처리를 한다는 점이 핵심이다.

### 2-10. Form 렌더링과 필드 수동 렌더링 ★★

- {{ form.as_p }}: 필드를 문단(&lt;p&gt;) 형태로 출력.
- {{ form.as_ul }}: &lt;li&gt;로 출력. 별도 &lt;ul&gt; 컨테이너 필요.
- {{ form.as_table }}: &lt;tr&gt;로 출력. 별도 &lt;table&gt; 필요.
- {{ form.title }}, {{ form.title.label_tag }}, {{ form.title.errors }}: 필드·레이블·오류 개별 출력.

```
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

### 2-11. 필드 재정의·위젯·오류 메시지 ★★

```
class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'my-title',
            'placeholder': 'Enter the title',
        }),
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        error_messages={'required': '내용을 입력해주세요.'},
    )

    class Meta:
        model = Article
        fields = '__all__'
```

ModelForm에 필드를 직접 재정의하면 모델 필드에서 자동 생성되는 설정을 모두 그대로 이어받는 것은 아니므로 필요한 검증 조건을 함께 명시해야 할 수 있다.

## 3. 강의 원본 확인문제 10개 (p070~p074)

원문 문항의 핵심을 보존해 재정리함. 강의에서 제시된 공식 정답에 따름. 정답 순서: 1 d / 2 c / 3 b / 4 c / 5 c / 6 b / 7 b / 8 c / 9 c / 10 b.

1. Django Form이 하는 일로 옳지 않은 것은? ① 입력 화면 생성 ② 입력 유효성 검사 ③ 데이터 자동 저장 처리 ④ DB에 접속해직접 테이블 삭제. 정답 ④ — Form의 역할이 아니다. 주의: 일반 Form이 자동 저장 기능을 제공한다는 의미로 ③을 읽으면 엄밀하지 않다. 강의는 Django Form 시스템의 기능을 포괄적으로 서술한 문맥이며 자동 저장은 ModelForm의 save()와 구별해야 한다.
2. ModelForm과 일반 Form의 차이로 옳은 것은? ① ModelForm은 DB와 무관 ② 일반 Form은 DB에 저장할 때 사용 ③ ModelForm은 모델과 연결해 DB 저장 가능 ④ 일반 Form은 검증 불가. 정답 ③.
3. Form 유효성 검사 메서드는? ① save ② is_valid ③ redirect ④ render. 정답 ②.
4. 각 필드를 &lt;p&gt;로 감싸 렌더링하는 옵션은? ① as_ul ② as_table ③ as_p ④ as_render. 정답 ③.
5. 사용자가 입력한 데이터를 저장하거나 수정할 때 사용하는 메서드? ① update ② create ③ save ④ delete. 정답 ③ — 이 문항은 ModelForm 사용 맥락.
6. HTML 입력 요소를 조정하는 것은? ① model ② widget ③ validator ④ queryset. 정답 ②.
7. ModelForm의 Meta에서 필드를 선택적으로 제외하는 속성은? ① fields ② exclude ③ remove ④ drop. 정답 ②.
8. 입력이 유효하지 않으면? ① 무조건 HTTP 500 ② Form 객체가 생성되지 않음 ③ is_valid() False와 오류 정보 ④ 잘못된값을 그대로 저장. 정답 ③.
9. placeholder나 class 등 추가 속성을 설정하는 곳은? ① fields ② model ③ attrs ④ exclude. 정답 ③.
10. POST 요청을 처리하는 올바른 설명은? ① 단순 화면 표시 ② 입력 데이터를 받아 유효성 검사 ③ DB 데이터를 조회해 화면 표시만 ④ URL 직접 접속 시 사용. 정답 ②.

## 4. 추가 예상문제 30개 — 문제편

### A. 객관식 15문제

1. 아래 코드에서 HTML &lt;textarea&gt; 렌더링에 직접 영향을 주는 인자는?

```
content = forms.CharField(widget=forms.Textarea)
```

① max_length ② widget ③ model ④ exclude

2. 다음 중 forms.ModelForm의 Meta에 모델을 지정할 때 사용하는 속성은? ① form ② instance ③ model ④ widget
3. ArticleForm(request.POST)의 request.POST 의미로 가장 적절한 것은? ① 기존 모델 객체 ② 제출된 폼 데이터 ③ HTML 속성 목록 ④ DB 컬럼 목록
4. form = ArticleForm()은 일반적으로 어떤 상태인가? ① 제출된 POST에 바인딩된 폼 ② 유효성 검사 실패 폼 ③ 데이터가 바인딩되지 않은 새 폼 ④ 저장된 모델 인스턴스
5. ModelForm에서 수정을 위한 유효한 생성 코드는? ① ArticleForm(request.POST, instance=article) ② ArticleForm(article, request.POST) ③ ArticleForm(model=article) ④ ArticleForm(request.GET, save=article)
6. ArticleForm(instance=article)은 주로 언제 사용하는가? ① 신규 객체 저장을 완료할 때 ② 기존 값을 담아 수정 폼 표시 시 ③ 파일 다운로드 시 ④ 마이그레이션 생성 시
7. form.is_valid()가 False가 된 다음 권장되는 흐름은? ① 새로운 빈 폼만 만들어 기존 입력을 삭제 ② 무조건 서버 500 반환 ③ 오류가 담긴 같은 폼 렌더링 ④ 검증 생략 후 저장
8. 아래 코드 실행 직후 옳은 설명은?

```
article = form.save(commit=False)
```

① 이미 DB 저장 완료 ② 유효한 ModelForm이라는 전제에서 미저장 인스턴스 생성 ③ 모든 필드 삭제 ④ Form의 오류가 초기화됨

9. HTML class 속성을 지정할 때 올바른 코드는? ① forms.TextInput(attrs={'class': 'x'}) ② forms.TextInput(fields='x') ③ forms.TextInput(model='x') ④ forms.TextInput(exclude='x')
10. 아래에서 {{ form.as_p }}가 자동 생성하지 않는 것은? ① 각 필드 표현 ② 필드별 p 배치 ③ 제출 버튼 ④ 필드 label
11. 다음 중 ModelForm이 일반 Form보다 추가로 제공하는 대표적 기능은? ① HTML 전체 페이지 자동 제작 ② Model 기반 필드 정의 및 저장 지원 ③ URL 자동 등록 ④ CSRF를 자동으로 끔
12. fields = ('title',)로 지정했다. 가장 타당한 해석은? ① title만 폼에 포함 ② title만 폼에서 제외 ③ title DB 컬럼 삭제 ④ 모든 필드 폼에 포함
13. 다음 중 서버에서 입력 검사를 수행하는 직접적인 메서드는? ① render() ② redirect() ③ is_valid() ④ path()
14. GET과 POST를 하나의 생성 View로 결합하는 핵심 기준은? ① 사용자 IP ② request.method ③ DB 파일명 ④ 템플릿 폴더명
15. 글 작성 후 상세 페이지로 redirect()하는 효과는? ① DB 저장을 자동으로 취소 ② 새로운 HTTP 요청을 유도해 제출 재전송위험을 줄이는 PRG 흐름 ③ Form을 영구 삭제 ④ 마이그레이션 실행

### B. 주관식 10문제

16. 일반 Form을 정의할 때 상속하는 Django 클래스의 전체 표기를 쓰시오.
17. Model과 연결된 입력 폼을 정의할 때 상속하는 Django 클래스를 쓰시오.
18. Form 데이터의 유효성 검사를 수행하여 불리언을 반환하는 메서드를 쓰시오.
19. ModelForm에서 기반 모델을 지정하는 내부 클래스 이름과 그 안의 속성 이름을 함께 쓰시오.
20. ModelForm에서 특정 필드들을 제외할 때 사용하는 Meta 속성을 쓰시오.
21. &lt;p&gt; 태그로 Form 필드를 출력하는 DTL 표현식을 쓰시오.
22. 폼에 제출된 POST 값을 전달하는 기본 코드 ArticleForm(____)의 빈칸을 채우시오.
23. 기존 article을 수정할 때 ArticleForm(request.POST, ____=article)의 빈칸을 채우시오.
24. form.save(____=False)에서 DB 저장을 지연시키는 인자를 쓰시오.
25. Widget에 placeholder 등의 HTML 속성을 지정하는 키워드를 쓰시오.

### C. 서술형 5문제

26. Django Form과 ModelForm의 차이점을 상속 클래스, 데이터베이스 연결, 유효성 검사, 저장 기능의 측면에서 서술하시오.
27. Django ModelForm을 이용한 게시글 생성 View에서 GET 요청과 POST 요청을 어떻게 처리하는지 순서대로 설명하시오. 유효성 검사에 실패했을 때 어떻게 동작해야 하는지도 포함하시오.
28. ArticleForm(request.POST)와 ArticleForm(request.POST, instance=article)의 차이와 instance가 필요한 이유를 설명하시오.
29. is_valid()와 save()의 역할을 비교하고, save(commit=False)가 필요한 사용 사례를 작성하시오.
30. Django Form에서 Widget과 attrs가 하는 역할을 설명하고, input의 class와 placeholder를 지정하는 코드를 작성하시오.

## 5. 추가 예상문제 — 정답과 오답 해설

### 객관식

| 번호 | 정답 | 핵심 해설 |
| --- | --- | --- |
| 1 | ② | widget은 HTML 입력 요소 표현 방식을 바꿈. |
| 2 | ③ | Meta.model = Article. |
| 3 | ② | POST로 전달된 폼 데이터. |
| 4 | ③ | 인자를 주지 않은 Form은 미바인딩 상태. |
| 5 | ① | instance=article을 통해 기존 객체 수정. |
| 6 | ② | GET 수정 화면에서 기존 데이터 미리 채움. |
| 7 | ③ | 바인딩된 form을 재표시해야 오류와 입력 보존. |
| 8 | ② | commit=False면 저장 전 모델 객체 반환. |
| 9 | ① | widget의 attrs 딕셔너리 사용. |
| 10 | ③ | submit 버튼은 별도 HTML. |
| 11 | ② | 모델 기반 자동 필드·저장 지원. |
| 12 | ① | fields는 포함할 필드 선택. |
| 13 | ③ | is_valid()가 유효성 검사 메서드. |
| 14 | ② | request.method == 'POST'로 분기. |
| 15 | ② | 성공한 POST 이후 GET으로 이동하는 PRG 패턴. |

### 주관식

1. forms.Form
2. forms.ModelForm
3. is_valid()
4. class Meta의 model 속성
5. exclude
6. {{ form.as_p }}
7. request.POST
8. instance
9. commit
10. attrs

### 서술형 만점 모범답안

26. Form vs ModelForm — Django Form은 forms.Form을 상속해 입력 필드를 직접 정의하며 사용자 입력의 HTML 렌더링과유효성 검사를 수행한다. ModelForm은 forms.ModelForm을 상속하고 내부 Meta에서 model과 fields 등을 지정해 Model 기반 필드를 구성한다. 둘 다 is_valid()로 검사할 수 있지만, ModelForm은 검증한 데이터를 save()로 데이터베이스에 저장하는 기능을기본 제공한다. 채점 키워드: forms.Form, forms.ModelForm, Meta, Model 연결, 유효성 검사, 저장.
27. 생성 흐름 — GET 요청에서는 빈 ArticleForm()을 생성해 Template에 렌더링한다. POST 요청에서는 ArticleForm(request.POST)로 입력을 바인딩하고 is_valid()로 검사한다. 유효한 경우 form.save()로 데이터를 저장하고 redirect()로 상세 페이지로 이동한다. 유효하지 않다면 기존의 바인딩된 Form을 오류 메시지와 함께 렌더링해 입력값을 유지한다. 채점 키워드: GET 빈 폼, POST 바인딩, is_valid(), save(), redirect(), 실패 시 오류 재렌더링.
28. instance — ArticleForm(request.POST)는 수정 대상을 지정하지 않으므로 유효성 검사 후 저장하면 일반적으로 새로운 모델인스턴스를 생성한다. ArticleForm(request.POST, instance=article)은 기존 article을 수정 대상으로 지정해 save()가 해당 객체의 데이터를 갱신하도록 한다. GET 수정 화면은 ArticleForm(instance=article)을 사용해 기존 값을 표시한다. 채점 키워드: 신규생성 vs 기존 수정, instance, POST 데이터, 기존 값 표시.
29. 검사·저장·지연 — is_valid()는 입력된 값이 필드의 조건에 맞는지 검사해 불리언 결과를 반환한다. save()는 유효성 검사를통과한 ModelForm의 데이터를 모델 인스턴스로 저장한다. save(commit=False)는 아직 DB에 저장하지 않은 인스턴스를 반환하므로, 예를 들어 로그인한 사용자를 article.author에 할당한 다음 article.save()로 저장할 때 사용한다. 채점 키워드: 유효성 검사, True/False, DB 저장, commit=False, 미저장 인스턴스, 후속 save.
30. Widget·attrs — Widget은 입력 필드를 HTML의 어떤 요소로 렌더링할지 지정하고, attrs는 해당 요소의 class, placeholder 같은 추가 HTML 속성을 지정한다. 예: title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title- input', 'placeholder': '제목 입력'})). 채점 키워드: HTML 입력 요소, widget, attrs, class, placeholder.

## 6. 코드 추론 보너스 8문제

1. Q: form = ArticleForm() 다음에 form.is_valid()의 결과는? A: 미바인딩 Form이므로 False (필드가 유효해 보이는 기본값이 있어도 바인딩되지 않았다).
2. Q: ArticleForm(request.POST)를 사용하고 form.save()하면 기존 글이 수정될까? A: 기존 instance를 지정하지 않았다면 일반적으로 새 인스턴스 생성으로 처리된다.
3. Q: 수정 페이지를 GET으로 열 때 ArticleForm(request.POST, instance=article)을 사용하면? A: GET의 POST 데이터는 비어있으므로 기존 데이터 표시용으로 부적절하다. ArticleForm(instance=article) 사용.
4. Q: form.is_valid()가 False인데 return render(..., {'form': ArticleForm()})하면? A: 기존 제출 데이터와 검증 오류가 사라진다.
5. Q: article = form.save(commit=False); article.author = request.user 후 끝나면? A: 아직 DB에 저장되지 않는다. article.save() 필요.
6. Q: &lt;form method="POST"&gt;{{ form.as_p }}&lt;button&gt;저장&lt;/button&gt;&lt;/form&gt;만 사용하면? A: CSRF 미들웨어가 활성인 일반 POST에서는 {% csrf_token %} 누락으로 403이 발생할 수 있다.
7. Q: class Meta: model = Article; exclude = ('title',)이면? A: title 이외의 대상 모델 필드가 폼에 포함된다(자동 포함 대상· 편집 가능 여부 등의 조건 적용).
8. Q: GET으로 /articles/create/를 열었을 때 바로 form.save()하면? A: 빈 폼에 사용자 입력이 없고 검증도 되지 않았으므로정상적인 저장 흐름이 아니다.

## 7. 틀리기 쉬운 함정 12개

1. forms.Form에 save()가 기본 제공된다? X.
2. ModelForm만 유효성 검사가 가능하다? X. Form도 가능.
3. is_valid()가 DB 저장까지 한다? X. 검사와 저장은 별도.
4. form.save()가 항상 새로운 행을 만든다? X. instance가 있으면 기존 행을 갱신할 수 있다.
5. instance는 HTML 속성이다? X. ModelForm 인스턴스 연결 인자.
6. fields는 모델에서 컬럼을 삭제한다? X. 폼에 노출할 필드 지정.
7. exclude는 필드 유효성 검사를 끈다? X. 해당 필드를 Form 구성에서 제외.
8. widget은 모델 필드의 데이터 타입을 바꾼다? X. HTML 표현을 제어.
9. attrs는 ModelForm 내부 Meta의 필수 속성이다? X. Widget의 HTML 추가 속성 등에 사용.
10. POST 검사 실패 때 빈 ArticleForm()으로 덮어쓴다? X. 기존 바인딩된 폼 보존.
11. {{ form.as_p }}가 &lt;form&gt; 태그와 CSRF 토큰을 만든다? X.
12. form.save(commit=False)가 DB를 저장한다? X.

## 8. 60분 시험 공략 및 6단원 복습 루틴

- 첫 복습 20분: Form vs ModelForm, is_valid(), Meta, instance, GET/POST View를 우선 학습.
- 암기 10분: Meta 속성, 코드 3가지(Form(), Form(request.POST), Form(request.POST, instance=...))를 백지에 작성.
- 문제풀이 20분: 강의 10제 + 추가 객관식 15제 + 주관식 10제. 틀린 이유 한 줄 기록.
- 서술 10분: 26~30번 중 2~3개를 3~5문장으로 쓰고 채점 키워드 체크.

시험장에서의 일반적 시간 배분(실제 문항 수에 따라 조정): 쉬운 객관식·주관식 20분 → 서술형·코드 추론 30분 → 검토 10분. 서술형은 정의 → 동작 순서 → 핵심 코드/예시 → 주의점 순으로 작성하면 누락이 줄어든다.

### 시험 직전 90초 암기 카드

- Form: forms.Form / ModelForm: forms.ModelForm
- 검사: form.is_valid() / 저장: form.save()
- 미저장: form.save(commit=False) → 속성 설정 → article.save()
- 새 입력 화면: ArticleForm()
- POST 제출: ArticleForm(request.POST)
- 수정 GET: ArticleForm(instance=article)
- 수정 POST: ArticleForm(request.POST, instance=article)
- Meta: model, fields, exclude
- 위젯: widget=forms.Textarea(attrs={...})
- 강의 확인문제 정답: d c b c c b b c c b

## 9. 1~6단원 연결 문제

1단원 MTV: Form을 정의해 View에서 사용하고 Template에서 표시한다. ModelForm은 Model과 입력 폼 사이의 연결을 편리하게 만든다.

2단원 Template·URLs: URL에서 View를 호출 → View에서 form을 context로 전달 → Template에서 {{ form.as_p }} 렌더링 → HTML form으로 POST 요청.

3단원 Model: Article의 title, content가 모델에 정의되며 ModelForm은 해당 필드를 기반으로 입력 필드를 구성할 수 있다.

4단원 ORM: Article.objects.get(pk=pk)로 수정할 객체를 조회; Form에 instance=article로 전달한다.

5단원 ORM with View: new/create와 edit/update를 분리했다면 6단원에서는 HTTP method 분기를 사용해 View를 결합한다.

### 통합 서술형 예시

문제: 사용자가 기존 게시글을 수정하는 요청이 Django 앱에서 처리되는 전체 과정을 URL, View, ORM, ModelForm, Template 개념을 사용해 설명하시오.

만점 답안: URLconf가 /articles/3/update/ 요청을 update View에 연결한다. View는 ORM을 이용해 Article.objects.get(pk=3) 으로 대상 게시글을 조회한다. GET 요청에서는 ArticleForm(instance=article)을 생성해 Template에 전달하고 기존 값이 채워진수정 폼을 보여준다. POST 요청에서는 ArticleForm(request.POST, instance=article)로 변경된 데이터를 바인딩하고 is_valid() 로 검사한다. 유효하면 form.save()로 기존 게시글을 수정하고 상세 페이지로 리다이렉트하며, 유효하지 않으면 입력값과 오류가담긴 Form을 다시 렌더링한다.

채점 키워드: URLconf, View, ORM 조회, GET, instance, POST, is_valid(), save(), redirect(), 오류 재렌더링.
