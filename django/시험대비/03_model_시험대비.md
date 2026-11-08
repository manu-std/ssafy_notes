# Django 3단원 시험대비 — Model

> 📎 개념 정리 노트: [`../03_model.md`](../03_model.md)
>
> ⚠️ 슬라이드를 바탕으로 재구성한 시험 대비 자료를 PDF에서 다시 추출한 것이라, 코드·표 일부가 원본과 다를 수 있다. '추가 예상문제'는 실제 출제를 보장하지 않는다.

근거: 업로드한 Django_Model.zip의 슬라이드 77장. 강의 내용과 별도 심화 설명을 구분한다. ★★★는 강의 강조·실습·확인문제 등을 근거로 추정한 우선순위이며 실제 출제를 보장하지 않는다.

## 0. 학습 목표와 20분 압축 공부 순서

- 5분: Model → Field types / options → Migration의 3단계 전체 흐름
- 5분: null과 blank, auto_now와 auto_now_add, makemigrations와 migrate 구별
- 4분: Admin 사이트 등록과 superuser 생성, SQLite, migrations 초기화
- 3분: 강의 원본 확인 문제 12개
- 3분: 틀린 개념만 다시 말로 설명하기

시험에 서술형이 있으면 정의 → 역할/차이 → 명령어 또는 예시 → 결과 순서로 답안을 구성한다.

## 1. 핵심 개념 완전 정리

### 1-1. Django Model이란? ★★★ (슬라이드 7~17)

- Model은 데이터베이스와 연결되는 파이썬 클래스로 데이터를 저장할 테이블의 구조를 정의한다.
- Django는 Model을 통해 데이터베이스에 대한 추상화를 제공한다. Django의 **ORM(Object-Relational Mapping)은** 파이썬 객체와 관계형 DB를 연결하여 SQL을 직접 작성하지 않고도 데이터에 접근하도록 지원한다. ORM이라는 용어는 이해를돕기 위한 연관 개념이다.
- models.py에 정의한 모델은 데이터 저장 구조를 나타내며, 정의만으로 실제 테이블이 즉시 생성되지는 않는다. 별도의 migrations 절차가 필요하다.
- 연결: urls.py 요청 경로 → views.py 요청 처리 및 Model 사용 → models.py DB 데이터 접근 → View에서 render()로 Template 반환.

```
# articles/models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
```

- Article → 테이블에 대응하는 모델 클래스.
- models.Model → Django 모델 기능을 제공하는 부모 클래스, 반드시 상속.
- title, content → DB 테이블의 컬럼에 대응하는 필드.
- Django는 별도 지정하지 않으면 기본적으로 기본키 id 필드를 자동 추가한다(프로젝트 기본키 설정에 따라 형식은 달라질 수있음).
- 개념 구별: 클래스는 테이블 구조, **인스턴스는 한 행(레코드)으로** 이해하면 편하다. 실제 DB 테이블 이름은 일반적으로 앱 이름_모델이름소문자 형식(예: articles_article).

빈출 함정

1. class Article(models.Model)을 class Article()로 쓰면 Django Model이 아니다.
2. models.Model과 models.CharField는 목적이 다르다: 전자는 모델의 부모 클래스, 후자는 개별 컬럼의 필드 타입.
3. View가 DB를 직접 구성하는 것이 아니라 Model이 구조와 데이터 접근을 담당한다.

### 1-2. Model Field = 타입 + 옵션 ★★★ (슬라이드 18~30)

**필드 타입(Field type)은** 어떤 종류의 데이터를 저장할지를 정의하고, **필드 옵션(Field option)은** 값의 제약이나 기본 동작을 지정한다.

