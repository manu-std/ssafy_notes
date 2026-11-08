# Django 07 — Static files & Media files

> 📎 확인문제·예상문제·암기카드: [`시험대비/07_static_media_시험대비.md`](시험대비/07_static_media_시험대비.md)

*(개발자가 미리 넣어 두는 파일(Static)과 사용자가 올리는 파일(Media)을 웹 주소로 제공하는 방법. 이미지 업로드는 3단원 Model 필드, 6단원 ModelForm·instance가 전부 다시 등장하는 종합 실습이다.)*

## 오늘의 목차

1. Static files vs Media files
2. 웹 서버와 정적 파일
3. Static files 기본 경로
4. Static files 추가 경로
5. 이미지 업로드
6. 업로드 이미지 제공
7. 업로드 이미지 수정
8. 참고 — upload_to 동적 경로, 배포 환경(AWS)

---

## 1. Static files vs Media files

| 구분 | Static files (정적 파일) | Media files (미디어 파일) |
|---|---|---|
| 정의 | 서버 측에서 변경되지 않고 **고정적으로 제공**되는 파일 | 사용자가 웹사이트를 통해 **직접 업로드**하는 파일 |
| 만드는 주체 | **개발자**가 미리 준비 | **사용자**가 업로드 |
| 성격 | '고정된' 파일 | 사이트 운영 중 사용자에 의해 생성·변경되는 '동적인' 파일 |
| 예시 | CSS, JavaScript, 이미지, 폰트 파일 (쇼핑몰 로고·아이콘) | 사용자가 상품 후기에 올리는 상품 사진 |
| 비유 | 식당의 '인쇄된 메뉴판' | — |

---

## 2. 웹 서버와 정적 파일

- 웹 서버의 기본 역할: **요청 받은 주소(URL)에 해당하는 자원을 찾아 응답**
  - 도서관 사서 비유: 'A-3 구역의 3번째' = URL, '책' = 자원(Resource)
- 웹 서버가 제공하는 가장 기본적인 자원이 정적 파일
- 정적 파일이 사용자에게 보이려면 **그 파일에 접근할 수 있는 고유한 주소(URL)가 반드시 필요**

### 처리 과정

1. 사용자: `http://example.com/images/logo.png` 입력해 이미지 요청
2. 웹 서버: `/images/logo.png` URL 확인 후 미리 약속된 폴더에서 `logo.png` 찾음
3. 웹 서버: 찾은 파일을 HTTP 응답에 담아 전송
4. 사용자: 브라우저가 응답받은 이미지를 화면에 표시

### 핵심 원리: 주소(URL)가 있어야 찾아갈 수 있음

- 컴퓨터에 파일이 존재하는 것만으로는 웹 페이지에 보일 수 없음

| 구분 | 개념 | 비유 |
|---|---|---|
| 서버 (내 컴퓨터) | 실제 파일 경로 | "내 방 책상 위 세 번째 서랍" |
| 웹 (인터넷 세상) | URL (웹 주소) | "서울시 강남구 테헤란로 999" |

> 💡 이 단원의 설정 변수들은 전부 이 둘 중 하나다 — **"실제 폴더 경로"냐**, **"웹 주소"냐**. (STATIC_URL·MEDIA_URL = 웹 주소 / STATICFILES_DIRS·MEDIA_ROOT = 실제 경로)

---

## 3. Static files 기본 경로

- 기본 경로: **`app폴더/static/`**

### CSS 적용

- `articles/static/stylesheets/style.css`에 CSS 파일 배치

```css
h1 {
  color: crimson;
}
```

```html
<!-- articles/index.html -->
{% load static %}
<link rel="stylesheet" href="{% static 'stylesheets/style.css' %}">
```

- static files 경로는 DTL의 **static tag** 사용
- built-in tag가 아니므로 **load tag로 import 후 사용**
- `app폴더/static/` **이후 경로**를 작성
- 결과: `href="/static/stylesheets/style.css"` (`/static/`으로 시작하는 웹 주소 생성)

### 이미지 적용

- `articles/static/images/sample-1.png`에 이미지 배치

