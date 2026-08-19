# 이미지 생성 파운데이션 모델 — GAN·디퓨전·CLIP 이론과 실습

> 📌 이 문서에서 `[개인 메모 · 시험범위 아님]`으로 표시된 부분은 필기자 본인의 개인적인 생각/질문이며, **강의 시험 범위에 포함되지 않는다.** 다른 대화에서 이 문서를 참고하더라도 해당 표시가 있는 내용은 시험 대비용 학습 내용으로 취급하지 말 것.

**오늘의 목차**
1. 이미지 파운데이션 모델이란
2. 파운데이션 모델이 강력해진 이유
3. 1세대 생성모델 — GAN
4. 2세대 생성모델 — 디퓨전 모델
5. 잠재 디퓨전 모델(LDM)
6. 멀티모달과 CLIP
7. 스테이블 디퓨전 종합
8. 지식 증류(Knowledge Distillation)
9. 실습 개요 — 4단계 워크플로우
10. 실습 1 — Stable Diffusion으로 이미지 생성
11. 실습 2 — CLIP으로 생성 이미지 평가
12. 실습 3 — ResNet-50과 CLIP 비교
13. 실습 4 — 생성 데이터로 ResNet-18 리니어 프로빙
14. 마무리

---

## 1. 이미지 파운데이션 모델이란

**파운데이션 모델**: 방대한 데이터로 사전학습된 하나의 모델을 다양한 용도로 재사용하는 것

- 파운데이션 모델은 **4억 개의 이미지-텍스트 쌍**을 대조 학습(contrastive learning)하여, 이미지 속 사물뿐 아니라 **화풍, 분위기, 동작** 등도 함께 학습함
- **기존 모델(전통적 분류기)**: 별도로 학습하지 않았다면 클래시파이만 가능 — 예: 사진을 보고 단순히 "여우"라고만 분류
- **파운데이션 모델**: 서로 다른 개념을 조합해서 이해할 수 있음 — 예: "우주에서 서핑하는 고양이" 사진을 "우주" + "서핑" + "고양이" 개념의 조합으로 분류 가능

---

## 2. 파운데이션 모델이 강력해진 이유

### ① 스케일의 규모

- 어마어마한 양의 데이터를 학습할 수 있게 됨
- 데이터가 많고 파라미터 수가 많아질수록 손실(loss)이 작아짐

### ② 자기지도학습 (Self-Supervised Learning)

- 레이블이 없는 데이터도, 데이터 자체의 상관관계를 통해 스스로 학습
- 이미지와 설명 텍스트가 서로 어울리는 짝인지 아닌지를 스스로 판단하며 학습
- 사람 라벨러가 사진을 보고 직접 라벨을 단 것이 아니라, **인터넷에 게시된 수많은 사진과 그 대체 텍스트(alt text)**를 그대로 사용

---

## 3. 1세대 생성모델 — GAN

- **2014년** 등장한 **적대적 생성 신경망(GAN)**
- 현세대 파운데이션 모델이 등장하기 전, 두 개의 신경망이 서로 경쟁하며 이미지를 생성

| 구성 요소 | 역할 | 비유 |
|---|---|---|
| **생성자(Generator)** | 이미지를 생성 | 위조범 |
| **판별자(Discriminator)** | 이미지의 진위를 가림 | 경찰 |

- 시간이 지날수록 생성자는 판별자를 더 잘 속이게 되고, **완벽한 위작을 만드는 것**을 목표로 학습하게 됨

### GAN의 동작 방식

- **입력**: 생성자가 임의로 생성하는 랜덤한 숫자 벡터 (보통 100차원 벡터)
- **생성**: 입력받은 벡터를 기반으로 이미지 생성

### 1세대 GAN의 특징

- 선명하고 사실적인 결과물
- 생성자가 이미지를 만드는 무작위 노이즈를 조금씩 바꾸면, 이미지도 자연스럽게 바뀜 → 노이즈를 조금씩 바꾸며 이미지를 의도대로 제어할 수 있는 가능성을 열었음 → 당시 학계에서 극찬받은 성과

