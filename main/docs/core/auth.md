# 인증

공개 조회 API는 인증이 필요하지 않습니다.\
일부 API만 네이버 통합 로그인 쿠키를 요구합니다.

| | |
|---|---|
| 공개 조회 | 인증 불필요. 채널, 라이브, VOD, 클립, 댓글 |
| 인증 방식 | 네이버 통합 로그인 쿠키 2개 |
| 관련 문서 | [Base URL](base-urls.md) · [필수 요청 헤더](headers.md) · [공통 규칙](conventions.md) |

***

## 쿠키

```http
Cookie: NID_AUT=<value>; NID_SES=<value>
```

`chzzk.naver.com` 에 로그인한 뒤 개발자 도구의 Application 탭에서 Cookies 항목의 두 값을 확인할 수 있습니다.

두 쿠키는 네이버 통합 로그인 세션이며 계정 자격증명과 같은 수준의 민감 정보입니다.

***

## 권한 3단계

| 단계 | 필요 조건 | 대상 |
|---|---|---|
| 공개 | 없음 | 채널, 라이브, VOD, 클립, 댓글 조회 |
| 로그인 | 쿠키 | `my-info`, `followings`, `getUserStatus`, 채팅 토큰, 차단 목록, 알림 |
| 채널 권한 | 쿠키 + 본인 채널 또는 매니저 | `manage/*` 전체, `stats/*` |

***

## 모듈별 요구 수준

| 모듈 | 공개 | 로그인 | 채널 권한 |
|---|---|---|---|
| [Channel](../modules/channel.md) | 13 | 3 | |
| [Live](../modules/live.md) | 5 | | |
| [Video](../modules/video.md) | 3 | | |
| [Clip](../modules/clip.md) | 6 | | |
| [Comment](../modules/comment.md) | 4 | | |
| [Chat](../modules/chat.md) | | 3 | |
| [Notification](../modules/notification.md) | | 3 | 1 (`alerts/*`) |
| [Discovery](../modules/discovery.md) | 11 | | |
| [Commerce](../modules/commerce.md) | 12 | | |
| [User](../modules/user.md) | 2 | 4 | |
| [Manage](../modules/manage.md) | | | 43 |
| [Stats](../modules/stats.md) | | | 3 |

합계가 모듈별 엔드포인트 수와 다를 수 있습니다.
일부 엔드포인트는 비로그인 상태에서도 응답하지만 필드가 비어서 반환됩니다.

***

## 확인된 권한 값

로그인 상태에서 `my-info` 와 `my-role` 응답에 포함됩니다.

`userRole` 은 `USER` 와 `STREAMER` 두 값이 확인됐습니다.

`permissions` 는 스트리머 본인일 때 반환됩니다.

| 값 | 의미 |
|---|---|
| CHANNEL_MANAGE | 채널 설정 |
| LIVE_CREATE | 방송 시작 |
| CHAT_MANAGE | 채팅 관리 |
| CHAT_BLIND | 채팅 블라인드 |
| VIDEO_DELETE | VOD 삭제 |
| VIDEO_HIDE | VOD 숨김 |
| SETTLEMENT_MANAGE | 정산 |
| PAID_WATCH_PARTY_SOURCE_PLAY | 유료 워치파티 |

이 문서는 읽기 전용 API만 다루므로 위 권한 중 실제로 사용되는 것은 조회 범위 판정뿐입니다.

***

## 민감 정보

아래 값은 공유하거나 저장소에 커밋해서는 안 됩니다.

| 값 | 출처 |
|---|---|
| NID_AUT · NID_SES | 브라우저 쿠키 |
| accTkn | [액세스 토큰 발급](../modules/chat.md#액세스-토큰-발급) |
| streamKey · streamUrl | [스트리밍 정보 조회](../modules/manage.md#스트리밍-정보-조회) |
| liveTokenList | [라이브 상태 조회](../modules/live.md#라이브-상태-조회) |
| Socket.IO auth | [알림 소켓 URL 발급](../modules/notification.md#알림-소켓-url-발급) |

크롬의 sanitized HAR 내보내기는 쿠키와 요청 헤더만 제거합니다.
위 값들은 모두 응답 본문에 있으므로 sanitize 후에도 그대로 남습니다.

***

## 관련 문서

[Base URL](base-urls.md) · [필수 요청 헤더](headers.md) · [공통 규칙](conventions.md)
