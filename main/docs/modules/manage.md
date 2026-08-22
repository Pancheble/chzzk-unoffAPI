# Manage

스튜디오 API로 본인 채널의 방송 설정, 권한, 채팅 관리 정보, 시청자 목록, 콘텐츠 목록을 조회할 수 있습니다.\
이 API를 호출하려면 본인 채널 또는 매니저 권한이 필요합니다.\
방송 설정 변경, 제재 추가와 해제, 금지어 편집, 매니저 지정 등 서버 상태를 변경하는 동작은 수록하지 않았습니다. ([제외 목록 참조](../reference/deprecated.md#읽기-전용-규칙으로-제외된-것))

| | |
|---|---|
| Base URL | `https://api.chzzk.naver.com/manage/v1`. 일부 `v2` |
| 응답 봉투 | A형. `code == 200` ([참조](../core/conventions.md#응답-봉투)) |
| 관련 문서 | [Stats](stats.md) · [Channel](channel.md) · [Notification](notification.md) |

채널 통계 3건은 별도 문서로 분리했습니다. ([Stats](stats.md))

***

## 수록 범위

스튜디오 캡처 315건에서 확인된 GET 경로 47개를 기준으로 합니다.

| 분류 | 건수 | 위치 |
|---|---|---|
| 채널 통계 | 3 | [Stats](stats.md) |
| 알림 세션 | 1 | [Notification](notification.md#이벤트-세션-9종) |
| 이 문서 | 43 | 이름 확인 23건, [미수록 20건](#미수록-경로) |

***

## 엔드포인트

**방송 정보**

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 · 민감 정보 | **GET /channels/{channelId}/streaming-info** | [스트리밍 정보 조회](#스트리밍-정보-조회) |
| 경로만 확인 | **GET /channels/{channelId}/streams** | 유효하나 실사용은 `streaming-info` |
| 실측 | **GET /channels/{channelId}/live-setting/normal** | [방송 설정 조회](#방송-설정-조회) |
| 실측 | **GET /channels/{channelId}/live-setting/chat** | [방송 설정 조회](#방송-설정-조회) |
| 실측 | **GET /channels/{channelId}/live-setting/chat-mode** | [방송 설정 조회](#방송-설정-조회) |
| 실측 | **GET /channels/{channelId}/live-setting/chat-condition** | [방송 설정 조회](#방송-설정-조회) |

**권한**

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /channels/{channelId}/my-role** | 내 역할 조회. `userRole`, `permissions` |
| 실측 | **GET /channels/{channelId}/my-status** | 내 상태 조회 |
| 실측 | **GET /channels/{channelId}/streaming-roles** | 매니저 목록 조회 |
| 실측 | **GET /manage/v2/channels/{channelId}/center-status** | 크리에이터 센터 상태 조회. v2 |

**채팅 관리**

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /channels/{channelId}/chat-rules** | 채팅 규칙 조회 |
| 실측 | **GET /channels/{channelId}/chats/prohibit-words** | 금지어 목록 조회 |
| 스키마 미상 | **GET /channels/{channelId}/restrict-users** | 활동 제한 사용자 조회 |
| 스키마 미상 | **GET /channels/{channelId}/restrict-release-requests** | 제한 해제 요청 조회 |
| 경로만 확인 | **GET /channels/{channelId}/users/{targetId}/chat-activity-count** | [미포착](#미포착-2건) |

**시청자**

| 상태 | HTTP Request | Description |
|---|---|---|
| 스키마 미상 | **GET /channels/{channelId}/followers** | 팔로워 목록 조회. 공개 API에는 없음 |
| 스키마 미상 | **GET /channels/{channelId}/subscribers** | 구독자 목록 조회 |

**콘텐츠**

| 상태 | HTTP Request | Description |
|---|---|---|
| 스키마 미상 | **GET /channels/{channelId}/videos** | VOD 목록 조회. 비공개 포함 |
| 스키마 미상 | **GET /channels/{channelId}/clips** | 클립 목록 조회 |
| 스키마 미상 | **GET /channels/{channelId}/clips/make-clips** | 내가 만든 클립 조회 |
| 스키마 미상 | **GET /channels/{channelId}/news-feeds** | 뉴스피드 조회 |
| 스키마 미상 | **GET /channels/{channelId}/party/summary** | 파티 요약 조회 |

**기타**

| 상태 | HTTP Request | Description |
|---|---|---|
| 경로만 확인 | **GET /auto-complete/categories** | [미포착](#미포착-2건) |

***

## 스트리밍 정보 조회

방송 송출에 필요한 정보와 알림 이벤트 세션 식별자를 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /manage/v1/channels/{channelId}/streaming-info** | 스트리밍 정보 조회 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| streamKey | String | 스트림 키. 민감 정보 |
| streamUrl | String | RTMP 송출 URL. 민감 정보 |
| sessionIOChannelId 계열 | String | [이벤트 세션 9종](notification.md#이벤트-세션-9종) |

```json
{
  "streamKey": "<32자>",
  "streamUrl": "rtmp://global-rtmp.lip2.navercorp.com:8080/relay"
}
```

`streamKey` 와 `streamUrl` 두 값이 있으면 제3자가 해당 채널로 송출할 수 있습니다.
HAR, 로그, 스크린샷에 남기지 않습니다.
크롬의 sanitized HAR 내보내기는 쿠키와 요청 헤더만 제거하므로 이 값들은 응답 본문에 그대로 남습니다.
노출된 경우 스튜디오에서 스트림 키를 재발급합니다.

알림 소켓에 접속하려면 이 응답의 `sessionIOChannelId` 에서 시작합니다.
키를 제외한 나머지 필드 구조는 확보되지 않았습니다.

***

## 방송 설정 조회

방송과 채팅 설정을 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /channels/{channelId}/live-setting/normal** | 방송 기본 설정 조회 |
| **GET /channels/{channelId}/live-setting/chat** | 채팅 설정 조회 |
| **GET /channels/{channelId}/live-setting/chat-mode** | 채팅 모드 조회 |
| **GET /channels/{channelId}/live-setting/chat-condition** | 채팅 조건 조회 |

공개 문서에는 `/live-setting` 단일 경로로 기재된 경우가 있으나 실제로는 위 4개로 분리되어 있습니다.

***

## 확인된 파라미터 값

| Field | 경로 | 값 |
|---|---|---|
| dateFilter | clips | `ALL` |
| orderFilter | clips | `LATEST` |
| sortType | subscribers | `RECENT` |
| keyword | auto-complete/categories | 검색어 |

전체 Enum은 [Enum 레퍼런스](../reference/enums.md)에 있습니다.

***

## 응답 스키마 미상 — 11건

경로와 인증은 확정됐으나 캡처한 채널에 데이터가 없어 응답이 비어 있었습니다.

`clips`, `clips/make-clips`, `followers`, `news-feeds`, `party/summary`,
`restrict-release-requests`, `restrict-users`, `subscribers`, `videos`
그리고 [Stats](stats.md)의 `stats/lives`, `stats/videos` 입니다.

빈 배열 또는 `null` 로 관측됐습니다. 데이터가 축적된 채널에서 재캡처하면 일괄 확인할 수 있습니다.

***

## 미포착 2건

경로는 확인됐으나 캡처에 잡히지 않았습니다. 해당 UI 조작이 필요합니다.

| 경로 | 유발 방법 |
|---|---|
| `GET /auto-complete/categories?keyword=` | 카테고리 검색창에 입력 |
| `GET /channels/{channelId}/users/{targetId}/chat-activity-count` | 시청자 목록에서 특정 사용자 선택 |

***

## 미수록 경로

스튜디오 캡처에서 확인된 47개 중 20개의 경로명을 확보하지 못했습니다.

<!-- 목록 확보 시 이 절을 채웁니다. 형식:
| 상태 | HTTP Request | Description |
|---|---|---|
-->

***

## 공개 API 와 겹치는 경로

| 경로 | 이 문서 | 공개 |
|---|---|---|
| chat-rules | `GET /manage/v1/channels/{id}/chat-rules` | [Channel](channel.md) |
| videos | `GET /manage/v1/channels/{id}/videos`. 비공개 포함 | [VOD 목록 조회](channel.md#vod-목록-조회) |
| clips | `GET /manage/v1/channels/{id}/clips` | [채널 클립 목록 조회](clip.md#채널-클립-목록-조회) |
| followers | `GET /manage/v1/channels/{id}/followers`. 목록 제공 | 공개는 `followerCount` 숫자만 |

***

## 버전

대부분 `manage/v1` 이며 `center-status` 만 `manage/v2` 로 관측됐습니다.
v2가 다른 경로에도 존재하는지는 확인되지 않았습니다.

***

## 관련 문서

[Stats](stats.md) · [Channel](channel.md) · [Notification](notification.md) · [제외된 API](../reference/deprecated.md) · [엔드포인트 목록](../reference/endpoints.md)