```html
<img src="{% static 'images/sample-1.png' %}" alt="sample image">
```

- 결과 URL: `http://127.0.0.1:8000/static/images/sample-1.png`

> 📌 앱이 여러 개면 각 앱 `static/` 폴더가 하나의 검색 공간으로 합쳐진다. 그래서 템플릿처럼 `articles/static/articles/logo.png`로 **앱 이름 폴더를 한 번 더** 두면 파일명 충돌을 피할 수 있다.

### {% load %}

- 특정 라이브러리의 태그와 필터를 현재 템플릿에서 사용할 수 있도록 불러옴
- `{% load static %}` = "이제부터 static 관련 태그를 사용하겠다"는 **선언문**
- 템플릿 파일 **가장 상단에 한 번만** 작성
- `{% extends %}`를 쓰는 템플릿은 **extends가 첫 줄, load는 그 아래**
- 부모 템플릿에서 load 했더라도 **자식 템플릿에서 다시 load** 해야 함

### {% static '경로' %}

- settings.py의 **STATIC_URL 값을 앞에 붙여** 정적 파일의 **웹 경로(URL)를** 생성 (실제 OS 파일 경로를 출력하는 게 아님)
- 예: `STATIC_URL = 'static/'`, 파일이 `static/css/style.css` → `{% static 'css/style.css' %}` → `/static/css/style.css`

### STATIC_URL

- 정적 파일의 **'웹 주소'**
- 정적 파일에 접근할 때 사용할 **URL의 시작 부분(접두사)을** 지정하는 설정
- 서버의 실제 파일 경로가 아니라 **오직 웹(브라우저)에서만 사용되는 주소**
- 정적 파일 폴더에 `'static/'`이라는 웹 주소 별명을 붙이는 것 → 브라우저가 이 별명으로 요청하면 Django가 약속된 실제 폴더에서 파일을 찾아 응답
- 기본 값: `'static/'`

> ⚠️ STATIC_URL을 바꿔도 파일의 실제 저장 위치가 바뀌는 건 아니다. 주소의 앞부분만 바뀐다.

### 정적 파일 URL 구성

```text
서버 주소 + STATIC_URL + 정적파일 경로
http://127.0.0.1:8000  +  /static/  +  images/sample-1.png
```

---

## 4. Static files 추가 경로

- **`STATICFILES_DIRS`에** 추가 경로 목록(리스트) 설정
- 기본 경로(앱의 `static/`) 외에 **추가적으로 탐색할 경로의 목록**을 지정하는 리스트
  - 기본 도서관 외 '외부 창고'들의 주소 목록 비유
  - 여러 앱에서 공통으로 쓰는 Bootstrap, JS 라이브러리처럼 **특정 앱에 속하지 않는 정적 파일**을 프로젝트 최상위(BASE_DIR)에 모아 관리할 때 유용

```python
# settings.py
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

- 각 앱의 `static/`뿐 아니라 프로젝트 최상위 `static/`에서도 정적 파일을 찾음
- 탐색 순서: **STATICFILES_DIRS 먼저**, 그 다음 각 앱의 `static/` 폴더

```html
<!-- 프로젝트 최상위 static/sample-2.png -->
<img src="{% static 'sample-2.png' %}" alt="sample image">
```

- 결과 URL: `http://127.0.0.1:8000/static/sample-2.png`

| 설정 | 정체 | 형태 |
|---|---|---|
| `STATIC_URL` | 웹 주소 접두사 | 문자열 `'static/'` |
| `STATICFILES_DIRS` | 추가로 찾을 **실제 폴더** 목록 | 리스트 `[BASE_DIR / 'static']` |

> 📌 참고: `STATIC_ROOT`는 배포할 때 `collectstatic` 명령으로 모든 정적 파일을 **한 곳에 모으는 폴더**다. STATICFILES_DIRS(찾을 곳)와는 다른 개념 (강의 범위 밖 보충).

---

## 5. 이미지 업로드

### ImageField()

