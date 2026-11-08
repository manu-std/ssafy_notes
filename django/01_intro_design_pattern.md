# Django 01 — Intro & Design Pattern

> 📎 확인문제·예상문제·암기카드: [`시험대비/01_intro_design_pattern_시험대비.md`](시험대비/01_intro_design_pattern_시험대비.md)

*(Django 트랙 1차시. 웹의 기본 구조 → 가상환경 → 프로젝트 생성 → MTV 패턴 → 요청·응답 흐름까지, 이후 모든 단원의 뼈대가 되는 내용이다.)*

## 오늘의 목차

1. 웹 기초 개념
2. 가상 환경
3. 의존성 패키지
4. Django 프로젝트 생성 및 서버 실행
5. 디자인 패턴 (MVC / MTV)
6. 프로젝트와 앱
7. 요청과 응답
8. Trailing Comma (후행 쉼표)
9. 프레임워크의 규칙

---

## 1. 웹 기초 개념

### Web Application (Web Service)

- 인터넷을 통해 사용자에게 제공되는 소프트웨어 프로그램
- 브라우저를 통해 접근하며, 다양한 디바이스로 접근 및 사용 가능

### 클라이언트 - 서버 구조

인터넷에 연결된 서로 다른 두 컴퓨터가 데이터를 주고받는 웹의 동작 방식 중 하나.

| 구분 | 역할 | 예시 |
|---|---|---|
| **클라이언트(Client)** | 서비스를 **요청**하는 주체 (HTTP Request를 보냄) | 웹 브라우저, 모바일 앱 |
| **서버(Server)** | 클라이언트의 요청에 **응답**하는 주체 (HTTP Response를 반환) | 웹 서버, 데이터베이스 서버 |

```text
주소 입력 → 브라우저가 HTTP 요청 → 서버가 요청 처리 → 응답(HTML 등) → 브라우저 화면에 표시
```

> ⚠️ 함정: "사용자의 요청을 받아 처리하는 역할" → **서버**. 요청을 *보내는* 쪽이 클라이언트다.

### Frontend와 Backend

| 구분 | 담당 | 구성 기술 |
|---|---|---|
| **Frontend** | 사용자 인터페이스 구성, 사용자와 애플리케이션의 상호작용 | HTML(구조), CSS(스타일), JavaScript(동작), 프론트엔드 프레임워크 |
| **Backend** | 서버 측에서 동작. 클라이언트 요청 처리, 비즈니스 로직, 인증, DB 상호작용 | 서버 언어, 백엔드 프레임워크, 데이터베이스, API |

> 💡 둘은 대립하는 개념이 아니라 **한 서비스를 구성하는 서로 다른 역할**이다. Django는 Python 기반 **백엔드** 웹 프레임워크.

### 웹 프레임워크

- 웹 애플리케이션을 빠르게 개발할 수 있도록 도와주는 도구
- 개발에 필요한 **기본 구조, 규칙, 라이브러리** 등을 제공
- 주요 목적: **웹 개발에 필요한 코드를 줄이고 구조화를 도움** → 협업·유지보수가 쉬워짐
- 예시: Django, Spring, Express

### Django

- Python 기반의 대표적인 웹 프레임워크
- **MTV 패턴** 기반, 보안 기능 내장, **ORM** 제공
- 다양한 템플릿 엔진 사용 가능 → "고정된 HTML 템플릿만 사용 가능"은 **틀린 설명**
- 구성요소: Models, Templates, Views → **Compiler는 포함되지 않음**

> ⚠️ Django는 컴파일러가 아니고, 정적 HTML만 보여주는 도구도 아니다 (동적 데이터 전달·템플릿 사용 가능).

---

## 2. 가상 환경

### 정의

- 하나의 컴퓨터 안에서 또 다른 **독립된 파이썬 환경**
- **Python global**: 컴퓨터 전체에서 사용되는 기본 Python 환경
- 가상 환경 A, B는 Python global 환경 안에서 각자 다른 버전의 패키지를 가질 수 있음

> 📌 가상 환경은 **Python 패키지/실행 환경을 격리**하는 것이지, CPU·RAM을 물리적으로 나누는 가상머신(VM)이 아니다.

### 필요한 이유

1. **프로젝트마다 다른 버전의 라이브러리 사용** 가능 (예: Django 4.2 / 5.2 동시 유지)
2. **의존성 충돌 방지**: 프로젝트별로 라이브러리를 독립적으로 관리
3. **팀원 간 협업**: 같은 버전의 라이브러리를 설치해 에러 가능성 감소

