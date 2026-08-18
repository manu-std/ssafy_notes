# 🌐 원격 저장소 (Remote Repository)

## 1. 원격 저장소란?

내 컴퓨터(로컬)가 아닌 **인터넷 서버에 있는 저장소**. 협업과 백업의 중심이 된다.

대표적인 호스팅 서비스: **GitHub · GitLab · Bitbucket**

기본 흐름은 두 가지다.

- **로컬에서 시작** → GitHub에 레포 생성 → 로컬과 원격을 연결해서 올리기(push)
- **GitHub에서 시작** → 레포를 **clone**해서 로컬로 받아오기

---

## 2. 로컬 ↔ 원격 연결하기

GitHub에서 레포를 만든 뒤, 로컬 저장소에 그 원격 주소를 **등록**한다. (파일이 바로 연결·동기화되는 게 아니라 "주소를 등록"하는 것 → 실제 반영은 push/pull로 싱크를 맞춰야 함)

```bash
git remote add origin <원격_저장소_주소>
```

### `origin`은 뭘까?

- 원격 저장소에 붙이는 **별칭(이름)**일 뿐, 로컬 입장에서 이름 자체는 중요하지 않다.
- **관습적으로 첫 번째로 등록하는 원격을 `origin`이라고 부른다.**
- 즉, 이름만 다르게 하면 **여러 원격 저장소에 올릴 수도 있다.**

---

## 3. `git remote` 명령어

```bash
git remote -v                 # 등록된 원격 목록 + 주소 확인
git remote add origin <주소>   # 원격 등록
git remote rm <원격이름>        # 원격 등록 삭제
```

---

## 4. Push — 원격에 올리기

push는 **파일이 아니라 "커밋(변경 이력)"을 업로드**하는 것이다. 이미 올라간 것 외에 **변경된 커밋만** 올라간다.

```bash
git push -u origin master
```

- `-u`(= `--set-upstream`)는 "앞으로 이 브랜치는 `origin master`에 push한다"고 **기본 목적지를 지정**하는 옵션.
- 한 번 `-u`로 지정해두면, 이후에는 **`git push`만 입력**해도 된다.

```bash
git push          # 처음에 -u로 지정해뒀다면 이렇게만 해도 OK
```

> 브랜치 이름은 환경에 따라 `master` 또는 `main`. 본인 저장소에 맞게 사용.

---

## 5. Pull vs Clone — 받아오기

| 구분 | 하는 일 | 언제 |
|------|---------|------|
| **clone** | 원격 저장소 **전체를 통째로 복제**해 새로 다운로드 | 새 팀원이 프로젝트를 **처음** 받아올 때 |
| **pull** | 원격의 **변경된 부분(커밋)만** 받아와 갱신 | 이미 저장소가 있고, **최신 내용으로 업데이트**할 때 |

```bash
git clone <원격_저장소_주소>    # 처음 복제
git pull origin master        # 변경사항 받아오기
```

---

## 6. 명령어 한눈에 보기

```bash
git remote add origin <주소>   # 원격 등록
git remote -v                 # 원격 확인
git remote rm origin          # 원격 삭제
git push -u origin master     # 첫 push (기본 목적지 지정)
git push                      # 이후 push
git pull origin master        # 변경사항 받기
git clone <주소>               # 전체 복제
```

---

## 7. `.gitignore`

### 목적

Git이 **추적(관리)하지 않을 파일**을 지정하는 파일. 로그, 빌드 결과물, 비밀번호·API 키 등 올리면 안 되는 것들을 제외한다.

```gitignore
*.txt          # 모든 txt 파일 제외
node_modules/  # 폴더 통째로 제외
.env           # 환경변수 파일 제외
```

### 주의사항

- **프로젝트 처음에 세팅**하는 것이 좋다.
- 이미 **버전 관리(추적)되고 있는 파일**은 나중에 `.gitignore`에 추가해도 **적용되지 않는다.** 이 경우 Git 캐시에서 먼저 빼줘야 한다.

```bash
git rm --cached <파일명>   # 추적만 해제 (실제 파일은 유지)
```

> 💡 [gitignore.io](https://www.toptal.com/developers/gitignore) 에서 언어·환경별 `.gitignore` 템플릿을 자동 생성할 수 있다.