- 이미지 파일을 업로드하기 위한 Django 모델 필드
- **이미지 파일 자체가 DB에 저장되는 것이 아님**
  - DB: `MEDIA_ROOT` 기준 **상대 경로(문자열)만** 저장 (예: `images/sample.png`)
  - 실제 파일: 서버의 특정 폴더(`MEDIA_ROOT`)에 저장
- `upload_to`는 선택 인자 (MEDIA_ROOT 아래 하위 폴더 지정)

```python
class Article(models.Model):
    # 이미지는 'MEDIA_ROOT경로/images/'에 저장되고,
    # DB에는 'images/sample.png'와 같은 경로 문자열이 저장됨
    image = models.ImageField(upload_to='images/')
```

### 미디어 파일 제공 전 준비사항

1. settings.py에 `MEDIA_ROOT`, `MEDIA_URL` 설정
2. 작성한 `MEDIA_ROOT`와 `MEDIA_URL`에 대한 URL 지정

| 설정 | 의미 | 설명 |
|---|---|---|
| `MEDIA_ROOT` | 미디어 파일의 **'실제 창고'** 주소 | 업로드 파일이 서버 어디에 저장될지 지정하는 **절대 경로**. 서버 내부에서만 쓰는 물리적 폴더 주소 |
| `MEDIA_URL` | 미디어 파일의 **'웹 주소' 별명** | MEDIA_ROOT의 파일에 웹에서 접근할 때 쓰는 URL 시작 부분. STATIC_URL과 같은 역할 |

```python
# settings.py
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'
```

```python
# 프로젝트 urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- `settings.MEDIA_URL`: "media/로 시작하는 URL 요청이 오면"
- `document_root=settings.MEDIA_ROOT`: "MEDIA_ROOT에 지정된 실제 폴더에서 파일을 찾아라"
- 개발 서버는 **static은 자동 제공, media는 자동 제공하지 않음** → 규칙을 직접 추가해야 함
- 이 `static()` 설정은 **개발 단계(DEBUG=True)에서만** 동작. 실제 서비스는 웹 서버나 S3 같은 저장소가 제공

> ⚠️ `static(URL, document_root=ROOT)` — 첫 인자는 **웹 주소**, `document_root`는 **실제 폴더**. 둘을 바꿔 쓰면 설정이 꼬인다.

### 이미지 업로드 구현

**① 모델에 image 필드 추가**

```python
# articles/models.py
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

- `blank=True`: 폼에서 이미지를 비워도 유효성 검사 통과 → 이미지 첨부 없이도 게시글 작성 가능
- blank 속성: 폼 유효성 검사 시 해당 필드를 필수 또는 선택 사항으로 만들지 결정 (3단원 null vs blank 복습)
- 기존 필드 사이에 작성해도 실제 테이블에는 **가장 우측(뒤)에** 추가됨

**② Pillow 설치 후 migration**

```bash
$ python manage.py makemigrations
SystemCheckError: System check identified some issues:
ERRORS:
articles.Article.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".
```

- **ImageField를 사용하려면 반드시 Pillow 라이브러리 필요**
- Pillow: 파이썬에서 이미지를 열고 크기 조절, 필터 적용 등 다양한 편집 작업을 수행한 후 저장할 수 있게 해주는 필수 이미지 처리 라이브러리 (ImageField는 이걸로 "진짜 이미지인지" 검증함)

```bash
$ pip install pillow
$ python manage.py makemigrations
$ python manage.py migrate
$ pip freeze > requirements.txt
```

**③ form에 enctype 속성 추가**

```html
<!-- articles/create.html -->
<h1>CREATE</h1>
<form action="{% url 'articles:create' %}" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form }}
  <input type="submit">
</form>
```

- enctype 속성: form 데이터가 서버로 제출될 때 **어떤 형식으로 인코딩될지** 지정
- 파일 업로드 시에는 **반드시 `multipart/form-data`로** 설정

**④ view에서 파일 데이터 전달**