> 확인 문제: 가상 환경 사용 이유 → **특정 프로젝트마다 독립적인 파이썬 패키지를 관리하기 위해**

### 명령어

| 단계 | 명령어 | 비고 |
|---|---|---|
| 생성 | `python -m venv venv` | 현재 디렉토리에 venv 폴더 생성. 이름은 자유지만 관례적으로 `venv` |
| 활성화 (Windows Git Bash) | `source venv/Scripts/activate` | 프롬프트 앞에 `(venv)` 표시되면 성공 |
| 활성화 (Windows PowerShell) | `.\venv\Scripts\Activate.ps1` | 셸에 따라 경로·명령이 다름 |
| 활성화 (Mac/Linux) | `source venv/bin/activate` | OS별로 venv 폴더 구조가 달라 명령어도 다름 |
| 종료 | `deactivate` | Python Global 환경으로 돌아감 |

> 확인 문제: venv로 가상환경 생성 → **`python -m venv 환경이름`** (`python install venv`, `pip install venv create`는 오답)
>
> ⚠️ `python -m venv venv`는 **생성만** 한다. 활성화는 별도 단계.

### 주의사항 및 권장사항

1. 가상 환경에 "들어가고 나오는" 것이 아니라, 사용할 Python 환경을 **On/Off로 전환**하는 개념
   - 활성화는 **현재 터미널 환경에만** 영향
   - 새 터미널 창을 열면 **다시 활성화** 필요
2. **프로젝트마다 별도의 가상 환경** 사용
3. venv 폴더는 **관련 프로젝트와 동일한 경로에 위치**
4. venv 폴더는 `.gitignore`에 작성해 **원격 저장소에 공유하지 않음**
   - 저장소 크기 감소, OS별 차이로 인한 문제 방지
   - 대신 `requirements.txt`를 공유해 각자 가상 환경 구성

---

## 3. 의존성 패키지

### 용어

| 용어 | 의미 |
|---|---|
| **의존성(Dependencies)** | 하나의 소프트웨어가 동작하기 위해 필요로 하는 다른 소프트웨어나 라이브러리 |
| **의존성 패키지** | 프로젝트가 의존하는 개별 라이브러리 (프로젝트 실행에 꼭 필요한 각각의 패키지) |
| **패키지** | 연관된 모듈들을 하나의 디렉토리에 모아놓은 것 |
| **pip** | 외부 패키지 설치를 도와주는 파이썬의 패키지 관리 시스템 |

### 명령어

| 목적 | 명령어 | 설명 |
|---|---|---|
| 목록 확인 | `pip list` | 현재 가상 환경에 설치된 라이브러리 목록. 갓 만든 환경엔 pip, setuptools 정도만 존재 |
| 의존성 기록 (내보내기) | `pip freeze > requirements.txt` | 설치된 모든 패키지와 버전을 파일로 저장. 파일명은 관례적으로 `requirements.txt` |
| 의존성 설치 (가져오기) | `pip install -r requirements.txt` | 파일에 명시된 라이브러리를 한 번에 설치 |

- `>` : pip 명령어가 아닌 **CLI(Shell)의 Redirection operator**. 이전 명령어의 출력을 파일로 보냄. 다시 실행하면 **기존 파일 내용을 덮어씀**
- `-r` : `--requirement`의 축약형. 텍스트 파일을 읽어 그 안의 모든 패키지를 설치하라는 옵션
- `requests` 하나만 설치해도 certifi, idna, urllib3 등 여러 패키지가 함께 설치됨 → requests 자체가 필요로 하는 의존성이 있기 때문

> ⚠️ `pip freeze`는 **그 시점에 설치된 패키지 전부**를 내보낸다. 프로젝트에서 실제로 import한 패키지만 골라 주는 기능이 아니다. 그리고 freeze는 "기록", 설치는 `install -r` — 역할을 헷갈리지 말 것.

### 의존성 관리가 필요한 이유

- **환경의 통일**: 버전이 다르면 함수명이나 동작이 달라질 수 있음 → "내 컴퓨터에선 되는데 네 컴퓨터에선 안 돼" 문제 해결
- **협업 효율**: 팀원 간 동일한 개발 환경을 즉시 구축 가능
- 시나리오: A가 GitHub에 push → B가 clone 후 실행 실패 → A의 패키지 목록을 알 수 없기 때문 → **패키지 목록(requirements.txt) 공유 필요**

