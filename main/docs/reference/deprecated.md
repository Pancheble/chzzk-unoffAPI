# 제외된 API · 정정된 사실

이 문서에 수록하지 않은 API와, 기존 라이브러리나 구 문서에 잘못 알려져 있던 사실을 정리합니다.\
다른 자료를 보고 온 경우 특정 API가 없는 이유를 여기에서 확인할 수 있습니다.

| | |
|---|---|
| 관련 문서 | [엔드포인트 전체 목록](endpoints.md) · [문서 규약](../CONTRIBUTING.md) |

| 분류 | 건수 |
|---|---|
| [읽기 전용 규칙으로 제외](#읽기-전용-규칙으로-제외된-것) | 12 |
| [구버전 · 경로 변경](#구버전--경로-변경) | 4 |
| [잘못 알려져 있던 사실](#잘못-알려져-있던-사실) | 7 |

***

## 읽기 전용 규칙으로 제외된 것

이 문서는 서버 상태를 변경하는 요청을 수록하지 않습니다.
그 결과 스트림 키나 채널 설정 변경 사고, 시청자 수 조작 경로가 문서에 포함되지 않습니다.

### 시청 이벤트 — 3건

| 경로 | 사유 |
|---|---|
| `POST /polling/v1/watch-event/live` | 시청 시간 집계 전용. 시청자 수 조작에 사용될 수 있음 |
| `POST /polling/v1/watch-event/video` | 위와 같음 |
| `POST /polling/v1/watch-event/clip` | 위와 같음 |

응답 본문이 없으며 요청에 `live-status` 의 `liveTokenList` 값이 필요합니다.
조회 목적으로는 호출할 필요가 없습니다.

### 스튜디오 쓰기 — 9건

| 경로 | Method |
|---|---|
| `/manage/v1/channels/{id}/live-setting/*` | PUT |
| `/manage/v1/channels/{id}/chats/prohibit-words` | POST |
| `/manage/v1/channels/{id}/chats/prohibit-words/{no}` | DELETE · PUT |
| `/manage/v1/channels/{id}/restrict-users` | POST |
| `/manage/v1/channels/{id}/restrict-users/{targetId}` | DELETE |
| `/manage/v1/channels/{id}/restrict-users/{targetId}/validate` | POST |
| `/manage/v1/channels/{id}/temporary-restrict-users` | POST |
| `/manage/v1/channels/{id}/restrict-release-requests/{no}/reject` | POST |
| `/manage/v1/channels/{id}/streaming-roles[/{targetId}]` | PUT · DELETE |
| `/manage/v1/channels/{id}/donations/mission/{approve,reject}` | POST |

위 목록은 라이브러리 소스를 기준으로 정리한 것이며, 스튜디오 실측 캡처(GET 47건)에는 포함되지 않았습니다.
따라서 이 규칙으로 누락된 검증 경로는 없습니다.

GET이 함께 존재하는 경로(`chat-rules`, `prohibit-words`, `restrict-users`, `streaming-roles`, `live-setting/*`)는 GET만 [Manage](../modules/manage.md)에 수록했습니다.

### 채팅 송신 — 1건

| cmd | 이름 |
|---|---|
| 3101 | SEND_CHAT |

수신 cmd는 [cmd 코드](../modules/chat.md#cmd-코드)에 있습니다.

### 예외 — 조회용 POST 1건

| 경로 | 사유 |
|---|---|
| `POST /service/v1/clips/detail-bulk` | 메서드는 POST이나 서버 상태를 변경하지 않음. 요청 본문에 `clipUIDList` 를 담아야 하므로 GET을 사용할 수 없음 |

수록 여부의 기준은 메서드가 아니라 서버 상태를 변경하는지 여부입니다. ([클립 벌크 조회 참조](../modules/clip.md#클립-벌크-조회))

***

## 구버전 · 경로 변경

기존 라이브러리를 사용하는 경우 아래 경로를 확인합니다.

| 구버전 | 현행 | 비고 |
|---|---|---|
| `GET /service/v2/channels/{id}/live-detail` | `/service/v3.3/...` | v1과 v2 모두 구버전 ([라이브 상세 조회](../modules/live.md#라이브-상세-조회)) |
| `GET /service/v1/channels/{id}/donations/missions` | `/service/v2/...` | v1과 v2가 공존 ([미션 목록 조회](../modules/commerce.md#미션-목록-조회)) |
| `GET /v1/chats/{cid}/users/{uid}/profile-card` | `.../profile` | `streamingChannelId` 파라미터가 추가로 필요 ([프로필 조회](../modules/chat.md#프로필-조회)) |
| `POST /service/live-status` | `GET /polling/v3.1/.../live-status` | [아래 참조](#1-post-servicelive-status-는-라이브-상태-api가-아닙니다) |

***

## 잘못 알려져 있던 사실

구 문서나 공개 라이브러리에 기재된 내용과 실측 결과가 다른 항목입니다.

### 1. POST /service/live-status 는 라이브 상태 API가 아닙니다

| | |
|---|---|
| 알려진 내용 | 라이브 상태 조회 |
| 실측 결과 | 행동 로그 수집기. 캡처 1,056건 중 113건이 이 요청 |

요청 본문에 `scene_id`, `action_id`, `event_context.referrer` 같은 분석용 필드가 포함됩니다.
데이터 수집용이므로 호출할 필요가 없습니다.

라이브 상태는 [라이브 상태 조회](../modules/live.md#라이브-상태-조회)에서 제공합니다.

### 2. GET /polling/live-detail 은 라이브 상세가 아닙니다

A/B 테스트 배정을 조회하는 API이며 `abTestNoList` 와 `entityId` 를 파라미터로 받습니다.
이름이 혼동을 유발하므로 근거로만 [A/B 테스트 배정 조회](../modules/live.md#ab-테스트-배정-조회)에 수록했습니다.

### 3. 채팅 시스템은 하나입니다

| | |
|---|---|
| 알려진 내용 | 구 방식 `kr-ss{N}` 과 신 방식 `ssio{N}` Socket.IO가 병존 |
| 실측 결과 | `ssio{N}` 은 채팅이 아니라 개인 알림 채널 |

관측된 WebSocket 프레임 8개가 모두 핸드셰이크와 하트비트였고 채팅 페이로드는 없었습니다. 앱 식별자는 `nng@glive` 입니다.

채팅은 [Chat](../modules/chat.md), 알림은 [Notification](../modules/notification.md)에 있습니다.

### 4. 채팅 서버 번호 공식은 전제가 다릅니다

| | |
|---|---|
| 알려진 내용 | `sum(charCodes) % 9 + 1` 공식이 있었으나 `kr-ss24`, `kr-ss35` 가 관측되어 modulus가 변경된 것으로 추정 |
| 실측 결과 | modulus 문제가 아니라 `cid` 에서 서버를 유도하는 방식 자체가 아님 |

동일한 `chatChannelId`(`N2dc9q`)가 `kr-ss24` 와 `kr-ss35` 양쪽에 접속해 모두 `retCode 0` 으로 성공했고, 양쪽 모두 `messageList` 를 정상 수신했습니다.

풀 내의 임의 서버에 접속하면 됩니다. ([서버 번호는 클라이언트가 정하지 않습니다](../modules/chat.md#서버-번호는-클라이언트가-정하지-않습니다))

### 5. 채팅 CONNECT 의 ver 은 3입니다

`ver` 값이 `2` 로 알려져 있으나 실제 값은 `3` 이며 `bdy` 구성도 확장됐습니다.
`libVer`, `windowId`, `timezone`, `devName`, `locale` 이 추가됐습니다.

응답 `cmd: 10100` 의 `bdy.sid` 를 이후 모든 요청에 포함해야 합니다. ([CONNECT 프레임](../modules/chat.md#connect-프레임))

### 6. 본인 채널은 시계열 데이터를 조회할 수 있습니다

| | |
|---|---|
| 알려진 내용 | 모든 조회 API가 현재 시점의 스냅샷만 제공하므로 직접 폴링해서 축적해야 함 |
| 실측 결과 | 본인 채널은 `manage/v1/.../stats/*` 로 과거 데이터를 조회할 수 있음 |

`avgCv`(평균 동시 시청자), `peakCv`(최고 동시 시청자), `avgKeepWatchingRate`(평균 시청 유지율) 등 공개 API로는 얻을 수 없는 지표가 포함됩니다. ([Stats 참조](../modules/stats.md))

타 채널은 여전히 폴링이 유일한 방법입니다. 이 정정은 본인 채널에만 해당합니다. ([채널 애널리틱스 참조](analytics.md))

### 7. 대댓글 경로는 replyComments 입니다

추정 경로로 `.../comments/{commentId}/replies` 가 기재되어 있었으나 실제 경로는 `replyComments` 입니다.
`limit` 없이 `offset` 만 받습니다. ([대댓글 조회](../modules/comment.md#대댓글-조회))

***

## 무효 필드

경로는 유효하지만 값이 채워지지 않는 필드입니다.

| Field | 위치 | 상태 |
|---|---|---|
| accumulateCount | `live-status` · `live-detail` | 양쪽 모두 항상 0. 엔드포인트 차이가 아님 |

누적 시청자 수가 필요하면 VOD의 `livePv` 를 사용하거나 직접 집계합니다. ([accumulateCount 참조](../modules/live.md#accumulatecount-는-무효-필드입니다))

***

## 강등된 항목

| 항목 | 이전 기재 | 현재 |
|---|---|---|
| scene 헤더 | 필수 | 선택. 통계용이며 없어도 동작 ([scene 참조](../core/headers.md#scene)) |
| trackingParams | 응답 필드로 설명 | 통계용. 조회 결과에 영향 없음 |
| recId | 응답 필드로 설명 | 추천 맥락 전달용. 문자열로 감싸진 JSON |
