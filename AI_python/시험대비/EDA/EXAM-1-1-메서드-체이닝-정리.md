# 시험 대비 — 1-1 데이터 EDA 및 모델 학습 : 빈칸 메서드 완전 정리

대상: `시험/(실습-문제) 1-1_데이터 EDA 및 모델 학습.ipynb` (Wine / **분류**)
　　　`시험/(과제-문제) 1-1_데이터 EDA 및 모델 학습.ipynb` (Boston / **회귀**)

참고 노트: `ssafy_notes/AI_python/01_numpy.md` · `02_pandas.md` · `03_data_preprocessing.md`

---

# 0. 판다스 기본 조작 — 빠른 참조

> 아래 1장(타입 지도)로 들어가기 전에, **DataFrame으로 할 수 있는 조작 전체**를 흐름 순서로 훑는다.
> 모든 표는 `호출 대상 → 반환 타입` 기준으로 읽어라.

## 0-1. 분석의 기본 순서

```
불러오기 → 조회 → 선택 → 필터 → 정렬 → 집계 → 시각화
  read_csv   head    []      []     sort   groupby   seaborn
             info   loc    조건    _values
          describe  iloc
```

## 0-2. 불러오기 / 만들기

| 코드 | 반환 |
| --- | --- |
| `pd.read_csv("a.csv")` | DataFrame |
| `pd.DataFrame({"a": [1,2], "b": [3,4]})` | DataFrame (dict → 컬럼) |
| `pd.Series([1,2,3])` | Series |
| `sns.load_dataset("mpg")` | DataFrame (seaborn 내장) |
| `load_wine(as_frame=True, return_X_y=True)` | **(DataFrame, Series)** 튜플 |
| `df.copy()` | DataFrame (**원본 보호용 — 습관 들여라**) |

```python
df, y = load_wine(as_frame=True, return_X_y=True)   # X는 DataFrame, y는 Series
df["quality"] = y                                    # Series를 새 컬럼으로 붙이기
```

> `as_frame=True`가 없으면 **ndarray**로 나와서 `df["col"]`을 못 쓴다. 시험에서 컬럼 이름으로 접근해야 하면 꼭 필요.

## 0-3. 조회 3종 세트 — 처음 데이터를 받으면 무조건 이것부터

| 메서드 / 속성 | 반환 | 무엇을 보나 |
| --- | --- | --- |
| `df.head(n)` | DataFrame | 위에서 n개 (기본 5) — **생김새** |
| `df.tail(n)` | DataFrame | 아래에서 n개 |
| `df.info()` | **출력만** (None 반환) | 행 수 · dtype · **결측치** — **구조** |
| `df.describe()` | DataFrame | 평균·std·min·max·사분위 — **내용** |
| `df.shape` | tuple | `(행, 열)` |
| `df.columns` | Index | 컬럼 이름들 |
| `df.index` | Index | 행 라벨들 |
| `df.dtypes` | Series | 컬럼별 자료형 |
| `df.values` | **ndarray** | 순수 숫자 배열 (컬럼명 소실) |

> 🔥 **`info()`는 구조(타입·결측치), `describe()`는 내용(통계량).** 역할이 다르다.
> `info()`는 반환값이 `None`이라 `x = df.info()` 하면 x는 None이다. **print 전용.**

## 0-4. 열(column) 선택 — 대괄호 개수가 타입을 바꾼다

```
df["a"]          ──► Series      (1차원)
df[["a"]]        ──► DataFrame   (2차원, 열 1개)
df[["a", "b"]]   ──► DataFrame   (2차원, 열 2개)
df.a             ──► Series      (점 표기 — 공백/한글 컬럼엔 못 씀)
```

| 코드 | 반환 | 언제 |
| --- | --- | --- |
| `df["alcohol"]` | **Series** | 통계·집계할 때 |
| `df[["alcohol", "ash"]]` | **DataFrame** | 여러 열을 표로 다룰 때 |
| `df[continuous_cols]` | DataFrame | 리스트 변수로 여러 열 |

> 🔥 **대괄호 2개면 DataFrame.** `df.groupby("q")["a"].mean()`은 Series, `df.groupby("q")[["a"]].mean()`은 DataFrame.
> 스케일러에 넣을 땐 2차원이 필요하므로 `df[["a"]]` 또는 `df[cols]`를 쓴다.

## 0-5. 행(row) 선택 — `loc` vs `iloc`

| 구분 | `df.loc` | `df.iloc` |
| --- | --- | --- |
| 기준 | **라벨(이름)** | **위치(정수)** |
| 예 | `df.loc[3, "alcohol"]` | `df.iloc[3, 0]` |
| 슬라이스 끝값 | **포함** (`df.loc[0:2]` → 3행) | **미포함** (`df.iloc[0:2]` → 2행) |
| 비유 | 301호 우편함(**이름**) | 왼쪽에서 3번째 우편함(**순서**) |

```python
df.loc[0]                       # 0번 라벨 행 → Series
df.loc[0, "alcohol"]            # 값 하나 → scalar
df.loc[df["ash"].idxmin(), "quality"]      # 조건으로 찾은 행의 특정 열
df.loc[df["지역"] == "서울", "매출"]        # 행 조건 + 열 선택
df.loc[df["단가"] < 4000, "단가"] = 4000    # 조건부 대입 (수정)

df.iloc[0, 1]                   # 0행 1열 (위치)
df.iloc[:5, :3]                 # 앞 5행, 앞 3열
```

> 🔥 **`.loc`만 "조건부 대입"이 된다.** `df[조건]["열"] = 값`은 원본에 반영이 안 될 수 있다(SettingWithCopyWarning).
> 값을 바꾸려면 **`df.loc[조건, "열"] = 값`** 한 줄로 써라.

| 반환 차원 정리 | 결과 |
| --- | --- |
| `df.loc[행1개, 열1개]` | scalar |
| `df.loc[행1개]` / `df.loc[행1개, 열여러개]` | Series |
| `df.loc[행여러개, 열1개]` | Series |
| `df.loc[행여러개, 열여러개]` | DataFrame |

## 0-6. 조건 필터 (Boolean Indexing)

```
df["a"] > 5   ──► bool Series   ──► df[bool Series] ──► DataFrame
```

```python
df[df["alcohol"] > 13]                                  # 단일 조건
df[(df["alcohol"] > 13) & (df["ash"] < 2.5)]            # AND
df[(df["quality"] == 0) | (df["quality"] == 2)]         # OR
df[~(df["quality"] == 1)]                               # NOT
df[df["quality"].isin([0, 2])]                          # 목록 포함 (OR의 축약형)
df[df["메뉴"].str.contains("라떼")]                       # 문자열 포함
df[df["alcohol"].between(12, 14)]                       # 범위 (양끝 포함)
```

| 연산자 | 의미 | 주의 |
| --- | --- | --- |
| `&` | AND | `and` ❌ → ValueError: ambiguous |
| `\|` | OR | `or` ❌ |
| `~` | NOT | `not` ❌ |

> 🔥 **각 조건은 반드시 괄호로 감싼다.** `&`가 `>`, `==`보다 우선순위가 높아서 괄호 없으면 TypeError.
> `and`/`or`가 안 되는 이유: 파이썬의 `and`는 **값 하나**의 참/거짓을 보는데, `(df.a > 1)`은 **True/False 여러 개가 든 Series**라서 "전체적으로 참이냐"가 모호하다.