### ⭐ 전체 흐름 요약 (이거 모르면 시험 못 친다)

```bash
python -m venv venv                # 1. 생성
source venv/Scripts/activate       # 2. 활성화
pip install django                 # 3. 패키지 설치
pip freeze > requirements.txt      # 4. 의존성 기록
pip install -r requirements.txt    # 5. 다른 환경에서 동일하게 설치
deactivate                         # 6. 비활성화
```

---

## 4. ⭐ Django 프로젝트 생성 및 서버 실행 (앙나중요!)

| 순서 | 명령어 | 설명 |
|---|---|---|
| 1. Django 설치 | `pip install django` | 버전 미지정 시 Python 3.11 기준 최신 5.2.x 설치 |
| 2. 프로젝트 생성 | `django-admin startproject firstpjt .` | `firstpjt` 폴더와 `manage.py` 생성. 끝의 `.`은 **현재 위치**에 생성한다는 의미 |
| 3. 서버 실행 | `python manage.py runserver` | **manage.py와 동일한 위치**에서 실행 |
| 4. 서버 확인 | `http://127.0.0.1:8000/` 접속 | 로켓 화면이 나오면 성공 |

> 📌 "Python 3.11 기준 5.2.x"인 이유: Django 6.0부터는 Python 3.12 이상이 필요해서, 3.11 환경에서 버전 없이 설치하면 설치 가능한 최신인 **5.2 LTS**가 깔린다.
>
> 확인 문제: 프로젝트 생성 명령어 → **`django-admin startproject 프로젝트이름`** (`django create project`, `python startproject` 등은 오답)

- runserver 시 나오는 경고
  - "unapplied migration(s)" 경고: 추후 Model 챕터에서 `migrate`로 해결
  - "This is a development server" 경고: 개발 단계와 무관, 신경 쓰지 않아도 됨

> ⚠️ `runserver`는 **개발용 서버**다. 운영 서비스에 그대로 쓰는 것은 권장되지 않는다.

### 프로젝트 폴더 구조

| 파일 | 역할 | 외우는 포인트 |
|---|---|---|
| `manage.py` | 프로젝트 관리 명령 실행 | `python manage.py runserver` |
| `settings.py` | 프로젝트 설정 | `INSTALLED_APPS`, DB 설정 등 |
| `urls.py` | URL과 View 연결 | URL 라우팅 |
| `__init__.py` | 해당 폴더를 Python 패키지로 인식 | — |
| `asgi.py` | ASGI 서버 인터페이스 | 비동기 웹 서버 연결 (배포 시) |
| `wsgi.py` | WSGI 서버 인터페이스 | 동기 웹 서버 연결 (배포 시) |

---

## 5. 디자인 패턴

### 디자인 패턴(Design Pattern)

- 소프트웨어 설계에서 **반복적으로 발생하는 문제**에 대한, 검증되고 재사용 가능한 일반적인 해결책
- "애플리케이션의 구조는 이렇게 구성하자"라는 모범 답안 또는 관행
- 대표적인 디자인 패턴: **MVC**

> 확인 문제: 반복되는 설계 문제의 일반적 해결 방법 → **디자인 패턴** (알고리즘, 프레임워크 아님)

### MVC 디자인 패턴

| 구성 | 역할 |
|---|---|
| **Model** | 데이터 및 비즈니스 로직 처리 |
| **View** | 사용자에게 보이는 화면 담당 |
| **Controller** | 사용자 입력을 받아 Model과 View를 제어 |

- 목적: 시각적 요소와 뒤에서 실행되는 로직을 서로 영향 없이, 독립적이고 쉽게 유지보수할 수 있는 애플리케이션을 만들기 위함

### MTV 디자인 패턴 (Model, Template, View)

- Django에서 애플리케이션을 구조화하는 디자인 패턴
- **기존 MVC 패턴과 동일하나 단순히 명칭을 다르게 정의한 것**

| MVC | Django MTV | 파일 | 역할 |
|---|---|---|---|
| Model | **Model** | `models.py` | 데이터와 관련된 로직 관리. 데이터 구조를 정의하고 DB 기록 관리 |
| View | **Template** | `<filename>.html` | 레이아웃과 화면 처리. 사용자 인터페이스 구조와 레이아웃 정의 |
| Controller | **View** | `views.py` | Model & Template 관련 로직을 처리해 응답 반환. 클라이언트 요청에 대해 처리를 분기 |

