# Django 7단원 CBT — Static & Media (30문항)

> 출제 범위: [`../07_static_media.md`](../07_static_media.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. Static files와 Media files의 구분으로 **옳은** 것은?

- ① Static은 개발자가 미리 준비한 파일, Media는 사용자가 업로드한 파일이다.
- ② Static은 사용자가 업로드한 파일, Media는 개발자가 준비한 파일이다.
- ③ Static은 이미지만, Media는 CSS·JS만 포함한다.
- ④ 둘 다 파일 자체가 DB에 저장된다.

---

### 2. Django 서비스를 AWS에 배포할 때 업로드 이미지 같은 파일을 저장하는 서비스는?

- ① EC2
- ② RDS
- ③ S3
- ④ IAM

---

### 3. 정적 파일이 웹 페이지에 보이기 위한 핵심 조건은?

- ① 파일이 DB에 저장되어 있어야 한다.
- ② 그 파일에 접근할 수 있는 고유한 URL이 있어야 한다.
- ③ 파일 이름이 static으로 시작해야 한다.
- ④ 파일이 manage.py와 같은 폴더에 있어야 한다.

---

### 4. Django가 정적 파일을 찾는 기본 경로는?

- ① `app폴더/static/`
- ② `프로젝트폴더/staticfiles/`
- ③ `app폴더/templates/static/`
- ④ `BASE_DIR/media/`

---

### 5. 템플릿에서 static 태그를 쓰기 전에 반드시 작성해야 하는 코드는?

- ① `{% load static %}`
- ② `{% import static %}`
- ③ `{% include static %}`
- ④ `{% extends static %}`

---

### 6. `{% load static %}`에 대한 설명으로 **옳지 않은** 것은?

- ① static 관련 태그를 쓰겠다는 선언이다.
- ② extends를 쓰는 템플릿에서는 extends 바로 다음 줄에 작성한다.
- ③ built-in 태그가 아니기 때문에 불러와야 한다.
- ④ 부모 템플릿에서 load했다면 자식에서는 다시 load할 필요가 없다.

---

### 7. `STATIC_URL = 'static/'`, 파일이 `articles/static/images/sample-1.png`일 때 `{% static 'images/sample-1.png' %}`가 만드는 주소는?

- ① `articles/static/images/sample-1.png`
- ② `/articles/images/sample-1.png`
- ③ `/static/images/sample-1.png`
- ④ `C:/project/articles/static/images/sample-1.png`

---

### 8. STATIC_URL에 대한 설명으로 **옳은** 것은?

- ① 정적 파일이 저장된 서버의 실제 폴더 경로다.
- ② 정적 파일을 추가로 탐색할 폴더 목록이다.
- ③ 값을 바꾸면 정적 파일의 실제 저장 위치도 함께 이동한다.
- ④ 정적 파일에 접근할 웹 주소의 접두사다.

---

### 9. 특정 앱에 속하지 않는 정적 파일을 프로젝트 최상위 static/ 폴더에서도 찾게 하는 설정은?

- ① `STATIC_URL = BASE_DIR / 'static'`
- ② `STATIC_ROOT = 'static/'`
- ③ `STATICFILES_DIRS = [BASE_DIR / 'static']`
- ④ `TEMPLATES['DIRS'] = [BASE_DIR / 'static']`

---

### 10. ImageField에 대한 설명으로 **옳은** 것은?

- ① 이미지 파일 자체(바이너리)가 DB 컬럼에 저장된다.
- ② DB에는 상대 경로 문자열만 저장된다.
- ③ 별도 라이브러리 없이 바로 사용할 수 있다.
- ④ upload_to는 반드시 지정해야 하는 필수 인자다.

---

### 11. ImageField 추가 후 makemigrations에서 `Cannot use ImageField because Pillow is not installed` 에러가 났다. 해결 방법은?

- ① ImageField를 CharField로 바꾸고 경로를 직접 저장한다.
- ② settings.py에 MEDIA_ROOT를 먼저 설정한다.
- ③ makemigrations 대신 migrate를 먼저 실행한다.
- ④ Pillow를 설치한 뒤 다시 makemigrations 한다.

---

### 12. MEDIA_ROOT와 MEDIA_URL에 대한 설명으로 **옳은** 것은?

- ① ROOT는 웹 주소 접두사, URL은 실제 저장 폴더다.
- ② ROOT는 실제 저장 폴더, URL은 웹 주소 접두사다.
- ③ 둘 다 업로드 파일의 웹 주소를 뜻하는 설정이다.
- ④ 둘 다 settings.py가 아니라 models.py에 작성한다.

---

### 13. 개발 서버에서 업로드 파일을 제공하기 위해 프로젝트 urls.py의 urlpatterns 뒤에 추가하는 코드는?

- ① `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
- ② `+ static(settings.MEDIA_ROOT, document_root=settings.MEDIA_URL)`
- ③ `+ include('media.urls')`
- ④ `+ static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)`

---

### 14. 위 `static()` 설정에 대한 설명으로 **옳지 않은** 것은?

- ① MEDIA_URL로 시작하는 요청을 MEDIA_ROOT 폴더에서 찾아 응답하게 한다.
- ② 개발 서버는 media 파일을 자동으로 제공하지 않아 직접 추가해야 한다.
- ③ DEBUG=True인 개발 단계에서만 동작한다.
- ④ 실제 운영 서비스에서도 이 설정으로 미디어 파일을 제공하는 것이 권장된다.

---

### 15. 이미지를 첨부하지 않아도 게시글을 작성할 수 있게 하려면?

- ① `image = models.ImageField(upload_to='images/', null=True)`
- ② `image = models.ImageField(upload_to='images/', default=None)`
- ③ `image = models.ImageField(upload_to='images/', blank=True)`
- ④ `image = models.ImageField(upload_to='images/', required=False)`

---

### 16. 파일 업로드 form에 반드시 추가해야 하는 속성은?

- ① `enctype="multipart/form-data"`
- ② `enctype="application/json"`
- ③ `method="FILE"`
- ④ `accept="multipart"`

---

### 17. 이미지 업로드 create view에서 빈칸에 알맞은 것은?

```python
form = ArticleForm(request.POST, _______)
```

- ① `request.GET`
- ② `request.FILES`
- ③ `request.IMAGE`
- ④ `instance=request.FILES`

---

### 18. ModelForm의 **두 번째 위치 인자**로 request.FILES를 넘기는 이유는?

- ① request.POST에 파일이 함께 들어 있어 순서를 맞추기 위해
- ② BaseModelForm 생성자의 두 번째 인자가 files라서
- ③ CSRF 토큰을 검증할 때 업로드 파일 정보가 필요해서
- ④ 두 번째 위치 인자 자리가 instance로 정해져 있어서

---

### 19. 상세 페이지에서 업로드된 이미지를 출력하려 한다. 빈칸에 들어갈 코드로 **옳은** 것은?

```html
{% if article.image %}
  _______
{% endif %}
```

- ① `<img src="{% static article.image %}">`
- ② `<img src="{{ article.image.path }}">`
- ③ `<img src="{{ article.image.url }}">`
- ④ `<img src="{{ article.image }}">`

---

### 20. 이미지가 포함된 게시글을 수정(POST)할 때 폼 생성 코드로 옳은 것은?

- ① `ArticleForm(request.POST, instance=article)`
- ② `ArticleForm(request.FILES, request.POST, instance=article)`
- ③ `ArticleForm(request.POST, request.FILES)`
- ④ `ArticleForm(request.POST, request.FILES, instance=article)`

---

## 함정 문제 (21~30)

### 21. `MEDIA_ROOT = BASE_DIR / 'media'`, `upload_to='images/'`인 ImageField에 cat.png를 올렸다(이름 충돌 없음). DB의 image 컬럼에 저장되는 값은?

- ① `media/images/cat.png`
- ② `images/cat.png`
- ③ `BASE_DIR/media/images/cat.png`
- ④ `/media/images/cat.png`

---

### 22. 위 파일의 웹 주소는? (`MEDIA_URL = 'media/'`, 개발 서버)

- ① `http://127.0.0.1:8000/media/images/cat.png`
- ② `http://127.0.0.1:8000/images/cat.png`
- ③ `http://127.0.0.1:8000/static/images/cat.png`
- ④ `http://127.0.0.1:8000/articles/media/cat.png`