| 필드 | 역할 | 시험 포인트 |
| --- | --- | --- |
| CharField(max_length=10) | 제한된 길이의 문자열 | max_length 필수, 짧은 텍스트 |
| TextField() | 긴 텍스트 | 일반적으로 max_length 없이 사용 |
| IntegerField() | 정수 | 숫자 |
| FloatField() | 실수 | 소수점 포함 숫자 |
| DateField() | 날짜 | 날짜만 저장 |
| TimeField() | 시간 | 시간만 저장 |
| DateTimeField() | 날짜+시간 | 생성/수정 시각 기록 |
| FileField() | 파일 | 파일 참조 및 업로드 |
| ImageField() | 이미지 | 이미지 파일 업로드 |

CharField vs TextField: 이름·제목처럼 길이가 예상되는 짧은 문자열은 CharField, 게시글 본문처럼 긴 문자열은 TextField가일반적이다. SQLite는 문자열 길이 제한을 DB 수준에서 엄격히 강제하지 않을 수 있으나, Django의 검증 로직은 구분해서 이해해야 한다.

| 옵션 | 의미 | 적용 관점 |
| --- | --- | --- |
| max_length=10 | 길이 제한 | 문자열 최대 길이, 필드 정의·검증 |
| null=True | DB 컬럼에 SQL NULL 저장 허용 | DB 레벨 |
| blank=True | 유효성 검사나 Form에서 빈 값 허용 | 검증/Form 레벨 |
| default='제목' | 값 미지정 시 기본값 제공 | 기본값 설정 |

**매우 중요: null과 blank는 서로 대체할 수 없다.**

```
title = models.CharField(max_length=10, null=False, blank=False)
content = models.TextField(blank=True)
```

- null=False 기본: DB에서 NULL 저장 불허.
- blank=False 기본: Form 등에서 필수 입력.
- null=True, blank=False라면 DB는 NULL을 허용해도 Form 검증에서는 비워둘 수 없다.
- blank=True, null=False라면 일반 문자열 필드는 빈 문자열 ''로 저장할 수 있지만 SQL NULL과는 다르다.
- 두 옵션은 각각의 기본값이 False이다.
- 강의의 default는 새 인스턴스 필드의 기본값에 대한 설명. 기존 행이 있는 테이블에 필수 필드를 새로 추가할 때 Migration의 기본값을 묻는 상황과 연결된다.

### 1-3. Migrations: 변경 설계도와 실제 반영 ★★★ (슬라이드 31~37, 46)

- Migration은 Django Model 정의의 변경 사항을 데이터베이스 스키마에 반영하고 변경 이력을 관리하는 방법이다.
- python manage.py makemigrations: Model 변경을 감지하여 migrations/0001_initial.py 등의 마이그레이션 파일을 생성.
- python manage.py migrate: 생성된 Migration 중 아직 적용되지 않은 것을 실제 DB에 적용.

```
python manage.py makemigrations
python manage.py migrate
```

정확한 순서: 모델 클래스 작성/수정 → makemigrations → migrate → 실제 DB 테이블/컬럼 반영.

시험 문장 확인

- “makemigrations 실행 시 DB에 테이블이 즉시 만들어진다” → ❌
- “migrate는 Migration 파일을 기준으로 DB 변경을 적용한다” → ✅
- “한번 모델을 만든 후 수정해도 migration 작업이 필요 없다” → ❌
- “변경사항이 없을 때마다 반드시 새 Migration이 생성된다” → ❌

### 1-4. 추가 Migrations와 기존 데이터 ★★★ (슬라이드 38~46)

