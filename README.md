## 쿠팡 웹사이트 QA 프로젝트입니다.

해당 프로젝트는 

엘리스 QA 트랙 1기 첫 개인 프로젝트입니다.

쿠팡 웹사이트의 각 기능들을 점검합니다.

<https://www.coupang.com/>

## 설치 방법

1. 파이썬과 pip 라이브러리가 필요합니다.

2. 아래 명령어 실행합니다.

- `$ python -m venv testvenv`
- `$ pip install -r requirements.txt`

3. 파이썬 3.13 버전으로 제작했습니다.

+ 낮은 버전으로는 동작하지 않을 수 있습니다.

## 사용법
1. 가상환경 활성화

    - `$ .testvenv\Scripts\activate`
    
        (Windows (CMD/PowerShell))
    
    - `$ source .venv/bin/activate`

        (Mac/Linux (bash/zsh))

2. 루트 디렉토리에 '.env' 파일 추가
    ``` md
        EMAIL = 본인쿠팡이메일주소
        PASSWORD = 본인쿠팡비밀번호
    ```

    - `$ pytest tests`
