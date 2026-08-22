# Base URL

치지직 API는 7개 호스트에 걸쳐 있습니다.\
어떤 호스트를 사용하는지에 따라 응답 봉투의 형태가 달라집니다. ([응답 봉투 참조](conventions.md#응답-봉투))

| | |
|---|---|
| 적용 범위 | 모든 요청 |
| 관련 문서 | [필수 요청 헤더](headers.md) · [공통 규칙](conventions.md) · [인증](auth.md) |

***

## 호스트 목록

| 별칭 | Host | 용도 | 봉투 |
|---|---|---|---|
| CHZZK | `https://api.chzzk.naver.com` | 대부분의 조회. 캡처 요청의 약 60% | [A형](conventions.md#a형--치지직-계열) |
| GAME | `https://comm-api.game.naver.com/nng_main` | 로그인 상태, 채팅 토큰, 프로필, 차단 목록 | A형 |
| COMMENT | `https://apis.naver.com/nng_main/nng_comment_api` | 댓글. VOD·채널 게시글·클립 | A형 |
| CREATOR | `https://creatorhub-api.naver.com` | 클립 뷰어 피드, 댓글 스티커 | [B형](conventions.md#b형--creator-hub-계열) |
| VOD | `https://apis.naver.com/neonplayer/vodplay/v3/playback/{videoId}` | VOD 재생 매니페스트 | XML (DASH MPD) |
| CHAT | `wss://kr-ss{N}.chat.naver.com/chat` | 실시간 채팅 WebSocket | 자체 JSON. cmd 코드 |
| NOTIFY | `wss://ssio{N}.nchat.naver.com/socket.io/` | 개인 알림 Socket.IO | Engine.IO v3 |

***

## CHZZK 경로 접두사

같은 호스트이지만 경로 접두사에 따라 성격이 다릅니다.

| 접두사 | 성격 | 모듈 |
|---|---|---|
| `/service/` | 일반 조회 | 대부분 |
| `/polling/` | 주기 호출용 경량 조회 | [Live](../modules/live.md) |
| `/commercial/` | 상업 기능 | [Commerce](../modules/commerce.md) |
| `/manage/` | 스튜디오. 본인 채널 권한 필요 | [Manage](../modules/manage.md) · [Stats](../modules/stats.md) |

`/manage/` 는 v1과 v2가 공존합니다. 대부분 v1이며 `center-status` 만 v2로 관측됐습니다.

***

## CREATOR 호스트

`creatorhub-api.naver.com` 은 스튜디오 통계 API가 아닙니다.

캡처에서 확인된 것은 클립 뷰어 추천 피드(`/clipviewer/*`)와 댓글 스티커 팩(`/comment/sticker*`) 두 가지입니다.
네이버 공통 크리에이터 플랫폼으로 블로그와 클립이 함께 사용하며, 응답 봉투도 `{header, body}` 형태로 다릅니다.

채널 통계는 이 호스트가 아니라 `/manage/v1/.../stats/*` 에 있습니다. ([Stats 참조](../modules/stats.md))

***

## 서버 번호

`CHAT` 과 `NOTIFY` 의 `{N}` 은 클라이언트가 계산하는 값이 아닙니다.

| 호스트 | 결정 방식 | 관측값 |
|---|---|---|
| CHAT | 풀 내 임의. 동일한 `chatChannelId` 가 서로 다른 서버에 접속해 모두 성공 | `kr-ss24`, `kr-ss35` |
| NOTIFY | 서버가 URL 전체를 반환 (`personal/session-url`) | `ssio07`, `ssio09`, `ssio24`, `ssio25` |

공개 라이브러리에 알려진 `sum(charCodes) % 9 + 1` 공식은 modulus 값이 틀린 것이 아니라 전제 자체가 성립하지 않습니다.
자세한 내용은 [서버 번호는 클라이언트가 정하지 않습니다](../modules/chat.md#서버-번호는-클라이언트가-정하지-않습니다)에 있습니다.

***

## NOTIFY 호스트

경로명이 `nchat` 이라 채팅으로 오인하기 쉽습니다.
앱 식별자가 `nng@glive` 이고 관측된 WebSocket 프레임이 모두 핸드셰이크와 하트비트였습니다.
개인 알림 채널입니다. ([Notification 참조](../modules/notification.md))

***

## 관련 문서

[필수 요청 헤더](headers.md) · [공통 규칙](conventions.md) · [인증](auth.md)
