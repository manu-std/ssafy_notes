# Django 1단원 시험대비 — Intro & Design Pattern

> 📎 개념 정리 노트: [`../01_intro_design_pattern.md`](../01_intro_design_pattern.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

근거: 제공된 SSAFY Django Intro & Design Pattern 슬라이드 이미지 123장. 시험 출제 중요도는 공식 출제 범위가 아니라 강의내용·확인문제·실습 중심 추정이다.

## A. 시험 직전 반드시 알아야 하는 내용

### 1. 웹 애플리케이션 / 클라이언트 / 서버 (슬라이드 8~15)

- 웹 애플리케이션(Web Application): 인터넷을 통해 사용자에게 제공하는 소프트웨어 프로그램. 브라우저를 통해 접근하고 상호작용한다.
- Client: 서비스를 요청하는 쪽(대표적으로 브라우저). HTTP Request를 보낸다.
- Server: 요청을 받아 처리하고 HTTP Response를 반환한다.
- 웹의 기본 흐름: 주소 입력 → 브라우저가 HTTP 요청 → 서버에서 요청 처리 → 응답(HTML 등) → 브라우저 화면에 표시.
- 함정: 요청을 보내는 주체는 클라이언트, 요청을 받아 처리하는 주체는 서버다.

### 2. Frontend / Backend (슬라이드 16~19)

- Frontend: 사용자가 직접 보는 화면과 상호작용하는 부분. HTML(구조), CSS(스타일), JavaScript(동작).
- Backend: 서버 쪽 비즈니스 로직, 데이터 처리, 인증, DB 연동, API 등을 수행. Django는 Python 기반 백엔드 웹 프레임워크다.
- 둘은 대립하는 개념이 아니라 한 서비스를 구성하는 서로 다른 역할이다.

### 3. Web Framework / Django (슬라이드 20~27)

- 웹 프레임워크: 웹 서비스를 빠르고 효율적으로 개발하도록 재사용 가능한 도구, 기본 구조, 규칙을 제공한다.
- Django: Python 웹 프레임워크, 다양한 기능이 기본 제공되는 편이며 ORM, 인증 및 보안 관련 기능 등을 지원한다. Django의 핵심 설계는 **MTV(Model–Template–View)다**.
- 프레임워크를 쓰는 이유: 반복 코드를 줄이고 정해진 구성에 맞춰 협업·유지보수할 수 있다.
- 함정: Django는 컴파일러가 아니며 단순히 HTML만 보여주는 도구도 아니다.

### 4. 가상환경과 의존성 패키지 (슬라이드 28~52)

- 가상환경(virtual environment): 프로젝트별 Python 패키지 설치 환경을 격리하는 공간. 서로 다른 프로젝트가 서로 다른 패키지 버전을 사용할 수 있다.
- 의존성(dependency): 소프트웨어 동작을 위해 필요한 다른 라이브러리/패키지.
- 주요 명령어 (Windows PowerShell 환경은 활성화 경로가 별도이므로 구분):

```
python -m venv venv                   # 가상환경 생성
source venv/Scripts/activate         # Git Bash(Windows)에서 활성화
# macOS/Linux: source venv/bin/activate
# Windows PowerShell: .\venv\Scripts\Activate.ps1
pip install django                   # Django 설치
pip list                             # 설치된 패키지 목록과 버전
pip freeze > requirements.txt        # 현재 환경의 패키지 목록 기록
pip install -r requirements.txt      # 요구 패키지 설치
deactivate                           # 가상환경 비활성화
```

- &gt;는 명령어 결과를 파일로 쓰기/덮어쓰기, -r은 요구사항 파일을 읽어 설치한다는 뜻.
- 중요: pip freeze는 그때 설치된 패키지 목록을 내보내며, 프로젝트에서 직접 사용한 패키지만 자동 선별해 주는 기능은 아니다.
- 주의: venv 폴더 자체를 Git에 올리는 대신 requirements.txt 등으로 환경을 재현하는 것이 일반적이다.
- 대표적인 오류: 다른 프로젝트의 패키지를 전역 환경에 설치하거나, 가상환경을 켜지 않고 설치하여 버전 충돌이 발생함.
- 가상환경은 Python 패키지/실행환경 격리를 위한 것이지, 컴퓨터 CPU나 RAM을 물리적으로 분리하는 가상머신(VM)이 아니다.

### 5. Django 프로젝트 시작 (슬라이드 53~59)

```
pip install django
django-admin startproject firstpjt .
python manage.py runserver
```

- django-admin startproject firstpjt .: 현재 폴더에 프로젝트 설정 패키지 firstpjt와 manage.py 등을 생성한다. 끝의 .은 현재 디렉터리를 의미한다.
- python manage.py runserver: 개발용 웹 서버를 실행한다. 기본 개발 주소는 http://127.0.0.1:8000/.
- 함정: runserver는 개발용이며 별도 설정 없이 운영 서비스용으로 사용하는 것이 권장되지 않는다.

### 6. 디자인 패턴 및 MTV/MVC (슬라이드 60~64, 99~103)

- 디자인 패턴: 반복적으로 마주치는 설계 문제에 대한 재사용 가능한 일반적 해결 방법.
- MVC: Model(데이터) / View(사용자에게 보이는 UI) / Controller(입력 처리와 흐름 조정).
- Django MTV: Model(데이터/DB 관련) / Template(화면 표현) / View(요청 처리, 로직, 응답).
- 개념적 대응: MVC Model ↔ MTV Model, MVC View ↔ MTV Template, MVC Controller ↔ MTV View. Django URLconf가 URL과 View를 연결하며 요청 전달에 기여하므로 1:1 완전 대응이라고 단정하지는 않는다.
- 가장 중요한 함정: Django의 View는 화면 HTML 그 자체가 아니라 요청을 처리하는 Python 함수/클래스다. 사용자에게 표현될 화면의 틀은 Template다.

### 7. 프로젝트와 앱 (슬라이드 65~76)

- Project: Django 웹서비스 전체에 적용하는 설정과 앱들을 포함하는 상위 구성.
- App: 게시판/계정/상품 등 독립된 기능 단위. 한 프로젝트 안에 여러 앱을 둘 수 있다.
- 앱 생성: python manage.py startapp articles.
- 새 앱 등록: 프로젝트의 settings.py에 있는 INSTALLED_APPS에 'articles', 등을 추가한다.
- startapp은 앱 파일을 생성하지만 프로젝트의 INSTALLED_APPS 등록까지 자동으로 하지는 않는다.

| 파일 | 역할 | 외우는 포인트 |
| --- | --- | --- |
| manage.py | 프로젝트 관리 명령 실행 | python manage.py runserver |
| settings.py | 프로젝트 설정 | INSTALLED_APPS, DB 설정 등 |
| urls.py | URL과 View 연결 | URL 라우팅 |
| asgi.py | ASGI 서버 인터페이스 | 비동기 서버 인터페이스 |
| wsgi.py | WSGI 서버 인터페이스 | 동기 서버 인터페이스 |

| 파일 | 역할 | 외우는 포인트 |
| --- | --- | --- |
| `__init__.py` | Python 패키지 표시 | 초기화 모듈 |
| admin.py | 관리자 사이트 설정 | admin 등록 |
| apps.py | 앱 설정 | AppConfig |
| models.py | 데이터 모델 정의 | DB 및 ORM 관련 |
| views.py | 요청 처리 / 응답 생성 | Django MTV의 View |
| tests.py | 테스트 작성 | 자동 테스트 |
| migrations/ | DB 스키마 변경 이력 | 모델 변경 기록 |

### 8. 요청·응답 구조 (슬라이드 77~86)

```
브라우저 GET /articles/ 요청
        ↓
프로젝트 urls.py  (경로 매칭)
        ↓
articles/views.py의 index(request)  (요청 처리)
        ↓
render(request, 'articles/index.html')
        ↓
articles/templates/articles/index.html (화면 템플릿)
        ↓
HTTP 응답 → 브라우저에 화면 표시
```

- 템플릿을 보여 주는 예:

```
# urls.py
from django.contrib import admin
from django.urls import path
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', views.index),
]

# articles/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'articles/index.html')

<!-- articles/templates/articles/index.html -->
<h1>Hello, Django</h1>
```

- 폴더 안에 같은 이름 articles가 반복되는 이유: 앱별 템플릿 이름 충돌 방지를 위한 네임스페이스 성격의 디렉터리 구성.
- View 함수의 첫 인자 request는 클라이언트 요청을 나타내는 객체.
- 페이지가 보이려면 URL, View, Template의 연결이 모두 맞아야 한다.

### 9. render() (슬라이드 97~98)

```
render(request, template_name, context=None)
```

- request: 요청 객체.
- template_name: 사용할 템플릿 경로/이름.
- context: 템플릿에 전달할 데이터(일반적으로 딕셔너리), 생략 가능.
- 반환값: 렌더링한 내용을 담은 HttpResponse 객체.
- 오답: render()는 URL을 등록하거나 DB를 초기화하는 함수가 아니다.

### 10. Trailing Comma (슬라이드 104~107)

- 항목의 마지막에도 붙인 쉼표. 예: INSTALLED_APPS = ['django.contrib.admin', 'articles',].
- 요소를 추가/삭제할 때 수정 범위를 줄이고 diff를 읽기 쉽게 하며 구문 에러를 방지하는 데 도움이 된다.
- 단, 모든 상황에서 쉼표가 무조건 같은 의미인 것은 아니다. 파이썬에서 (1)은 정수, (1,)은 요소 하나짜리 튜플이다.

### 11. 프레임워크 사용 시 주의 (슬라이드 108~110)

- urls.py가 URL을 담당하고, views.py가 요청 처리 로직을 담당하며, 화면은 Template로 분리하는 등의 정해진 역할과 설계규칙을 지켜야 이해와 유지보수가 쉽다.
- 강의는 Django의 설계 철학과 프레임워크 내 정해진 규칙을 강조한다. '마음대로 다른 파일에 코드를 넣어도 결과만 같으면 된다'라는 문장은 위험한 오답이다.

## B. 12개 강의 원문 확인문제 정답표 (슬라이드 112~116)

| 번호 | 정답 | 핵심 해설 |
| --- | --- | --- |
| 1 | b | Client가 요청, Server가 처리·응답 |
| 2 | b | Framework는 개발 구조와 기능 제공 |
| 3 | d | Compiler는 MTV 구성 요소가 아님 |
| 4 | b | 가상환경은 프로젝트별 패키지 격리 |
| 5 | c | django-admin startproject myproject |
| 6 | c | Design Pattern은 반복 설계 문제 해결법 |
| 7 | c | App은 기능 단위 |
| 8 | c | python -m venv myenv |
| 9 | c | Django는 고정된 HTML만 사용하지 않음 |
| 10 | c | render가 템플릿 렌더링 후 응답 반환 |
| 11 | b | settings.py의 INSTALLED_APPS에 등록 |
| 12 | b | 화면 표현 담당은 Template |

## C. 추가 객관식 예상문제 15개 (강의 원문 문제와 별개)

1. 웹브라우저가 /articles/로 HTTP 요청을 보낼 때 Django에서 해당 경로를 View에 연결하는 파일은? ① settings.py ② urls.py ③ models.py ④ admin.py
2. 다음 중 Django MTV의 View에 관한 설명으로 가장 적절한 것은? ① HTML만 저장한다 ② 데이터베이스를 자동 삭제한다 ③ 요청을 처리하고 응답을 구성한다 ④ 가상환경을 생성한다
3. MVC의 Controller와 가장 유사한 역할을 담당하는 Django MTV 구성요소는? ① Template ② View ③ Model ④ Migration
4. python manage.py startapp users를 실행한 직후, 프로젝트가 해당 앱을 인식하도록 강의에서 수행한 추가 작업은? ① urls.py 삭제 ② settings.py의 INSTALLED_APPS 등록 ③ models.py를 settings.py로 이동 ④ templates 폴더 삭제
5. 설치된 패키지들의 버전 목록을 requirements.txt에 저장하는 올바른 명령은? ① pip install requirements.txt ② pip list &gt; install ③ pip freeze &gt; requirements.txt ④ python -m requirements
6. requirements.txt에 적힌 패키지를 설치하는 명령은? ① pip install -r requirements.txt ② pip freeze -r requirements.txt ③ pip list requirements.txt ④ python manage.py install
7. 앱의 데이터 모델을 정의하는 파일은? ① views.py ② apps.py ③ models.py ④ tests.py
8. django-admin startproject firstpjt . 마지막 점(.)의 의미는? ① 상위 폴더 ② 프로젝트 이름 생략 ③ 현재 폴더 ④ Python 최신 버전
9. 일반적인 요청 처리 흐름으로 가장 적절한 것은? ① Template→URL→View→Client ② URL→View→Template→응답 ③ Model→Client→URL→View ④ View→가상환경→Template
10. 다음 중 render()의 인자에 관한 설명으로 옳지 않은 것은? ① 첫 인자는 요청 객체이다 ② 두 번째 인자는 템플릿 이름이다 ③ 세 번째 context는 필수이다 ④ HttpResponse를 반환한다
11. 웹서비스 사용자에게 보여 줄 HTML 화면을 주로 담당하는 Django MTV 요소는? ① Model ② View ③ Template ④ URLconf
12. Git Bash(Windows) 강의 실습에서 venv라는 가상환경을 활성화하는 명령은? ① source venv/Scripts/activate ② python manage.py runserver ③ pip list ④ deactivate
13. 다음 중 프로젝트와 앱의 관계로 옳은 것은? ① 앱은 하나의 프로젝트만 포함할 수 없다 ② 프로젝트에 여러 앱을 포함할 수 있다 ③ 프로젝트와 앱은 동일한 개념이다 ④ 앱은 Django 외부의 운영체제이다
14. Python에서 요소가 한 개인 튜플 표현으로 올바른 것은? ① (7) ② {7} ③ (7,) ④ [7]
15. Django의 개발 서버 실행 명령어는? ① django-admin startapp ② python manage.py runserver ③ pip install django ④ python -m venv venv

정답: 1② 2③ 3② 4② 5③ 6① 7③ 8③ 9② 10③ 11③ 12① 13② 14③ 15②.

핵심 오답 해설: 3번: MVC의 Controller 역할에 가장 가까운 것이 Django의 View(정확한 1:1 대응은 아님). 4번: startapp과 앱등록은 별개. 8번: 마지막 .은 현재 디렉터리. 10번: context는 선택 인자. 14번: (7)은 정수, (7,)은 튜플.

## D. 주관식 / 빈칸 10문제

1. 클라이언트의 요청을 받아 처리하고 응답을 보내는 주체는? → 서버(Server)
2. Django 디자인 패턴의 세 구성 요소를 순서대로 쓰시오. → Model, Template, View
3. Django 앱을 프로젝트에 등록하는 설정 리스트 이름은? → INSTALLED_APPS
4. 프로젝트의 URL 경로 설정을 담당하는 파일은? → urls.py
5. Django에서 View 함수의 요청 인자로 흔히 사용하는 변수 이름은? → request
6. render(request, _______, context)에서 빈칸의 의미는? → template_name / 템플릿 경로
7. Python 가상환경 생성 명령어를 쓰시오(가상환경 이름 venv). → python -m venv venv
8. 설치된 패키지를 requirements.txt에 기록하는 전체 명령어를 쓰시오. → pip freeze &gt; requirements.txt
9. 앱 이름이 articles일 때 Django 앱 생성 명령어를 쓰시오. → python manage.py startapp articles
10. 웹 프레임워크에서 자주 반복되는 설계 문제를 해결하기 위한 재사용 가능한 해결 방식은? → 디자인 패턴

## E. 서술형 5문제 및 채점 키워드

### 1. Django MTV 패턴의 각 구성 요소와 역할을 설명하시오.

모범답안: Django는 Model, Template, View로 관심사를 분리한다. Model은 데이터 구조와 데이터베이스 관련 처리를 담당한다. Template은 사용자에게 보이는 화면 표현을 담당한다. View는 클라이언트 요청을 처리하고 필요한 데이터를 준비하여 Template을 렌더링하거나 응답을 반환한다. 필수 키워드: Model=데이터, Template=화면, View=요청 처리/로직, 역할 분리.

### 2. 가상환경을 사용하는 이유와 requirements.txt의 용도를 설명하시오.

모범답안: 프로젝트마다 필요한 패키지와 버전이 다를 수 있어 가상환경으로 의존성을 분리한다. 이를 통해 버전 충돌을 줄인다. pip freeze &gt; requirements.txt로 설치된 패키지 버전을 기록하고, 다른 환경에서 pip install -r requirements.txt로 해당 의존성을 설치해 재현할 수 있다. 필수 키워드: 프로젝트별 분리, 패키지 버전 충돌 방지, freeze, install -r.

### 3. 사용자가 /articles/ 주소에 접속하여 화면을 볼 때 Django의 처리 흐름을 설명하시오.

모범답안: 브라우저가 서버로 HTTP 요청을 보내면 Django의 URL 설정이 요청 경로와 연결된 View를 찾는다. View가 요청을 처리하고 Template을 지정하여 render()를 호출한다. Django가 Template을 렌더링한 HttpResponse를 반환하면 브라우저가 이를 표시한다. 필수 키워드: 클라이언트 요청 → URLconf → View → Template → HttpResponse → 브라우저.

### 4. 프로젝트(Project)와 앱(App)의 차이를 설명하시오.

모범답안: 프로젝트는 Django 서비스 전체의 설정과 여러 앱을 관리하는 상위 단위이고, 앱은 게시판이나 계정처럼 특정 기능을 담당하는 구성 단위다. 하나의 프로젝트에 여러 앱을 둘 수 있다. 앱 생성 후 필요한 경우 settings.py의 INSTALLED_APPS에 등록하여사용한다. 필수 키워드: 전체 설정, 기능 단위, 여러 앱 포함, INSTALLED_APPS.

### 5. render() 함수의 세 인자를 설명하고 반환값을 쓰시오.

모범답안: 첫 인자인 request는 클라이언트 요청 객체다. 두 번째 template_name은 렌더링할 템플릿의 이름 또는 경로다. 선택적인세 번째 context는 템플릿에 전달하는 데이터로 일반적으로 딕셔너리를 사용한다. render()는 템플릿이 렌더링된 내용을 담은 HttpResponse 객체를 반환한다. 필수 키워드: request, template_name, context(선택), HttpResponse.

## F. 한 번 더 출제될 만한 응용·함정 8가지

1. Django View = 실제 화면 → 틀림. 실제 화면 표현은 Template.
2. startapp만 실행하면 자동으로 앱 등록 → 틀림. INSTALLED_APPS 설정이 필요.
3. pip freeze가 새 환경에 패키지 설치 → 틀림. 설치는 pip install -r.
4. render()가 HTML 문자열을 직접 반환 → 정확하지 않음. HttpResponse 반환.
5. urls.py가 HTML 파일을 직접 렌더링한다 → 기본 구성에선 틀림. URL 연결, View가 응답 처리.
6. python -m venv venv가 가상환경을 생성 및 활성화한다 → 틀림. 생성과 활성화는 별도 단계.
7. Trailing comma는 모든 자료형에서 의미가 항상 같다 → 틀림. 한 요소 튜플에선 쉼표가 중요.
8. Django가 정적 HTML만 지원한다 → 틀림. 동적 데이터 전달 및 템플릿 사용 가능.

## G. 단원 15분 복습 루틴

- 0~3분: Client ↔ Server, Frontend ↔ Backend, Framework 역할을 구두로 설명.
- 3~6분: MTV와 MVC 매칭, Model/Template/View 각각 한 줄 설명.
- 6~9분: venv, pip freeze, pip install -r, startproject, startapp, runserver 명령어 백지에 작성.
- 9~12분: settings.py, urls.py, models.py, views.py 및 요청·응답 전체 경로 그림 그리기.
- 12~15분: 원문 확인문제 12개와 상단 함정 8가지를 빠르게 확인.

## H. 시험에서 점수 잃지 않는 팁

1. 역할을 묻는 문제: 파일명보다 기능을 먼저 떠올린다. URL=매핑, View=로직, Template=화면, Model=데이터.
2. 명령어 문제: 동사와 목적어를 묶어 기억한다. startproject=프로젝트, startapp=앱, runserver=서버 시작, freeze=목록 저장, install -r=목록대로 설치.
3. 서술형: 정의 하나만 쓰지 말고 용도·작동 과정·결과를 포함한다. 특히 흐름 문제에서는 화살표 순서가 중요.
4. 유사 개념 함정: MVC Controller ↔ Django View, MVC View ↔ Django Template.
5. 명령어 플랫폼 구분: 슬라이드의 source venv/Scripts/activate는 Windows Git Bash 기준. macOS/Linux의 source venv/ bin/activate와 혼동하지 말기.

자료 사용 안내: 이 문서는 제공된 슬라이드 내용에 근거해 재구성한 개인 학습용 가이드이며, '추가 예상문제'는 실제 시험 문제라고 보장할 수 없다. 슬라이드 자체 확인문제 12문항은 112~116번 페이지의 문제와 답안을 참조하였다.