```
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

| 항목 | 기록 시점 | 기억법 |
| --- | --- | --- |
| auto_now_add=True | 처음 생성 시각 | add = 최초 추가 |
| auto_now=True | 객체 저장 시 갱신되는 시각 | now = 저장 시 현재 시각 |

기술적 주의: auto_now=True는 일반적인 Model.save() 수행 시 자동 갱신되지만, QuerySet.update() 같은 일부 DB 갱신 경로에서는 자동 갱신되지 않는다. 시험 기본 범위에서는 “수정 시각 기록”으로 기억.

기존 레코드가 있는 DB에 NOT NULL 새 필드를 넣을 때 과거 행의 해당 컬럼 값이 없기 때문에 Django가 값 충전 방법을 묻는다.

- 강의 예시에서는 makemigrations 과정에서 일회성 기본값 제공 혹은 중단 후 모델에서 기본값 설정을 선택한다.
- 기존 데이터가 비어 있거나 필드가 null=True인 등 조건이 다르면 기본값 질문이 생략될 수 있다.
- 일회성 기본값은 과거 레코드의 컬럼을 채우기 위한 것이며, 모델 필드의 영구적 default=와 구분한다.
- migrations/0002_...py가 생성되면 migrate로 실제 DB에 적용한다.

### 1-5. Django Admin 사이트 ★★★ (슬라이드 47~59)

Admin은 Django가 제공하는 자동 생성 관리자 인터페이스로, 등록된 모델의 데이터를 생성(Create)·조회(Read)·수정(Update)· 삭제(Delete)할 수 있다.

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Admin 기본 접속: 로컬 개발 서버에서 http://127.0.0.1:8000/admin/.
- 먼저 기본 인증 관련 테이블이 구축되도록 migrate를 해야 한다.
- createsuperuser는 관리자 계정 생성 명령이다. username / email(설정에 따라 선택) / password 등을 입력한다.
- 관리자 계정 생성과 특정 모델의 Admin 등록은 서로 다른 작업이다.

```
# articles/admin.py
from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

- 모델의 Admin 화면 표시/관리에는 admin.site.register(Article) 등록이 필요하다.
- 관리자의 CRUD 조작은 DB 데이터에 반영된다.
- 모든 모델이 자동으로 Admin에 나열되는 것은 아니다.

### 1-6. 초기화, 보조 명령어, SQLite ★★ (슬라이드 60~68)

기본 명령어

```
python manage.py showmigrations
python manage.py sqlmigrate articles 0001
```

- showmigrations: Migration 파일과 적용 여부 확인 (보통 [X]는 적용됨).
- sqlmigrate articles 0001: 지정 Migration이 수행하는 SQL 내용을 출력. 실제 실행을 위한 명령이 아니다.
- migrate를 처음 실행하면 여러 Migration이 적용되는 이유: 기본 설치 앱(admin, auth, contenttypes, sessions 등)에도 초기 migration 파일이 있기 때문.

SQLite

- Django 기본 설정에서 사용하는 가벼운 관계형 데이터베이스 엔진.
- 파일 하나(db.sqlite3)에 저장 가능한 형태로 개발·학습에 편리하다.
- SQLite를 DBMS로, db.sqlite3을 그 DB의 파일로 구분.
- SQLite라고 해서 모든 환경에서 스키마 제약이 동일하게 동작하는 것은 아니다.

DB 초기화(강의의 로컬 실습 상황)

- 강의는 자신이 작성한 앱의 migration 파일(일반적으로 __init__.py 제외)과 db.sqlite3 삭제 후 다시 makemigrations, migrate하는 흐름을 소개한다.
- 주의: 이는 개발/학습 DB 초기화에 한정하며, 실제 서비스 데이터가 있으면 삭제로 데이터가 유실된다. 팀 프로젝트·운영 환경에서 그대로 실행하면 안 된다.
- Git의 .gitignore에 로컬 학습 DB 파일을 제외하는 예시가 소개된다. 팀 프로젝트의 DB 관리 정책은 별도로 고려.

## 2. 1·2·3단원 누적 연결

| 상황 | 1단원 연결 | 2단원 연결 | 3단원 핵심 |
| --- | --- | --- | --- |
| 사용자가 게시글 목록 주소 접근 | MTV: View가 요청 처리 | urls.py가 View 연결 | View가 Model을 통해 DB 데이터를 조회할 수 있음 |
| 게시글 페이지 표시 | render() 호출 | Template / DTL | Model에서 읽은 값을 context로 전달 가능 |
| 새 게시글 입력 | Django 요청·응답 흐름 | HTML Form GET/POST의 구분 | Model로 레코드 저장하는 개념 (실제 CRUD API는 후속 단원) |
| DB 구조 바꾸기 | 프로젝트 앱 구성 | URL/템플릿 수정과 별개 | models.py → makemigrations → migrate |

