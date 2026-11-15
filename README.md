# URL-Shortener

Flask로 구현한 URL 단축 프로젝트입니다. 원본 URL과 단축 키를 데이터베이스에 저장합니다.
현재 저장소의 구현 내용을 정리하며, 배포 또는 서비스 운영 여부를 의미하지 않습니다.

## 구현 기능
- 영문 대소문자와 숫자로 임의의 6자리 키를 생성하고 DB에서 중복을 확인합니다.
- 선택적으로 사용자 지정 키를 받으며, 이미 사용 중인 키는 오류로 처리합니다.
- 단축 링크 생성 후 결과 화면으로 이동하고, 단축 키로 원본 URL에 리다이렉트합니다.
- 원본 URL 조회 API와 URL 입력, 커스텀 키 입력, 결과 표시 템플릿을 제공합니다.
- `urls` 테이블에 ID, 원본 URL(최대 2,000자), 고유 단축 키(최대 30자)를 저장합니다.

## 기술 구성
- Python 3.10.12를 사용하도록 `.python-version`에 지정되어 있습니다.
- `requirement.txt`에 Flask 3.1.0, Flask-SQLAlchemy 3.1.1, PyMySQL 1.1.1, Flask-Cors 5.0.0 등이 명시되어 있습니다.
- Jinja 템플릿과 정적 JavaScript를 사용하며 화면에서 Tailwind CSS CDN을 불러옵니다.

## 프로젝트 구조
- `URLShortener/__init__.py`: 앱 생성, 설정 선택, 블루프린트 등록, 테이블 생성 코드입니다.
- `URLShortener/main.py`, `redirect.py`: 단축·조회 API와 리다이렉트 라우트입니다.
- `URLShortener/models.py`, `db.py`: URL 모델과 SQLAlchemy 초기화 코드입니다.
- `URLShortener/templates/`, `static/`: 화면 템플릿과 정적 파일입니다.
- `config.py`, `run.py`, `log/debug_print.py`: 환경 설정, 실행 진입점, 디버그 출력 코드입니다.

## 로컬 실행
1. Python 3.10.12 환경에서 저장소 루트로 이동합니다.
2. `pip install -r requirement.txt`로 의존성을 설치합니다.
3. 앱이 `dotenv`를 import하지만 의존성 목록에는 없으므로 `pip install python-dotenv`도 실행합니다.
4. `config.py`의 빈 `SQLALCHEMY_DATABASE_URI`를 사용 가능한 DB 접속 URI로 설정합니다. 환경 변수만 지정해도 자동 반영되는 코드는 없습니다.
5. `export FLASK_ENV=development`로 설정 클래스를 명시적으로 선택합니다.
6. `python run.py`로 실행하고 `http://localhost:5000`에 접속합니다.

`FLASK_ENV`가 `development`, `testing`, `production`이면 각각 DevelopmentConfig, TestingConfig, ProductionConfig를 불러옵니다.
미설정 시에는 안내 출력만 하고 설정 클래스를 적용하지 않으므로 값을 명시해야 합니다.
DB가 준비되면 앱 초기화 시 `db.create_all()`을 호출합니다. 실행 스크립트는 debug 모드를 켭니다.
프런트엔드의 API 주소 설정도 로컬 환경에 맞는지 확인해야 합니다.

## 엔드포인트
아래 라우트는 모두 GET 방식이며, API 입력은 JSON 본문이 아닌 쿼리 매개변수입니다.
- `GET /`: URL 입력 화면을 반환합니다. 매개변수는 없습니다.
- `GET /api/shorten?url=...&custom_key=...`: `url`은 필수, `custom_key`는 선택입니다. 저장 후 결과 화면으로 리다이렉트합니다.
- `GET /api/ready?short_url=...`: 필수 `short_url`을 결과 템플릿에 표시합니다.
- `GET /api/unshorten?url=...`: 필수 `url`의 마지막 경로 조각으로 조회하며 `{"unshortened": 원본 URL}`을 반환합니다. 미등록 키는 404입니다.
- `GET /<short_key>`: 경로의 단축 키로 원본 URL에 이동하며, 키가 없으면 설정된 오류 페이지 주소로 이동합니다.

## 알려진 한계 / TODO
- 키 생성 코드에는 해시 기반 생성 방식으로 변경하는 TODO가 남아 있습니다. 현재는 임의 생성 후 중복 조회 방식입니다.
- 리다이렉트 코드에는 URL 스킴 보정 로직을 더 견고하게 만드는 TODO가 남아 있습니다. 현재는 http/https가 없으면 http를 붙입니다.