## 0-7. 정렬

| 코드 | 대상 | 반환 |
| --- | --- | --- |
| `df.sort_values("alcohol")` | 값 기준 오름차순 | DataFrame |
| `df.sort_values("alcohol", ascending=False)` | 내림차순 | DataFrame |
| `df.sort_values(["a", "b"])` | 다중 기준 | DataFrame |
| `s.sort_values(ascending=False)` | Series 정렬 | Series |
| `s.sort_index()` | **인덱스** 기준 정렬 | Series |
| `df.nlargest(5, "alcohol")` | 상위 5행 | DataFrame |
| `df.nsmallest(5, "alcohol")` | 하위 5행 | DataFrame |

> `value_counts()`는 **개수 내림차순**으로 나오므로, 인덱스 순서로 비교하려면 `.sort_index()`를 붙인다.
> (실습 TODO 1-4의 assert가 `.sort_index().equals(...)`인 이유)

## 0-8. 열 추가 · 삭제 · 이름 변경

```python
df["quality"] = y                          # 추가 (Series 대입)
df["ratio"] = df["a"] / df["b"]            # 파생 변수 (벡터 연산)

df.drop("B", axis=1)                       # 열 삭제 → 새 DataFrame
df.drop("MEDV", axis=1)                    # X 만들 때 쓰는 그것
df.drop(0, axis=0)                         # 행 삭제
df.drop(columns=["a", "b"])                # 이렇게도 됨

s.drop("MEDV")                             # Series는 인덱스 라벨로 삭제

df.rename(columns={"old": "new"})          # 이름 변경
df.columns = [c.upper() for c in df.columns]   # 전부 대문자로 (과제 노트북이 쓰는 방식)
```

| `axis` | 뜻 | 기억법 |
| --- | --- | --- |
| `axis=0` | **행** 방향 (기본) | 0 = 세로로 훑음 = 행 |
| `axis=1` | **열** 방향 | 1 = 가로로 훑음 = 열 |

> 🔥 **`drop`은 원본을 바꾸지 않는다.** 반드시 `df = df.drop(...)`로 다시 담거나 `inplace=True`를 쓴다.
> 시험에선 `X = df.drop("MEDV", axis=1)` 형태로 **X/y 분리**할 때 가장 많이 나온다.

## 0-9. 자료형 변환

| 코드 | 의미 |
| --- | --- |
| `df["a"].astype(int)` | 정수로 |
| `df[cols].astype(int)` | 여러 열 한 번에 |
| `df["a"].astype(str)` | 문자열로 |
| `pd.to_numeric(df["a"], errors="coerce")` | 숫자로, 실패하면 NaN |

## 0-10. 값 변환 — `apply` / `map` / `replace`

| 메서드 | 대상 | 설명 |
| --- | --- | --- |
| `s.apply(함수)` | Series | 원소마다 함수 적용 |
| `s.map({0:"A", 1:"B"})` | Series | **딕셔너리로 값 치환** |
| `df.apply(함수, axis=0/1)` | DataFrame | 열/행 단위 적용 |
| `df.replace(old, new)` | DataFrame | 값 치환 |
| `np.where(조건, 참값, 거짓값)` | 배열 | **삼항 연산자의 벡터판** |

```python
y = np.where(y == 0, 0, 1)                     # 다중분류 → 이진분류
df["등급"] = df["alcohol"].apply(lambda x: "높음" if x > 13 else "낮음")
```

## 0-11. 인덱스 다루기

| 코드 | 효과 |
| --- | --- |
| `df.reset_index()` | 인덱스를 **일반 컬럼으로** 꺼냄 (groupby 결과 정리용) |
| `df.reset_index(drop=True)` | 인덱스를 **버리고** 0,1,2…로 새로 매김 |
| `df.set_index("col")` | 특정 컬럼을 인덱스로 |

> 🔥 **인덱스는 필터링해도 살아남는다.** `X_train[mask]`와 `y_train[mask]`가 정렬되는 이유가 이것.
> 반대로 `.values`나 `scaler.transform()`을 거치면 **인덱스가 사라져서** X와 y의 행이 어긋날 수 있다.

## 0-12. 표 합치기

| 코드 | 방식 |
| --- | --- |
| `pd.concat([df1, df2])` | 위아래로 붙이기 (행 추가) |
| `pd.concat([df1, df2], axis=1)` | 좌우로 붙이기 (열 추가) |
| `pd.merge(df1, df2, on="key")` | 공통 키로 결합 (**엑셀 VLOOKUP**) |

## 0-13. 집계 — groupby / agg / pivot_table

| 코드 | 결과 모양 |
| --- | --- |
| `df.groupby("k")["v"].mean()` | Series (long) |
| `df.groupby("k")[["v","w"]].mean()` | DataFrame |
| `df.groupby("k").agg({"v":"sum", "w":"mean"})` | DataFrame (컬럼별 다른 집계) |
| `df.groupby("k")["v"].agg(["sum","mean","count"])` | DataFrame (여러 통계) |
| `pd.pivot_table(df, values="v", index="a", columns="b", aggfunc="sum")` | **wide 표** |

| `.count()` vs `.size()` | |
| --- | --- |
| `.count()` | **NaN 제외** 개수 |
| `.size()` | **NaN 포함** 전체 행 수 |

> 두 값이 다르면 그 차이만큼 결측치가 있다는 신호다.

## 0-14. 반환 타입 총정리 (외울 표)

| 호출 | 반환 |
| --- | --- |
| `df["a"]` | **Series** |
| `df[["a"]]`, `df[["a","b"]]` | **DataFrame** |
| `df[df["a"] > 1]` | **DataFrame** |
| `df.loc[행1, 열1]` | **scalar** |
| `df.mean()` | **Series** (컬럼별) |
| `df["a"].mean()` | **scalar** |
| `df.groupby("k")["v"].mean()` | **Series** (그룹별) |
| `df["a"].value_counts()` | **Series** |
| `df["a"].idxmax()` | **인덱스 라벨** |
| `df.corr()` | **DataFrame** (정방행렬) |
| `df.isnull()` | **bool DataFrame** |
| `df.isnull().sum()` | **Series** |
| `df.describe()` | **DataFrame** |
| `df.info()` | **None** (출력만) |
| `df.columns`, `df.index` | **Index** |
| `df.values`, `df["a"].values` | **ndarray** |
| `df.shape` | **tuple** |
| `df.drop(...)`, `df.fillna(...)`, `df.sort_values(...)` | **새 DataFrame** (원본 불변) |

## 0-15. 원본이 바뀌나 안 바뀌나

| 원본 **안 바뀜** (새 객체 반환) | 원본 **바뀜** |
| --- | --- |
| `drop` `fillna` `dropna` `sort_values` `rename` `replace` `astype` `copy` | `df["새열"] = ...` |
| → `df = df.drop(...)` 로 다시 담아야 함 | `df.loc[조건, "열"] = ...` |
| `inplace=True`를 주면 원본이 바뀜 | `model.fit(...)` (sklearn은 객체 자체가 학습됨) |

> 🔥 시험에서 "왜 안 바뀌지?" 하는 대부분의 원인이 이것. **`inplace=True`를 쓰거나 재대입하라.**

---

# 1. 가장 먼저 — 타입 지도

> **시험에서 막히는 이유는 메서드를 몰라서가 아니라, "이걸 지금 누구한테 부를 수 있지?"를 몰라서다.**
> 아래 사다리 하나만 머리에 넣으면 대부분 풀린다.

