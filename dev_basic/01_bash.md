## Bash (Bourne Again SHell) 기본 명령어 정리

Bash는 리눅스와 macOS 등 유닉스 계열 운영체제에서 가장 기본적으로 사용되는 명령어 인터프리터이자 쉘 스크립트 언어입니다.

### 핵심 기본 명령어 모음

| 명령어 | 설명 | 사용 예시 |
| :--- | :--- | :--- |
| `pwd` | 현재 작업 중인 디렉토리의 절대 경로를 출력합니다. | `pwd` |
| `touch` | 새 파일을 만듭니다. | `touch 파일명` |
| `start` | 파일을 엽니다. (윈도우? 깃배시 전용/ 맥은 open) | `start` |
| `ls` | 현재 디렉토리 내의 파일 및 폴더 목록을 출력합니다. | `ls -al` (숨김 파일 포함 상세 정보 표시) |
| `cd` | 원하는 디렉토리로 이동합니다. (Change Directory) | `cd /var/log` 또는 `cd ..` (상위 디렉토리 이동) |
| `mkdir` | 새로운 디렉토리(폴더)를 생성합니다. | `mkdir new_folder` |
| `rm` | 파일 또는 디렉토리를 삭제합니다. | `rm file.txt` 또는 `rm -rf folder_name` (폴더 강제 삭제) |
| `cp` | 파일 또는 디렉토리를 복사합니다. | `cp file1.txt file2.txt` |
| `mv` | 파일이나 디렉토리를 이동시키거나 이름을 변경합니다. | `mv old_name.txt new_name.txt` |
| `cat` | 파일의 전체 내용을 터미널 화면에 그대로 출력합니다. | `cat config.txt` |
| `clear` | 터미널 화면에 표시된 이전 입력과 출력들을 모두 깨끗이 지웁니다. | `clear` |