주의: 2단원의 GET 폼은 서버로 값을 전달하는 원리를 다룬다. 실제 데이터 변경을 위한 POST, CSRF, ORM CRUD 구현은 이 강의(3단원)의 중심이 아니므로 시험 범위를 과장하지 않는다.

## 3. 강의 원본 확인문제 12개 (슬라이드 70~73)

다음은 강의 문제의 취지를 짧게 재진술한 것이며, 정답은 강의 73번 슬라이드와 대조했다.

| 번호 | 문제 핵심 | 정답 | 근거 |
| --- | --- | --- | --- |
| 1 | Django 모델 클래스가 상속할 부모 | models.Model | Model 기본 기능 제공 |
| 2 | 이름과 같은 짧은 문자열의 필드 | CharField | 제한된 길이 텍스트 |
| 3 | 빈 값이 필수 입력인 Form 관련 기본 설정 | blank=False | 기본적으로 필수 입력 |
| 4 | 모델 필드의 기본값 지정 | default | 기본값 설정 |
| 5 | 날짜와 시간을 함께 저장하는 필드 | DateTimeField | 날짜+시간 |
| 6 | 변경 이력을 파일로 생성하는 명령 | python manage.py makemigrations | 설계도 생성 |
| 7 | 생성된 Migration을 DB에 실제 적용 | migrate | 실제 반영 |
| 8 | CharField 문자열 길이 제한 옵션 | max_length | 최대 길이 |
| 9 | 기본 DB 엔진 | SQLite | 기본 설정 |
| 10 | Model 필드와 DB의 대응 관계 | 데이터베이스 컬럼 | 필드 → 컬럼 |
| 11 | 모델을 Admin 사이트에 등록 | admin.site.register() | Admin 등록 |
| 12 | 생성 시각을 자동 기록 | auto_now_add=True | 최초 생성 시각 |

원본 정답 기호(강의 73쪽): 1 c / 2 b / 3 d / 4 a / 5 c / 6 b / 7 c / 8 b / 9 d / 10 c / 11 c / 12 d.

## 4. 추가 예상 객관식 15문제 (정답은 뒤에)

Q1. Django Model에 대한 설명으로 틀린 것은? ① Python 클래스로 정의한다. ② models.Model을 상속한다. ③ 정의하는 즉시 DB 테이블이 생성된다. ④ 필드는 DB 컬럼 구조에 대응한다.

Q2. 다음 코드에서 max_length=20의 역할은? title = models.CharField(max_length=20) ① 객체 20개 생성 ② 문자열 길이 제한 ③ 20초 간 저장 ④ 자동 생성되는 ID 최대치

Q3. 다음 중 게시글 본문처럼 긴 문자열 저장에 일반적으로 적합한 것은? ① DateField ② IntegerField ③ TextField ④ TimeField

Q4. blank=True의 직접적인 의미는? ① SQL NULL 저장 필수 ② Form 유효성 검증 시 빈 값 허용 ③ 기본값을 True로 설정 ④ 데이터베이스를 초기화

Q5. null=True의 주요 적용 영역은? ① URL 라우팅 ② 데이터베이스 컬럼의 NULL 허용 ③ 화면 레이아웃 ④ 가상환경 설정

Q6. Model 클래스에서 필드를 새로 추가한 직후 일반적으로 필요한 명령어 순서는? ① migrate → makemigrations ② makemigrations → migrate ③ createsuperuser → render ④ sqlmigrate → startapp