## 1-1. 객체 사다리 (pandas)

```
                    ┌─────────────────────────────────────────────┐
                    │              DataFrame  (2차원 표)           │
                    └─────────────────────────────────────────────┘
     df["col"] │          df[["a","b"]] │        df.groupby("k")["v"] │
       (1개)   ▼            (리스트)    ▼                            ▼
        ┌──────────────┐        DataFrame              ┌──────────────────┐
        │   Series     │        (그대로)                │  SeriesGroupBy   │
        │  (1차원 열)   │                               └──────────────────┘
        └──────────────┘                                        │ .mean() .sum()
   .mean() │      │ .idxmax()                                   │ .count() .size()
   .std()  │      │ .value_counts()                             ▼
   .max()  ▼      ▼                                        ┌──────────┐
      ┌────────┐  ┌────────┐                               │  Series  │
      │ scalar │  │ Series │  ← 또 사다리를 탈 수 있음        └──────────┘
      └────────┘  └────────┘
```

**핵심 규칙 3줄**

| 규칙 | 내용 |
| --- | --- |
| ① | `DataFrame`에 집계함수(`.mean()`)를 부르면 → **컬럼별 결과가 담긴 `Series`** |
| ② | `Series`에 집계함수를 부르면 → **값 하나(`scalar`)** |
| ③ | `GroupBy`에 집계함수를 부르면 → **그룹별 결과가 담긴 `Series`** |

> 그래서 `df.mean()`은 Series, `df["a"].mean()`은 숫자. **한 칸 내려갈 때마다 차원이 하나 줄어든다.**

## 1-2. `.idxmax()`가 특별한 이유

```
Series ──.max()────► 값         (얼마나 큰가)
       └─.idxmax()─► 인덱스 라벨 (누가 제일 큰가)
```

- 문제가 **"가장 ~한 것의 이름/번호"** 를 물으면 → 무조건 `.idxmax()` / `.idxmin()`
- 문제가 **"가장 큰 값"** 을 물으면 → `.max()` / `.min()`
- `groupby(...).mean().idxmax()`에서 idxmax가 돌려주는 건 **groupby의 기준 컬럼 값**(= 클래스 번호)이다.

## 1-3. 메서드 vs 함수 — 어디에 붙어 있나

| 형태 | 소속 | 대표 예시 |
| --- | --- | --- |
| `df.xxx()` | **DataFrame의 메서드** | `groupby` `corr` `describe` `isnull` `drop` `fillna` `head` `quantile` |
| `s.xxx()` | **Series의 메서드** | `mean` `std` `idxmax` `value_counts` `nunique` `between` `sort_values` `abs` |
| `pd.xxx()` | **pandas 모듈의 함수** | `pd.qcut` `pd.cut` `pd.Series` `pd.DataFrame` `pd.pivot_table` `pd.concat` |
| `np.xxx()` | **numpy 모듈의 함수** | `np.triu` `np.ones_like` `np.isclose` `np.nan` |
| `sns.xxx()` | **seaborn 모듈의 함수** | `heatmap` `histplot` `scatterplot` `boxplot` `pairplot` |
| `plt.xxx()` | **pyplot 모듈의 함수** | `subplots` `show` `tight_layout` `figure` |
| `ax.xxx()` | **Axes(그림 한 칸)의 메서드** | `set_title` `set_xlabel` `legend` `grid` `plot` |
| `모델.xxx()` | **sklearn estimator의 메서드** | `fit` `transform` `predict` `fit_transform` `predict_proba` |
| `metric(y, p)` | **sklearn.metrics의 함수** | `r2_score` `confusion_matrix` `roc_auc_score` |

> ⚠️ **`pd.qcut`은 `df.qcut`이 아니다.** `qcut` / `cut` / `merge` / `concat`은 pandas **모듈 함수**다.
> 반대로 `groupby` / `corr`은 **DataFrame의 메서드**라서 `pd.groupby(df, ...)` 같은 건 없다.

## 1-4. 헷갈리는 소속 정리표

| 이건 누구 거? | 정답 | 왜 헷갈리나 |
| --- | --- | --- |
| `.value_counts()` | **Series 전용**으로 외워라 | df에 부르면 pandas 2.x부터 되긴 하나 "행 조합"을 센다 — 의미가 다름 |
| `.between(lo, hi)` | **Series 전용** | DataFrame엔 없음 |
| `.nunique()` | Series / DataFrame 둘 다 | Series → scalar, DataFrame → Series |
| `.corr()` | DataFrame → **정방 DataFrame** / `s1.corr(s2)` → scalar | 인자 유무로 완전히 다름 |
| `.quantile(q)` | Series → scalar / DataFrame → Series | 대상이 뭐냐로 결과 차원이 갈림 |
| `.isnull()` | DataFrame → **같은 크기 bool DataFrame** | 개수가 아님! `.sum()`을 또 붙여야 개수 |
| `len(df)` | **파이썬 내장 함수** | 행 개수. `df.shape[0]`과 동일 |
| `.values` | **속성** (괄호 없음) | `df["a"].values` → `ndarray` |
| `.shape` `.columns` `.index` `.dtypes` | **속성** (괄호 없음) | `df.shape()` 하면 TypeError |

---

# 2. 전체 흐름

```
[Step 1] 로드 → 구조 파악 → 통계량 → 필터/비율 → 그룹집계 → 상관관계 → 시각화
                                      ↓
[Step 1] 결측치 탐지·대체 → 이상치(IQR) 탐지·제거
                                      ↓
[Step 2] X/y 분리 → train_test_split → StandardScaler(fit_transform / transform)
                                      ↓
[Step 2] 모델 선언 → .fit() → .predict() → 평가지표
                                      ↓
[Step 3] cross_val_score → PCA → KMeans → 시각화
```

---

# 3. 구조 파악 — `len` / `shape` / `nunique`

| 호출 | 반환 타입 | 값 |
| --- | --- | --- |
| `len(df)` | `int` | 행 수 |
| `df.shape` | `tuple` | `(행, 열)` |
| `df.shape[0]` / `df.shape[1]` | `int` | 행 수 / 열 수 |
| `df.columns` | `Index` | 컬럼 이름들 |
| `len(df.columns)` | `int` | 열 수 |
| `df["col"].nunique()` | `int` | 고유값 개수 |
| `df["col"].unique()` | `ndarray` | 고유값 배열 |

```python
# 실습(Wine) — quality까지 df에 넣어놨으므로 14가 정답
sample_count  = len(df)          # 178
feature_count = df.shape[1]      # 14  ← quality 포함!
class_count   = y.nunique()      # 3   (= df["quality"].nunique())

# 과제(Boston) — 타겟 MEDV를 빼야 하므로 -1
sample_count  = len(df)          # 506
feature_count = df.shape[1] - 1  # 12  ← MEDV 제외
```

> 🔥 **시험 포인트**: 똑같이 "특성 수"를 물어도 **실습은 `df.shape[1]`, 과제는 `df.shape[1] - 1`**.
> assert의 기대값(14 / 12)을 먼저 보고 **타겟 포함 여부를 역산**하라.

---

# 4. 기초 통계량 — Series 집계

```
Series ──► scalar
```

