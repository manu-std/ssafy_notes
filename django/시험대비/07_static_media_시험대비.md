# Django 7단원 시험대비 — Static files & Media files

> 📎 개념 정리 노트: [`../07_static_media.md`](../07_static_media.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

출처: 업로드된 Django_Staticfiles.zip (75장). 중요도는 강의 반복·실습·확인문제를 기준으로 추정한 학습 우선순위이며 실제 출제를 보장하지 않는다. 활용: 핵심 개념 → 코드 따라쓰기 → 예상문제(해설 보기 전에 풀기) → 오답 → 90초 암기카드.

## 0. 이번 단원에서 반드시 설명할 수 있어야 할 질문

1. Static과 Media의 파일 생성 주체가 어떻게 다른가?
2. STATIC_URL과 STATICFILES_DIRS의 차이는?
3. {% load static %}와 {% static '...' %}가 하는 일은?
4. MEDIA_ROOT와 MEDIA_URL은 각각 실제 경로인가, 브라우저 URL인가?
5. 이미지 업로드에 request.FILES와 enctype="multipart/form-data"가 함께 필요한 이유는?
6. ImageField와 upload_to, Pillow는 어떤 역할을 하는가?
7. article.image.url과 {% static %} 중 업로드 이미지를 보여주는 올바른 방식은?
8. 개발환경에서 미디어 제공 URL 패턴을 어떻게 구성하는가?
9. 업로드 이미지를 수정할 때 instance와 request.FILES를 어떻게 조합하는가?
10. EC2, S3, RDS는 각각 무엇을 담당하는가?

## 1. 출제 예상 중요도와 원본 슬라이드

| 우선순위 | 개념 | PPT 위치 |
| --- | --- | --- |
| ★★★ | Static과 Media 비교 | 5–11, 30–32 |
| ★★★ | static 기본 경로, load/static 태그 | 12–22 |
| ★★★ | STATIC_URL vs STATICFILES_DIRS | 18, 23–29 |
| ★★★ | MEDIA_ROOT vs MEDIA_URL | 35–39 |
| ★★★ | ImageField, Pillow, upload_to | 34, 40–42, 55–58 |
| ★★★ | 폼의 enctype + View의 request.FILES | 43–47, 52–53 |
| ★★★ | 이미지 표시 .url / 이미지 수정 | 48–53 |
| ★★ | URL 패턴 개발서버 미디어 제공 | 38–39 |
| ★★ | AWS EC2/S3/RDS | 59–63 |
| ★ | BaseModelForm / 추가 실습 | 64–66 |
| ★★★ | 강의 확인문제와 정답 | 67–71 |

## 2. 핵심 개념 완전 정리

### 2.1 Static files (정적 파일)

- 정의: 웹사이트 개발자가 미리 준비해 제공하는 CSS, JavaScript, 로고 등의 파일. 요청마다 서버가 동적으로 내용을 생성하지않는 자산.
- 경로: Django 앱 기본 탐색 경로는 앱이름/static/이다. 예: articles/static/articles/logo.png처럼 앱 이름으로 네임스페이스를 두면 앱 간 파일명 충돌을 줄일 수 있다.
- 주의: 정적 파일을 위한 경로는 URL 패턴의 Django View에 연결하는 것과 다르다. 개발 서버에서 자동 제공되는 조건과 실제배포에서의 정적 파일 제공 방식은 구분한다.

```
{% load static %}
<link rel="stylesheet" href="{% static 'stylesheets/style.css' %}">
<img src="{% static 'images/sample.png' %}" alt="예시">
```

- {% load static %}: 템플릿에서 static 태그 라이브러리를 불러온다.
- {% static 'images/sample.png' %}: 정적 파일의 URL을 생성한다. 실제 운영체제 절대 경로를 출력하는 태그가 아니다.
- href와 src에 일반 상대경로를 직접 지정하는 것과 비교하라.
- 템플릿 상속에서는 load 태그 적용 범위를 주의하자. 다른 템플릿 파일에서 static 태그를 사용한다면 해당 템플릿에도 load가필요할 수 있다.

### 2.2 STATIC_URL과 STATICFILES_DIRS

```
# settings.py 예시
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

- STATIC_URL: 정적 파일의 웹 접근 URL 접두사. 강의 예시에서는 /static/...에 해당한다.
- STATICFILES_DIRS: 앱의 static/ 이외에 Django가 정적 파일을 추가 탐색할 파일시스템 디렉터리 목록.
- STATICFILES_DIRS는 복수 목록이므로 [...] 형태로 지정한다.
- BASE_DIR / 'static'은 pathlib.Path 문법으로 프로젝트 기준 디렉터리 아래 static 디렉터리를 나타낸다.
- STATIC_ROOT는 운영 배포에서 collectstatic 결과를 수집하는 대상 경로로, STATICFILES_DIRS와 다르다. 강의 범위를 넓힌 보충 개념.
- 함정: STATIC_URL을 바꿔도 파일의 원래 저장 위치가 자동으로 이동하는 것은 아니다.

### 2.3 Media files (미디어 파일)

- 정의: 웹사이트 이용자가 직접 업로드하는 이미지 등의 파일.
- 일반적으로 서버 또는 별도 스토리지에 저장하고 DB에는 경로/파일 이름 등을 저장한다. 강의 예시의 ImageField는 이미지 바이너리 자체를 일반 문자열 컬럼에 저장하는 구조가 아니다.
- Static: 개발자가 준비 / Media: 사용자가 업로드.

```
# settings.py
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'
```

- MEDIA_ROOT: 업로드 파일이 저장되는 실제 디렉터리(파일시스템 경로).
- MEDIA_URL: 업로드 파일을 브라우저에서 접근하는 URL 접두사.
- URL을 나타내는 변수와 저장 위치를 나타내는 변수를 혼동하면 안 된다.

```
# 프로젝트 urls.py — 개발 환경에서만 예시
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('articles/', include('articles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)는 개발 환경에서 미디어 파일을 요청 URL과 실제 저장소에연결하기 위한 예시다. 프로덕션 미디어 파일 서비스 방법으로 그대로 사용하지 않는다.
- urlpatterns += ...는 기존 URL 패턴 리스트에 항목을 덧붙이는 파이썬 구문이다.

### 2.4 ImageField와 Pillow

```
# models.py
class Article(models.Model):
    title = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/', blank=True)
```

- ImageField: 업로드된 이미지 파일을 다루는 Django 모델 필드.
- 이미지 유효성 검증을 위해 Pillow 라이브러리가 필요하다. pip install Pillow.
- upload_to='images/': 업로드 저장 디렉터리 하위 경로. 예에서 파일 경로는 MEDIA_ROOT / 'images' / 파일명의 형태로 저장될수 있다.
- blank=True: Form 유효성 검사에서 이미지 입력을 선택 사항으로 허용한다.
- null과 blank는 역할이 다르다(3단원 복습). FileField/ImageField는 보통 blank=True로 선택 입력을 나타낸다.
- Model 필드 추가 후 makemigrations → migrate가 필요하다(3단원 복습).

### 2.5 이미지 업로드 전체 흐름 (반드시 순서 암기)

```
<!-- create.html -->
<form action="{% url 'articles:create' %}" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="등록">
</form>

# views.py — ModelForm 기반
from django.shortcuts import render, redirect

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    return render(request, 'articles/create.html', {'form': form})
```

1. 사용자가 파일 선택 후 POST 요청을 보냄.
2. HTML의 enctype="multipart/form-data"가 파일을 포함하는 본문 인코딩 방식으로 제출되도록 함.
3. Django는 일반 폼 데이터는 request.POST, 업로드 파일은 request.FILES로 전달.
4. ArticleForm(request.POST, request.FILES)로 폼 바인딩.
5. form.is_valid() 후 form.save()가 모델 인스턴스와 업로드 파일을 저장.
6. 업로드 파일의 경로/이름 정보를 사용해 화면에서 접근.

대표 함정

- method="POST"만으로 충분하지 않다. 파일 업로드 폼에는 enctype도 필요하다.
- request.POST에는 업로드 파일 자체가 담기지 않는다.
- request.FILES를 전달하지 않으면 새 파일이 바인딩되지 않는다.
- CSRF 토큰은 다른 목적: 사용자의 의도 없는 요청을 방어하며 파일 인코딩 방식과 다르다.
- form.is_valid()가 False면 저장하지 않고 오류 정보를 포함한 폼을 재표시하도록 작성한다.

### 2.6 업로드 이미지 제공

```
{% if article.image %}
  <img src="{{ article.image.url }}" alt="게시글 이미지">
{% endif %}
```

- .url: 저장된 업로드 파일을 접근할 수 있는 URL을 반환한다.
- {% static '...' %}는 개발자가 정해 둔 정적 파일 URL 생성에 사용한다. 사용자 업로드 이미지의 접근에는 일반적으로 article.image.url을 사용한다.
- if 체크: 이미지가 없는 게시글에서 .url을 무조건 참조하면 오류가 발생할 수 있다.
- .name: 파일 필드에 저장된 파일 이름/상대 경로; .path: 로컬 파일시스템 스토리지에서의 절대 경로(일부 원격 스토리지에는지원되지 않음); .url: 접근 URL.

### 2.7 수정 기능에서 파일 업로드

```
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/update.html', {'form': form})
```

- instance=article: 기존 글 수정. 생략하면 새로운 글을 생성할 수 있음(6단원 연결).
- request.FILES: 새 이미지 업로드를 처리.
- 수정 폼에도 enctype="multipart/form-data" 필수.
- 새 파일을 올리지 않고 기존 파일을 유지하는 동작과 기존 파일을 삭제하는 동작은 구분하여 생각한다.

### 2.8 upload_to 동적 경로

```
# 저장 경로를 동적으로 구성하는 함수 예시
def articles_image_path(instance, filename):
    return f'images/{instance.pk}/{filename}'
class Article(models.Model):
    image = models.ImageField(upload_to=articles_image_path, blank=True)
```

- 문자열: 고정 업로드 하위 경로.
- 함수(callable): instance, filename을 받아 상대 경로 문자열 반환.
- 함정: 신규 객체가 아직 DB에 저장되지 않아 첫 파일 저장 때 instance.pk가 None일 수 있다. 따라서 pk 기반 경로를 쓸 때는저장 시점을 고려해야 한다. 위 코드는 함수 형태를 설명하는 예시이며 신규 업로드 경로의 안전한 완성형은 아니다.
- 사용자 제공 파일명을 경로에 그대로 사용할 때는 파일 이름 충돌·보안·스토리지 정책도 고려한다(심화).

### 2.9 AWS EC2/S3/RDS

| AWS 서비스 | 분류 | 역할 |
| --- | --- | --- |
| EC2 | 컴퓨팅 | Django 등의 애플리케이션 서버 실행 |
| S3 | 객체 스토리지 | 정적·미디어 이미지 등의 파일 저장 |
| RDS | 관리형 관계형 DB | 데이터베이스 관리 |

- 출제 함정: 이미지 파일 저장 서비스를 고르면 S3, 관계형 DB 관리 서비스를 고르면 RDS.
- 서버·스토리지·DB를 분리할 수 있고 확장성, 관리, 가용성 측면에서 장점이 있다.

### 2.10 BaseModelForm (간단 이해)

- ModelForm 내부 구현과 연결되는 기반 클래스. 모델 필드를 바탕으로 폼 필드를 생성하고 연결하는 기능을 제공한다.
- 입문 수준 시험에서는 forms.ModelForm의 정의·Meta·save() 사용법을 우선 익힌다.

## 3. 반드시 암기할 비교표

| 혼동 개념 | 왼쪽 | 오른쪽 |
| --- | --- | --- |
| Static / Media | 개발자가 미리 준비 | 사용자가 업로드 |
| STATIC_URL / STATICFILES_DIRS | 웹 URL 접두사 | 추가 정적 파일 탐색 디렉터리 목록 |
| MEDIA_ROOT / MEDIA_URL | 실제 저장 위치 | 브라우저 접근 URL 접두사 |
| {% static %} / article.image.url | 정적 파일 URL | 업로드 이미지 URL |
| request.POST / request.FILES | 일반 입력값 | 업로드 파일 |
| blank=True / null=True | 폼 검증에서 비워도 됨 | DB에 NULL 저장 허용 |
| instance=article 있음/없음 | 기존 인스턴스 수정 | 새 인스턴스 생성 가능 |
| enctype / {% csrf_token %} | 파일 전송을 위한 본문 인코딩 | CSRF 보안 처리 |

## 4. 강의 원본 확인문제 — 학습용 핵심 재구성 10문제

PPT 67–71장의 강의 확인문제와 정답이 다루는 핵심을 요약·재구성한 버전. 원문을 정확히 옮긴 문제가 아니라 원문의 학습목표에맞춘 문항이다.

O1. 다음 중 정적 파일의 설명으로 가장 적절한 것은? ① 사용자가 업로드한 프로필 사진 ② 서버가 미리 준비한 CSS 파일 ③ DB의고객 레코드 ④ 서버에서 계산한 숫자 → ②. 설명: Static files는 미리 준비된 파일이다.

O2. STATIC_URL이 주로 정하는 것은? ① 물리적 파일 저장 경로 ② URL 접두사 ③ DB 이름 ④ 요청 메서드 → ②.

O3. ImageField로 저장된 이미지 필드의 DB 값은 일반적으로 무엇인가? ① 이미지 전체 바이너리 ② 파일 경로/이름 정보 ③ Pillow 버전 ④ HTML 이미지 태그 → ②.

O4. ImageField의 저장 경로를 지정하는 인자는? ① default ② upload_to ③ media_path ④ blank → ②.

O5. 업로드 이미지 접근을 위한 가장 적절한 템플릿 코드는? ① {% static article.image %} ② {{ article.image.url }} ③ {{ MEDIA_ROOT }} ④ {{ article.image.path }} → ②.

O6. 개발환경에서 업로드 파일 URL 제공 시 사용하는 예시 식의 올바른 조합은? urlpatterns += static(①, document_root=②) → ① settings.MEDIA_URL / ② settings.MEDIA_ROOT.

O7. 템플릿 내 static 태그 라이브러리를 불러오는 올바른 문법은? ① {% import static %} ② {% prepare static %} ③ {% use static %} ④ {% load static %} → ④.

O8. 앱 기본 경로 이외 추가 정적 파일 탐색 경로를 설정하는 것은? ① STATIC_URL ② STATIC_ROOT ③ STATICFILES_DIRS ④ MEDIA_URL → ③.

O9. 정적 파일을 이용한 디자인 변경에 대한 설명으로 옳은 것은? ① URL만 바꾸면 DB 구조도 바뀐다 ② CSS 등 정적 파일을 통해화면 표현을 변경할 수 있다 ③ 업로드 파일은 반드시 static 태그로 출력해야 한다 ④ 모든 정적 파일은 RDS에 저장한다 → ②.

O10. ImageField를 사용하기 위해 설치해야 하는 이미지 처리 라이브러리는? ① Django REST Framework ② Pillow ③ NumPy ④ Bootstrap → ②.

## 5. 추가 객관식 예상문제 15개

정답은 뒤의 정답표에 따로 배치했다. 우선 보지 말고 풀기.

1. 다음 중 미디어 파일에 해당하는 것은? A. 사이트 공통 CSS B. 제작자가 배치한 로고 C. 사용자가 게시글에 올린 사진 D. 프로젝트의 urls.py
2. STATICFILES_DIRS = [BASE_DIR / 'static']의 목적은? A. 미디어 URL 변경 B. 추가 정적 탐색 경로 지정 C. DB 생성 D. html form 생성
3. {% static 'images/a.png' %}는 무엇을 만드는가? A. Django 모델 B. 파일 URL C. DB 컬럼 D. 폼 오류
4. MEDIA_ROOT = BASE_DIR / 'media'의 의미는? A. 이미지 URL 접두사 B. 저장할 실제 디렉터리 C. 앱 이름 D. 관리자 경로
5. MEDIA_URL = 'media/'의 주된 의미는? A. DB파일 이름 B. 업로드 파일 URL 접두사 C. 업로드 파일 용량 D. 정적 파일 경로 목록
6. 이미지 업로드 form에서 반드시 필요한 enctype 값은? A. application/json B. multipart/form-data C. text/plain D. image/png
7. ArticleForm(request.POST, request.FILES)에서 request.FILES의 역할은? A. HTML 제목 B. 업로드 파일 전달 C. DB 삭제 D. CSS 경로
8. 기존 Article 이미지 업데이트에 적절한 ModelForm 생성은? A. ArticleForm(request.POST) B. ArticleForm(instance=request.POST) C. ArticleForm(request.POST, request.FILES, instance=article) D. ArticleForm(MEDIA_URL)
9. 이미지가 없는 경우 .url 오류를 피하는 적절한 코드는? A. {% if article.image %} B. {% url article.image %} C. {% load article.image %} D. {% static article.image %}
10. ImageField(upload_to='images/')에서 images/는 일반적으로 어디 기준 경로인가? A. MEDIA_ROOT 내부 B. STATIC_URL URL C. HTML template directory D. 데이터베이스 테이블명
11. Django ImageField 사용에 필요한 외부 라이브러리는? A. requests B. Pillow C. pandas D. React
12. AWS에서 파일 객체 스토리지에 해당하는 서비스는? A. EC2 B. S3 C. RDS D. IAM
13. AWS에서 관계형 DB 관리 서비스는? A. Lambda B. RDS C. Route53 D. CloudFront
14. settings.DEBUG가 True일 때 강의의 개발용 MEDIA URL 연결 코드를 작성하는 이유는? A. 파일 업로드 유효성 검사 생략 B. 개발 서버에서 업로드 파일 접근 테스트 C. DB 자체 삭제 D. 정적 파일 이름 변경
15. 다음 중 옳지 않은 설명은? A. STATIC_URL은 URL 접두사다 B. MEDIA_ROOT는 파일시스템 경로다 C. request.POST만 전달하면 업로드 파일도 항상 ModelForm에 바인딩된다 D. static 태그 라이브러리는 load한다

### 객관식 정답/해설

1 C — 사용자 업로드 사진.

2 B — 추가 정적 탐색 경로.

3 B — URL 생성.

4 B — 물리적 저장 경로.

5 B — 미디어 공개 URL 접두사.

6 B — 파일 전송 인코딩.

7 B — 파일 데이터.

8 C — 파일과 기존 인스턴스 모두 전달.

9 A — 파일 없을 때 조건부 렌더링.

10 A — MEDIA_ROOT 아래 상대 경로.

11 B — 이미지 검증 지원.

12 B — 객체 스토리지.

13 B — 관리형 RDB.

14 B — 개발 환경용 매핑.

15 C — 파일은 request.FILES로 받아야 한다.

## 6. 주관식 예상문제 10개

1. Django에서 정적 파일의 URL 접두사를 지정하는 설정 이름은? → STATIC_URL
2. 앱별 static 폴더 외의 정적 파일 탐색 경로 목록을 정하는 설정은? → STATICFILES_DIRS
3. 템플릿에서 static 태그 라이브러리를 가져오는 코드 전체는? → {% load static %}
4. 사용자 업로드 파일이 저장될 실제 서버 디렉터리를 정하는 설정은? → MEDIA_ROOT
5. 업로드 파일에 접근할 URL 접두사 설정은? → MEDIA_URL
6. Django에서 업로드된 이미지 처리에 필요한 외부 라이브러리는? → Pillow
7. HTML Form에서 파일 데이터를 전송하기 위한 enctype 속성값은? → multipart/form-data
8. View에서 일반 입력값과 별도로 업로드 파일을 받는 요청 속성은? → request.FILES
9. DB에 저장된 ImageField의 URL을 템플릿에서 출력하는 표현식은? → {{ article.image.url }}
10. 사용자가 업로드한 이미지 저장 하위 경로를 Model 필드에서 정하는 옵션은? → upload_to

## 7. 서술형 예상문제 5개 — 만점 모범답안과 채점 키워드

### S1. Static과 Media의 차이, 경로 설정을 비교하시오.

모범답안: Static files는 개발자가 미리 준비한 CSS, JavaScript, 로고 등의 파일이고 Media files는 사용자가 서비스 이용 중 업로드한 파일이다. Static은 STATIC_URL로 웹 URL 접두사를 지정하고 STATICFILES_DIRS로 추가 탐색 경로를 지정한다. Media는 MEDIA_ROOT로 실제 파일 저장 디렉터리, MEDIA_URL로 브라우저 접근 URL 접두사를 설정한다. 채점 키워드: 개발자 준비 / 사용자 업로드 / URL / 물리적 경로.

### S2. 게시글 이미지 업로드 과정 전체를 서술하시오.

모범답안: 모델에 ImageField를 선언하고 Pillow를 설치한다. 필드 추가에 필요한 마이그레이션을 적용한다. HTML Form에는 method="POST", enctype="multipart/form-data", CSRF 토큰을 설정한다. View에서 ArticleForm(request.POST, request.FILES)로파일을 포함해 바인딩한다. is_valid()를 통과한 경우 save()로 저장하고, 템플릿에서는 article.image.url을 사용하여 접근할 수있다. 개발 단계에는 MEDIA_ROOT와 MEDIA_URL을 설정하고 개발용 URL 제공도 구성한다. 채점 키워드: ImageField / Pillow / multipart / request.FILES / is_valid / save / .url.

### S3. MEDIA_ROOT와 MEDIA_URL을 구분하고 각각 예를 제시하시오.

모범답안: MEDIA_ROOT는 업로드한 파일이 실제 저장되는 서버의 디렉터리로 BASE_DIR / 'media'처럼 지정한다. MEDIA_URL은 저장된 파일에 웹 브라우저가 접근할 때 사용하는 URL 접두사로 'media/'처럼 지정할 수 있다. 즉 전자는 파일시스템 경로이고 후자는웹 URL이다. 채점 키워드: 실제 디렉터리 / 웹 URL 접두사 / 차이.

### S4. 이미지를 포함한 기존 게시글을 수정하는 과정을 서술하시오.

모범답안: 요청된 pk로 기존 Article 인스턴스를 조회하고, POST 시 ArticleForm(request.POST, request.FILES, instance=article)로 폼을 구성한다. 이때 instance는 기존 글을 수정 대상으로 지정하고 request.FILES는 새 업로드 파일을 전달한다. Form의 유효성을 검증한 다음 저장한다. 템플릿 form은 multipart/form-data로인코딩해야 한다. 채점 키워드: 기존 객체 조회 / instance / request.FILES / enctype / is_valid / save.

### S5. Django 애플리케이션의 EC2, S3, RDS 역할을 설명하시오.

모범답안: EC2는 Django 애플리케이션을 실행하는 컴퓨팅 자원, S3는 이미지 등 정적·미디어 파일을 저장하는 객체 스토리지, RDS는 관계형 데이터베이스를 관리하는 서비스다. 역할을 분리하면 서버·파일·DB 자원을 필요에 맞게 관리하고 확장할 수 있다. 채점 키워드: EC2 컴퓨팅 / S3 객체 저장 / RDS 관계형 DB.

## 8. 코드 추론·빈칸 보완 8개

C1. STATIC_URL = 'static/'이고 {% static 'images/a.png' %}가 사용되면 기본 URL은? → /static/images/a.png (일반적인 루트구성 기준)

C2. MEDIA_ROOT = BASE_DIR / 'media', upload_to='images/', 업로드 이름이 cat.png이고 이름 충돌이 없다면 저장 상대경로는? → images/cat.png; 물리적 경로는 BASE_DIR/media/images/cat.png.

C3. 코드 빈칸: ArticleForm(request.POST, _____) → request.FILES.

C4. 업로드 폼 enctype 속성 누락 시 어떤 문제가 생기는가? → 파일이 정상적으로 request.FILES에 들어오지 않아 업로드가 실패할 수 있음.

C5. &lt;img src="{{ article.image.path }}"&gt;가 웹 접근용으로 부적절한 이유는? → path는 파일시스템 경로이지 웹 URL이 아님. .url 사용.

C6. 새 파일로 수정할 때 ArticleForm(request.POST, request.FILES)만 생성하면? → 기존 인스턴스 지정이 없어 새 객체 생성으로이어질 수 있음. instance=article 필요.

C7. urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)에서 두 설정의 순서를 바꾸면? → URL 접두사와 실제 저장 경로가 뒤바뀌어 설정이 잘못됨.

C8. 아래 코드에서 업로드 파일이 없는 글이라면 무엇을 보완해야 하는가?

```
<img src="{{ article.image.url }}">
```

→ {% if article.image %}로 감싸 이미지가 있을 때만 .url에 접근.

## 9. 실전형 헷갈림 포인트 12개

1. STATIC_URL은 실제 저장 경로가 아니다.
2. STATICFILES_DIRS는 파일 리스트가 아니라 탐색 디렉터리의 리스트.
3. {% load static %}와 {% static ... %}는 역할이 다르다.
4. Static files와 Media files는 누가 생성/업로드했는지 기준이 다르다.
5. MEDIA_ROOT는 파일시스템 위치, MEDIA_URL은 접근 URL.
6. ImageField는 대체로 DB에 파일 경로/이름을 저장한다.
7. ImageField의 이미지 처리를 위해 Pillow가 필요하다.
8. upload_to는 일반적으로 MEDIA_ROOT 내부 상대경로.
9. POST 파일 업로드에는 multipart/form-data + request.FILES를 함께 기억한다.
10. 파일 업로드와 CSRF 방어는 전혀 다른 기능.
11. 새 글 생성과 수정은 instance 존재 여부가 다르다.
12. .url과 .path는 다르며, ImageField가 비어 있을 때 .url 접근은 피한다.

## 10. 이전 단원 연결 문제

- 2단원 Template: DTL의 {% %}는 템플릿 태그에 사용된다. 여기서는 {% load static %}와 {% static ... %}.
- 3단원 Model: ImageField를 추가했으면 makemigrations → migrate.
- 4단원 ORM: 모델 인스턴스의 article.image는 ImageField를 통해 다루는 파일 객체 성격이다.
- 5단원 CRUD: POST로 생성·수정하며 성공 후 redirect하는 흐름.
- 6단원 Form: ModelForm, is_valid(), save(), instance + 이번 단원의 request.FILES.

## 11. 시험 전 90초 초압축 암기장

```
Static = 개발자 제공 CSS/JS/로고
Media = 사용자 업로드 이미지
STATIC_URL = URL 접두사
STATICFILES_DIRS = 추가 정적 파일 검색 경로 리스트
{% load static %}
{% static 'images/a.png' %}
MEDIA_ROOT = 물리적 저장 디렉터리
MEDIA_URL = 접근 URL 접두사
ImageField(upload_to='images/', blank=True)
pip install Pillow
<form method="POST" enctype="multipart/form-data">
ArticleForm(request.POST, request.FILES)
ArticleForm(request.POST, request.FILES, instance=article)
{% if article.image %}{{ article.image.url }}{% endif %}
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 개발 중
EC2 = 서버 / S3 = 객체 저장 / RDS = 관계형 데이터베이스
```

## 12. 이번 단원 학습 전략 (권장 35분)

- 0~8분: 2장 비교표를 백지에 다시 적어보고 Static과 Media 경로 설정 구분.
- 8~16분: 업로드 코드(HTML form → View → ModelForm → ImageField → 템플릿)를 손으로 1회 완성.
- 16~26분: 객관식 15문제 + 주관식 10문제, 정답 확인 전 셀프 채점.
- 26~32분: 서술형 S2(업로드 전체 흐름)와 S4(수정 흐름)를 키워드로 써보기.
- 32~35분: 오답만 다시 풀고, 마지막 90초 암기장 암송.

### 복습 체크리스트

- STATIC_URL과 STATICFILES_DIRS 차이를 즉시 말할 수 있다.
- MEDIA_ROOT와 MEDIA_URL 차이를 즉시 말할 수 있다.

업로드 Form의 두 핵심 요소(POST, enctype)와 CSRF 역할을 구분한다. • request.POST와 request.FILES 차이를 설명한다.

- 생성과 수정의 ModelForm 호출 차이를 정확히 적는다.
- 업로드 이미지를 화면에 보여 주는 DTL 구문을 적는다.
- EC2, S3, RDS를 즉시 구분한다.

학습자료 범위 주의: 개발 환경의 static(...) 미디어 제공 방식은 운영 환경에 그대로 적용하면 안 된다. 실제 운영에서는 서버/스토리지의 배포 설정과 보안 제어가 필요하다. 원본 확인문제는 본 문서에서 핵심 학습목표 기준으로 재구성했으므로 강의 슬라이드의 문구 및 보기와 동일하지 않을 수 있다.