Q7. makemigrations만 실행한 상태에서 가장 옳은 설명은? ① 변경사항을 DB에 반드시 적용했다. ② 관리자 계정을 생성했다. ③ Migration 파일을 만들었으나 실제 DB 반영은 별개다. ④ 모든 테이블이 삭제된다.

Q8. 신규 객체가 처음 만들어진 시각을 자동 기록하는 옵션은? ① auto_now ② max_length ③ blank ④ auto_now_add

Q9. 객체의 저장 시 변경 시각을 자동 기록하는 옵션은? ① auto_now ② default ③ null ④ auto_now_add

Q10. 기존 데이터가 있는 테이블에 NULL을 허용하지 않는 필드를 추가할 때 기본값을 묻는 이유는? ① URL 미등록 ② 기존 행에새 컬럼 값이 필요할 수 있기 때문 ③ 브라우저 캐시 때문 ④ 가상환경 미설치

Q11. Admin에서 모델 데이터를 관리하도록 모델을 등록할 코드는? ① admin.site.register(Article) ② render(Article) ③ models.Model(Article) ④ include(Article)

Q12. 관리자 계정 생성 명령은? ① python manage.py startadmin ② python manage.py runserver ③ python manage.py createsuperuser ④ python manage.py makemigrations

Q13. showmigrations의 목적은? ① 템플릿 미리보기 ② Migration 적용 여부 표시 ③ 서버 종료 ④ 이미지 업로드

Q14. sqlmigrate articles 0001에 가장 가까운 설명은? ① 지정 Migration이 수행할 SQL을 보여준다. ② 관리자 계정을 삭제한다. ③ DB 데이터를 모두 초기화한다. ④ HTML 파일을 자동 생성한다.

Q15. 다음 중 Django 기본 설치 환경의 데이터베이스 관련 설명으로 맞는 것은? ① DB는 HTML 파일이다. ② SQLite는 오직 클라우드 DB이다. ③ db.sqlite3는 SQLite 데이터베이스 파일로 쓰일 수 있다. ④ 개발 DB는 삭제해도 언제나 안전하다.

### 객관식 정답 및 해설

1. ③: 모델 정의와 DB 반영은 별개. makemigrations와 migrate 필요.
2. ②: 문자열 최대 길이 설정. 생성 건수 제한이 아니다.
3. ③: TextField는 일반적으로 장문에 사용한다.
4. ②: blank는 검증/Form 관련, null은 DB 관련.
5. ②: DB 컬럼이 SQL NULL을 허용하도록 설정.
6. ②: 마이그레이션 생성 → 실제 적용 순서.
7. ③: makemigrations는 스키마 변경 내역 파일 생성.
8. ④: auto_now_add는 최초 생성 시각.
9. ①: auto_now는 일반적인 모델 저장 시 갱신 시각.
10. ②: 과거 행에 새 필드 값이 없을 수 있어 보완 필요.
11. ①: admin.py에서 모델 등록.
12. ③: createsuperuser로 관리자 계정 생성.
13. ②: 어떤 Migration이 적용됐는지 표시.
14. ①: SQL 출력 기능이며 그 자체가 적용을 의미하지 않는다.
15. ③: Django 기본 개발 DB로 자주 쓰는 SQLite 파일.

## 5. 추가 예상 주관식 10문제 (단답·코드 빈칸)

S1. Django 모델을 정의할 때 상속하는 클래스를 정확히 적으시오.

S2. title = models.____(max_length=30)에서 제목용 짧은 문자열 필드 타입을 적으시오.

S3. 데이터베이스 컬럼에서 NULL 저장 허용 여부를 설정하는 옵션을 적으시오.

S4. Model 변경 사항을 기반으로 Migration 파일을 생성하는 전체 명령어를 적으시오.

S5. 생성된 Migration 파일을 데이터베이스에 반영하는 전체 명령어를 적으시오.

S6. created_at = models.DateTimeField(____=True)에서 최초 생성 시각 자동 기록 옵션을 적으시오.