| 메서드 | 의미 | 비고 |
| --- | --- | --- |
| `.mean()` | 평균 | NaN 자동 제외 |
| `.median()` | 중앙값 | |
| `.std()` | 표준편차 | **pandas는 ddof=1 (표본)** |
| `.min()` / `.max()` | 최소 / 최대 | |
| `.sum()` / `.count()` | 합 / 개수(NaN 제외) | |
| `.describe()` | 위 전부 한 번에 | 반환 = Series |

```python
malic_mean  = df["malic_acid"].mean()
malic_std   = df["malic_acid"].std()

medv_mean   = df["MEDV"].mean()
medv_median = df["MEDV"].median()
medv_std    = df["MEDV"].std()
medv_min    = df["MEDV"].min()
medv_max    = df["MEDV"].max()
```

> ⚠️ **numpy와 pandas의 std가 다르다.** `np.std()`는 ddof=0(모집단), `pd.Series.std()`는 ddof=1(표본).
> 기대값이 미세하게 안 맞으면 이걸 의심하라. (`sklearn.StandardScaler`는 ddof=0을 쓴다)

---

# 5. 조건 필터와 비율 — bool Series 트릭

```
Series ──[비교연산]──► bool Series ──.mean()──► 비율(0~1)
                                  └─.sum()───► 개수
```

**이 패턴은 시험에 거의 반드시 나온다.**

```python
# "Color intensity가 10 이상인 샘플의 비율(%)"
high_color_ratio = (df["color_intensity"] >= 10).mean() * 100

# 같은 뜻, 길게 쓴 버전
high_color_ratio = len(df[df["color_intensity"] >= 10]) / len(df) * 100
```

| 표현 | 결과 |
| --- | --- |
| `(s >= 10)` | bool Series |
| `(s >= 10).sum()` | **True 개수** (True=1이라서) |
| `(s >= 10).mean()` | **True 비율 0~1** |
| `df[s >= 10]` | 조건 만족 행만 남긴 DataFrame |

**조건 결합** (`02_pandas.md` 8절과 동일)

```python
df[(df["a"] > 1) & (df["b"] < 5)]    # ✅ &, |, ~  + 각 조건 괄호
df[(df["a"] > 1) and (df["b"] < 5)]  # ❌ ValueError: ambiguous
```

**상위 N% 뽑기**

```python
# Magnesium 상위 10% 샘플들의 평균 Proline
thr = df["magnesium"].quantile(0.9)              # scalar
high_magnesium_proline_mean = df[df["magnesium"] >= thr]["proline"].mean()

# 한 줄 버전
high_magnesium_proline_mean = df[df["magnesium"] >= df["magnesium"].quantile(0.9)]["proline"].mean()

# 대안 (기대값이 안 맞으면 이걸로 시도) — 개수 기준
high_magnesium_proline_mean = df.nlargest(int(len(df) * 0.1), "magnesium")["proline"].mean()
```

> 💡 `quantile(0.9)`는 **값 기준** 상위 10% 경계, `nlargest(n)`은 **개수 기준** 상위 n개.
> "상위 10%"라고만 하면 보통 `quantile`이 정답이지만, 동점값 처리 때문에 뽑히는 개수가 달라질 수 있다.

---

# 6. 그룹 집계 — groupby 3단 체이닝

```
DataFrame ──.groupby("키")──► DataFrameGroupBy
          ──["값컬럼"]───────► SeriesGroupBy
          ──.mean()──────────► Series (index = 그룹키)
          ──.idxmax()────────► 그룹키 하나
```

```python
top_alcohol_class = df.groupby("quality")["alcohol"].mean().idxmax()
```

**한 번에 못 쓰겠으면 잘라 쓰고 print를 찍어라.**

```python
g = df.groupby("quality")["alcohol"]   # SeriesGroupBy
m = g.mean()                            # Series
print(m)                                # 눈으로 확인
top_alcohol_class = m.idxmax()          # 정답
```

| groupby 뒤에 올 수 있는 것 | 반환 |
| --- | --- |
| `.mean() .sum() .max() .min() .median() .std()` | Series |
| `.count()` | Series (**NaN 제외** 개수) |
| `.size()` | Series (**NaN 포함** 행 수) |
| `.agg(["mean","std"])` | DataFrame |
| `.agg({"a":"sum","b":"mean"})` | DataFrame |
| `[["a","b"]].mean()` | **DataFrame** (컬럼 2개 이상이면) |

**응용 — "최솟값을 가진 샘플의 클래스"**

이건 groupby가 아니다. **행 하나를 찾는 문제**다.

```python
# ash가 최소인 "행"의 위치 → 그 행의 quality
min_ash_class = df.loc[df["ash"].idxmin(), "quality"]
#                      └ Series.idxmin() → 행 인덱스 라벨
#               └ df.loc[행라벨, 열이름] → scalar
```

> 🔥 **groupby냐 loc이냐 구분법**
> - "**클래스별** 평균이 가장 큰 클래스" → 그룹 요약이 필요 → `groupby`
> - "**최솟값을 가진 샘플**의 클래스" → 개별 행 1개를 지목 → `idxmin()` + `.loc`

**"분포에서 피크가 가장 높은 클래스"**

histplot으로 그렸을 때 **막대가 제일 높은** 클래스 = 그 구간에 샘플이 제일 많이 몰린 클래스.

```python
proline_peak_class = df["quality"].value_counts().idxmax()          # 1
# 또는
proline_peak_class = df.groupby("quality")["proline"].count().idxmax()
```

> ⚠️ 이건 "평균이 가장 높은"이 **아니다.** Wine에서 proline **평균** 최대는 class 0이지만, **피크(빈도)** 최대는 class 1이다.
> 애매하면 `sns.histplot(data=df, x="proline", hue="quality")`를 그려서 눈으로 확인하는 게 가장 빠르고 안전하다.

---

# 7. 상관관계 — corr의 두 얼굴

```
DataFrame.corr()          ──► DataFrame  (정방 대칭 행렬)
Series.corr(other Series) ──► scalar
DataFrame.corr()["MEDV"]  ──► Series     (한 열만 뽑음)
```

```python
corr = df.corr()                     # 실습 TODO 2
corr = df.corr(numeric_only=True)    # 문자열 컬럼이 섞여 있으면 필수
```

**"타겟과 상관 가장 높은 특성 이름"**

```python
# 자기 자신(상관 1.0)을 반드시 제거해야 한다
corr_with_medv   = df.corr(numeric_only=True)["MEDV"].drop("MEDV")   # Series
top_corr_feature = corr_with_medv.abs().idxmax()                      # 이름 (str)
top_corr_value   = corr_with_medv[top_corr_feature]                   # 값 (부호 유지)
```

> 🔥 **과제 노트북의 함정**: `top_corr_feature = corr_with_medv.abs().idxmax()` 줄이 **이미 주어져 있다.**
> 거기에 `.drop("MEDV")`가 없으므로, **빈칸인 `corr_with_medv`를 만들 때 MEDV를 미리 빼놔야** 한다.
> 안 그러면 자기 자신(1.0)이 뽑혀서 답이 `"MEDV"`가 된다. **주어진 코드를 읽고 빈칸을 역산하는 문제.**

```python
# 실습 TODO 1-12: alcohol과 가장 상관 높은 특성
top_corr_with_alcohol = df.corr()["alcohol"].drop("alcohol").idxmax()   # "proline"
```

**"상관 상위 5개 특성" (실습 TODO 5)**