---

### 23. STATICFILES_DIRS의 `static/style.css`와 `articles/static/style.css`가 **둘 다** 있을 때 `{% static 'style.css' %}`가 제공하는 파일은?

- ① articles 앱의 style.css
- ② 두 파일이 합쳐진 style.css
- ③ STATICFILES_DIRS 쪽 파일
- ④ 이름이 겹쳐서 에러가 발생한다.

---

### 24. `STATICFILES_DIRS`의 형태로 **옳은** 것은?

- ① 추가로 탐색할 **폴더** 경로들의 리스트
- ② 제공할 정적 **파일** 이름들의 리스트
- ③ 정적 파일 URL 접두사 문자열
- ④ collectstatic 결과를 모으는 단일 폴더

---

### 25. `{% load static %}`과 `{% static '...' %}`의 역할로 **옳은** 것은?

- ① load static이 URL을 만들고, static 태그는 선언만 한다.
- ② load static은 태그를 불러오는 선언, static 태그가 URL을 만든다.
- ③ 둘은 같은 기능이라 하나만 써도 된다.
- ④ load static은 settings.py에 한 번만 작성한다.

---

### 26. form에 enctype 없이 `method="POST"`만 쓴 채 이미지를 업로드하면?

- ① 이미지가 정상적으로 업로드되어 저장된다.
- ② CSRF 검증에 실패해 403이 난다.
- ③ 이미지가 request.POST에 담겨 저장된다.
- ④ request.FILES가 비어 업로드되지 않는다.

