# User

사용자 API로 로그인 상태, 차단 목록, 배지, 닉네임 색상 코드를 조회할 수 있습니다.\
6건 중 4건이 로그인을 요구합니다.\
로그인 사용자 본인에 대한 정보를 다루므로 타 채널 분석에는 사용하지 않습니다. ([채널 애널리틱스 참조](../reference/analytics.md))

| | |
|---|---|
| Base URL | `https://comm-api.game.naver.com/nng_main` · `https://api.chzzk.naver.com` |
| 응답 봉투 | A형. `code == 200` ([참조](../core/conventions.md#응답-봉투)) |
| 관련 문서 | [Channel](channel.md) · [Chat](chat.md) · [Notification](notification.md) |

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 · 인증 필요 | **GET /v1/user/getUserStatus** | [로그인 상태 조회](#로그인-상태-조회) |
| 실측 · 인증 필요 | **GET /v1/privateUserBlocks/allUserIdHash** | [차단 목록 조회](#차단-목록-조회) |
| 경로만 확인 · 인증 필요 | **GET /service/v1/personal/personal-data** | [개인 설정 데이터 조회](#개인-설정-데이터-조회) |
| 실측 · 인증 필요 | **GET /service/v1/badge-awards/unread** | [안 읽은 배지 조회](#안-읽은-배지-조회) |
| 실측 | **GET /service/v1/badges/assets/last-updated** | [배지 에셋 갱신 시각 조회](#배지-에셋-갱신-시각-조회) |
| 실측 | **GET /service/v2/nickname/color/codes** | [닉네임 색상 코드 조회](#닉네임-색상-코드-조회) |

알림 소켓 발급 경로인 `personal/session-url` 은 이 모듈이 아니라 [Notification](notification.md)에 있습니다. 경로가 비슷하므로 혼동에 주의합니다.

***

## 로그인 상태 조회

로그인 여부와 기본 사용자 정보를 조회할 수 있습니다.\
쿠키의 유효성을 확인하는 가장 가벼운 방법입니다.\
이 API를 호출하려면 로그인이 필요합니다.

| HTTP Request | Description |
|---|---|
| **GET https://comm-api.game.naver.com/nng_main/v1/user/getUserStatus** | 로그인 상태 조회 |

요청 파라미터가 없습니다.

**Response Body**

| Field | Type | Description |
|---|---|---|
| userIdHash | String | 사용자 해시. 32자 |
| nickname | String | 닉네임 |
| profileImageUrl | String | 프로필 이미지 URL |
| loggedIn | Boolean | 로그인 여부 |

`userIdHash` 는 `channelId` 와 형식이 같은 32자 hex입니다. 스트리머 본인은 두 값이 동일합니다. ([식별자 참조](../core/conventions.md#헷갈리는-3쌍))

**오류**

쿠키가 없거나 만료된 경우 HTTP 401이 아니라 `loggedIn: false` 로 반환됩니다.
응답 봉투는 성공이므로 `loggedIn` 값을 직접 확인해야 합니다.

***

## 차단 목록 조회

로그인 사용자가 차단한 사용자 목록을 조회할 수 있습니다.\
이 API를 호출하려면 로그인이 필요합니다.

| HTTP Request | Description |
|---|---|
| **GET https://comm-api.game.naver.com/nng_main/v1/privateUserBlocks/allUserIdHash** | 차단 목록 조회 |

요청 파라미터가 없습니다.

**Response Body**

| Field | Type | Description |
|---|---|---|
| content | String[] | 차단한 사용자의 `userIdHash` 목록 |

댓글과 채팅 응답의 `privateUserBlock` 필드와 대응합니다. 클라이언트에서 차단 사용자를 숨길 때 이 목록으로 필터링합니다.

***

## 개인 설정 데이터 조회

로그인 사용자의 개인 설정 데이터를 조회할 수 있습니다.\
이 API를 호출하려면 로그인이 필요합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/personal/personal-data** | 개인 설정 데이터 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| fields | String | * | 조회할 항목. 콤마로 구분. [채널 부가 데이터 조회](channel.md#채널-부가-데이터-조회)와 같은 패턴 |

사용 가능한 `fields` 값과 응답 스키마는 이번 캡처에서 확인되지 않았습니다.

***

## 안 읽은 배지 조회

읽지 않은 배지 획득 알림을 조회할 수 있습니다.\
이 API를 호출하려면 로그인이 필요합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/badge-awards/unread** | 안 읽은 배지 조회 |

요청 파라미터가 없습니다.

채널의 업적 배지는 이 모듈이 아니라 [Channel](channel.md#엔드포인트)의 `achievement-badges` 에 있습니다.

***

## 배지 에셋 갱신 시각 조회

배지 이미지 에셋의 갱신 시각을 조회할 수 있습니다. 캐시 무효화에 사용합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/badges/assets/last-updated** | 배지 에셋 갱신 시각 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| badgeType | String | * | 배지 종류 |

***

## 닉네임 색상 코드 조회

채팅에 사용되는 닉네임 색상 코드 목록을 조회할 수 있습니다.

경로 버전이 `v2` 입니다. 이 모듈에서 유일합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v2/nickname/color/codes** | 닉네임 색상 코드 조회 |

요청 파라미터가 없습니다.

***

## 관련 문서

[Channel](channel.md) · [Chat](chat.md) · [Notification](notification.md) · [공통 규칙](../core/conventions.md) · [엔드포인트 목록](../reference/endpoints.md)
