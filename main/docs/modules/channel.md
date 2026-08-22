# Channel

채널 API로 채널 기본 정보, 채널 부가 데이터, 내 상태, 팔로잉 목록을 조회할 수 있습니다.\
대부분 인증이 필요하지 않으며, `my-info` 와 `followings` 3건만 로그인이 필요합니다.\
인증 없이 얻을 수 있는 채널 지표가 모여 있어 타 채널 분석의 출발점이 됩니다.

| | |
|---|---|
| Base URL | `https://api.chzzk.naver.com` |
| 응답 봉투 | A형. `code == 200` ([참조](../core/conventions.md#응답-봉투)) |
| 관련 문서 | [Live](live.md) · [Video](video.md) · [Clip](clip.md) · [Manage](manage.md) |

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /service/v1/channels/{channelId}** | [채널 기본 정보 조회](#채널-기본-정보-조회) |
| 실측 | **GET /service/v1/channels/{channelId}/data** | [채널 부가 데이터 조회](#채널-부가-데이터-조회) |
| 실측 · 인증 필요 | **GET /service/v1.1/channels/{channelId}/my-info** | [내 정보 조회](#내-정보-조회) |
| 실측 | **GET /service/v1/channels/{channelId}/videos** | [VOD 목록 조회](#vod-목록-조회) |
| 실측 · 인증 필요 | **GET /service/v1/channels/followings** | [팔로잉 목록 조회](#팔로잉-목록-조회) |
| 실측 · 인증 필요 | **GET /service/v1/channels/followings/live** | [팔로잉 목록 조회](#팔로잉-목록-조회) |
| 실측 | **GET /service/v1/channels/{channelId}/chat-rules** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/channels/{channelId}/announcements** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/channels/{channelId}/live-schedule** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/channels/{channelId}/live-recommended** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/channels/{channelId}/follow** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/channels/{channelId}/cafe-connection** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/channels/{channelId}/achievement-badges** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/channels/{channelId}/party-donation-info** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/channels/{channelId}/log-power/prediction** | [부가 엔드포인트](#부가-엔드포인트) |

클립 목록은 이 모듈이 아니라 클립 API에 있습니다. ([채널 클립 목록 조회](clip.md#채널-클립-목록-조회))

### manage 와 겹치는 경로

같은 이름의 경로가 공개 API와 스튜디오 API에 각각 존재하며 반환 범위가 다릅니다.

| 경로 | 이 모듈 | [Manage](manage.md) |
|---|---|---|
| chat-rules | `GET /service/v1/channels/{id}/chat-rules` | `GET /manage/v1/channels/{id}/chat-rules` |
| videos | `GET /service/v1/channels/{id}/videos`. 공개분만 | `GET /manage/v1/channels/{id}/videos`. 비공개 포함 |
| clips | `GET /service/v1/channels/{id}/clips` | `GET /manage/v1/channels/{id}/clips` |
| followers | 없음. `followerCount` 숫자만 제공 | `GET /manage/v1/channels/{id}/followers`. 목록 제공 |

***

## 채널 기본 정보 조회

채널의 기본 정보를 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/channels/{channelId}** | 채널 기본 정보 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 조회할 채널 식별자 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| channelId | String | 채널 식별자 |
| channelName | String | 채널 이름 |
| channelImageUrl | String | 채널 이미지 URL |
| channelDescription | String | 채널 소개 |
| followerCount | Int | 채널의 팔로워 수 |
| openLive | Boolean | 방송 중 여부 |
| verifiedMark | Boolean | 채널 인증 마크 여부 |
| activatedChannelBadgeIds | String[] | 활성화된 채널 배지 식별자 목록 |

**오류**

존재하지 않는 채널을 요청해도 `code` 는 200으로 반환됩니다. 내용만 비어서 옵니다.

```json
{ "channelId": null, "channelName": "(알 수 없음)", "followerCount": 0 }
```

봉투만으로는 실패를 구분할 수 없으므로 `channelId` 가 `null` 인지 확인해야 합니다.

팔로워 수의 추이는 이 API에서 제공하지 않습니다.
타 채널은 이 엔드포인트를 주기적으로 호출해 직접 축적해야 합니다. ([트랙 B 참조](../reference/analytics.md#트랙-b--타-채널))
본인 채널은 [Stats](stats.md)에서 조회할 수 있습니다.

***

## 채널 부가 데이터 조회

채널 개설일, 누적 방송시간, 소셜 링크 등의 부가 데이터를 조회할 수 있습니다.\
인증 없이 누적 지표를 얻을 수 있는 몇 안 되는 API입니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/channels/{channelId}/data** | 채널 부가 데이터 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 조회할 채널 식별자 |
| fields | String | * | 조회할 항목. 콤마로 구분하며 요청한 항목만 반환 |

`fields` 에 사용할 수 있는 값입니다.

| 값 | 반환 내용 |
|---|---|
| channelHistory | 개설일(`firstLiveDate`)과 누적 방송시간(`totalLiveHours`) |
| description | 채널 소개 |
| socialLinks | 소셜 링크 목록 |
| topExposedVideos | 상단 고정 영상 또는 진행 중인 라이브 |
| banners | 채널 배너 |
| donationRankingsExposure | 후원 랭킹 공개 여부 |
| achievementBadgeExposure | 업적 배지 공개 여부 |
| logPowerActive | 로그파워 사용 여부 |
| logPowerRankingExposure | 로그파워 랭킹 공개 여부 |
| missionDonationChannelHomeExposure | 미션 후원 홈 노출 여부 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| channelHistory | Object | 채널 이력 |
| channelHistory.firstLiveDate | String | 첫 방송 일시. 채널 개설 시점 |
| channelHistory.totalLiveHours | Int | 누적 방송시간. 단위는 시간 |
| socialLinks | Object[] | 소셜 링크 목록 |
| socialLinks.title | String | 링크 이름 |
| socialLinks.landingUrl | String | 링크 URL |
| activatedAchievementBadgeIds | String[] | 활성화된 업적 배지. 요청하지 않아도 항상 반환 |

<details><summary>응답 예시 — <code>fields=channelHistory,socialLinks</code></summary>

```json
{
  "code": 200,
  "content": {
    "socialLinks": [
      { "title": "X", "landingUrl": "https://x.com/..." },
      { "title": "YouTube", "landingUrl": "https://www.youtube.com/channel/..." }
    ],
    "channelHistory": {
      "firstLiveDate": "2024-05-18 16:56:56",
      "totalLiveHours": 4259
    },
    "donationRankingsExposure": false,
    "activatedAchievementBadgeIds": [],
    "achievementBadgeExposure": true,
    "logPowerActive": true,
    "logPowerRankingExposure": false
  }
}
```
</details>

***

## 내 정보 조회

해당 채널에 대한 로그인 사용자의 상태를 조회할 수 있습니다.\
팔로우, 구독, 제재, 권한 정보를 한 번에 반환합니다.\
이 API를 호출하려면 로그인이 필요합니다. ([인증 참조](../core/auth.md))

경로 버전이 `v1.1` 입니다. 이 모듈에서 유일합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1.1/channels/{channelId}/my-info** | 내 정보 조회 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| userRole | String | `USER` 또는 `STREAMER` |
| permissions | String[] | 스트리머 본인일 때 8종 반환 ([권한 값 참조](../core/auth.md#확인된-권한-값)) |
| following | Object | 팔로우 정보 |
| following.following | Boolean | 팔로우 여부 |
| following.followDate | String | 팔로우 시작 일시 |
| following.notification | Boolean | 알림 설정 여부 |
| subscription | Object | 구독 정보 |
| subscription.subscribing | Boolean | 구독 여부 |
| restriction | Object | 제재 정보 |
| restriction.restrict | Boolean | 제재 여부 |
| cheatKey | Boolean | 치트키 사용 여부 ([참조](commerce.md#치트키--오퍼월)) |
| playerAdFlag | Object | `preRoll`, `midRoll`, `postRoll` |

<details><summary>응답 예시</summary>

```json
{
  "code": 200,
  "content": {
    "channelId": "<channelId>",
    "userRole": "USER",
    "permissions": [],
    "following": { "following": true, "notification": true, "followDate": "2026-01-20 14:36:07" },
    "cheatKey": false,
    "naverMembership": false,
    "restriction": {
      "restrict": false, "origin": false, "restrictReleaseState": "NONE",
      "judgment": null, "availableReleaseRequestDate": null,
      "restrictUserNickname": null, "fromDate": null, "toDate": null
    },
    "privateUserBlock": false,
    "subscription": {
      "subscribing": false, "subscriptionDeferred": false,
      "subscriptionAlertNotified": false, "subscriptionAlertRefused": false,
      "subscriptionDisabled": false, "subscriptionExpireNotifyRequired": false,
      "subscriptionGift": false
    },
    "playerAdFlag": { "preRoll": true, "midRoll": true, "postRoll": true }
  }
}
```
</details>

***

## VOD 목록 조회

채널의 공개된 VOD 목록을 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/channels/{channelId}/videos** | VOD 목록 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 조회할 채널 식별자 |
| page | Int | * | 요청하는 페이지. 0부터 시작 ([참조](../core/conventions.md#페이지네이션--3가지-혼재)) |
| size | Int | * | 조회할 VOD 개수. 24 확인 |
| pagingType | String | optional | `PAGE` |

**Response Body**

| Field | Type | Description |
|---|---|---|
| data | Object[] | VOD 요약 목록 ([VOD 객체 참조](video.md#vod-객체)) |
| totalCount | Int | 전체 개수 |
| totalPage | Int | 전체 페이지 수 |

전체 VOD를 수집할 때는 이 목록보다 VOD 체인이 정확합니다.
`GET /service/v3/videos/{videoNo}` 의 `nextVideo.videoNo` 를 따라 순회하면 누락이 적습니다. ([VOD 체인 참조](video.md#vod-체인))
이 목록은 체인의 출발점이 되는 최신 `videoNo` 를 얻는 데 사용합니다.

***

## 팔로잉 목록 조회

로그인 사용자가 팔로우한 채널 목록을 조회할 수 있습니다.\
`/live` 는 그중 방송 중인 채널만 반환합니다.\
이 API를 호출하려면 로그인이 필요합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/channels/followings** | 팔로잉 목록 조회 |
| **GET /service/v1/channels/followings/live** | 방송 중인 팔로잉 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| page | Int | * | 요청하는 페이지. 0부터 시작 |
| size | Int | * | 조회할 개수. 505까지 요청 가능한 것을 확인. 상한은 미확인 |
| sortType | String | * | 정렬 방식. `FOLLOW` 확인. 그 외 값은 미확인 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| totalCount | Int | 전체 개수 |
| totalPage | Int | 전체 페이지 수 |
| followingList | Object[] | 팔로잉 목록 |
| followingList.channel | Object | 채널 정보 |
| followingList.streamer.openLive | Boolean | 방송 중 여부 |
| followingList.liveInfo | Object | 방송 중일 때의 제목과 시청자 수 |

***

## 부가 엔드포인트

아래 API는 모두 `GET /service/v1/channels/{channelId}/…` 형태이며 요청 파라미터가 없습니다.
인증이 필요하지 않습니다.

| 경로 | 내용 |
|---|---|
| chat-rules | 채팅 규칙 |
| announcements | 공지 |
| live-schedule | 방송 예정 |
| live-recommended | 추천 라이브 |
| follow | 팔로우 정보 |
| cafe-connection | 카페 연동 |
| achievement-badges | 업적 배지 |
| party-donation-info | 파티 후원 |
| log-power/prediction | 로그파워 예측 |

***

## 관련 문서

[Live](live.md) · [Video](video.md) · [Clip](clip.md) · [Manage](manage.md) · [채널 애널리틱스](../reference/analytics.md) · [엔드포인트 목록](../reference/endpoints.md)