> ⚠️ **가장 헷갈리는 지점**: MVC의 View = Django의 **Template**, MVC의 Controller = Django의 **View**. Django의 View는 화면 HTML 자체가 아니라 **요청을 처리하는 Python 함수/클래스**다.
>
> 확인 문제: 사용자에게 보여지는 화면을 구성하는 요소 → **Template**

- View 동작 예시: Model에서 데이터 가져옴 → Template으로 보내 화면 구성 → 응답으로 만들어 클라이언트에 반환

### 왜 MTV라고 부를까 (Django 공식 FAQ)

- Django에서 "View"는 **어떤 데이터를 보여줄지**를 설명하는 것 (어떻게 보이는지가 아님)
- 따라서 View = 특정 URL에 대한 파이썬 콜백 함수
- **어떻게 보일지**는 Template에 위임
- "Controller"에 해당하는 것은 **프레임워크 자체** (URL 설정에 따라 요청을 적절한 View에 전달)

> 💡 그래서 "MVC Controller ↔ MTV View"는 **개념적 대응**이지 완전한 1:1은 아니다. URLconf가 요청을 View로 넘기는 일부를 맡고 있기 때문.

---

## 6. 프로젝트와 앱

| 구분 | 설명 |
|---|---|
| **Django project** | **애플리케이션의 집합**. DB 설정, URL 연결, 전체 앱 설정 등을 처리 |
| **Django application** | **독립적으로 작동하는 기능 단위 모듈**. 각자 특정 기능을 담당하며 다른 앱들과 함께 하나의 프로젝트를 구성 |

- 예시
  - 카페 프로젝트 → 게시글, 댓글, 회원 관리 앱
  - 쇼핑몰 프로젝트 → 상품 조회, 배송 조회, 결제 앱
  - 교육 관리 프로젝트 → 학생 관리, 문제 관리, 점수 관리 앱

> 확인 문제: App의 역할 → **하나의 기능 또는 모듈 단위를 구성** (전체 서버 운영, 웹사이트 전체 구조 담당은 프로젝트 쪽 설명)

### 앱 생성 → 등록

```bash
python manage.py startapp articles
```

```python
# settings.py
INSTALLED_APPS = [
    'articles',              # 직접 만든 앱
    'django.contrib.admin',
    # ...
]
```

- `startapp`은 앱 폴더와 파일을 **만들기만** 하고, `INSTALLED_APPS` 등록은 **자동으로 해주지 않는다**
- 반드시 **앱 생성 → 등록** 순서 (등록을 먼저 하면 해당 앱 모듈이 없어 에러)

> 확인 문제: 새 앱을 프로젝트에 등록하는 파일 → **`settings.py`의 `INSTALLED_APPS`에** 앱 이름을 추가해야 Django가 인식

### 앱 폴더 구조

| 파일 | 역할 |
|---|---|
| `admin.py` | 관리자 사이트 설정 (모델 등록) |
| `apps.py` | 앱의 정보·설정 (AppConfig) |
| `models.py` | 데이터 모델 정의 — MTV의 **M** |
| `views.py` | 요청 처리 / 응답 생성 — MTV의 **V** |
| `tests.py` | 테스트 코드 작성 |
| `migrations/` | DB 스키마 변경 이력 (모델 변경 기록) |
| `__init__.py` | Python 패키지 표시 |

---

## 7. 요청과 응답

### Django 요청 & 응답 흐름 (4단계)

1. 브라우저가 `http://127.0.0.1:8000/articles/`로 **요청**
2. `urls.py`가 `articles/` 주소와 일치하는 **view 함수 호출**
3. `views.py`의 index view 함수가 (models, templates와 상호작용해) **응답 객체 생성 및 반환**
4. 브라우저는 view 함수가 반환한 응답 객체를 해석해 **페이지를 렌더링**

```text
브라우저 GET /articles/
   ↓
urls.py              (경로 매칭)
   ↓
views.index(request) (요청 처리)
   ↓
render(request, 'articles/index.html')
   ↓
articles/templates/articles/index.html
   ↓
HTTP 응답 → 브라우저 화면 표시
```

- 데이터 흐름: **URLs → View → Template**
- 코드 작성 순서도 데이터 흐름을 따라 **URLs → View → Template** 순으로 작성

### ① URLs (`urls.py`)

```python
from django.contrib import admin
from django.urls import path
from articles import views   # articles 패키지에서 views 모듈을 가져옴

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', views.index),   # url 경로는 반드시 '/'로 끝나야 함
]
```

