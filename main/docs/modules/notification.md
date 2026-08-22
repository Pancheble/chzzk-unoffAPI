# Notification

알림 API로 개인 알림 소켓의 접속 URL을 발급받고 알림 이벤트를 수신할 수 있습니다.\
소켓 URL 발급에는 로그인이 필요하며, 이벤트 세션 URL 발급에는 채널 권한이 필요합니다.

| | |
|---|---|
| Base URL | `wss://ssio{N}.nchat.naver.com/socket.io/` · `https://api.chzzk.naver.com` |
| 응답 봉투 | A형. `code == 200` ([참조](../core/conventions.md#응답-봉투)) |
| 관련 문서 | [Chat](chat.md) · [Manage](manage.md) |

호스트명이 `nchat` 이라 채팅으로 오인하기 쉽습니다.
관측된 WebSocket 프레임 8개는 모두 핸드셰이크(`0{sid...}`, `40`)와 하트비트(`2`, `3`)였으며 채팅 페이로드는 없었습니다.
앱 식별자도 `nng@glive` 입니다. 개인 알림 채널입니다.
실시간 채팅은 [Chat](chat.md)에 있습니다.

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 · 인증 필요 | **GET /service/v1/personal/session-url** | [알림 소켓 URL 발급](#알림-소켓-url-발급) |
| 스키마 미상 · 인증 필요 | **GET /manage/v1/alerts/{sessionIOChannelId}/session-url** | [이벤트 세션 URL 발급](#이벤트-세션-url-발급) |
| 실측 | **WSS ssio{N}.nchat.naver.com/socket.io/** | [Socket.IO 연결](#socketio-연결) |
| 실측 · 인증 필요 | **GET /v1/notification/new** | [새 알림 여부 조회](#새-알림-여부-조회) |

***

## 알림 소켓 URL 발급

개인 알림 소켓에 접속할 URL을 발급받을 수 있습니다.\
이 API를 호출하려면 로그인이 필요합니다.

경로가 `personal` 이라 개인 데이터 조회로 보이지만 실제로는 소켓 URL 발급 API입니다.
개인 설정 데이터는 [별도 엔드포인트](user.md#개인-설정-데이터-조회)입니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/personal/session-url** | 알림 소켓 URL 발급 |

요청 파라미터가 없습니다.

**Response Body**

| Field | Type | Description |
|---|---|---|
| result.url | String | 접속 URL. `auth` 토큰 포함. 민감 정보 |
| result.app | String | 앱 식별자. `nng@glive` |

```json
{
  "content": {
    "result": {
      "url": "https://ssio24.nchat.naver.com:443?auth=<token>",
      "app": "nng@glive"
    }
  }
}
```

URL 전체를 서버가 반환하므로 서버 번호를 계산할 필요가 없습니다.
관측된 번호는 `ssio07`, `ssio09`, `ssio24`, `ssio25` 이며 임의로 배정됩니다.

`auth` 토큰으로 개인 알림을 수신할 수 있습니다. 공유하지 않으며 문서에 옮길 때는 플레이스홀더로 치환합니다.

***

## Socket.IO 연결

```
wss://ssio{N}.nchat.naver.com/socket.io/?auth=<token>&EIO=3&transport=websocket
```

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| auth | String | * | [발급받은 URL](#알림-소켓-url-발급)에서 추출한 토큰 |
| EIO | Int | * | `3`. Engine.IO v3 |
| transport | String | * | `websocket` |

### 클라이언트 버전

`socket.io-client` v4는 기본값이 `EIO=4` 이므로 그대로 접속하면 실패합니다.

| 방법 | 내용 |
|---|---|
| 클라이언트 버전 맞추기 | `socket.io-client@2.x` 사용 |
| 프로토콜 강제 | 옵션으로 `EIO=3` 지정 |

```js
// socket.io-client v2
const io = require('socket.io-client');
const socket = io('https://ssio24.nchat.naver.com', {
  query: { auth: '<token>' },
  transports: ['websocket'],
});
```

### 관측된 프레임

| 프레임 | 의미 |
|---|---|
| `0{"sid":"...","upgrades":[],"pingInterval":25000,"pingTimeout":60000}` | Engine.IO 핸드셰이크 |
| `40` | Socket.IO 연결 |
| `2` / `3` | ping / pong |

이벤트 페이로드는 관측되지 않았습니다. 알림이 실제로 발생해야 확인할 수 있습니다.

***

## 이벤트 세션 URL 발급

후원, 구독 등 개별 이벤트 세션의 접속 URL을 발급받을 수 있습니다.\
이 API를 호출하려면 채널 권한이 필요합니다.

| HTTP Request | Description |
|---|---|
| **GET /manage/v1/alerts/{sessionIOChannelId}/session-url** | 이벤트 세션 URL 발급 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| sessionIOChannelId | String | * | `{type}@{...}` 형식. [아래 9종](#이벤트-세션-9종) |

**Response Body**

캡처 시점에 `url` 과 `app` 이 비어 있었습니다. 실제 알림 소켓 연결이 발생하지 않아서로 추정됩니다.

| 미확인 항목 | 확인 방법 |
|---|---|
| url · app 의 실제 값 | 후원이나 구독이 실제 발생한 상태에서 재캡처 |
| 각 채널의 이벤트 페이로드 구조 | 9종 전량 미확인. 위와 같음 |

후원 알림 오버레이나 실시간 구독 감지를 구현할 때 사용하는 경로입니다.
현재는 경로만 확인됐고 페이로드 구조는 확인되지 않았습니다.

### 이벤트 세션 9종

`GET /manage/v1/channels/{channelId}/streaming-info` 응답에서 확인할 수 있습니다. ([스트리밍 정보 조회 참조](manage.md#스트리밍-정보-조회))

| sessionIOChannelId | 용도 |
|---|---|
| donation@… | 후원 |
| subscription@… | 구독 |
| gift@… | 선물 |
| partydonation@… | 파티 후원 |
| mission@… | 미션 후원 |
| newsfeed@… | 뉴스피드 |
| video@… | 영상 |
| studio@… | 스튜디오 |
| streamershop@… | 스트리머 상점 |

***

## 새 알림 여부 조회

읽지 않은 알림의 존재 여부를 조회할 수 있습니다.\
소켓을 사용하지 않고 폴링으로 확인할 때 사용합니다.\
이 API를 호출하려면 로그인이 필요합니다.

| HTTP Request | Description |
|---|---|
| **GET https://comm-api.game.naver.com/nng_main/v1/notification/new** | 새 알림 여부 조회 |

요청 파라미터가 없습니다.

***

## 관련 문서

[Chat](chat.md) · [Manage](manage.md) · [User](user.md) · [Commerce](commerce.md) · [엔드포인트 목록](../reference/endpoints.md)