### GAN의 한계 — 모드 붕괴(Mode Collapse)

> 혁신적이었지만, 경찰(판별자)이 너무 똑똑했다 — 생성자와 판별자 두 모델의 균형을 맞추기가 매우 어려웠고, 한쪽이 학습이 잘 되면 다른 한쪽이 제대로 학습되지 않는 문제가 발생했다.

- **모드 붕괴**: 학습이 진행될수록 생성자가 판별자를 속이기 쉬운 몇 가지 종류의 이미지만 반복적으로 생성하는 현상
- 예: 위조범이 0~9 숫자를 생성해야 하는데, 3과 8이 유독 "진짜" 판정을 잘 받는다면, 생성자는 3과 8 정도만 반복적으로 생성하게 됨 — 다양한 이미지가 다같이 좋아지길 원했는데 그렇게 되지 않는 문제

---

## 4. 2세대 생성모델 — 디퓨전 모델

- **2020년** 등장한 파운데이션 모델 이론
- 큰 흐름: **노이즈(형태를 완전히 잃은 이미지) → 추가된 노이즈를 예측/제거 → 선명한 이미지 생성**
- 학습 과정에서 특정 이미지가 "망가지는" 과정(노이즈가 더해지는 과정)을 학습하고, 이 내용을 기반으로 노이즈를 제거하는 능력을 갖춤 — 즉 "이 이미지에 어떤 노이즈가 추가됐을까"를 학습하고, 생성(예측) 시점에는 그 예측 능력을 이용해 노이즈를 걷어내는 방향으로 사용

> `[개인 메모 · 시험범위 아님]` 이거 왜 학습모드와 예측모드가 반대로 동작하는지, 어떻게 그런 구조가 되는지 자세히 설명해줄 것

**답변**

이 질문은 디퓨전 모델을 처음 배울 때 거의 누구나 걸리는 지점이다. 결론부터 말하면, "학습과 예측이 반대 방향으로 동작한다"는 인상은 사실 **두 가지 서로 다른 개념 — ①"이미지에 노이즈를 더하고 빼는 방향"과 ②"신경망이 실제로 계산하는 내용" — 을 하나로 섞어서 생기는 착시**다. 하나씩 풀어보자.

**① 순방향/역방향은 "데이터에 무슨 일이 일어나는가"를 말하는 것이지, "모델이 무엇을 계산하는가"를 말하는 게 아니다**

- **순방향 과정**은 학습 데이터를 만들기 위한 절차다. 우리가 가진 진짜 이미지 x₀에, 우리가 직접 정해둔 방식(노이즈 스케줄)으로 노이즈를 조금씩(수천 번에 걸쳐) 더해서 x_t를 만든다. 이 과정 자체에는 신경망이 전혀 관여하지 않는다 — 정해진 수식에 따라 기계적으로 노이즈를 섞는 것뿐이다. 중요한 건, 우리가 노이즈를 직접 더했기 때문에 "정확히 어떤 노이즈가 얼마나 더해졌는지(정답 ε)"를 항상 이미 알고 있다는 점이다.
- **역방향 과정**은 생성(이미지를 실제로 만들어내는) 시점에 쓰이는 절차다. 순수한 노이즈 x_T에서 시작해서, 노이즈를 조금씩 걷어내며 x₀ 방향으로 되돌아간다.

즉 "순방향=더하기", "역방향=빼기"는 **이미지에 어떤 처리가 가해지는지**에 대한 설명이지, 신경망이 학습 때와 생성 때 서로 상반된 두 가지 일을 한다는 뜻이 아니다.

**② 신경망이 실제로 하는 일은 학습 때나 생성 때나 완전히 동일하다 — "지금 입력에 노이즈가 얼마나 들어있는지 맞히기"**

