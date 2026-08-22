# 필수 요청 헤더

치지직 API는 웹 클라이언트가 붙이는 커스텀 헤더를 요구합니다.\
이 헤더가 없으면 상당수의 엔드포인트가 실패합니다.\
공개 라이브러리 문서에는 대부분 기재되어 있지 않은 부분입니다.

| | |
|---|---|
| 적용 범위 | 모든 HTTP 요청 |
| 필수 커스텀 헤더 | `front-client-platform-type` · `front-client-product-type` · `deviceId` |
| 관련 문서 | [Base URL](base-urls.md) · [공통 규칙](conventions.md) · [인증](auth.md) |

```http
Accept: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...
Origin: https://chzzk.naver.com
Referer: https://chzzk.naver.com/
front-client-platform-type: PC
front-client-product-type: web
deviceId: <UUID v4. 클라이언트가 생성하여 재사용>
```

***

## 커스텀 헤더

| Header | required | Value | Description |
|---|---|---|---|
| front-client-platform-type | * | `PC`. `MOBILE` 은 미확인 | 플랫폼 구분 |
| front-client-product-type | * | `web`. `app` 은 미확인 | 제품 구분 |
| deviceId | * | UUID v4 | 클라이언트가 생성하는 기기 식별자. 서버 발급이 아님 |
| scene | optional | 숫자 (25, 51, 73 등) | 화면 식별자. 통계용이며 생략해도 동작 |

### deviceId

서버가 발급하는 값이 아니라 클라이언트가 생성하는 값입니다.
웹 클라이언트는 UUID v4를 만들어 localStorage에 저장하고 계속 재사용합니다.

```python
import uuid
DEVICE_ID = str(uuid.uuid4())   # 한 번 생성하여 저장 후 재사용
```

요청마다 새로 생성하면 서버에서는 새 기기가 계속 접속하는 것으로 관측됩니다. 한 번 생성한 값을 고정하여 사용합니다.

### scene

생략할 수 있습니다. 웹 클라이언트가 화면별 통계를 위해 붙이는 값이며 조회 결과에 영향을 주지 않습니다.

***

## CORS 프리플라이트

커스텀 헤더 때문에 브라우저에서 호출하면 본 요청 전에 `OPTIONS` 요청이 먼저 발생합니다.

서버 사이드에서 호출하는 경우 프리플라이트가 발생하지 않으므로 본 요청만 보내면 됩니다.
캡처한 HAR에 `OPTIONS` 가 다수 보이는 것은 이 때문이며, 실제 조회는 그 뒤의 `GET` 요청입니다.

***

## 인증이 필요한 요청

쿠키를 추가로 전달합니다. ([인증 참조](auth.md))

```http
Cookie: NID_AUT=<value>; NID_SES=<value>
```

***

## 관련 문서

[Base URL](base-urls.md) · [공통 규칙](conventions.md) · [인증](auth.md)