---

### 27. 파일 업로드 form의 enctype과 `{% csrf_token %}`에 대한 설명으로 **옳은** 것은?

- ① enctype은 파일 인코딩용, csrf_token은 위조 방지용이다.
- ② enctype="multipart/form-data"를 쓰면 csrf_token은 생략해도 된다.
- ③ csrf_token이 파일을 multipart 형식으로 인코딩해 준다.
- ④ 파일 업로드 form은 GET 방식으로 보내야 csrf_token이 필요 없다.

---

### 28. 다음 함수를 upload_to에 지정했을 때, **새 글**의 첫 업로드에서 생길 수 있는 문제는?

```python
def articles_image_path(instance, filename):
    return f'images/{instance.pk}/{filename}'
```

- ① filename이 항상 None이라 에러가 난다.
- ② upload_to에는 함수를 쓸 수 없어 에러가 난다.
- ③ pk가 None이라 images/None/ 경로가 된다.
- ④ MEDIA_ROOT가 무시되고 static 폴더에 저장된다.

---

### 29. settings.py에 MEDIA_ROOT·MEDIA_URL만 설정하고 프로젝트 urls.py에 `static(...)`을 추가하지 않았다. 업로드 이미지 주소로 접속하면? (개발 서버)

- ① 정상적으로 이미지가 보인다.
- ② static 폴더에서 대신 찾아 보여준다.
- ③ 403 Forbidden이 난다.
- ④ 일치하는 URL 패턴이 없어 404가 난다.

---

### 30. 다음 중 Media file에 해당하는 것은?

- ① Bootstrap CSS 파일
- ② 사이트 상단 로고 이미지
- ③ 회원이 올린 프로필 사진
- ④ 프로젝트 공통 JavaScript 파일

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ① | ③ | ② | ① | ① | ④ | ③ | ④ | ③ | ② |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ② | ① | ④ | ③ | ① | ② | ② | ③ | ④ |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ② | ① | ③ | ① | ② | ④ | ① | ③ | ④ | ③ |