- **학습 시**: 순방향 과정으로 만든 x_t와 시점 t를 신경망에 넣으면, 신경망은 "여기 섞여 있는 노이즈가 뭐였을까(예측값 ε_θ)"를 출력한다. 이 예측값을 우리가 실제로 넣었던 정답 노이즈 ε와 비교해 손실(MSE)을 계산하고, 손실을 줄이는 방향으로 가중치를 역전파로 업데이트한다. 즉 학습 시 신경망의 임무는 언제나 "노이즈 맞히기(추정)"이지 "이미지 생성"이 아니다.
- **생성(예측) 시**: 이때는 정답 이미지가 없다 — 오직 순수 노이즈 x_T만 있을 뿐이다. 이 x_T를, 학습을 마쳐 가중치가 고정된 같은 신경망에 넣어서 "여기 섞여 있는 노이즈가 뭘까"를 또 예측한다. **여기까지는 학습 때와 계산이 완전히 동일하다.** 다만 이번엔 그 예측값을 손실 계산이나 가중치 업데이트에 쓰는 대신, "예측된 노이즈를 x_T에서 조금 걷어내 좀 더 깨끗한 x_(T-1)을 만드는 데" 사용한다. 이 걷어내는 계산 한 번이 역방향 과정의 한 스텝이고, 이를 T번 반복하면 x₀(완성된 이미지)에 도달한다.

정리하면: **신경망이 계산하는 함수 자체는 학습 때와 생성 때 똑같이 "노이즈 예측"이다.** 달라지는 건 그 예측값을 가지고 무엇을 하느냐다 — 학습 때는 정답과 비교해 가중치를 고치는 데 쓰고, 생성 때는 이미지를 실제로 한 단계 덜 노이지하게 만드는 데 쓴다.

**③ 그렇다면 왜 굳이 "노이즈를 예측"하게 학습시키고, "이미지를 직접 그리라"고 학습시키지 않을까**

- 신경망에게 "순수 노이즈를 보고 완성된 이미지를 한 번에 그려내라"고 학습시키면, 입력·출력 간 관계가 너무 복잡하고 비약이 커서 매우 어렵고 불안정한 과제가 된다.
- 반면 "지금 이미지에 노이즈가 얼마나, 어떻게 섞여 있는지 맞혀라"는 훨씬 작고 안정적인 회귀(regression) 문제다. 아래 "디퓨전 모델의 특징"에서 다루는 "노이즈를 예측·제거한다는 목표가 안정적이고 학습 실패 확률을 줄인다"는 설명이 바로 이 이유 때문이다.
- 이렇게 "작은 단계 하나만 잘 맞히는" 모델을 만들어 두면, 생성할 때는 이 작은 단계를 수천 번 이어 붙여서 결과적으로 큰 변화(순수 노이즈 → 완성된 이미지)를 만들어낼 수 있다. 이것이 디퓨전 모델의 핵심 설계 철학이다.

### 순방향 과정 (Forward Process)

- 이미지에 아주 미세한 노이즈를 수천 번에 걸쳐 조금씩 더함
- 최종적으로 원본의 형태를 완전히 잃어버린 **가우시안 노이즈** 상태가 됨
- 가우시안 노이즈: 정규분포를 따르는, TV 정적 같은 노이즈

### 역방향 과정 (Reverse Process)

- 완전한 노이즈에서 시작해서, 노이즈 예측기가 예측한 노이즈를 살짝 걷어냄
- 이 과정에서 우리가 넣은 노이즈와 예측한 노이즈의 차이를 비교
- 이 차이를 줄이는 방향으로 가중치를 수정
- 위 과정을 정해진 횟수만큼 반복 — **컴퓨팅 비용이 많이 듦**

### 디퓨전 모델의 특징

- 노이즈를 예측하고 제거한다는 목표 자체가 안정적이라 **학습 실패 확률을 줄임**
- 단계마다 사용자가 작성한 텍스트를 참고할 수 있음
- 단계적 이미지 생성 방식 덕분에 **모드 붕괴 없이 다채로운 결과 생성**
- 모든 단계가 프롬프트를 참조할 수 있기 때문에 훌륭한 결과를 냄

### 디퓨전 모델의 한계

