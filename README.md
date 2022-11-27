# 취소표가 필요해!

> 취소표라도 간절한 당신에게 기차표를 구해드립니다

**취소표가 필요해!**는 원하는 시간대의 코레일 기차표를 대신 예매해주는
서비스입니다. 원하는 시간대의 표가 매진되었을 때 취소표를 누구보다 빠르게 발견해
예매해드립니다.

## :cog: 내 서버에 올리기

**취소표가 필요해!**를 자신의 서버에 올려 사용하고 싶으시다면 아래 설명을
따라주세요.

### 0. 프로젝트 클론

```bash
git clone https://github.com/gim-hangil/cancel4me
```

### 1. 프론트엔드 설치

```bash
cd web
npm install
npm build
```

### 2. 백엔드 설치

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. 실행

```bash
cd web
npm install -g serve
serve build
```

```bash
cd server
python main.py
```

## :sparkles: 기여하기

오류나 기능에 대한 제보는 [이쪽](/issues)으로 부탁드립니다!

## :pencil2: 라이선스

[MIT 라이선스](/blob/main/LICENSE)를 따릅니다.

상업적/개인적 이용, 자유로운 수정 및 배포가 가능합니다. 이 소프트웨어를 사용함에
따른 어떠한 손해도 책임지지 않습니다. 세부 사항은 라이선스 문서를 참고해주세요!
