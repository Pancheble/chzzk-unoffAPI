# Live

라이브 API로 방송 상태와 방송 상세 정보를 조회할 수 있습니다.\
인증이 필요하지 않습니다.\
시청자 수를 주기적으로 확인할 때는 `live-detail` 보다 가벼운 `live-status` 를 사용합니다.

| | |
|---|---|
| Base URL | `https://api.chzzk.naver.com` |
| 응답 봉투 | A형. `code == 200` ([참조](../core/conventions.md#응답-봉투)) |
| 관련 문서 | [Channel](channel.md) · [Chat](chat.md) · [채널 애널리틱스](../reference/analytics.md) |

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /polling/v3.1/channels/{channelId}/live-status** | [라이브 상태 조회](#라이브-상태-조회) |
| 실측 | **GET /service/v3.3/channels/{channelId}/live-detail** | [라이브 상세 조회](#라이브-상세-조회) |
| 실측 | **GET /polling/live-detail** | [A/B 테스트 배정 조회](#ab-테스트-배정-조회) |
| 경로만 확인 | **GET /service/v1/lives/{liveId}/ads/current** | [광고](#광고) |
| 경로만 확인 | **GET /service/v1/live/{liveId}/auto-play-info** | [광고](#광고) |

경로에 `lives`(복수)와 `live`(단수)가 함께 쓰입니다. 오타가 아니라 실제 경로입니다.

### 이름과 기능이 다른 경로

| 경로 | 실제 기능 |
|---|---|
| `GET /polling/v3.1/.../live-status` | 라이브 상태 조회 |
| `GET /service/v3.3/.../live-detail` | 라이브 상세 조회 |
| `GET /polling/live-detail` | 라이브 상세가 아니라 A/B 테스트 배정 조회 |
| `POST /service/live-status` | 라이브 상태가 아니라 행동 로그 수집기. [이 문서에서 제외](../reference/deprecated.md) |

`polling` 은 상태, `service` 는 상세를 반환합니다. `polling/live-detail` 만 예외입니다.

***

## 라이브 상태 조회

채널의 현재 방송 상태와 동시 시청자 수를 조회할 수 있습니다.\
`live-detail` 보다 응답이 가벼워 주기 호출에 적합합니다.

| HTTP Request | Description |
|---|---|
| **GET /polling/v3.1/channels/{channelId}/live-status** | 라이브 상태 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 조회할 채널 식별자 |
| includePlayerRecommendContent | Boolean | optional | 추천 콘텐츠 포함 여부. `false` 확인 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| status | String | `OPEN` 또는 `CLOSE` |
| concurrentUserCount | Int | 현재 동시 시청자 수 |
| accumulateCount | Int | 항상 0으로 반환됩니다. [아래 참조](#accumulatecount-는-무효-필드입니다) |
| liveTitle | String | 방송 제목 |
| liveCategory | String | 카테고리 코드 |
| liveCategoryValue | String | 카테고리 표시명 |
| categoryType | String | 카테고리 분류 (예: `GAME`) |
| tags | String[] | 방송 태그 |
| openDate | String | 방송 시작 일시. `YYYY-MM-DD HH:mm:ss` |
| closeDate | String | 방송 종료 일시. 방송 중이면 `null` |
| chatChannelId | String | 채팅방 식별자 ([Chat 참조](chat.md)) |
| chatActive | Boolean | 채팅 활성 여부 |
| chatAvailableGroup | String | 채팅 참여 가능 그룹 |
| chatDonationRankingExposure | Boolean | 후원 랭킹 노출 여부 |
| livePollingStatusJson | String | 폴링 주기 정보. 문자열로 감싸진 JSON ([참조](../core/conventions.md#문자열로-감싸진-json)) |
| liveTokenList | String[] | 민감 정보. 외부에 공유하지 않습니다 |
| adult | Boolean | 성인 제한 여부 |
| userAdultStatus | String | 성인 인증 상태 |
| skipPreRollAd | Boolean | 프리롤 광고 스킵 여부 |
| clipActive | Boolean | 클립 생성 허용 여부 |
| timeMachineActive | Boolean | 타임머신 허용 여부 |

<details><summary>응답 예시</summary>

```json
{
  "code": 200,
  "content": {
    "liveTitle": "...", "status": "OPEN",
    "concurrentUserCount": 1926, "accumulateCount": 0,
    "cvExposure": true, "paidPromotion": false, "adult": false,
    "krOnlyViewing": false, "abroadCountry": false,
    "openDate": "2026-07-24 19:31:33", "closeDate": null,
    "clipActive": true, "timeMachineActive": true,
    "chatChannelId": "N2dcLY",
    "tags": ["넥슨커넥트", "메이플", "..."],
    "categoryType": "GAME",
    "liveCategory": "MapleStory", "liveCategoryValue": "메이플스토리",
    "livePollingStatusJson": "{...}",
    "faultStatus": null, "liveConnecting": false,
    "skipPreRollAd": false, "userAdultStatus": "AGE_RESTRICTION",
    "blindType": null,
    "chatActive": true, "chatAvailableGroup": "ALL",
    "chatAvailableCondition": "NONE", "minFollowerMinute": 0,
    "allowSubscriberInFollowerMode": true,
    "chatSlowModeSec": 0, "chatEmojiMode": false,
    "chatDonationRankingExposure": true,
    "dropsCampaignNo": null,
    "liveTokenList": ["<base64 token>"],
    "watchPartyNo": null, "watchPartyTag": null, "watchPartyType": null,
    "playerRecommendContent": { "categoryLives": [], "channelLatestVideos": [] }
  }
}
```
</details>

### 폴링 주기

`livePollingStatusJson` 을 파싱하면 `callPeriodMilliSecond` 가 있습니다. 관측값은 10000ms입니다.

```python
import json
period = json.loads(content["livePollingStatusJson"])["callPeriodMilliSecond"] / 1000
```

이보다 자주 호출하면 IP 차단으로 이어질 수 있습니다.

### accumulateCount 는 무효 필드입니다

이름은 누적 시청자 수를 뜻하지만 `live-status` 와 `live-detail` 양쪽 모두 0으로 관측됐습니다.
엔드포인트에 따른 차이가 아니라 필드 자체가 채워지지 않습니다.

누적 시청자 수가 필요한 경우 아래 방법을 사용합니다.

| 시점 | 방법 |
|---|---|
| 방송 종료 후 | VOD의 `livePv` ([VOD 객체 참조](video.md#vod-객체)) |
| 방송 중 | `concurrentUserCount` 를 주기적으로 조회하여 직접 집계 |

***

## 라이브 상세 조회

방송의 상세 정보와 재생 정보를 조회할 수 있습니다.

경로 버전이 `v3.3` 입니다. 공개 라이브러리에 알려진 v2는 구버전입니다. ([제외된 API 참조](../reference/deprecated.md))

| HTTP Request | Description |
|---|---|
| **GET /service/v3.3/channels/{channelId}/live-detail** | 라이브 상세 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 조회할 채널 식별자 |
| cu · dt · tm | String | optional | 캐시 무효화 또는 통계용으로 보이며 생략 가능한 것으로 관측 |

**Response Body**

[라이브 상태 조회](#라이브-상태-조회)의 필드에 재생 정보가 추가됩니다.

| Field | Type | Description |
|---|---|---|
| livePlaybackJson | String | 재생 정보. 문자열로 감싸진 JSON ([참조](../core/conventions.md#문자열로-감싸진-json)) |

### concurrentUserCount 가 두 API에서 다릅니다

같은 시점에 두 API를 호출했을 때 값이 달랐습니다.

| 엔드포인트 | 관측값 |
|---|---|
| `polling/v3.1/.../live-status` | 1926 |
| `service/v3.3/.../live-detail` | 4866 |

캡처 시점 차이일 가능성이 있으나 확인되지 않았습니다.
시계열로 축적하는 경우 한쪽 API로 통일하는 편이 안전하며, 폴링 비용이 낮은 `live-status` 를 권장합니다.

***

## A/B 테스트 배정 조회

웹 클라이언트의 A/B 테스트 배정을 조회합니다.\
경로 이름과 달리 라이브 상세 정보를 반환하지 않습니다.

| HTTP Request | Description |
|---|---|
| **GET /polling/live-detail** | A/B 테스트 배정 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| entityId | String | * | 대상 식별자 |
| abTestNoList | String | * | 테스트 번호 목록. 콤마로 구분 |

실사용 가치는 낮으나 경로 이름이 `live-detail` 이라 혼동하기 쉬워 수록합니다.
라이브 상세 정보는 [라이브 상세 조회](#라이브-상세-조회)에서 제공합니다.

***

## 광고

방송 중 광고 정보를 조회합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/lives/{liveId}/ads/current** | 현재 광고 조회 |
| **GET /service/v1/live/{liveId}/auto-play-info** | 자동재생 정보 조회 |

경로만 확인했으며 파라미터와 응답은 검증되지 않았습니다.

광고 표시 여부 자체는 `live-status` 의 `skipPreRollAd` 와 `my-info` 의 `playerAdFlag` 로도 확인할 수 있습니다. ([내 정보 조회 참조](channel.md#내-정보-조회))

상점과 후원 관련 광고는 [Commerce](commerce.md#광고--유료상품)에 있습니다.

***

## 관련 문서

[Channel](channel.md) · [Chat](chat.md) · [Video](video.md) · [채널 애널리틱스](../reference/analytics.md) · [엔드포인트 목록](../reference/endpoints.md)