| 한계 | 설명 |
|---|---|
| **일관성 부족** | 매번 스타일이나 얼굴이 미묘하게 혹은 완전히 달라짐. "기억"이라는 개념이 없기 때문에 출발점(초기 노이즈)이 달라지면 결과물도 완전히 달라짐 |
| **문맥 이해 부족** | 텍스트 이해 능력이 부족해서 주제만 파악하는 수준 |
| **느린 속도와 비용** | 생성 과정이 순차적 노이즈 제거이므로 오래 걸리고 비용이 폭발함 — 결과 하나 받는 데 몇 분씩 걸림 |

> 강사님 의견: 요즘 이미지 생성 모델이 발전하면서 게임 업계가 위험해질 수 있고, 특히 3D 모델링 업계가 위협받을 수 있다는 시각을 제시함 (개인적 견해로 소개된 내용)

---

## 5. 잠재 디퓨전 모델(LDM)

디퓨전 모델의 느린 속도·높은 비용 문제를 개선하기 위해 등장.

### LDM 동작 방식

1. 인코더를 활용해 512×512×3 이미지를 **잠재 벡터**로 압축
2. 컨볼루션을 반복해서 특징을 뽑아냄
3. 잠재 벡터 공간에서 노이즈를 섞고 지우는 작업(디퓨전 과정 전체)을 수행
4. 디코더를 활용해 다시 512×512×3으로 복원

> ⚠️ **원문 수치 정정**: 원문 노트에는 압축 결과가 "64×64×3"이라고 되어 있었지만, 실제 Stable Diffusion 계열 LDM의 VAE 인코더는 채널 수를 3(RGB)이 아니라 **4**로 압축하는 것이 표준이다. 512×512 이미지를 공간 방향으로 1/8배 축소해 512÷8=64, 즉 가로·세로가 64가 되는 부분은 맞다. 하지만 채널 수 4는 축소 배율로 계산되는 값이 아니라 VAE를 설계할 때 정해두는 잠재 공간의 채널 수(하이퍼파라미터)이며, Stable Diffusion 1.x/2.x 계열에서는 4로 고정되어 있다. 즉 정확한 잠재 벡터 크기는 **64×64×4**.

- 핵심 아이디어: 픽셀 공간이 아니라 훨씬 작은 잠재 공간에서 디퓨전 연산을 수행하므로 계산량이 크게 줄어듦

---

## 6. 멀티모달과 CLIP

**멀티모달**: 텍스트, 이미지, 오디오, 비디오 등 서로 다른 형태의 데이터를 함께 이해하고 처리하는 기술 — AI도 인간처럼 세상을 입체적으로 이해하기 위한 접근

- 이전에도 많은 멀티모달 시도가 있었으나, CLIP 논문에서 어떤 아키텍처를 가져다 썼는지를 상세히 설명함
- **CLIP**: **2021년** OpenAI가 발표한 인공지능 모델
- 인터넷에 올라온 자연스러운 설명(대체 텍스트)으로 학습 진행
- **대조 학습(Contrastive Learning)** 기반 — 이미지와 텍스트를 나란히 두고 서로 맞는 쌍인지 비교하며 학습

### CLIP 동작 방식

1. 이미지 인코더와 텍스트 인코더가 각각 사진과 글을 벡터로 변환
2. 만들어진 모든 이미지 벡터와 텍스트 벡터를 각각 쌍으로 놓고, 정답 쌍이면 가깝게, 오답 쌍이면 멀게 설정
3. **코사인 유사도**로 거리 조절 — 정답 쌍(이미지-텍스트)의 벡터 방향은 비슷하게, 정답이 아닌 쌍은 서로 밀어냄
4. 두 인코더는 각각 **비전 트랜스포머(ViT)**, **텍스트 트랜스포머** 구조
5. 이 밀고 당기는 과정을 데이터 수만큼 반복하면, 관련 있는 내용끼리 모여 있는 잠재 공간이 만들어짐

---

## 7. 스테이블 디퓨전 종합

**스테이블 디퓨전**은 앞에서 다룬 요소(LDM, CLIP 등)를 모두 합친 모델.