```python
top_features = (df.corr()["quality"]           # Series
                  .abs()                        # 음의 상관도 강한 관계다 → 절댓값
                  .sort_values(ascending=False) # 내림차순
                  [1:6]                         # 0번은 quality 자기자신 → 제외
                  .index)                       # Index (→ .tolist() 가능)
print("선택된 feature:", top_features.tolist())
```

| 체인 단계 | 타입 |
| --- | --- |
| `df.corr()` | DataFrame |
| `["quality"]` | Series |
| `.abs()` | Series |
| `.sort_values(ascending=False)` | Series |
| `[1:6]` | Series (슬라이스) |
| `.index` | **Index** |
| `.tolist()` | list |

> 문제에 `print(..., top_features.tolist())`가 이미 있다 → **`.tolist()`를 가진 타입(Index/Series/ndarray)으로 끝내야 한다**는 힌트다. `.index`까지 붙이는 이유.

**"|corr| >= 0.7 인 특성 쌍" (과제 TODO 3)**

```python
c = df.corr(numeric_only=True)
cols = c.columns
strong_corr_pairs = [
    (a, b, c.loc[a, b])
    for i, a in enumerate(cols)
    for b in cols[i + 1:]              # ← i+1부터 시작: 대각선·중복 자동 제거
    if abs(c.loc[a, b]) >= 0.7
]
```

<details><summary>고급 버전 (stack 사용)</summary>

```python
c = df.corr(numeric_only=True).abs()
upper = c.where(np.triu(np.ones(c.shape), k=1).astype(bool))
strong_corr_pairs = upper.stack()[lambda s: s >= 0.7].index.tolist()
```
</details>

---

# 8. 결측치

```
DataFrame ──.isnull()──► bool DataFrame ──.sum()──► Series(컬럼별) ──.sum()──► 총 개수
```

```python
df.isnull()             # 같은 크기 bool 표
df.isnull().sum()       # 컬럼별 결측 개수 (Series)
df.isnull().sum().sum() # 전체 결측 개수 (scalar)

missing_counts = df.isnull().sum().sort_values(ascending=False)   # 과제 TODO 2
```

> `.isnull()` == `.isna()` (완전 동일). 반대는 `.notnull()` / `.notna()`.

**대체 (실습 TODO 6)**

```python
df_filled = df_missing.fillna(df_missing.mean())
#                             └ DataFrame.mean() → Series(컬럼별 평균)
#                               fillna가 컬럼 이름으로 자동 매칭해서 채운다
```

| 방법 | 코드 |
| --- | --- |
| 평균 대체 | `df.fillna(df.mean())` |
| 중앙값 대체 | `df.fillna(df.median())` |
| 특정 컬럼만 | `df["a"] = df["a"].fillna(df["a"].mean())` |
| 앞 값으로 | `df.ffill()` |
| 행 삭제 | `df.dropna()` |
| sklearn | `SimpleImputer(strategy="mean").fit_transform(X)` |

**시각화**

```python
sns.heatmap(df_missing.isnull(), cbar=False)   # bool 표를 그대로 히트맵에
```

---

# 9. 이상치 — IQR 공식

```
Q1  = s.quantile(0.25)       # scalar
Q3  = s.quantile(0.75)       # scalar
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
```

**탐지**

```python
outliers = df[(df["alcohol"] < lower) | (df["alcohol"] > upper)]
```

**제거 (실습 TODO 6)**

```python
Q1 = df_filled["alcohol"].quantile(0.25)
Q3 = df_filled["alcohol"].quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

df_no_outliers = df_filled[(df_filled["alcohol"] >= lower) & (df_filled["alcohol"] <= upper)]
# 또는 Series 전용 메서드로 더 짧게
df_no_outliers = df_filled[df_filled["alcohol"].between(lower, upper)]
```

**비율 (과제 TODO 2)**

```python
medv_outlier_ratio = ((df["MEDV"] < medv_outlier_lower) |
                      (df["MEDV"] > medv_outlier_upper)).mean() * 100
```

**전 컬럼 IQR + 데이터 누수 방지 (과제 TODO 5)** — 이 노트북 최고 난이도 빈칸

```python
# 1) train으로만 경계 계산 → dict에 저장
iqr_bounds = {}
for col in continuous_cols:
    Q1 = X_train[col].quantile(0.25)
    Q3 = X_train[col].quantile(0.75)
    IQR = Q3 - Q1
    iqr_bounds[col] = (Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)

# 2) "모든 컬럼이 정상 범위" boolean Series — True로 시작해서 &= 로 누적
mask_train = pd.Series(True, index=X_train.index)
for col, (lo, hi) in iqr_bounds.items():
    mask_train &= X_train[col].between(lo, hi)
X_train = X_train[mask_train]
y_train = y_train[mask_train]

# 3) test에도 "train에서 만든" 경계를 그대로 적용 (재계산 금지!)
mask_test = pd.Series(True, index=X_test.index)
for col, (lo, hi) in iqr_bounds.items():
    mask_test &= X_test[col].between(lo, hi)
X_test = X_test[mask_test]
y_test = y_test[mask_test]
```

| 조각 | 타입 / 역할 |
| --- | --- |
| `pd.Series(True, index=...)` | 전부 True인 bool Series (**AND 누적의 초기값**) |
| `X_train[col].between(lo, hi)` | bool Series |
| `mask &= 조건` | bool Series 원소별 AND |
| `X_train[mask_train]` | 필터링된 DataFrame |
| `y_train[mask_train]` | 필터링된 Series (**인덱스가 같아야 정렬됨**) |

> 🔥 **데이터 누수(Data Leakage)** — 서술형 단골.
> ❌ 전체 데이터로 통계량 계산 → 분할
> ✅ 분할 → **train으로만** 통계량 계산 → train/test에 동일 적용

---

# 10. 시각화 — matplotlib 뼈대 + seaborn 내용물

## 10-1. 역할 분담

| 라이브러리 | 역할 | 호출 형태 |
| --- | --- | --- |
| **matplotlib** | 도화지(Figure)와 칸(Axes)을 만든다, 축·제목·범례 | `plt.subplots()`, `ax.set_title()` |
| **seaborn** | 그 칸 안에 그림을 그린다 | `sns.histplot(..., ax=ax[0])` |

```
plt.subplots()          ──► (Figure, Axes)               ← 칸 하나
plt.subplots(ncols=3)   ──► (Figure, ndarray of Axes)    ← ax[0], ax[1], ax[2]
plt.subplots(2, 2)      ──► (Figure, 2차원 ndarray)       ← axes[0, 0], axes[1, 1]
```

```python
fig, ax = plt.subplots(figsize=(18, 5), ncols=3)
sns.histplot(..., ax=ax[0])       # ← 어느 칸에 그릴지 ax= 로 지정
ax[0].set_title("...")            # ← 제목은 Axes의 메서드
fig.tight_layout()                # ← 레이아웃은 Figure의 메서드
plt.show()
```

## 10-2. Axes-level vs Figure-level (**중요한 함정**)

| 종류 | 함수 | `ax=` 인자 | 반환 |
| --- | --- | --- | --- |
| **Axes-level** | `histplot` `scatterplot` `boxplot` `heatmap` `lineplot` `barplot` `countplot` `regplot` `kdeplot` `violinplot` | ✅ 있음 | `Axes` |
| **Figure-level** | `pairplot` `jointplot` `relplot` `displot` `catplot` `lmplot` | ❌ **없음** | `PairGrid` / `FacetGrid` |

