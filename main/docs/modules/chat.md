# Chat

채팅 API로 실시간 채팅 메시지를 수신할 수 있습니다.\
WebSocket 접속에 로그인 쿠키로 발급받은 액세스 토큰이 필요합니다.\
이 문서는 읽기 전용 API만 다루므로 채팅 송신(`cmd 3101`)은 수록하지 않았습니다.

| | |
|---|---|
| Base URL | `wss://kr-ss{N}.chat.naver.com/chat` · `https://comm-api.game.naver.com/nng_main` |
| 응답 봉투 | HTTP는 A형. WebSocket은 `cmd`/`bdy` 프레임 |
| 관련 문서 | [Live](live.md) · [Video](video.md) · [Notification](notification.md) |

실시간 수신이 필요하지 않은 경우 [다시보기 채팅 조회](video.md#다시보기-채팅-조회)로 방송 전체의 채팅 로그를 받을 수 있습니다.
토큰 발급과 WebSocket 접속이 필요하지 않습니다.

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **WSS kr-ss{N}.chat.naver.com/chat** | [WebSocket 연결](#websocket-연결) |
| 실측 · 인증 필요 | **GET /v1/chats/access-token** | [액세스 토큰 발급](#액세스-토큰-발급) |
| 실측 · 인증 필요 | **GET /v1/chats/{chatChannelId}/users/{userIdHash}/profile** | [프로필 조회](#프로필-조회) |

***

## 접속 절차

```
1. GET /polling/v3.1/channels/{channelId}/live-status   → chatChannelId
2. GET /v1/chats/access-token?channelId={chatChannelId} → accTkn
3. wss://kr-ss{N}.chat.naver.com/chat  접속
4. cmd 100 (CONNECT) 전송 → cmd 10100 응답의 bdy.sid 보관
5. 이후 모든 요청에 sid 포함
```

`chatChannelId` 는 방송마다 변경됩니다. 재접속할 때마다 1번부터 다시 수행합니다.

***

## 액세스 토큰 발급

채팅 서버 접속에 사용할 토큰을 발급받을 수 있습니다.\
이 API를 호출하려면 로그인이 필요합니다.

| HTTP Request | Description |
|---|---|
| **GET https://comm-api.game.naver.com/nng_main/v1/chats/access-token** | 액세스 토큰 발급 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | `chatChannelId`. 채널 식별자가 아님 |
| chatType | String | * | `STREAMING` |

**Response Body**

| Field | Type | Description |
|---|---|---|
| accTkn | String | 채팅 서버 접속 토큰. 민감 정보 |

`accTkn` 은 채팅 계정 도용에 사용될 수 있습니다. 공유하거나 저장소에 커밋하지 않습니다.

***

## WebSocket 연결

```
wss://kr-ss{N}.chat.naver.com/chat
```

### 서버 번호는 클라이언트가 정하지 않습니다

공개 라이브러리에 아래와 같은 서버 번호 계산식이 알려져 있습니다.

```js
serverId = Math.abs(sum(charCodes)) % 9 + 1   // 1~9
```

이 계산식은 성립하지 않습니다. modulus 값이 틀린 것이 아니라 전제 자체가 다릅니다.

캡처한 WebSocket 프레임에서 동일한 `chatChannelId` 가 서로 다른 두 서버에 접속해 모두 성공했습니다.

```
wss://kr-ss24.chat.naver.com/chat  ← cid "N2dc9q" → retCode 0 SUCCESS
wss://kr-ss35.chat.naver.com/chat  ← cid "N2dc9q" → retCode 0 SUCCESS
```

양쪽 모두 `messageList` 를 정상 수신했습니다.
`cid` 에서 서버를 유도하는 방식이 아니라 풀 내의 임의 서버에 접속하는 방식입니다.

| 항목 | 상태 |
|---|---|
| 관측된 서버 번호 | `kr-ss24`, `kr-ss35` |
| 유효 번호 범위 | 미확인 |

### CONNECT 프레임

`ver` 값은 `3` 입니다. 공개 라이브러리에 `2` 로 알려져 있으나 실제 값은 `3` 이며 바디 구성도 다릅니다.

```json
{
  "ver": "3",
  "cmd": 100,
  "svcid": "game",
  "cid": "<chatChannelId>",
  "sid": null,
  "bdy": {
    "uid": "<userIdHash>",
    "devType": 2001,
    "accTkn": "<accessToken>",
    "auth": "SEND",
    "libVer": "4.11.0",
    "osVer": "Windows/10",
    "devName": "Google Chrome/150.0.0.0",
    "locale": "ko",
    "timezone": "Asia/Seoul",
    "uuid": "<UUID>",
    "windowId": "<UUID>"
  }
}
```

응답 `cmd: 10100` 의 `bdy.sid` 를 이후 모든 요청에 포함해야 합니다.

| Field | 미검증 사항 |
|---|---|
| auth | `SEND` 로 관측. `READ` 로 `uid` 없이 접속 가능한지 미확인 |
| libVer · windowId | 필수 여부 미확인 |

수신만 하는 경우 `auth: "READ"` 의 동작 여부를 먼저 확인해 볼 수 있습니다.

### cmd 코드

수신에 사용되는 코드입니다.

| cmd | 이름 | 방향 |
|---|---|---|
| 0 / 10000 | PING / PONG | 양방향 |
| 100 / 10100 | CONNECT / CONNECTED | 양방향 |
| 5101 / 15101 | REQUEST_RECENT_CHAT / RECENT_CHAT | 양방향 |
| 93101 | CHAT | 수신 |
| 93102 | DONATION | 수신 |
| 93006 | EVENT | 수신 |
| 94005 / 94006 / 94008 | KICK / BLOCK / BLIND | 수신 |
| 94010 / 94015 | NOTICE / PENALTY | 수신 |

송신 코드인 `3101 SEND_CHAT` 은 이 문서의 범위 밖입니다.

***

## 메시지 객체

수신 프레임의 `bdy` 에 포함되는 메시지입니다.

| Field | Type | Description |
|---|---|---|
| messageTypeCode | Int | 메시지 종류. [아래 표](#messagetypecode) 참조 |
| extras | String | 문자열로 감싸진 JSON ([참조](../core/conventions.md#문자열로-감싸진-json)) |
| profile | String | 문자열로 감싸진 JSON. 시스템 메시지면 `"{}"` |

### messageTypeCode

| 값 | 의미 |
|---|---|
| 1 | TEXT |
| 2 | IMAGE |
| 3 | STICKER |
| 4 | VIDEO |
| 5 | RICH |
| 10 | DONATION |
| 11 | SUBSCRIPTION |
| 30 | SYSTEM_MESSAGE |

### extras

```json
{ "chatType": "STREAMING", "osType": "PC", "extraToken": "<token>",
  "streamingChannelId": "<channelId>", "emojis": {} }
```

`extraToken` 은 민감 정보입니다. 공유하지 않습니다.

### profile

```json
{ "userIdHash": "<hash>", "nickname": "<nick>", "profileImageUrl": "",
  "userRoleCode": "common_user", "badge": null, "title": null,
  "verifiedMark": false, "activityBadges": [] }
```

시스템 메시지는 `userIdHash` 가 `SYSTEM_MESSAGE` 리터럴이고 `profile` 이 `"{}"` 로 옵니다.

```python
import json
profile = json.loads(msg["profile"]) if msg["profile"] != "{}" else None
```

***

## 프로필 조회

채팅 참여자의 프로필을 조회할 수 있습니다.\
이 API를 호출하려면 로그인이 필요합니다.

경로가 `profile-card` 가 아니라 `profile` 이며 `streamingChannelId` 파라미터가 추가로 필요합니다. ([정정된 사실 참조](../reference/deprecated.md))

| HTTP Request | Description |
|---|---|
| **GET https://comm-api.game.naver.com/nng_main/v1/chats/{chatChannelId}/users/{userIdHash}/profile** | 프로필 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| chatChannelId | String | * | 채팅방 식별자 |
| userIdHash | String | * | 조회할 사용자 해시 |
| chatType | String | * | `STREAMING` |
| streamingChannelId | String | * | 채널 식별자. 누락하면 실패 |

***

## 개인정보

채팅 응답에는 다른 이용자의 닉네임과 `userIdHash` 가 포함됩니다. 수집·보관 시 개인정보 취급에 유의합니다.

***

## 관련 문서

[Live](live.md) · [Video](video.md) · [Notification](notification.md) · [Enum 레퍼런스](../reference/enums.md) · [엔드포인트 목록](../reference/endpoints.md)