| 한계 | 설명 |
|---|---|
| 추론 속도 | 순차적 디퓨전 과정으로 인해 속도 이슈 존재 |
| 의미론적 오류 | 복잡한 문장의 형용사와 명사를 혼동 |
| 구조적 결함 | 손가락 개수, 문자 등 세밀한 논리에서 오류 |
| 높은 하드웨어 성능 요구 | — |

---

## 8. 지식 증류 (Knowledge Distillation)

- 방대한 지식을 작고 가벼운 모델에게 효율적으로 전달하는 **모델 압축 기술**
- 결과만 전달하는 게 아니라, 문제를 해결하는 **사고방식 자체를 가르치는 것**에 가까움
- **티처(Teacher) 모델의 우도(likelihood)**를 **스튜던트(Student) 모델**이 학습함으로써, 적은 파라미터로도 정교한 판단 능력을 배움
- 효과: **경량화**, **속도 향상**, **저비용**

> 강의에서는 **SANA** 모델이 LDM(압축된 잠재 공간) + CLIP류의 멀티모달 이해 + 지식 증류 기법을 결합한 최신 사례로 짧게 언급됨 (성능이 우수하다고만 소개되었고, 구체적인 수치나 벤치마크는 다뤄지지 않음)

---

## 9. 실습 개요 — 4단계 워크플로우

이번 실습은 **이미지 파운데이션 모델의 활용과 비교**를 중심으로, Text-to-Image 생성 → CLIP 기반 이미지 평가 → CNN 기반 모델(ResNet) 비교 → 생성 데이터로 ResNet18 리니어 프로빙까지 전체 워크플로우를 경험하는 실습.

### 실습 목적 및 배경

- **파운데이션 모델 이해**: Stable Diffusion, CLIP, ResNet 등 다양한 사전학습 모델의 개념과 활용 방법을 익히고, 생성형·인식형 모델의 차이를 파악
- **멀티모달 융합 실습**: 텍스트와 이미지를 동시에 다루는 CLIP 모델로 생성 이미지의 의미적 적합성을 평가
- **전이 학습과 생성 데이터 활용**: Stable Diffusion으로 생성한 이미지를 ResNet18 모델 학습에 활용해, 생성 데이터의 가치를 탐구
- **모델 비교 분석 능력 향상**: CLIP과 전통 CNN의 분류 결과를 비교

### 실습으로 얻어가는 역량

- 프롬프트 엔지니어링 (효과적인 positive/negative prompt 작성)
- 멀티모달 평가 (CLIP 유사도 측정·해석, CLIP-ResNet 비교)
- CNN 활용 능력 (ResNet 계열 모델 불러오기, 전이학습, 리니어 프로빙 구현)
- 데이터 생성 및 확장 전략 (생성 데이터로 데이터 부족 문제 대응)

### 파운데이션 모델 재정의 (실습 노트북 기준)

대규모 데이터와 컴퓨팅 자원으로 사전학습된, 범용적인 인공지능 모델. 특정 태스크에 맞춘 모델이 아니라 다양한 분야로 전이(Transfer)하여 활용할 수 있도록 설계됨.

| 특징 | 설명 |
|---|---|
| 대규모 학습 데이터 | 수억~수십억 개의 이미지·텍스트·멀티모달 데이터 사용 |
| 범용성 | 추가 학습 없이도 여러 다운스트림 작업에 적용 가능 |
| 전이 학습 효율성 | 소량 데이터로도 fine-tuning 가능 |

| 분야 | 예시 |
|---|---|
| 언어 | GPT, BERT |
| 비전 | ViT, ResNet(사전학습 버전), CLIP |
| 멀티모달 | CLIP, BLIP |
| 생성형 | Stable Diffusion, DALL·E |

### 4대 파트