> 🔥 `sns.pairplot(..., ax=ax[0])` → **TypeError.** Figure-level은 자기가 Figure를 통째로 만든다.

## 10-3. 공통 인자

| 인자 | 의미 | 타입 |
| --- | --- | --- |
| `data=df` | 대상 DataFrame | DataFrame |
| `x=`, `y=` | 축에 놓을 **컬럼 이름(문자열)** | str (또는 Series/배열 직접) |
| `hue=` | **색으로 나눌 기준 컬럼** | str |
| `bins=` | 히스토그램 구간 수 | int |
| `kde=True` | 밀도 곡선 겹쳐 그리기 | bool |
| `alpha=` | 투명도 (겹친 점 보이게) | float |
| `ax=` | 그릴 칸 | Axes |

> 💡 `x`만 주면 **세로** 히스토그램, **`y`만 주면 가로(눕힌)** 히스토그램, **`x`·`y` 둘 다 주면 2차원** 히스토그램.
> 실습 TODO 3의 세 문제가 정확히 이 셋이다.

## 10-4. heatmap 인자 (실습 TODO 2 / 과제 TODO 3)

| 인자 | 의미 |
| --- | --- |
| `annot=True` | 칸마다 **숫자 표시** |
| `fmt=".2f"` | 숫자 **소수점 2자리** 포맷 |
| `cmap="coolwarm"` | 음수 파랑 ↔ 양수 빨강 |
| `mask=` | True인 칸을 **가림** (bool 배열) |
| `vmin=-1, vmax=1` | 색 기준 고정 |
| `linewidths=` | 칸 사이 선 |

**상삼각 마스킹** — `np.triu`가 핵심

| 함수 | 뜻 |
| --- | --- |
| `np.triu(m)` | **상**삼각(upper)만 True, 나머지 0 |
| `np.tril(m)` | **하**삼각(lower)만 True |
| `k=0` (기본) | 대각선 **포함** |
| `k=1` | 대각선 **제외** |

```python
# 실습 TODO 2 정답 — 대각선도 빼고, 윗부분도 빼고, grid 제거, 배경 흰색
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))     # k=0 → 대각선 + 상삼각 가림

sns.set_style("white")                             # 배경 흰색 + grid 제거를 한 번에
plt.figure(figsize=(14, 12))                       # 변수가 많으니 크게
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm")
plt.grid(False)                                    # 혹시 남은 grid 제거
plt.show()
```

| 요구사항 | 대응 인자 |
| --- | --- |
| Figure size를 키워라 | `plt.figure(figsize=(14,12))` |
| 수치적으로 와닿게 | `annot=True` |
| 소수점 두자리 | `fmt=".2f"` |
| coolwarm | `cmap="coolwarm"` |
| 대각선 제외 + 윗부분 제외 | `mask=np.triu(np.ones_like(corr, dtype=bool))` |
| grid 없애기 | `plt.grid(False)` 또는 `sns.set_style("white")` |
| 배경 흰색 | `sns.set_style("white")` |

## 10-5. 시각화 빈칸 정답 모음

```python
# ── 실습 TODO 3 ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 5), ncols=3)

# 1. 가로로 눕히기 → x 대신 y
sns.histplot(data=df, y="flavanoids", bins=20, kde=True, ax=ax[0])

# 2. 클래스별 분포 → hue
sns.histplot(data=df, x="flavanoids", bins=20, kde=True, hue="quality", ax=ax[1])

# 3. 두 변수 동시 → x, y 둘 다 (2D 히스토그램)
sns.histplot(data=df, x="flavanoids", y="total_phenols", hue="quality", ax=ax[2])

fig.tight_layout(); plt.show()


# ── 실습 TODO 4 ────────────────────────────────────────────
sns.scatterplot(data=df, x="flavanoids", y="total_phenols", hue="quality")
plt.show()


# ── 실습 TODO 5 ────────────────────────────────────────────
top_features = df.corr()["quality"].abs().sort_values(ascending=False)[1:6].index
print("선택된 feature:", top_features.tolist())

sns.pairplot(data=df, vars=list(top_features), hue="quality")   # ax= 못 씀!
plt.show()


# ── 과제 TODO 3-4 ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
plt.tight_layout(); plt.show()


# ── 과제 TODO 9 (실제값 vs 예측값) ──────────────────────────
fig, ax = plt.subplots(figsize=(8, 8))

sns.scatterplot(x=y_test, y=y_pred, alpha=0.6, ax=ax)     # x,y에 Series/배열 직접 전달 가능

lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
ax.plot(lims, lims, "r--", lw=2, label="Ideal (y=x)")     # ax.plot은 matplotlib 메서드

ax.set_title(f"Actual vs Predicted (RMSE={rmse:.3f}, R2={r2:.4f})", fontsize=13)
ax.set_xlabel("Actual MEDV ($1000s)")
ax.set_ylabel("Predicted MEDV ($1000s)")
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()
```

---

# 11. sklearn — 3단 파이프라인

> **sklearn의 모든 것은 이 패턴 하나다.**

```
① 선언   model = 클래스(하이퍼파라미터)     ← 아직 아무것도 안 배움
② 학습   model.fit(X_train, y_train)        ← 반환값은 self (그래서 체이닝 가능)
③ 적용   model.predict(X_test)              ← 예측기(모델)
        model.transform(X_test)             ← 변환기(스케일러/PCA)
```

| 메서드 | 누가 가지고 있나 | 입력 → 출력 |
| --- | --- | --- |
| `.fit(X, y)` | 모든 estimator | → **self** |
| `.transform(X)` | 변환기 (Scaler, PCA) | `ndarray` → `ndarray` |
| `.fit_transform(X)` | 변환기 | fit + transform 한 번에 (**train 전용**) |
| `.predict(X)` | 예측기 (Regression, Classifier, KMeans) | `ndarray` → `ndarray` (예측값) |
| `.predict_proba(X)` | **분류기만** | → `(n, 클래스수)` 확률 배열 |
| `.fit_predict(X)` | KMeans 등 | fit + predict 한 번에 |

> 🔥 **가장 자주 나오는 함정**
> - train은 `fit_transform`, **test는 반드시 `transform`만**. test에 `fit_transform`을 쓰면 데이터 누수.
> - `model.fit(...)`은 **반환값을 변수에 담을 필요가 없다.** 객체 자체가 바뀐다(in-place).
>   `model = model.fit(X, y)`도 되지만 `model.fit(X, y)`만 써도 동일.

## 11-1. train_test_split — **함수**이고, 반환은 **4개짜리 튜플**

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,      # test 비율
    random_state=42,    # 재현성 고정
    stratify=y,         # 클래스 비율 유지
)
```

> **반환 순서를 외워라: `X_train, X_test, y_train, y_test`** (X 둘 먼저, y 둘 나중)

| 요구사항 문구 | 대응 인자 |
| --- | --- |
| "test는 30%" | `test_size=0.3` |
| "결과를 고정" / "재현성" | `random_state=42` |
| "train엔 전부 0, test엔 전부 1이 들어가는 것 방지" | **`stratify=y`** |
| "연속형이라 stratify 불가 → 10구간으로 나눠서" | `stratify=pd.qcut(y, q=10, labels=False)` |

```python
# ── 실습 TODO 7
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)
scaler = StandardScaler()      # 선언만! fit/transform은 아래 주어진 코드가 함

