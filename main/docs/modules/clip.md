# Clip

클립 API로 채널의 클립 목록, 클립 상세 정보, 원본 영상 매핑 정보를 조회할 수 있습니다.\
클립 API는 인증이 필요하지 않습니다.\
클립 뷰어 API 2건은 `CREATOR` 호스트(`https://creatorhub-api.naver.com`)를 사용하며 응답 봉투가 다릅니다. ([응답 봉투 참조](../core/conventions.md#응답-봉투))

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /service/v1/channels/{channelId}/clips** | [채널 클립 목록 조회](#채널-클립-목록-조회) |
| 실측 | **GET /service/v1/clips/{clipUID}/detail** | [클립 상세 조회](#클립-상세-조회) |
| 조회용 POST | **POST /service/v1/clips/detail-bulk** | [클립 벌크 조회](#클립-벌크-조회) |
| 실측 | **GET /service/v1/clips/upload/enable** | [업로드 가능 여부 조회](#업로드-가능-여부-조회) |
| 실측 | **GET /api/v5.0/clipviewer/card** | [클립 뷰어 카드 조회](#클립-뷰어-카드-조회) |
| 실측 | **GET /api/v5.0/clipviewer/cards** | [클립 뷰어 피드 조회](#클립-뷰어-피드-조회) |

클립에 달린 댓글은 댓글 API로 조회합니다. `objectType` 은 `CLIP`, `objectId` 는 `clipUID` 입니다. ([댓글 API 참조](comment.md#objecttype))

***

## 클립 객체

목록 조회, 상세 조회, 벌크 조회가 공통으로 반환하는 객체입니다.

| Field | Type | Description |
|---|---|---|
| clipUID | String | 클립 식별자. 10자 (예: `L0gvjE67xM`) |
| videoId | String | 클립 영상 에셋 식별자. 36자 |
| clipTitle | String | 클립 제목 |
| ownerChannelId | String | 원본 방송 채널 식별자 |
| ownerChannel | Object | 원본 방송 채널 정보. `optionalProperties` 로 요청한 경우에만 반환 |
| makerChannel | Object | 클립을 만든 채널 정보. `optionalProperties` 로 요청한 경우에만 반환 |
| thumbnailImageUrl | String | 썸네일 이미지 URL |
| categoryType | String | 카테고리 분류 (예: `GAME`) |
| clipCategory | String | 카테고리 코드 (예: `Hollow_Knight`) |
| duration | Int | 클립 길이. 단위는 초 |
| adult | Boolean | 성인 제한 여부 |
| createdDate | String | 클립 저장 일시. `YYYY-MM-DD HH:mm:ss`, KST 이며 시간대 표기가 없음 |
| readCount | Int | 조회수 |
| recId | String | 추천 맥락. 문자열로 감싸진 JSON ([참조](../core/conventions.md#문자열로-감싸진-json)) |
| blindType | String | 블라인드 사유 |
| privateUserBlock | Boolean | 차단 여부 |

한 클립은 `clipUID` 와 `videoId` 를 모두 가지며 용도가 다릅니다.
댓글 조회, 상세 조회, 벌크 조회는 `clipUID` 를 사용하고,
클립 뷰어 카드 조회의 `seedMediaId` 는 `videoId` 를 사용합니다.
`seedMediaId` 에 `clipUID` 를 넣었을 때의 동작은 확인되지 않았습니다.

***

## 채널 클립 목록 조회

한 채널의 클립 목록을 조회할 수 있습니다.\
커서 방식으로 페이징하며, 정렬 기준 필드인 `clipUID` 가 커서 역할을 합니다. ([페이지네이션 참조](../core/conventions.md#커서-방식이-특이합니다))

| HTTP Request | Description |
|---|---|
| **GET /service/v1/channels/{channelId}/clips** | 채널 클립 목록 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 조회할 채널 식별자 |
| filterType | String | * | 필터. `ALL` 확인. 그 외 값은 미확인 |
| orderType | String | * | 정렬. `RECENT` 확인. `POPULAR` 는 미확인 |
| size | Int | * | 조회할 클립 개수. 50 확인 |
| clipUID | String | * | 커서. 첫 요청은 빈 값 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| size | Int | 요청한 페이지 크기 |
| data | Object[] | [클립 객체](#클립-객체) 목록 |
| page | Object | 페이지 정보 |
| page.next | Object | 다음 커서. `{ "clipUID": "..." }` 형태이며 마지막 페이지면 `null` |
| page.prev | Object | 이전 커서 |

<details><summary>응답 예시</summary>

```json
{
  "code": 200,
  "content": {
    "size": 50,
    "page": { "next": { "clipUID": "PXHD1Pg1jT" }, "prev": null },
    "data": [{
      "clipUID": "L0gvjE67xM",
      "videoId": "4C6BC202B403BF62556C9DB99EB76A0D53A0",
      "clipTitle": "...",
      "ownerChannelId": "<channelId>",
      "ownerChannel": null,
      "thumbnailImageUrl": "...",
      "categoryType": "GAME", "clipCategory": "Hollow_Knight",
      "duration": 100, "adult": false,
      "createdDate": "2026-07-25 00:43:22",
      "recId": "{...}",
      "readCount": 10, "blindType": null, "privateUserBlock": false
    }]
  }
}
```
</details>

**예제**

```python
def iter_clips(channel_id):
    params = {"filterType": "ALL", "orderType": "RECENT", "size": 50, "clipUID": ""}
    while True:
        content = unwrap(requests.get(
            f"{BASE}/service/v1/channels/{channel_id}/clips",
            params=params, headers=HEADERS))
        yield from content["data"]

        nxt = (content.get("page") or {}).get("next")
        if not nxt or not nxt.get("clipUID"):
            return
        params.update(nxt)
```

***

## 클립 상세 조회

클립 하나의 상세 정보를 조회할 수 있습니다.\
여러 건을 조회할 때는 [클립 벌크 조회](#클립-벌크-조회)를 사용합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/clips/{clipUID}/detail** | 클립 상세 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| clipUID | String | * | 조회할 클립 식별자 |
| optionalProperties | String | optional | 함께 반환할 부가 정보. 콤마 구분이 아니라 반복 파라미터로 전달. `COMMENT` · `PRIVATE_USER_BLOCK` · `PENALTY` · `MAKER_CHANNEL` · `OWNER_CHANNEL` |

```
?optionalProperties=COMMENT&optionalProperties=MAKER_CHANNEL&optionalProperties=OWNER_CHANNEL
```

**Response Body**

| Field | Type | Description |
|---|---|---|
| content | Object | [클립 객체](#클립-객체) |
| content.optionalProperty | Object | 요청한 항목만 채워져 반환 |

`makerChannel` 은 클립을 만든 채널이고 `ownerChannel` 은 원본 방송 채널입니다. 두 값은 서로 다를 수 있습니다.

***

## 클립 벌크 조회

여러 클립의 메타 정보를 한 번에 조회할 수 있습니다.\
메서드는 `POST` 이지만 서버 상태를 변경하지 않는 조회 API 입니다. 요청 본문에 식별자 목록을 담아야 하므로 `GET` 을 쓰지 않습니다.

| HTTP Request | Description |
|---|---|
| **POST /service/v1/clips/detail-bulk** | 클립 벌크 조회 |

**Request Body**

| Field | Type | required | Description |
|---|---|---|---|
| clipUIDList | String[] | * | 조회할 클립 식별자 목록. 한 번에 10개 확인 |
| optionalProperties | String[] | optional | [클립 상세 조회](#클립-상세-조회)와 같은 값. 배열로 전달 |

```json
{
  "clipUIDList": ["IqtvsrPt0w", "CVfAnkGunH", "..."],
  "optionalProperties": ["COMMENT", "PRIVATE_USER_BLOCK", "PENALTY", "MAKER_CHANNEL", "OWNER_CHANNEL"]
}
```

**Response Body**

| Field | Type | Description |
|---|---|---|
| metaMap | Object | `clipUID` 를 키로 하는 [클립 객체](#클립-객체) 맵 |

배열이 아니라 맵으로 반환되므로 요청 순서는 보존되지 않습니다.
존재하지 않는 `clipUID` 를 함께 요청했을 때의 동작은 확인되지 않았으며, `metaMap` 에서 누락되는 것으로 보입니다.

***

## 업로드 가능 여부 조회

클립 업로드 기능의 사용 가능 여부를 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/clips/upload/enable** | 업로드 가능 여부 조회 |

요청 파라미터가 없습니다. 응답은 boolean 플래그 하나로 관측됐으며 전체 스키마는 확인되지 않았습니다.

***

## 클립 뷰어 카드 조회

클립이 원본 방송의 어느 지점에서 잘렸는지 조회할 수 있습니다.\
원본 영상 번호와 시작 위치를 제공하는 유일한 API 입니다.\
이 API는 `https://creatorhub-api.naver.com` 을 사용하며, 응답 봉투가 `header.code == 0` 을 성공으로 씁니다. ([응답 봉투 참조](../core/conventions.md#b형--creator-hub-계열))

벌크 조회가 없어 클립 한 개당 한 번씩 호출해야 합니다. 대량 수집 시에는 메타 정보를 [클립 벌크 조회](#클립-벌크-조회)로 묶고 이 API만 개별 호출합니다.

| HTTP Request | Description |
|---|---|
| **GET /api/v5.0/clipviewer/card** | 클립 뷰어 카드 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| seedMediaId | String | * | 클립의 `videoId`. 36자이며 `clipUID` 와 다름 |
| seedType | String | * | `SPECIFIC` |
| serviceType | String | * | `CHZZK` |
| mediaType | String | * | `SHORT_FORM` |
| recType | String | * | `CHZZK` |
| panelType | String | * | `sdk_chzzk` |
| deviceType | String | * | `html5_mo` |
| referer | String | * | `https://chzzk.naver.com/clips/{clipUID}`. URL 인코딩하여 전달 |
| userInteraction | String | * | `true` |

**Response Body**

| Field | Type | Description |
|---|---|---|
| card | Object | 카드 정보 |
| card.content | Object | 카드 본문 |
| card.content.extraLinks | Object[] | [extraLinks](#extralinks) 목록 |
| card.content.contentId | String | `clipUID` |
| card.content.mediaId | String | 클립 영상 에셋 `videoId` |
| card.content.count | Int | 재생 수 |
| card.content.category | Object | `{ "parent": "GAME", "child": "PCGAMES" }` |
| card.content.mediaScaleType | String | `CROP` |
| card.content.serviceId | Int | `2113`. 치지직 클립 고정값으로 보이나 확인되지 않음 |
| card.content.liveBadge | Object | 방송 중일 때의 라이브 링크 |

### extraLinks

| Field | Type | Description |
|---|---|---|
| type | String | 링크 종류. `TEXT` 는 원본 영상 링크, `GENRE` 는 카테고리 클립 목록 링크 |
| title | String | 원본 방송 제목 |
| link | String | 원본 영상 링크. 형태는 [원본 상태에 따라 달라짐](#원본-상태에-따른-링크-형태) |
| appLink | String | 앱 딥링크 (`navergameapp://`) |

```json
{
  "type": "TEXT",
  "title": "[스텔라이브 롤] 메리 크리스마스 이브",
  "link":    "https://chzzk.naver.com/video/4970352?currentTime=7946",
  "appLink": "navergameapp://chzzk/video/4970352?currentTime=7946"
}
```

`type` 이 `TEXT` 인 항목의 `link` 에서 두 값을 얻습니다.

| 위치 | 값 |
|---|---|
| `/video/{n}` | 원본 영상 번호 `videoNo` |
| `?currentTime={n}` | 원본 영상 기준 클립 시작 위치. 단위는 초 |

`currentTime` 은 클립의 시작점이며 중앙이나 끝점이 아닙니다.
따라서 원본 영상에서 클립이 차지하는 구간은 `[currentTime, currentTime + duration]` 이고 단위는 초입니다.
예를 들어 `currentTime=7946` 은 2시간 12분 26초 지점을 가리킵니다.

다시보기 채팅의 `playerMessageTime` 은 밀리초입니다. 두 값을 함께 다룰 때 단위가 다릅니다. ([다시보기 채팅 참조](video.md#다시보기-채팅-조회))

### 원본 상태에 따른 링크 형태

`link` 의 형태는 원본 방송의 상태에 따라 달라집니다.

| 원본 방송 상태 | link |
|---|---|
| 방송 종료 후 다시보기 생성됨 | `https://chzzk.naver.com/video/{videoNo}?currentTime={초}` |
| 방송 진행 중 | `https://chzzk.naver.com/live/{channelId}` |
| 다시보기 미저장 또는 삭제 | 확인되지 않음 |

`/live/` 형태에는 시작 위치가 없습니다. 경로를 분기하지 않고 파싱하면 `videoNo` 자리에 채널 식별자가 들어갑니다.

```python
from urllib.parse import urlparse, parse_qs

def parse_clip_origin(extra_links):
    for e in extra_links or []:
        if e.get("type") != "TEXT":
            continue
        u = urlparse(e.get("link", ""))
        parts = u.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "video":
            return {
                "title": e.get("title"),
                "videoNo": int(parts[1]),
                "currentTime": int(parse_qs(u.query).get("currentTime", [0])[0]),
            }
    return None
```

### 방송 진행 중일 때의 근사

`link` 가 `/live/` 를 가리켜 시작 위치를 얻을 수 없는 경우, 저장 시각과 방송 시작 시각의 차이로 근사할 수 있습니다.

```
오프셋 ≈ clip.createdDate − live.openDate
구간   ≈ [오프셋 − clip.duration, 오프셋]
```

원본 라이브 시작이 `2026-07-24 19:08:46` 인 캡처에서 확인한 값입니다.

| clipUID | duration | 추정 구간 |
|---|---|---|
| L0gvjE67xM | 100 | 5:32:56 ~ 5:34:36 |
| IqtvsrPt0w | 103 | 5:32:36 ~ 5:34:19 |

`createdDate` 는 클립이 저장된 시각이므로 오차가 수십 초 단위로 발생합니다.
방송이 종료되어 다시보기가 생성되면 `extraLinks` 에서 정확한 값을 다시 조회할 수 있습니다.

### 매니페스트의 시간값

같은 응답의 `vod.playback` 에도 시간값이 있으나 모두 클립 내부 기준입니다. 원본 영상 기준 오프셋은 `extraLinks` 에만 있습니다.

| 위치 | 예시 | 의미 |
|---|---|---|
| `nvod:Thumbnail[n]/@targetTime` | `PT0.000S` ~ `PT1M30.000S` | 클립 내부 썸네일 시각 |
| `nvod:Tracking/nvod:TimeTable` | `[3, 5, 8, 13, 21, 34, 60]` | QoE 전송 시점. 재생 후 n초 |
| `Period/@duration` | `PT1M40.224S` | 클립 길이 |
| `MPD/@nvod:serverTime` · `@expireTime` | ISO 8601 | 매니페스트 서명 및 만료 |

### 확인되지 않은 사항

- 다시보기가 생방송 전체를 담지 않고 앞부분이 잘린 경우, `currentTime` 이 다시보기 기준인지 라이브 기준인지 확인되지 않았습니다. 링크가 그대로 동작해야 하므로 다시보기 기준일 가능성이 높습니다.
- `seedMediaId` 에 `clipUID` 를 사용할 수 있는지 확인되지 않았습니다.

***

## 클립 뷰어 피드 조회

추천 클립 목록을 조회할 수 있습니다.\
특정 클립이 아니라 무한스크롤 피드를 반환합니다.\
이 API는 `https://creatorhub-api.naver.com` 을 사용하며 응답 봉투가 다릅니다.

| HTTP Request | Description |
|---|---|
| **GET /api/v5.0/clipviewer/cards** | 클립 뷰어 피드 조회 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| session | Object | 세션 정보 |
| session.id | String | 세션 식별자. 다음 요청에 `sessionId` 로 전달 |
| session.expireAt | Int | 만료 시각. epoch |
| session.hasMore | Boolean | 다음 페이지 존재 여부 |
| session.pageIndex | Int | 현재 페이지. 0부터 시작 |
| session.pageSize | Int | 페이지 크기. 10 확인 |
| session.enableReverse | Boolean | 역방향 스크롤 가능 여부 |

```json
"session": { "id": "<uuid>", "expireAt": 1784922975, "hasMore": true,
             "pageIndex": 0, "pageSize": 10, "enableReverse": false }
```

추천 맥락은 `recId` 로 전달되며 문자열로 감싸진 JSON 입니다. ([참조](../core/conventions.md#문자열로-감싸진-json))

***

## 관련 문서

[Channel](channel.md) · [Video](video.md) · [Comment](comment.md) · [공통 규칙](../core/conventions.md) · [엔드포인트 목록](../reference/endpoints.md)