1. Stable Diffusion 모델로 컨셉 기반 이미지 생성 (Positive Prompt + Negative Prompt)
2. CLIP 모델로 생성 이미지와 사용자 정의 레이블 간 의미적 유사도 평가
3. ResNet-50으로 동일 이미지 분류 후 CLIP 결과와 비교
4. Stable Diffusion으로 생성한 합성 데이터셋으로 ResNet-18 전이 학습 (리니어 프로빙)

### 재현성을 위한 시드 고정

```python
import numpy as np
import random

torch.manual_seed(42)          # PyTorch CPU 연산 시드 고정
torch.cuda.manual_seed(42)     # PyTorch GPU 연산 시드 고정
np.random.seed(42)             # NumPy 시드 고정
random.seed(42)                # Python 내장 random 시드 고정

torch.backends.cudnn.deterministic = True  # 결정론적 알고리즘 사용 (재현성)
torch.backends.cudnn.benchmark = False     # 벤치마크 기능 비활성화 (재현성)
```

---

## 10. 실습 1 — Stable Diffusion으로 이미지 생성

**Stable Diffusion**: 텍스트 설명(프롬프트)을 입력받아 이미지를 생성하는 Text-to-Image 생성형 파운데이션 모델

**이미지 생성 절차**: 노이즈 가득한 랜덤 이미지에서 시작 → 텍스트 조건에 맞게 점진적으로 노이즈를 제거(diffusion process) → 최종적으로 프롬프트와 일치하는 이미지 생성

- **Positive Prompt**: 원하는 이미지의 핵심 컨셉을 상세히 기술 (특정 화풍·분위기 키워드 포함 가능, 한글보다 영어 작성이 안정적)
- **Negative Prompt**: 이미지에 나타나지 않았으면 하는 요소들을 기술 (예: "저품질, 흐릿함, 왜곡됨, 텍스트")

```python
from diffusers import StableDiffusionPipeline

# HuggingFace에서 Stable Diffusion 모델 불러오기
model_id = "runwayml/stable-diffusion-v1-5"   # 문제가 있으면 "sd-legacy/stable-diffusion-v1-5"로 대체

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

positive_prompt = "A watercolor painting of a red fox sitting on a forest floor, vibrant autumn colors"
negative_prompt = "low quality, blurry, distorted, text"

result = pipe(
    positive_prompt,
    negative_prompt=negative_prompt,
    guidance_scale=8.5,        # 프롬프트를 얼마나 강하게 따를지 (높을수록 충실하지만, 너무 높으면 부자연스러워짐)
    num_inference_steps=50,    # 노이즈 제거 단계 수 (많을수록 품질↑, 생성 시간↑)
    num_images_per_prompt=4,   # 한 번에 생성할 이미지 개수
)
images = result.images

for i, img in enumerate(images):
    img.save(f"generated_image_{i}.png")
    display(img)
```

> 📌 `torch_dtype=torch.float16`: 모델 가중치를 16비트 부동소수점으로 로드해 메모리 사용량을 줄이고 계산 속도를 높임 (GPU에서 특히 효과적)

---

## 11. 실습 2 — CLIP으로 생성 이미지 평가

생성된 이미지가 의도한 컨셉과 부합하는지 CLIP 모델로 평가. CLIP은 이미지와 텍스트를 같은 임베딩 공간에 투영해 유사도를 계산.

- 사용 모델: OpenAI **CLIP (ViT-B/32)**, HuggingFace `CLIPProcessor`로 전처리
- 방법: 정답 레이블 1개 + 혼동 가능한 오답 레이블 여러 개를 준비 → 이미지와 각 텍스트 간 유사도(내적 기반) 계산 → 가장 높은 점수가 모델의 예측 레이블

```python
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

image = Image.open("generated_image_0.png")

labels = [
    "a watercolor painting of a fox",   # 정답 (의도한 레이블)
    "a watercolor painting of a dog",   # 오답 1 — 동물만 다름
    "an oil painting of a fox",         # 오답 2 — 화풍만 다름
    "a photo of a fox"                  # 오답 3 — 스타일이 사진으로 다름
]

processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)

inputs = processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)

with torch.no_grad():                              # 추론만 수행, 가중치 업데이트 없음
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image     # 이미지 1장 vs 각 텍스트 레이블의 유사도 점수
    probs = logits_per_image.softmax(dim=1)          # 확률값으로 변환 (합=1)

best_idx = logits_per_image.argmax(dim=1).item()
print(f"CLIP 예측 결과: '{labels[best_idx]}' 라벨이 가장 타당하다고 예측되었습니다.")
```