```python
# articles/views.py
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
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

- ModelForm의 **2번째 인자로 `request.FILES`** 전달
- 이유: ModelForm의 상위 클래스인 **BaseModelForm의 생성자 함수가 2번째 위치 인자로 파일(`files`)을 받도록** 설정되어 있기 때문 (`__init__(self, data=None, files=None, ...)`)

| 요청 데이터 | 담기는 곳 |
|---|---|
| 일반 입력값 (title, content) | `request.POST` |
| 업로드 파일 (image) | `request.FILES` |

**⑤ 결과 확인**

- 작성 페이지에 `<input type="file" name="image" accept="image/*" id="id_image">` 생성
- 업로드한 파일은 `MEDIA_ROOT` 경로(`media/images/sample-1.png`)에 저장
- DB의 image 컬럼에는 `images/sample-1.png` 같은 **경로 문자열만** 저장 → DB 용량을 가볍게 유지하고 성능을 높이는 데 효율적

> ⚠️ 이미지 업로드 3종 세트 — 하나라도 빠지면 파일이 안 올라간다.
> 1. 모델: `ImageField` (+ Pillow)
> 2. 템플릿: `enctype="multipart/form-data"`
> 3. 뷰: `ArticleForm(request.POST, request.FILES)`
>
> `{% csrf_token %}`은 보안용이지 파일 인코딩과는 무관하다.

---

## 6. 업로드 이미지 제공

- ImageField의 **`.url` 속성**: 업로드 파일의 웹 주소
- ImageField나 FileField에 저장된 파일 객체에서 `.url`을 사용하면 웹에서 접근 가능한 전체 URL 주소를 얻음

```html
<!-- articles/detail.html -->
{% if article.image %}
  <img src="{{ article.image.url }}" alt="image">
{% endif %}
```

- 이미지를 업로드하지 않은 게시물에서 `article.image.url`을 쓰면 **ValueError** 발생 → if 태그로 이미지가 있을 때만 출력
- 결과 URL: `http://127.0.0.1:8000/media/images/sample-1.png`

| 속성 | 값 | 용도 |
|---|---|---|
| `.name` | `images/sample-1.png` | DB에 저장된 상대 경로 |
| `.path` | `C:/.../media/images/sample-1.png` | 서버의 실제 파일 경로 (웹에서 못 씀) |
| `.url` | `/media/images/sample-1.png` | **웹 접근 주소 → img src에는 이것** |

> ⚠️ 업로드 이미지에 `{% static %}`을 쓰면 안 된다. static 태그는 개발자가 넣어 둔 정적 파일용, 업로드 파일은 `.url`.

---

## 7. 업로드 이미지 수정

- 수정 페이지 form에도 **enctype 속성** 추가

```html
<!-- articles/update.html -->
<h1>UPDATE</h1>
<form action="{% url 'articles:update' article.pk %}" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form }}
  <input type="submit">
</form>
```

- update view 함수에서도 **`request.FILES`** 추가

```python
# articles/views.py
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
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

- `request.FILES` → 새 이미지 처리 / `instance=article` → 새 글이 아니라 **기존 글 수정** (6단원)

---

## 8. 참고 — upload_to 동적 경로, 배포 환경(AWS)

### upload_to에 함수 넣기

```python
def articles_image_path(instance, filename):
    return f'images/{instance.pk}/{filename}'

class Article(models.Model):
    image = models.ImageField(upload_to=articles_image_path, blank=True)
```

- 문자열: 고정 하위 경로 / 함수(callable): `instance`, `filename`을 받아 **상대 경로 문자열을 반환**
- ⚠️ 새 글은 저장 전이라 첫 업로드 시점에 `instance.pk`가 `None`일 수 있다 → 위 코드는 "함수 형태" 예시일 뿐, pk 기반 경로는 저장 시점을 고려해야 함

### AWS EC2 / S3 / RDS

| 서비스 | 분류 | 역할 |
|---|---|---|
| **EC2** | 컴퓨팅 | Django 애플리케이션 서버 실행 |
| **S3** | 객체 스토리지 | 정적·미디어(이미지 등) 파일 저장 |
| **RDS** | 관리형 관계형 DB | 데이터베이스 관리 |

- 서버·파일 저장소·DB를 분리하면 확장성·관리·가용성 측면에서 유리
- 함정: "이미지 파일 저장" → **S3**, "관계형 DB 관리" → **RDS**