- `articles/`로 요청이 오면 request 객체를 views 모듈의 index 함수에 전달하며 호출
- `views.index`에 괄호를 붙이지 않는 이유: 요청이 **왔을 때** 호출되어야 하므로 함수 자체(주소)만 넘겨 둔다

### ② View (`views.py`)

```python
from django.shortcuts import render

def index(request):
    return render(request, 'articles/index.html')
```

- 특정 경로의 template과 request 객체를 결합해 **응답 객체를 반환**
- 모든 view 함수는 **첫 번째 인자로 요청 객체를 필수로 받음** (매개변수 이름은 관례적으로 `request`)

### render()

```python
render(request, template_name, context=None)
```

| 인자 | 의미 |
|---|---|
| `request` | 요청 객체 |
| `template_name` | 사용할 템플릿 경로/이름 |
| `context` | 템플릿에 전달할 데이터 (딕셔너리). **선택 인자** |

- 반환값: 템플릿을 렌더링한 **HttpResponse 객체**
- 확인 문제: `render()` → 요청, 템플릿 이름, context 데이터를 받아 **템플릿을 렌더링한 HTTP 응답을 반환**

> ⚠️ render()는 URL을 등록하거나 DB를 다루는 함수가 아니다. "HTML 문자열을 반환한다"도 부정확 — **HttpResponse**를 반환한다.

### ③ Template

1. articles 앱 폴더 안에 `templates` 폴더 생성 (**폴더명은 반드시 `templates`, 개발자가 직접 생성**)
2. templates 폴더 안에 `articles` 폴더 생성
3. articles 폴더 안에 템플릿 파일(`index.html`) 생성

```html
<!-- articles/templates/articles/index.html -->
<h1>Hello, Django</h1>
```

### Template 경로 규칙

- Django는 **`app폴더/templates/`까지를 기본 경로**로 인식
- view 함수에서 템플릿 경로 작성 시 **그 이후 경로만** 작성
  - 실제 위치: `articles/templates/articles/index.html`
  - render에 쓰는 경로: `'articles/index.html'`

> 💡 `templates/` 안에 앱 이름 폴더(`articles/`)를 한 번 더 두는 이유: 여러 앱의 템플릿이 모두 같은 검색 경로에 합쳐지기 때문에, 앱마다 `index.html`이 있으면 **이름이 충돌**한다. 앱 이름 폴더가 네임스페이스 역할을 한다.

---

## 8. Trailing Comma (후행 쉼표)

- 리스트, 딕셔너리, 튜플 등에서 **마지막 요소 뒤에 쉼표를 추가**하는 것
- 문법적으로 아무 영향 없음, 일반적으로 선택사항
  - **예외: 단일 요소 튜플을 만들 때는 필수** — `(1)`은 정수, `(1,)`은 튜플
- 사용 이유: 새 요소 추가나 순서 변경이 편리, diff가 깔끔해짐, 목록이 확장될 것으로 예상될 때 사용, 가독성과 유지보수성 향상
- 권장 패턴: 각 값을 별도 줄에 배치 → 항상 후행 쉼표 추가 → 닫는 괄호는 다음 줄에 배치
- **닫는 괄호와 같은 줄에 후행 쉼표를 두는 것은 권장하지 않음**

```python
# Correct
FILES = [
    'setup.cfg',
    'tox.ini',
    ]

# Wrong
FILES = ['setup.cfg', 'tox.ini',]
```

---

## 9. 프레임워크의 규칙

### 지금까지 등장한 Django 규칙 3가지

1. `urls.py`에서 각 url 문자열 경로는 **반드시 `/`로 끝남**
2. `views.py`에서 모든 view 함수는 **첫 번째 인자로 요청 객체**를 받음 (매개변수 이름은 `request`)
3. Django는 **특정 경로(`app폴더/templates/`)에** 있는 template 파일만 읽어올 수 있음

### 프레임워크 규칙의 의미

- 프레임워크마다 설계 철학이나 목표를 반영한 규칙이 있음 (일관성 유지, 보안 강화, 유지보수성 향상, 최적화)
- 프레임워크는 **도구와 환경을 제공하기 위해 규칙을 정해 놓은 것**
- 이를 잘 활용해 기능 구현 방법을 표준화하고 개발 프로세스를 단순화해야 함

> ⚠️ "결과만 같으면 아무 파일에 코드를 넣어도 된다"는 위험한 오답. URL은 urls.py, 요청 처리는 views.py, 화면은 Template — 정해진 역할을 지켜야 이해와 유지보수가 쉽다.