S7. updated_at = models.DateTimeField(____=True)에서 일반적인 저장 시각 갱신 옵션을 적으시오.

S8. 관리자 계정 생성에 필요한 python manage.py ... 명령어를 적으시오.

S9. admin.site.____(Article)의 빈칸을 채우시오.

S10. 적용된 Migration 목록을 확인하는 python manage.py ... 명령어를 적으시오.

### 주관식 정답과 채점 포인트

- S1: models.Model — 대소문자, 점 표기에 유의.
- S2: CharField — TextField와 구별.
- S3: null — blank는 별개.
- S4: python manage.py makemigrations — migrate와 혼동 금지.
- S5: python manage.py migrate — 실제 적용.
- S6: auto_now_add — 최초 생성.
- S7: auto_now — 일반 모델 저장 시 갱신.
- S8: python manage.py createsuperuser.
- S9: register — admin.site.register.
- S10: python manage.py showmigrations.

## 6. 추가 예상 서술형 5문제 + 만점 모범답안

### E1. Django Model의 개념과 역할을 설명하고 실제 DB 테이블 반영 과정을 서술하시오.

모범답안: Django Model은 데이터베이스 테이블의 구조를 파이썬 클래스로 정의하는 기능이다. 개발자는 models.Model을 상속받은 클래스를 만들고 필드를 지정하여 데이터의 종류와 조건을 정의한다. 이후 python manage.py makemigrations로 변경 내용을 담은 Migration 파일을 생성하고, python manage.py migrate로 이를 데이터베이스에 적용하여 테이블이나 컬럼 구조를 반영한다.

필수 키워드: 파이썬 클래스 / models.Model / 테이블 구조 / makemigrations / migrate.

### E2. CharField와 TextField를 비교하고 max_length의 역할을 설명하시오.

모범답안: CharField는 이름이나 제목처럼 길이가 비교적 짧고 제한이 필요한 문자열에 사용하며 max_length 옵션으로 최대 길이를설정한다. TextField는 게시글 본문처럼 길이가 긴 텍스트를 저장할 때 사용한다. 두 필드는 저장하려는 문자열의 특성에 따라 선택한다.

필수 키워드: 짧은 문자열 / 긴 문자열 / max_length / 예시.

### E3. null과 blank의 차이를 설명하고 null=True, blank=False의 의미를 서술하시오.

모범답안: null은 데이터베이스에서 SQL NULL 저장을 허용하는지 정하는 옵션이고, blank는 Form 등의 데이터 유효성 검사에서빈 값을 허용하는지 정하는 옵션이다. 따라서 null=True, blank=False이면 데이터베이스는 NULL을 저장할 수 있지만, Form에서는 기본적으로 해당 필드를 필수 입력으로 검사한다.

필수 키워드: DB / SQL NULL / Form 검증 / 필수 입력.

### E4. 기존 데이터가 있는 Article 모델에 생성일 필드를 추가할 때 발생 가능한 문제와 해결 절차를 설명하시오.

모범답안: 기존 행에는 새로 추가하는 생성일 컬럼 값이 없기 때문에, NULL을 허용하지 않는 필드를 추가하면 Django가 기존 레코드에 채울 기본값을 요구할 수 있다. 개발자는 일회성 기본값을 지정하거나 모델에 적절한 기본값·NULL 허용 등 정책을 설정한다. 그런 뒤 makemigrations로 변경 설계도를 생성하고 migrate로 DB에 반영한다. 생성일 자동 기록은 DateTimeField(auto_now_add=True)를 사용할 수 있다.

필수 키워드: 기존 행 / NULL 불가 / 기본값 / makemigrations / migrate.

### E5. Django Admin 사이트에서 게시글 CRUD를 하기 위한 준비 과정과 각 단계의 역할을 설명하시오.

