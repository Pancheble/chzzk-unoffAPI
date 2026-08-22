# Commerce

커머스 API로 채널의 후원 설정, 미션 목록, 스트리머 상점 정보를 조회할 수 있습니다.\
인증이 필요하지 않습니다.\
후원 설정을 반환하는 API이며 후원 내역을 반환하지는 않습니다.

| | |
|---|---|
| Base URL | `https://api.chzzk.naver.com` |
| 응답 봉투 | A형. `code == 200` ([참조](../core/conventions.md#응답-봉투)) |
| 관련 문서 | [Channel](channel.md) · [Notification](notification.md) |

***

## 엔드포인트

**후원**

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /service/v1/channels/{channelId}/donations/chat-setting** | [후원 설정 조회](#후원-설정-조회) |
| 실측 | **GET /service/v1/channels/{channelId}/donations/video-setting** | [후원 설정 조회](#후원-설정-조회) |
| 실측 | **GET /service/v1/channels/{channelId}/donations/mission-setting** | [후원 설정 조회](#후원-설정-조회) |
| 실측 | **GET /service/v2/channels/{channelId}/donations/missions** | [미션 목록 조회](#미션-목록-조회) |

**상업 기능**

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /commercial/v1/streamer-shop/{channelId}/products** | [스트리머 상점 조회](#스트리머-상점-조회) |
| 실측 | **GET /commercial/v1/streamer-shop/{channelId}/notifiable** | [스트리머 상점 조회](#스트리머-상점-조회) |
| 실측 | **GET /commercial/v1/channels/{channelId}/donation-campaigns** | 후원 캠페인 조회 |
| 실측 | **GET /commercial/v1/cheat-key/status** | [치트키 · 오퍼월](#치트키--오퍼월) |
| 실측 | **GET /commercial/v1/cheat-key/promotion-status** | [치트키 · 오퍼월](#치트키--오퍼월) |
| 실측 | **GET /commercial/v1/offerwall/total-reward** | [치트키 · 오퍼월](#치트키--오퍼월) |

**광고 · 유료상품**

| 상태 | HTTP Request | Description |
|---|---|---|
| 경로만 확인 | **GET /service/v1/paid-product/init** | [광고 · 유료상품](#광고--유료상품) |
| 경로만 확인 | **GET /service/v1/ad/display-status** | [광고 · 유료상품](#광고--유료상품) |

***

## 미션 목록 조회

채널의 미션 후원 목록을 조회할 수 있습니다.

v1과 v2가 공존하며 v2가 현행입니다. v1은 구버전입니다. ([제외된 API 참조](../reference/deprecated.md))

| HTTP Request | Description |
|---|---|
| **GET /service/v2/channels/{channelId}/donations/missions** | 미션 목록 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 조회할 채널 식별자 |
| filterStatus | String | optional | 미션 상태 필터. 사용 가능한 값은 미확인 |
| page | Int | * | 요청하는 페이지. 0부터 시작 ([참조](../core/conventions.md#페이지네이션--3가지-혼재)) |
| size | Int | * | 조회할 미션 개수 |

미션 승인과 거절은 서버 상태를 변경하는 동작이므로 이 문서의 범위 밖입니다.
미션 발생을 실시간으로 감지하려면 알림 소켓의 `mission@` 세션을 사용합니다. ([이벤트 세션 참조](notification.md#이벤트-세션-9종))

***

## 후원 설정 조회

채널이 후원을 받는 방식에 대한 설정을 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/channels/{channelId}/donations/chat-setting** | 채팅 후원 설정 조회 |
| **GET /service/v1/channels/{channelId}/donations/video-setting** | 영상 후원 설정 조회 |
| **GET /service/v1/channels/{channelId}/donations/mission-setting** | 미션 후원 설정 조회 |

| 경로 | 내용 |
|---|---|
| chat-setting | 채팅 후원 허용 여부, 최소 금액 등 |
| video-setting | 영상 후원 설정 |
| mission-setting | 미션 후원 설정 |

### 후원 내역

후원 내역을 반환하는 공개 API는 이번 캡처에서 확인되지 않았습니다.
후원 랭킹의 노출 여부만 라이브 상태의 `chatDonationRankingExposure` 로 확인할 수 있습니다. ([라이브 상태 조회 참조](live.md#라이브-상태-조회))

VOD 다시보기 채팅에서는 후원을 건별로 확인할 수 있습니다. `messageTypeCode` 가 10인 메시지가 후원입니다. ([다시보기 채팅 조회 참조](video.md#다시보기-채팅-조회))

***

## 스트리머 상점 조회

채널의 스트리머 상점 상품 목록을 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /commercial/v1/streamer-shop/{channelId}/products** | 상점 상품 조회 |
| **GET /commercial/v1/streamer-shop/{channelId}/notifiable** | 상점 알림 가능 여부 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 조회할 채널 식별자 |
| catalogType | String | * | 카탈로그 종류. 사용 가능한 값은 미확인. `products` 에만 사용 |

`notifiable` 은 쿼리 파라미터가 없습니다.

VOD 상세의 `streamerShopCatalogTagActive` 가 `true` 이면 해당 영상에 상품 태그가 있습니다. ([VOD 객체 참조](video.md#vod-객체))

***

## 치트키 · 오퍼월

치트키 사용 상태와 오퍼월 누적 리워드를 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /commercial/v1/cheat-key/status** | 치트키 상태 조회 |
| **GET /commercial/v1/cheat-key/promotion-status** | 치트키 프로모션 조회 |
| **GET /commercial/v1/offerwall/total-reward** | 오퍼월 누적 리워드 조회 |

| 경로 | 내용 | 파라미터 |
|---|---|---|
| cheat-key/status | 치트키 사용 상태 | 없음 |
| cheat-key/promotion-status | 프로모션 진행 여부 | 없음 |
| offerwall/total-reward | 누적 리워드 | `clientPlatformType` |

`my-info` 응답의 `cheatKey` 필드와 연동됩니다. ([내 정보 조회 참조](channel.md#내-정보-조회))

***

## 광고 · 유료상품

| HTTP Request | Description |
|---|---|
| **GET /service/v1/ad/display-status** | 광고 노출 상태 조회 |
| **GET /service/v1/paid-product/init** | 유료상품 초기화 |

| 경로 | 파라미터 |
|---|---|
| ad/display-status | `pgId`, `pgType` |
| paid-product/init | 없음 |

경로만 확인했으며 파라미터 값과 응답은 검증되지 않았습니다.

라이브 광고는 [Live](live.md#광고)에 있습니다.

***

## 관련 문서

[Channel](channel.md) · [Live](live.md) · [Video](video.md) · [Notification](notification.md) · [엔드포인트 목록](../reference/endpoints.md)
