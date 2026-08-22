# Video

VOD API로 다시보기 상세 정보, 다시보기 채팅, 재생 매니페스트를 조회할 수 있습니다.\
인증이 필요하지 않습니다.\
다시보기 채팅은 WebSocket 없이 HTTP만으로 전량 수집할 수 있어 채널 분석의 주 데이터원이 됩니다.

| | |
|---|---|
| Base URL | `https://api.chzzk.naver.com`. 매니페스트만 `apis.naver.com` |
| 응답 봉투 | A형. `code == 200`. 매니페스트만 XML |
| 관련 문서 | [Channel](channel.md) · [Chat](chat.md) · [Comment](comment.md) · [채널 애널리틱스](../reference/analytics.md) |

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /service/v3/videos/{videoNo}** | [VOD 상세 조회](#vod-상세-조회) |
| 실측 | **GET /service/v1/videos/{videoNo}/chats** | [다시보기 채팅 조회](#다시보기-채팅-조회) |
| 실측 | **GET /neonplayer/vodplay/v3/playback/{videoId}** | [재생 매니페스트 조회](#재생-매니페스트-조회) |

`videoNo` 와 `videoId` 는 용도가 다릅니다. ([식별자 참조](../core/conventions.md#식별자))

***

## VOD 객체

[VOD 상세 조회](#vod-상세-조회)가 반환하는 객체입니다.

| Field | Type | Description |
|---|---|---|
| videoNo | Int | VOD 번호. 댓글과 채팅 API가 사용 |
| videoId | String | 재생용 식별자. 36자 |
| videoTitle | String | VOD 제목 |
| videoType | String | `REPLAY` 또는 `UPLOAD` |
| duration | Int | 길이. 단위는 초 |
| livePv | Int | 생방송 당시 시청자 수 |
| readCount | Int | VOD 조회수. `livePv` 와 다른 값 |
| liveOpenDate | String | 원래 방송이 시작된 일시 |
| publishDate | String | VOD가 게시된 일시. `liveOpenDate` 와 다름 |
| publishDateAt | Int | 게시 일시. epoch ms |
| inKey | String | 재생 매니페스트의 `key` 파라미터. 민감 정보 |
| radioModeInKey | String | 라디오 모드용 재생 키 |
| prevVideo | Object | 이전 VOD 요약 |
| nextVideo | Object | 다음 VOD 요약. [VOD 체인](#vod-체인)에 사용 |
| videoChatChannelId | String | 다시보기 채팅용 채팅방 식별자 |
| videoChatEnabled | Boolean | 다시보기 채팅 제공 여부 |
| chapterActive | Boolean | 챕터 사용 여부 |
| chapters | Object[] | 챕터 목록. 빈 배열 사례만 관측 |
| watchTimeline | Int | 시청 위치. 단위는 초. 용도 미확인 |
| vodStatus | String | `ABR_HLS` |
| categoryType | String | 카테고리 분류 ([Enum 참조](../reference/enums.md)) |
| videoCategory | String | 카테고리 코드 |
| channel | Object | `channelId`, `channelName`, `verifiedMark` |
| streamerShopCatalogTagActive | Boolean | 상품 태그 여부 ([스트리머 상점 조회 참조](commerce.md#스트리머-상점-조회)) |
| exposure · adult · blindType | | 노출 제한 정보 |

응답에 재생 키 `inKey` 가 포함됩니다. 원본을 보관하는 것은 무방하나 로그나 화면에 출력하지 않습니다.

### livePv 와 readCount

두 값은 모집단이 다릅니다.

| Field | 의미 |
|---|---|
| livePv | 생방송 당시 시청자 수 |
| readCount | VOD 조회수 |

서로 다른 지표이므로 합산하면 의미가 없습니다.

### liveOpenDate 와 publishDate

`publishDate` 는 VOD가 게시된 시각이며 방송 시작보다 늦습니다.
캡처에서는 18:30에 시작한 방송의 VOD가 19:06에 게시됐습니다.
방송 구간을 계산할 때는 `liveOpenDate` 를 사용합니다.

***

## VOD 상세 조회

VOD 하나의 상세 정보를 조회할 수 있습니다.

경로 버전이 `v3` 입니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v3/videos/{videoNo}** | VOD 상세 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| videoNo | Int | * | 조회할 VOD 번호 |
| dt | String | optional | 빈 값으로 전달. 용도 미확인 |

**Response Body**

`content` 가 [VOD 객체](#vod-객체)입니다.

<details><summary>응답 예시</summary>

```json
{
  "code": 200,
  "content": {
    "videoNo": 14350160,
    "videoId": "89FC02148E88ADA8667456C6A3282113CD28",
    "videoTitle": "...", "videoType": "REPLAY",
    "publishDate": "2026-07-24 19:06:56", "publishDateAt": 1784887616367,
    "thumbnailImageUrl": "...", "trailerUrl": null,
    "duration": 2111, "readCount": 324, "livePv": 9806,
    "categoryType": "ETC", "videoCategory": "talk", "videoCategoryValue": "talk",
    "exposure": true, "adult": false, "clipActive": true, "commentActive": true,
    "tags": ["..."],
    "channel": { "channelId": "...", "channelName": "...", "verifiedMark": true,
                 "activatedChannelBadgeIds": [] },
    "blindType": null, "watchTimeline": 24,
    "paidProductId": null, "tvAppViewingPolicyType": "ALLOWED",

    "liveOpenDate": "2026-07-24 18:30:47",
    "chapterActive": false, "chapters": [],
    "inKey": "<재생 키>", "radioModeInKey": "<라디오모드 키>",
    "previewUrl": "...", "vodStatus": "ABR_HLS",
    "liveRewindPlaybackJson": null, "encryptionType": null,
    "prevVideo": null,
    "nextVideo": { "videoNo": 14324879, "videoId": "...", "videoTitle": "...",
                   "videoType": "REPLAY", "publishDate": "...", "thumbnailImageUrl": "...",
                   "trailerUrl": "..." },
    "videoChatEnabled": true, "videoChatChannelId": "<chatChannelId>",
    "paidProduct": null, "membershipBenefitType": null,
    "adParameter": {...}, "dab": {...},
    "streamerShopCatalogTagActive": false, "aiCaptionActive": false,
    "paidPromotion": false, "userAdultStatus": null
  }
}
```
</details>

### VOD 체인

`nextVideo.videoNo` 를 따라가면 채널의 전체 VOD를 순회할 수 있습니다.
[VOD 목록 조회](channel.md#vod-목록-조회)의 페이지네이션보다 누락이 적습니다.

```python
def walk_vods(start_video_no, headers):
    no = start_video_no
    while no:
        v = unwrap(requests.get(f"{BASE}/service/v3/videos/{no}", headers=headers))
        yield v
        nxt = v.get("nextVideo")
        no = nxt["videoNo"] if nxt else None
```

응답에 고리가 있으면 순회가 끝나지 않습니다. 방문한 `videoNo` 를 기록해 중복을 확인하는 편이 안전합니다.

***

## 다시보기 채팅 조회

VOD에 남은 채팅 로그를 조회할 수 있습니다.\
WebSocket이나 토큰 발급 없이 HTTP만으로 전량 수집할 수 있습니다.\
실시간 수신이 필요한 경우에만 [Chat](chat.md)을 사용합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/videos/{videoNo}/chats** | 다시보기 채팅 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| videoNo | Int | * | 조회할 VOD 번호 |
| playerMessageTime | Int | * | 재생 위치. 단위는 밀리초. 첫 요청은 0 |
| previousVideoChatSize | Int | * | 함께 반환할 이전 채팅 개수. 50 확인 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| nextPlayerMessageTime | Int | 다음 요청에 사용할 `playerMessageTime` |
| videoChats | Object[] | 채팅 메시지 목록 |
| previousVideoChats | Object[] | 이전 채팅 목록 |

**videoChats**

| Field | Type | Description |
|---|---|---|
| playerMessageTime | Int | 재생 위치. 단위는 밀리초 |
| messageTime | Int | 실제 발생 시각. epoch ms |
| content | String | 채팅 내용 |
| messageTypeCode | Int | 메시지 종류. `1` TEXT, `10` DONATION, `11` SUBSCRIPTION, `30` SYSTEM ([Enum 참조](../reference/enums.md#채팅)) |
| messageStatusType | String | 메시지 상태. `NORMAL` 등 |
| userIdHash | String | 작성자 해시. 시스템 메시지는 `SYSTEM_MESSAGE` 리터럴 |
| chatChannelId | String | 채팅방 식별자 |
| extras | String | 문자열로 감싸진 JSON ([참조](../core/conventions.md#문자열로-감싸진-json)) |
| profile | String | 문자열로 감싸진 JSON. 시스템 메시지면 `"{}"` |

```json
{
  "content": {
    "nextPlayerMessageTime": 124168,
    "previousVideoChats": [],
    "videoChats": [{
      "chatChannelId": "N2dboT",
      "messageTime": 1784885547666,
      "playerMessageTime": 96666,
      "userIdHash": "<hash>",
      "content": "채팅 내용",
      "messageTypeCode": 1,
      "messageStatusType": "NORMAL",
      "extras": "{...}",
      "profile": "{...}"
    }]
  }
}
```

`playerMessageTime` 의 단위는 밀리초입니다.
클립의 `currentTime` 은 초 단위이므로 두 값을 함께 다룰 때 단위가 다릅니다. ([클립 뷰어 카드 조회 참조](clip.md#클립-뷰어-카드-조회))

**예제**

`nextPlayerMessageTime` 을 다음 요청의 `playerMessageTime` 으로 전달하여 반복합니다.

```python
def collect_vod_chats(video_no, headers):
    t = 0
    while True:
        c = unwrap(requests.get(
            f"{BASE}/service/v1/videos/{video_no}/chats",
            params={"playerMessageTime": t, "previousVideoChatSize": 50},
            headers=headers,
        ))
        chats = c.get("videoChats") or []
        if not chats:
            return
        yield from chats
        nt = c.get("nextPlayerMessageTime")
        if nt is None or nt <= t:      # 커서가 전진하지 않으면 종료
            return
        t = nt
```

종료 조건은 두 가지입니다. `videoChats` 가 비었거나 `nextPlayerMessageTime` 이 전진하지 않는 경우입니다.
두 번째 조건이 없으면 같은 위치를 계속 요청하게 됩니다.

***

## 재생 매니페스트 조회

VOD의 재생 매니페스트를 조회할 수 있습니다.\
응답이 JSON이 아니라 DASH MPD 형식의 XML이며 응답 봉투가 없습니다.

| HTTP Request | Description |
|---|---|
| **GET https://apis.naver.com/neonplayer/vodplay/v3/playback/{videoId}** | 재생 매니페스트 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| videoId | String | * | 36자 재생용 식별자. `videoNo` 가 아님 |
| key | String | * | [VOD 상세 조회](#vod-상세-조회)의 `inKey`. 라디오 모드는 `radioModeInKey` |
| sid · devt 등 | String | optional | 미검증 |

**Response Body**

`urn:naver:vod:2020` 네임스페이스로 `nvod:Source`, `nvod:TimeTable`, `nvod:SeekingThumbnail` 등이 포함됩니다.

| 요소 | 내용 |
|---|---|
| `MPD/@nvod:serverTime` · `@expireTime` | 매니페스트 서명 및 만료. ISO 8601 |
| `Period/@duration` | 길이. `PT1M40.224S` 형식 |
| `nvod:Thumbnail[n]/@targetTime` | 썸네일 시각 |
| `nvod:Tracking/nvod:TimeTable` | QoE 전송 시점 |

화질 트랙은 `144p`, `360p`, `480p`, `720p`, `1080p`, `alow.stream` 이 관측됐습니다.

클립의 매니페스트에 있는 시간값은 모두 클립 내부 기준입니다. 원본 방송 기준 오프셋이 아닙니다. ([매니페스트의 시간값 참조](clip.md#매니페스트의-시간값))

***

## 관련 문서

[Channel](channel.md) · [Chat](chat.md) · [Comment](comment.md) · [Clip](clip.md) · [채널 애널리틱스](../reference/analytics.md) · [엔드포인트 목록](../reference/endpoints.md)
