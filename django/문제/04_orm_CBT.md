# Django 4단원 CBT — ORM (30문항)

> 출제 범위: [`../04_orm.md`](../04_orm.md) · 1~20번 기본, 21~30번 헷갈리기 쉬운 함정 문제
>
> 정답 위치는 문제를 쓰기 전에 시드 고정 난수로 먼저 정했다 — 기본(`20261108`) ①~④ 각 5개, 함정(`20261109`) 단원별 3·3·2·2개(10단원 합계 각 25개), 같은 번호 3연속 없음.

---

## 기본 문제 (1~20)

### 1. ORM에 대한 설명으로 **옳은** 것은?

- ① ORM을 쓰면 SQL이 전혀 실행되지 않는다.
- ② 객체와 DB 데이터를 매핑해 Python 코드로 DB를 조작하게 해준다.
- ③ HTML과 Python 코드를 분리하기 위한 템플릿 시스템이다.
- ④ Django에서만 존재하는 데이터베이스 엔진이다.

---

### 2. `Article.objects.all()`에서 `objects`의 정체는?

- ① 테이블을 정의한 모델 클래스
- ② QuerySet API 메서드
- ③ DB 질의의 진입점인 Manager
- ④ 조회 결과로 받은 모델 인스턴스

---

### 3. QuerySet에 대한 설명으로 **옳지 않은** 것은?

- ① DB에서 가져온 객체 목록이며 for문으로 순회할 수 있다.
- ② 0개 이상의 데이터를 담을 수 있다.
- ③ all()과 filter()는 둘 다 QuerySet 객체를 반환한다.
- ④ get()도 조건에 맞는 객체를 QuerySet으로 감싸 반환한다.

---

### 4. 기존 데이터가 없는 상태에서 다음 코드를 실행한 직후 `Article.objects.all()`의 결과는?

```python
article = Article()
article.title = 'first'
article.content = 'django!'
```

- ① `<QuerySet []>`
- ② `<QuerySet [<Article: Article object (1)>]>`
- ③ `<QuerySet [<Article: Article object (None)>]>`
- ④ DoesNotExist 예외

---

### 5. 다음 중 호출 즉시 DB에 저장되는 코드는?

- ① `Article.objects.create(title='a', content='b')`
- ② `Article(title='a', content='b')`
- ③ `article = Article(); article.title = 'a'`
- ④ `Article.objects.filter(title='a')`

---

### 6. save() 메서드에 대한 설명으로 **옳지 않은** 것은?

- ① 객체를 DB에 저장하는 인스턴스 메서드다.
- ② pk가 없는 객체면 새로 생성(INSERT)한다.
- ③ pk가 있는 객체면 기존 행을 수정(UPDATE)한다.
- ④ 저장하기 전에 입력값의 유효성을 자동으로 검사한다.

---

### 7. 아직 저장하지 않은 새 Article 인스턴스의 `article.pk` 값은?

- ① `None`
- ② `0`
- ③ `1`
- ④ AttributeError 발생

---

### 8. pk=100인 글이 없을 때 `Article.objects.get(pk=100)`의 결과는?

- ① None 반환
- ② 빈 QuerySet 반환
- ③ MultipleObjectsReturned 예외
- ④ DoesNotExist 예외

---

### 9. `content='django!'`인 글이 3개일 때 `Article.objects.get(content='django!')`의 결과는?

- ① 가장 먼저 저장된(pk가 가장 작은) 객체 하나를 반환
- ② `MultipleObjectsReturned` 예외 발생
- ③ 3개가 담긴 QuerySet을 반환
- ④ `DoesNotExist` 예외 발생

---

### 10. 조건에 맞는 데이터가 하나도 없을 때 `Article.objects.filter(title='abc')`의 결과는?

- ① DoesNotExist 예외
- ② `<QuerySet []>`
- ③ `None`
- ④ `False`

---

### 11. get()을 사용하기에 가장 적합한 상황은?

- ① 제목에 특정 단어가 포함된 글을 모두 찾을 때
- ② 전체 게시글 목록을 한 번에 가져와 보여줄 때
- ③ 같은 내용(content)을 가진 여러 글을 모두 찾을 때
- ④ pk처럼 고유한 값으로 객체 하나를 찾을 때

---

### 12. 1번 글의 제목을 'byebye'로 바꿔 **DB에 반영**하려 한다. 빈칸에 들어갈 코드는?

```python
article = Article.objects.get(pk=1)
article.title = 'byebye'
_______
```

- ① `article.update()`
- ② `article.commit()`
- ③ `article.save()`
- ④ `Article.objects.save(article)`

---

### 13. Article 1개를 삭제할 때 `article.delete()`의 반환값 형태는?

- ① `{'articles.Article': 1}`
- ② `(1, {'articles.Article': 1})`
- ③ `(1, True)`
- ④ `<QuerySet [<Article: Article object (1)>]>`

---

### 14. 1~3번 글이 있는 상태에서 1번 글을 삭제하고 새 글을 생성했다. 강의 환경(SQLite) 기준 새 글의 pk는?