모범답안: 먼저 Django 모델을 작성하고 makemigrations, migrate로 데이터베이스 구조를 반영한다. 관리자 인증을 위한 DB 테이블이 준비되었으면 python manage.py createsuperuser로 관리자 계정을 생성한다. 다음으로 앱의 admin.py에서 admin.site.register(Article)로 게시글 모델을 등록하고 서버를 실행한다. 관리자 계정으로 /admin/에 로그인하면 등록된 모델 데이터를 생성·조회·수정·삭제할 수 있다.

필수 키워드: DB 적용 / superuser / admin.py / admin.site.register / CRUD.

## 7. 고난도 함정 10개 — 객관식 오답 방지

1. Model = DB 자체 (X): Model은 데이터 구조를 정의하는 파이썬 클래스.
2. 모델만 작성하면 DB 테이블 생성 (X): Migration 적용 필요.
3. makemigrations가 DB를 변경 (X): 파일 생성 담당.
4. migrate가 마이그레이션 파일 생성 (X): DB 반영 담당.
5. blank=True면 반드시 SQL NULL 저장 (X): Form 검증 옵션.
6. null=True면 입력 화면에서 언제나 선택 입력 (X): blank가 별개.
7. auto_now가 최초 생성일 전용 (X): 저장 시각 갱신.
8. auto_now_add가 수정할 때마다 갱신 (X): 최초 생성 시각.
9. superuser를 만들면 모든 앱 모델이 자동 등록 (X): admin.site.register() 필요.
10. sqlmigrate만 실행하면 Migration이 적용됨 (X): SQL 출력 담당.

## 8. 시험 직전 90초 암기 카드

```
Model = DB 테이블 설계용 파이썬 클래스
상속 = models.Model
필드 = DB 컬럼 / 인스턴스 = DB 행
CharField(max_length=10) = 짧은 문자열
TextField() = 긴 문자열
DateTimeField() = 날짜 + 시간
null = DB NULL / blank = Form 빈 값 / default = 기본값
생성 시각 = auto_now_add=True
수정 시각 = auto_now=True (일반적인 모델 저장)
모델 수정 → makemigrations(파일 생성) → migrate(DB 반영)
showmigrations = 적용 여부 / sqlmigrate = SQL 확인
createsuperuser = 관리자 계정 생성
admin.site.register(Article) = 모델 관리자 화면 등록
SQLite = Django 기본 DB 엔진 / db.sqlite3 = DB 파일
```

### 시험 실전 답안 팁

- 선택지가 비슷하면 **무엇을 변경하느냐(DB 스키마/폼 검증/로그인/관리화면)를** 먼저 구분한다.
- 두 명령어를 비교하는 문제는 파일 생성과 실제 적용을 먼저 떠올린다.
- 코드 빈칸에서 auto_now/auto_now_add, blank/null은 최초·수정 / DB·Form 두 쌍으로 외운다.
- 서술형은 명령어만 쓰지 말고 역할과 실행 결과까지 한 문장씩 적는다.
- 객관식은 단정어 “항상/반드시/자동으로/즉시”를 주의하되, 단정어 자체만으로 오답 판단하지 않는다.

## 9. 자체 채점 체크리스트

- models.Model 상속 필요성을 설명할 수 있다.
- 테이블/행/컬럼과 Model/인스턴스/필드의 대응을 안다.
- CharField와 TextField의 용도 차이를 안다.
- null, blank, default를 서로 구별한다.
- makemigrations와 migrate 차이 및 순서를 안다.
- auto_now와 auto_now_add를 구별한다.
- 기존 데이터가 있는 테이블에 새 필드 추가 시 기본값 문제가 생기는 이유를 안다.
- 관리자 계정 생성과 모델 등록의 차이를 안다.
- showmigrations와 sqlmigrate의 용도를 안다.
- SQLite와 db.sqlite3의 차이를 설명할 수 있다.

출제 예상은 이 PPT의 교육 목표와 강조도 기준. 공식 확인문제 12개 외 추가 문제 30개는 자체 제작 문제이다.