> 이런 방식으로 CLIP을 활용하면 별도 학습 없이도 이미지가 어떤 텍스트 설명과 가장 어울리는지 알 수 있어, 생성된 이미지의 내용이 의도와 맞는지 평가할 수 있음

---

## 12. 실습 3 — ResNet-50과 CLIP 비교

동일 이미지를 전통적인 CNN 분류 모델인 **ResNet-50**으로 분류하고, CLIP의 결과와 비교.

| 구분 | ResNet-50 | CLIP |
|---|---|---|
| 분류 범주 | ImageNet 사전학습, 고정된 **1000개** 카테고리 중 선택 | 임의의 텍스트 라벨과 자유롭게 비교 |
| 화풍/문맥 고려 | 불가능 | 가능 (텍스트에 스타일·상황을 반영해 평가) |
| 예시 결과 (수채화 여우 그림) | "kit fox", "red fox" 등 여우 종류로만 분류 (화풍 정보 없음) | "수채화 여우 그림"임을 스타일까지 파악 |

```python
from torchvision import transforms, models

resnet50 = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
resnet50 = resnet50.to(device).eval()   # 평가 모드 — 드롭아웃/배치정규화 비활성화, 일관된 예측 보장

imagenet_classes = models.ResNet50_Weights.IMAGENET1K_V2.meta["categories"]

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),                       # ResNet-50 입력 크기에 맞춤
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],      # ImageNet 표준 평균
                         std=[0.229, 0.224, 0.225])       # ImageNet 표준 표준편차
])
img_tensor = preprocess(image).unsqueeze(0).to(device)    # 배치 차원 추가

with torch.no_grad():
    output = resnet50(img_tensor)
probs = torch.nn.functional.softmax(output, dim=1)[0]

top5_prob, top5_idx = probs.topk(5)   # 확률 상위 5개 클래스
```

> CLIP과 전통 CNN의 차이: CLIP은 유연한 텍스트 설명으로 이미지의 다양한 측면(내용+스타일)을 평가할 수 있는 반면, ResNet 같은 CNN은 학습된 범주 내에서만 분류할 수 있음. ResNet은 화풍이 특이하면 오분류할 수도 있지만, 대체로 주된 객체를 맞추는 데는 집중함

---

## 13. 실습 4 — 생성 데이터로 ResNet-18 리니어 프로빙

Stable Diffusion으로 생성한 합성 이미지 데이터셋을 활용해 ResNet-18을 전이학습(리니어 프로빙). 챕터 3-1 CNN 실습(전이학습 파일)과 연계된 내용.

### 데이터셋 구성

두 클래스(fox, dog) 각각에 대해 프롬프트로 이미지를 여러 장 생성 (실습에서는 클래스당 예시로 5장). 테스트 데이터는 앞서 생성했던 여우 그림을 활용.

```python
import os
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

classes = {
    "fox": "a watercolor painting of a red fox sitting on a forest floor, detailed, vibrant",
    "dog": "small adorable Maltipoo dog with distinctive black-and-white fluffy fur, round eyes"
}
neg_prompt = "low quality, blurry, distorted, text"

os.makedirs("data/train/fox", exist_ok=True)
os.makedirs("data/train/dog", exist_ok=True)

for cls, prompt in classes.items():
    result = pipe(
        prompt,
        negative_prompt=neg_prompt,
        guidance_scale=7.5,          # 텍스트 조건 준수 정도
        num_inference_steps=50,      # 확산 단계 수 (품질-속도 트레이드오프)
        num_images_per_prompt=1,     # 한 번에 생성할 이미지 수
    )
    for i, img in enumerate(result.images):
        img.save(f"data/train/{cls}/{cls}_{i}.png")
```