- ① 1
- ② 3
- ③ 0
- ④ 4

---

### 15. 제목에 'django'가 포함된 글을 **대소문자 구분 없이** 찾는 코드는?

- ① `Article.objects.filter(title__contains='django')`
- ② `Article.objects.filter(title__icontains='django')`
- ③ `Article.objects.filter(title='django')`
- ④ `Article.objects.filter(title_icontains='django')`

---

### 16. Field Lookup 문법에 대한 설명으로 **옳은** 것은?

- ① `필드명__lookup=값` 형태로 언더스코어 2개를 쓴다.
- ② `필드명.lookup=값` 형태로 점을 쓴다.
- ③ filter()에서는 쓸 수 없고 get()에서만 쓴다.
- ④ `title='Django'`와 `title__exact='Django'`는 다른 결과를 낸다.

---

### 17. `Article.objects.filter(pk__gte=10)`의 의미는?

- ① pk가 10 미만인 글
- ② pk가 10 초과인 글
- ③ pk가 10 이상인 글
- ④ pk가 10인 글 하나

---

### 18. `Article.objects.exclude(title='abc')`의 결과는?

- ① 제목이 abc인 글만
- ② 제목에 abc가 포함된 글만
- ③ 제목이 abc인 글을 제외한 나머지
- ④ 제목이 abc인 글을 DB에서 삭제

---

### 19. Django shell에 대한 설명으로 **옳은** 것은?

- ① 실행한 QuerySet API가 실제 DB에 그대로 반영된다.
- ② shell에서 만든 데이터는 shell을 종료하면 자동으로 사라진다.
- ③ `shell -v 2`는 ORM이 실행하는 SQL을 출력하는 옵션이다.
- ④ IPython을 먼저 설치해야만 shell을 실행할 수 있다.

---

### 20. 전체 게시글을 템플릿에 출력하려 할 때 빈칸에 들어갈 코드는?

```python
def index(request):
    articles = _______
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)
```

- ① `Article.objects.get()`
- ② `Article.all()`
- ③ `Article.objects.all()`
- ④ `Article.objects.filter(pk=1)`

---

## 함정 문제 (21~30)

### 21. `article = Article.objects.get(pk=1)` 다음에 `article.objects.all()`을 실행하면?

- ① 1번 글만 담긴 QuerySet이 반환된다.
- ② AttributeError가 발생한다.
- ③ 전체 글이 담긴 QuerySet이 반환된다.
- ④ 1번 글의 필드 이름 목록이 반환된다.

---

### 22. `result = article.save()`를 실행했을 때 result의 값은?

- ① `None`
- ② 저장된 article 객체
- ③ `True`
- ④ 저장된 행의 pk

---

### 23. Article 모델에 author 필드가 있다. author가 'anonymous'인 **모든** 글의 제목을 한 번에 '익명'으로 바꾸는 코드는?

- ① `Article.objects.get(author='anonymous').title = '익명'`
- ② `Article.objects.filter(author='anonymous').update(title='익명')`
- ③ `Article.objects.filter(author='anonymous').save(title='익명')`
- ④ `Article.objects.update(author='anonymous', title='익명')`

---

### 24. `Article.objects.filter(title__startswith='Dj')`의 결과에 포함되는 제목은?

- ① 'Django 입문'
- ② 'Hello Django'
- ③ '장고 Django'
- ④ 'Learn Dj'

---

### 25. `article = Article.objects.filter(pk=1)` 다음에 `article.title`에 접근하면?

- ① 1번 글의 제목 문자열이 그대로 나온다.
- ② QuerySet이라 None이 반환된다.
- ③ 빈 문자열('')이 나온다.
- ④ AttributeError가 발생한다.

---

### 26. `Article.objects.all().delete()`를 실행한 뒤의 상태로 옳은 것은?

- ① articles_article 테이블 자체가 DB에서 삭제된다.
- ② migration 파일까지 함께 삭제된다.
- ③ 모든 레코드가 삭제되고 테이블은 남는다.
- ④ 삭제된 행은 휴지통에 보관되어 복구할 수 있다.

---

### 27. `article = Article.objects.create(title='a', content='b')` 직후 `article.pk`의 값은?

- ① `None` — save()를 호출해야 생긴다.
- ② `0`
- ③ `'a'`
- ④ DB가 배정한 정수 pk

---

### 28. ORM의 쿼리 처리 순서로 **옳은** 것은?

- ① Python 코드 → DB 실행 → SQL 변환 → Python 객체로 변환
- ② SQL 작성 → Python 코드 변환 → DB 실행 → QuerySet 반환
- ③ Python 코드 → SQL 변환 → DB 실행 → Python 객체로 변환
- ④ DB 실행 → SQL 변환 → Python 코드 → QuerySet 반환

---

### 29. `Article.objects.filter(title='Welcome')`과 **같은 결과**를 내는 코드는?