- **1. ①** 만드는 주체가 기준이다. 로고·CSS는 Static, 후기 사진처럼 사용자가 올린 건 Media.
- **2. ③** EC2 = 애플리케이션 서버 실행, S3 = 객체 스토리지(파일 저장), RDS = 관리형 관계형 DB.
- **3. ②** 컴퓨터에 파일이 있는 것만으로는 안 된다. 웹에서 찾아갈 주소(URL)가 필요하다.
- **4. ①** 기본 경로는 각 앱의 static 폴더. static 태그에는 그 이후 경로만 적는다.
- **5. ①** static은 built-in 태그가 아니라서 load로 불러와야 한다.
- **6. ④** load는 템플릿마다 따로 적용된다. 부모에서 load했어도 자식에서 static을 쓰려면 다시 load해야 한다.
- **7. ③** 서버 주소 + STATIC_URL + 정적 파일 경로. static 태그는 실제 파일 경로가 아니라 웹 주소를 만든다.
- **8. ④** STATIC_URL은 브라우저에서만 쓰는 주소의 시작 부분. ②는 STATICFILES_DIRS 설명.
- **9. ③** STATICFILES_DIRS는 앱 static 외에 추가로 탐색할 실제 폴더 목록(리스트). 탐색 순서는 STATICFILES_DIRS가 먼저.
- **10. ②** 파일은 MEDIA_ROOT 폴더에, DB에는 `images/sample.png` 같은 경로 문자열만. Pillow가 필요하고 upload_to는 선택 인자.
- **11. ④** ImageField는 이미지 검증에 Pillow 라이브러리가 반드시 필요하다. 설치 후 freeze로 requirements.txt도 갱신.
- **12. ②** ROOT = 실제 창고(서버 내부 경로), URL = 웹 주소 별명. settings.py에 `MEDIA_ROOT = BASE_DIR / 'media'`, `MEDIA_URL = 'media/'`.
- **13. ①** 첫 인자는 웹 주소(MEDIA_URL), document_root는 실제 폴더(MEDIA_ROOT). 순서가 바뀌면 설정이 꼬인다.
- **14. ④** 운영 환경에서는 웹 서버나 S3 같은 저장소가 미디어 파일을 제공한다.
- **15. ③** 폼 검증에서 빈 값을 허용하는 건 blank. null은 DB 레벨, required는 모델 필드 옵션이 아니다.
- **16. ①** enctype은 form 데이터를 어떤 형식으로 인코딩할지 정한다. 파일 업로드는 multipart/form-data 필수.
- **17. ②** 일반 입력값은 request.POST, 업로드 파일은 request.FILES에 담긴다.
- **18. ②** `__init__(self, data=None, files=None, ...)`. instance는 키워드 인자로 넘긴다.
- **19. ③** 업로드 파일의 웹 주소는 `.url`. .path는 서버 파일 경로라 웹에서 못 쓰고, static 태그는 개발자가 넣은 정적 파일용. 이미지 없는 글에서 .url을 쓰면 ValueError라 if로 감싼다.
- **20. ④** data → files 순서의 위치 인자 + 기존 글 수정용 instance. ②는 순서가 바뀌었고, ①은 파일이, ③은 instance가 빠졌다. 수정 form에도 enctype이 필요하다.
- **21. ②** DB에는 MEDIA_ROOT 기준 상대 경로만 저장된다. 실제 파일은 BASE_DIR/media/images/cat.png에 있다.
- **22. ①** 서버 주소 + MEDIA_URL + DB에 저장된 상대 경로. `article.image.url`이 이 주소를 만들어 준다.
- **23. ③** 탐색 순서는 STATICFILES_DIRS가 먼저, 그다음 각 앱의 static. 먼저 찾은 파일이 쓰인다.
- **24. ①** `[BASE_DIR / 'static']`처럼 폴더 목록. ③은 STATIC_URL, ④는 STATIC_ROOT.
- **25. ②** load는 "이 템플릿에서 static 태그를 쓰겠다"는 선언(템플릿마다 필요), static 태그가 STATIC_URL을 붙여 주소를 만든다.
- **26. ④** multipart/form-data가 아니면 파일 내용이 전송되지 않는다. 이미지 필드가 blank=True면 에러 없이 이미지만 빠진 채 저장돼서 더 헷갈린다.
- **27. ①** 둘은 전혀 다른 기능이라 파일 업로드 POST form에는 둘 다 필요하다.
- **28. ③** upload_to는 함수(instance, filename → 경로 문자열)도 받는다. 다만 새 객체는 파일 저장 시점에 아직 pk가 없을 수 있다.
- **29. ④** 개발 서버는 static은 자동 제공하지만 media는 직접 URL 규칙을 추가해야 제공한다.
- **30. ③** 기준은 "누가 만들었나". 사용자가 업로드하면 Media, 개발자가 미리 넣어 두면 Static(이미지라도).