> ⚠️ 원본 실습 노트북 코드에는 `number_inference_steps`라는 오타가 있었음 — diffusers 라이브러리의 실제 파라미터명은 `num_inference_steps`이므로, 오타 그대로 실행하면 이 값이 무시되고 라이브러리 기본 스텝 수로 동작하게 됨. 위 코드는 정정된 버전.

같은 방식으로 `data/test/fox`, `data/test/dog`에 테스트용 이미지도 생성.

```python
# 학습용 transform — 데이터 증강 포함
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
train_dataset = ImageFolder("data/train", transform=train_transforms)
train_loader = DataLoader(train_dataset, batch_size=5, shuffle=True)

# 테스트용 transform — 증강 없이 원본 그대로 (공정한 평가를 위함)
test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
test_dataset = ImageFolder("data/test", transform=test_transforms)
test_loader = DataLoader(test_dataset, batch_size=5, shuffle=True)
```

> `ImageFolder`는 폴더 구조를 기반으로 데이터셋을 자동 구성함 — `data/train/fox`, `data/train/dog` 폴더의 이미지를 각각 `fox`, `dog` 클래스로 자동 인식

### 모델 준비 — 리니어 프로빙

```python
import torch.nn as nn
import torch.optim as optim

model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# 기존 가중치 고정 (Freeze) — 특징 추출부는 그대로 유지
for param in model.parameters():
    param.requires_grad = False

# 새로운 출력층으로 교체 — 우리 클래스 개수(fox, dog → 2개)에 맞춤
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(train_dataset.classes))
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.fc.parameters(), lr=0.001, momentum=0.9)  # 새 fc층 파라미터만 학습
```

### 학습 루프 (3 epoch)

```python
model.train()
num_epochs = 3

for epoch in range(num_epochs):
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()               # ① 기울기 초기화
        outputs = model(inputs)             # ② 순전파
        loss = criterion(outputs, labels)   # ③ 손실 계산
        loss.backward()                     # ④ 역전파
        optimizer.step()                    # ⑤ 가중치 업데이트

        running_loss += loss.item() * inputs.size(0)

    epoch_loss = running_loss / len(train_dataset)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}")
```

> 데이터가 적고 단순하기 때문에, 모든 epoch이 끝난 후 모델이 합성 데이터에 꽤 낮은 loss로 금방 수렴함

### 평가 및 역정규화

```python
mean = [0.485, 0.456, 0.406]
std  = [0.229, 0.224, 0.225]

def denormalize(img_tensor, mean=mean, std=std):
    """정규화된 이미지를 다시 [0,1] 범위로 되돌려 사람이 볼 수 있게 변환"""
    mean = torch.tensor(mean, device=img_tensor.device).view(-1, 1, 1)
    std = torch.tensor(std, device=img_tensor.device).view(-1, 1, 1)
    img = img_tensor * std + mean
    return img.clamp(0, 1)

model.eval()
correct, total = 0, 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        predicted = outputs.argmax(dim=1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"테스트 데이터셋에서 모델 정확도: {100 * correct / total:.2f}%")
```

- **리니어 프로빙**의 핵심: 컨볼루션(특징 추출부)은 얼리고, 새로 만든 마지막 출력층만 학습 → 학습할 파라미터 수가 크게 줄어 작은 데이터셋에도 빠르게 학습 가능
- 실제 현업에서는 이 방법을 데이터 증강이나 새로운 클래스 추가에 활용할 수 있음

---

## 14. 마무리

이번 실습에서는 텍스트-투-이미지 생성부터, 생성된 이미지를 CLIP으로 평가하고, 기존 CNN 모델(ResNet)과 비교해보았으며, 나아가 생성 데이터로 모델을 전이 학습(리니어 프로빙)하는 일련의 과정을 구현했다. 이러한 흐름을 통해 딥러닝 모델의 **생성 능력**과 **인식 능력**을 모두 체험하고, 각 기법의 특징을 이해하는 것이 이번 실습의 목표.