- ① `Article.objects.get(title='Welcome')`
- ② `Article.objects.filter(title__contains='Welcome')`
- ③ `Article.objects.filter(title__exact='Welcome')`
- ④ `Article.objects.exclude(title='Welcome')`

---

### 30. 기본 설정에서 `article.id`와 `article.pk`에 대한 설명으로 **옳은** 것은?

- ① id는 DB 값, pk는 저장 전 임시 값이다.
- ② 둘은 같은 기본키 값을 가리킨다.
- ③ pk는 save() 후에만, id는 생성 즉시 값이 있다.
- ④ id는 문자열, pk는 정수로 반환된다.

---

## 정답 및 해설

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ② | ③ | ④ | ① | ① | ④ | ① | ④ | ② | ② |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ③ | ② | ④ | ② | ① | ③ | ③ | ① | ③ |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| ② | ① | ② | ① | ④ | ③ | ④ | ③ | ③ | ② |

- **1. ②** ORM은 Python과 DB(SQL) 사이의 번역자다. SQL은 ORM이 내부적으로 만들어 실행한다.
- **2. ③** Article=모델 클래스, objects=매니저(쿼리의 진입점, 모든 모델에 자동 추가), all()=QuerySet API 메서드.
- **3. ④** get()은 QuerySet이 아니라 모델 인스턴스 하나를 반환한다.
- **4. ①** save()를 호출하지 않았으므로 DB에는 아직 아무것도 없다.
- **5. ①** create()는 생성과 저장을 한 번에 하는 단축 메서드. ②③은 save() 전이라 미저장, ④는 조회.
- **6. ④** save()는 값을 검사하지 않고 그대로 저장한다. 입력값 검증은 Form의 몫(6단원).
- **7. ①** pk는 save() 이후에 배정된다. 그래서 출력도 `Article object (None)`.
- **8. ④** get()은 결과가 0개면 DoesNotExist, 2개 이상이면 MultipleObjectsReturned.
- **9. ②** get()은 딱 하나일 때만 성공한다. 여러 개를 원하면 filter().
- **10. ②** filter()는 결과가 없어도 예외 없이 빈 QuerySet을 반환한다.
- **11. ④** get()은 0개·2개 이상이면 예외가 나므로 pk 같은 고유한 값으로 조회할 때 쓴다.
- **12. ③** 조회 → 값 변경 → save(). 대입만 하면 메모리 속 객체만 바뀌고 DB는 그대로다. save()는 pk가 있으면 UPDATE.
- **13. ②** (삭제된 총 개수, 모델별 삭제 개수 딕셔너리) 튜플을 반환한다.
- **14. ④** 한 번 쓴 pk는 재사용하지 않는다(Django가 SQLite 테이블에 AUTOINCREMENT를 붙이기 때문).
- **15. ②** i = case-insensitive. ④는 언더스코어가 1개라 잘못된 문법.
- **16. ①** filter·exclude·get 모두에서 쓸 수 있고, exact는 생략 가능한 기본 lookup이라 ④의 두 코드는 같다.
- **17. ③** gt(>), gte(>=), lt(<), lte(<=). e = equal.
- **18. ③** exclude는 조건에 맞는 행을 빼고 조회한다. 삭제가 아니다.
- **19. ①** shell은 Django 환경에서 실행되므로 실제 DB에 그대로 반영된다. `-v 2`는 자동 import 목록 출력, IPython은 편의 도구일 뿐 필수가 아니다.
- **20. ③** 모델클래스.매니저.메서드 구조. 템플릿에서는 for 태그로 하나씩 꺼내 쓴다.
- **21. ②** objects(Manager)는 모델 **클래스**로만 접근한다. 인스턴스에서 부르면 "Manager isn't accessible via Article instances".
- **22. ①** save()는 아무것도 반환하지 않는다. 생성된 객체를 반환하는 건 `objects.create()`.
- **23. ②** 여러 레코드 일괄 수정은 QuerySet의 update(). ④는 조건 없이 모든 글의 author와 title을 바꿔 버린다. 강의 확인문제 10번.
- **24. ①** startswith는 앞부분 일치. 'Dj'가 어딘가에 들어 있기만 하면 되는 건 contains.
- **25. ④** filter()는 결과가 1개여도 QuerySet이다. 객체 하나가 필요하면 get() 또는 `[0]`.
- **26. ③** delete()는 데이터(행)를 지운다. 테이블 구조와 migration은 그대로다. 강의 확인문제 11번.
- **27. ④** create()는 생성과 저장을 한 번에 하고 저장된 객체를 반환하므로 pk가 이미 있다.
- **28. ③** QuerySet API(Python) → ORM이 SQL로 변환 → DB 실행 → 결과를 QuerySet·인스턴스로 변환해 돌려준다.
- **29. ③** lookup을 생략하면 exact. ①은 반환 타입이 다르고(인스턴스), ②는 'Welcome!' 같은 제목도 포함한다.
- **30. ②** 자동 생성 기본키 필드 이름이 id이고, pk는 "기본키"를 가리키는 별칭이다. 저장 전엔 둘 다 None.