# ── 과제 TODO 4 (회귀라서 qcut으로 구간화 후 stratify)
X = df.drop("MEDV", axis=1)
y = df["MEDV"]
y_binned = pd.qcut(y, q=10, labels=False, duplicates="drop")   # pd 모듈 함수!
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y_binned)
```

| `pd.qcut` 인자 | 의미 |
| --- | --- |
| `q=10` | **10개 구간(십분위)** 으로 나눔 |
| `labels=False` | 구간 이름 대신 **정수 0~9** 반환 |
| `duplicates="drop"` | 경계가 겹치면 구간 합치기 (에러 방지) |

> `pd.cut`은 **값 범위를 균등 분할**, `pd.qcut`은 **개수를 균등 분할(분위수)**. stratify용으로는 `qcut`.

## 11-2. StandardScaler

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()                      # ① 선언
X_train_scaled = scaler.fit_transform(X_train) # ② train: fit + transform
X_test_scaled  = scaler.transform(X_test)      # ③ test : transform만!
```

```python
# ── 과제 TODO 6 (연속형 컬럼만 표준화 후 DataFrame으로 복원)
scaler = StandardScaler()
X_train_scaled_num = scaler.fit_transform(X_train[continuous_cols])   # ndarray
X_test_scaled_num  = scaler.transform(X_test[continuous_cols])        # ndarray

X_train = X_train.copy()
X_test  = X_test.copy()
X_train[continuous_cols] = X_train_scaled_num      # ndarray → DataFrame 컬럼에 대입
X_test[continuous_cols]  = X_test_scaled_num
```

> ⚠️ `scaler.transform()`의 반환은 **컬럼 이름이 사라진 `ndarray`**다.
> DataFrame으로 되돌리려면 `pd.DataFrame(arr, columns=..., index=...)` 하거나, 위처럼 **기존 컬럼에 대입**한다.
> `index=`를 안 맞추면 나중에 `y`와 행이 어긋난다.

## 11-3. 모델 학습·예측

```python
# ── 실습 TODO 8 (분류)
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(max_iter=1000)        # ConvergenceWarning 방지
clf.fit(X_train_norm, y_train)
y_pred = clf.predict(X_test_norm)

# ── 과제 TODO 7-8 (회귀)
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

> ⚠️ **실습 노트북 버그 주의**: 주어진 코드에 `y_score = clf.predict_proba(X_test)[:, 1]`이 있는데,
> 여기 `X_test`는 **표준화 안 된 원본**이다. 정확히 하려면 `X_test_norm`이어야 한다. 시험에서는 **학습에 쓴 것과 같은 전처리를 거친 데이터**를 넣는 게 원칙.

| 학습 후 생기는 속성 | 의미 |
| --- | --- |
| `model.coef_` | 회귀 계수 (**학습 전엔 없음** → `hasattr(model,'coef_')`로 학습 여부 확인) |
| `model.intercept_` | 절편 |
| `clf.classes_` | 클래스 라벨 |
| `pca.explained_variance_ratio_` | 주성분별 설명 분산 비율 |
| `kmeans.labels_` | 군집 라벨 |

> 💡 sklearn에서 **뒤에 언더스코어(`_`)가 붙은 속성은 "학습으로 알아낸 값"** 이라는 규칙이다.

## 11-4. 평가 지표 — 전부 **함수**, 인자 순서 `(정답, 예측)`

```python
# 회귀 (과제 TODO 8)
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
rmse = root_mean_squared_error(y_test, y_pred)
mae  = mean_absolute_error(y_test, y_pred)
r2   = r2_score(y_test, y_pred)

# 분류 (실습 TODO 8)
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
auc = roc_auc_score(y_test, y_score)
```

| 지표 | 함수 | 입력 | 좋은 값 |
| --- | --- | --- | --- |
| RMSE | `root_mean_squared_error(y, p)` | 예측값 | 작을수록 |
| MAE | `mean_absolute_error(y, p)` | 예측값 | 작을수록 |
| R² | `r2_score(y, p)` | 예측값 | 1에 가까울수록 |
| 정확도 | `accuracy_score(y, p)` | 예측 **라벨** | 클수록 |
| 혼동행렬 | `confusion_matrix(y, p)` | 예측 **라벨** | 대각선이 클수록 |
| 리포트 | `classification_report(y, p)` | 예측 **라벨** | — |
| ROC-AUC | `roc_auc_score(y, y_score)` | **확률/점수** ⚠️ | 1에 가까울수록 |

> 🔥 **ROC-AUC만 입력이 다르다.** `y_pred`(0/1 라벨)가 아니라 **`predict_proba(X)[:, 1]`(양성 확률)** 을 넣어야 한다.
> 구버전 sklearn엔 `root_mean_squared_error`가 없다 → `mean_squared_error(y, p, squared=False)` 또는 `np.sqrt(mean_squared_error(y, p))`.

## 11-5. 교차검증 (실습 TODO 9)

```python
from sklearn.model_selection import cross_val_score
f1_scores = cross_val_score(clf, X_train_norm, y_train, cv=5, scoring="f1")
print("Average F1-score (CV):", f1_scores.mean())
```

| 인자 | 의미 |
| --- | --- |
| 1번째 | **학습 안 된 모델 객체** (함수 안에서 알아서 fit 함) |
| `X`, `y` | 전체 데이터 |
| `cv=5` | 5-fold |
| `scoring="f1"` | 이진 F1. 다중분류면 `"f1_macro"`, 회귀면 `"r2"` / `"neg_root_mean_squared_error"` |

> 반환은 **`ndarray` (fold별 점수 5개)**. 그래서 `f1_scores.mean()`이 가능하다.
> 문제에 `.mean()`이 이미 있으면 **평균이 아니라 배열을 담으라는 뜻**이다 — 변수명이 `f1_scores`(복수)인 것도 힌트.

## 11-6. PCA + KMeans (실습 TODO 10)

```python
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

X_pca     = PCA(n_components=2).fit_transform(X_train_norm)         # (n, 2) ndarray
y_cluster = KMeans(n_clusters=2, random_state=42).fit_predict(X_pca) # (n,) 라벨

fig, ax = plt.subplots(figsize=(9, 3), ncols=2)
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=y_cluster, ax=ax[0])
ax[0].set_title("KMeans Clusters")
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=y_train,   ax=ax[1])
ax[1].set_title("True Labels")
fig.tight_layout(); plt.show()
```

| 표현 | 의미 |
| --- | --- |
| `X_pca[:, 0]` | 1번째 주성분 (전체 행, 0번 열) — **numpy 2차원 인덱싱** |
| `X_pca[:, 1]` | 2번째 주성분 |
| `n_components=2` | 몇 차원으로 줄일지 |
| `n_clusters=2` | 몇 개 군집으로 나눌지 |
| `fit_predict` | `fit()` + `labels_` 를 한 번에 |

> `X_pca`는 DataFrame이 아니라 **ndarray**라서 `X_pca["PC1"]`이 아니라 `X_pca[:, 0]`이다.
> seaborn의 `x=`/`y=`에는 **컬럼 이름 문자열뿐 아니라 배열도 직접** 넣을 수 있다 (`data=`를 안 줄 때).

---

# 12. 실습(Wine) TODO 1 — 12문제 정답 한눈에

```python
# 1  총 샘플 수
sample_count = len(df)                                              # 178
# 2  특성 수 (quality 포함)
feature_count = df.shape[1]                                         # 14
# 3  클래스 개수
class_count = y.nunique()                                           # 3
# 4  클래스별 샘플 수 (Series)
class_distribution = y.value_counts()
# 5  Alcohol 평균 최대 클래스
top_alcohol_class = df.groupby("quality")["alcohol"].mean().idxmax() # 0
# 6  Malic acid 평균
malic_mean = df["malic_acid"].mean()
# 7  Malic acid 표준편차
malic_std = df["malic_acid"].std()
# 8  Color intensity >= 10 비율(%)
high_color_ratio = (df["color_intensity"] >= 10).mean() * 100
# 9  Ash 최솟값을 가진 샘플의 클래스
min_ash_class = df.loc[df["ash"].idxmin(), "quality"]                # 1
# 10 Proline 분포 피크가 가장 높은 클래스
proline_peak_class = df["quality"].value_counts().idxmax()           # 1
# 11 Magnesium 상위 10%의 평균 Proline
high_magnesium_proline_mean = df[df["magnesium"] >= df["magnesium"].quantile(0.9)]["proline"].mean()
# 12 Alcohol과 상관 가장 높은 특성
top_corr_with_alcohol = df.corr()["alcohol"].drop("alcohol").idxmax() # "proline"
```

> ⚠️ 11번은 `quantile(0.9)` 기준으로 뽑히는 개수가 데이터에 따라 달라질 수 있다.
> assert가 실패하면 `df.nlargest(int(len(df)*0.1), "magnesium")["proline"].mean()`으로 바꿔 시도하라.

---

# 13. 시험장 전략 — 막혔을 때 순서

## 13-1. 문제를 읽는 순서

1. **assert의 기대값을 먼저 본다.** → 답의 타입/차원/스케일을 역산할 수 있다.
   - `== 178` → 정수 하나 → `len()` / `.shape[]`
   - `.sort_index().equals(pd.Series(...))` → **Series**여야 함 → `.value_counts()`
   - `np.isclose(x, 2.33)` → 실수 하나 → `.mean()`
   - `== 0` / `== 1` (작은 정수) → **클래스 번호** → `.idxmax()` / `.idxmin()`
   - `in df.columns` → **컬럼 이름 문자열** → `.idxmax()` on corr Series
2. **아래 이미 주어진 코드를 본다.** → 빈칸이 어떤 타입이어야 하는지 확정된다.
   - `top_features.tolist()` → Index / Series / ndarray
   - `f1_scores.mean()` → ndarray
   - `scaler.fit(X_train)` → scaler는 **선언만** 하면 됨
   - `corr_with_medv.abs().idxmax()` → **자기 자신이 미리 빠져 있어야** 함
3. **한 줄로 쓰려 하지 말고 쪼갠다.** 중간에 `print()`.

## 13-2. 체이닝 조립 공식

> **"어떤 대상(DataFrame)을 → 어떻게 좁히고(선택/필터/그룹) → 무엇으로 요약하고(집계) → 무엇을 꺼낼까(값/이름)"**

| 문제 문구 | 체인 |
| --- | --- |
| "**A별** B의 평균이 가장 큰 A" | `df.groupby("A")["B"].mean().idxmax()` |
| "**A별** B의 최솟값이 가장 작은 A" | `df.groupby("A")["B"].min().idxmin()` |
| "B가 최소인 **샘플**의 A" | `df.loc[df["B"].idxmin(), "A"]` |
| "B가 x 이상인 **비율(%)**" | `(df["B"] >= x).mean() * 100` |
| "B **상위 10%**의 C 평균" | `df[df["B"] >= df["B"].quantile(0.9)]["C"].mean()` |
| "A와 **상관 가장 높은** 특성" | `df.corr()["A"].drop("A").abs().idxmax()` |
| "**클래스별 개수**" | `df["A"].value_counts()` |
| "**결측치 개수**" | `df.isnull().sum()` |
| "**이상치 경계**" | `Q1 - 1.5*IQR`, `Q3 + 1.5*IQR` |

## 13-3. 마지막 수단

`print()`로 중간 결과를 보고 **눈으로 읽어서 상수를 직접 대입**해도 assert는 통과한다.
(부분점수용 최후수단이지만, 시간이 없으면 0점보다 낫다)

---

# 14. 자주 틀리는 것 모음

| ❌ 틀린 코드 | ✅ 고친 코드 | 이유 |
| --- | --- | --- |
| `df.shape()` | `df.shape` | 속성이라 괄호 없음 |
| `df.isnull()` 로 개수 | `df.isnull().sum()` | isnull은 bool 표를 돌려줌 |
| `df["a"].max()` 로 클래스 번호 | `df["a"].idxmax()` | max는 값, idxmax는 라벨 |
| `df.corr()["A"].idxmax()` | `.drop("A")` 먼저 | 자기 자신이 1.0으로 1등 |
| `df[(a>1) and (b<5)]` | `df[(a>1) & (b<5)]` | Series는 `&`, `\|`, `~` |
| `df[a>1 & b<5]` | `df[(a>1) & (b<5)]` | 연산자 우선순위 → 괄호 필수 |
| `df.qcut(y, 10)` | `pd.qcut(y, 10)` | qcut은 **모듈 함수** |
| `scaler.fit_transform(X_test)` | `scaler.transform(X_test)` | 데이터 누수 |
| `sns.pairplot(..., ax=ax[0])` | `sns.pairplot(...)` | Figure-level엔 `ax=` 없음 |
| `roc_auc_score(y_test, y_pred)` | `roc_auc_score(y_test, y_score)` | AUC는 **확률**이 필요 |
| `train_test_split` 반환을 `X_train, y_train, X_test, y_test`로 받기 | `X_train, X_test, y_train, y_test` | 순서 고정 |
| `LogisticRegression()` 그대로 | `LogisticRegression(max_iter=1000)` | ConvergenceWarning |
| test로 IQR 재계산 | train의 `iqr_bounds` 재사용 | 데이터 누수 |
| 스케일링 후 `X_train`이 ndarray | `pd.DataFrame(arr, columns=, index=)` | 컬럼명·인덱스 소실 |

---

# 15. import 치트시트

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

from sklearn.datasets           import load_wine, fetch_openml
from sklearn.model_selection    import train_test_split, cross_val_score, KFold
from sklearn.preprocessing      import StandardScaler, MinMaxScaler
from sklearn.impute             import SimpleImputer
from sklearn.linear_model       import LinearRegression, LogisticRegression
from sklearn.decomposition      import PCA
from sklearn.cluster            import KMeans
from sklearn.metrics import (
    root_mean_squared_error, mean_absolute_error, r2_score,      # 회귀
    accuracy_score, f1_score, confusion_matrix,                   # 분류
    classification_report, roc_curve, roc_auc_score,
)
```

| 모듈 | 들어있는 것 | 기억법 |
| --- | --- | --- |
| `sklearn.datasets` | 데이터 로드 | 데이터 |
| `sklearn.model_selection` | split / CV | **나누는** 것 |
| `sklearn.preprocessing` | Scaler / Encoder | **전처리** |
| `sklearn.impute` | SimpleImputer | **결측치** |
| `sklearn.linear_model` | Linear/Logistic Regression | **선형 모델** |
| `sklearn.decomposition` | PCA | **분해** = 차원축소 |
| `sklearn.cluster` | KMeans | **군집** |
| `sklearn.metrics` | 모든 평가지표 | **평가** |
