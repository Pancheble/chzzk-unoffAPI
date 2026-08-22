# 공통 규칙

응답 봉투, 페이지네이션, 문자열 JSON, 식별자 네 가지를 다룹니다.\
모듈 문서를 읽기 전에 확인해 두면 나머지 문서를 이해하기 쉽습니다.

***

## 응답 봉투

호스트마다 응답 봉투의 형태와 성공 조건이 다릅니다.

### A형 — 치지직 계열

`api.chzzk.naver.com`, `comm-api.game.naver.com`, `nng_comment_api` 가 사용합니다.

```json
{ "code": 200, "message": null, "content": { } }
```

HTTP 상태 코드가 200이어도 `code` 가 200이 아닐 수 있습니다. `code` 로 판정합니다.

### B형 — Creator Hub 계열

`creatorhub-api.naver.com` 이 사용합니다.

```json
{ "header": { "code": 0, "message": "" }, "body": { } }
```

성공 조건이 `0` 입니다. A형과 같은 코드로 판정하면 정상 응답을 실패로 처리하게 됩니다.

### C형 — 통계 수집기

```json
{ "result_code": 1, "result_data": { "message": "success" } }
```

이 문서는 읽기 전용 API만 다루므로 C형을 반환하는 엔드포인트는 수록하지 않았습니다. 참고용으로만 기재합니다.

### 파싱

```python
def unwrap(resp):
    j = resp.json()
    if "content" in j:                      # A형
        if j.get("code") != 200:
            raise RuntimeError(f'code={j.get("code")} {j.get("message")}')
        return j["content"]
    if "body" in j:                         # B형
        if j.get("header", {}).get("code") != 0:
            raise RuntimeError(j["header"].get("message"))
        return j["body"]
    raise RuntimeError("unknown envelope")
```

***

## 페이지네이션 — 3가지 혼재

세 가지 방식이 함께 쓰입니다.

| 방식 | 요청 파라미터 | 응답 | 사용처 |
|---|---|---|---|
| page | `page`, `size`, `pagingType=PAGE` | `totalCount`, `totalPage` | 팔로잉, VOD, 댓글 |
| offset | `offset`, `size` | `page.next.offset` | 검색, 대댓글 |
| cursor | 정렬 기준 필드 자체 | `page.next.{키}` | 클립, 카테고리 |

### 커서 방식이 특이합니다

커서 방식은 별도의 커서 토큰을 쓰지 않고, 정렬 기준이 되는 필드 자체를 다음 페이지 키로 사용합니다.

```json
// 클립: 다음 요청에 clipUID=PXHD1Pg1jT
"page": { "next": { "clipUID": "PXHD1Pg1jT" }, "prev": null }

// 카테고리: 정렬 기준 3개가 함께 커서를 구성
"page": { "next": { "concurrentUserCount": 7307, "openLiveCount": 172, "categoryId": "Lost_Ark" } }
```

`page.next` 가 `null` 이면 마지막 페이지입니다.

```python
def paginate_cursor(url, params, headers):
    while True:
        content = unwrap(requests.get(url, params=params, headers=headers))
        yield from content["data"]
        nxt = content.get("page", {}).get("next")
        if not nxt:
            return
        params.update(nxt)      # 커서 키를 그대로 파라미터에 병합
```

***

## 문자열로 감싸진 JSON

아래 필드는 JSON 객체가 아니라 JSON 문자열로 반환됩니다. 한 번 더 파싱해야 합니다.

| Field | 위치 |
|---|---|
| livePlaybackJson | 라이브 상세 |
| livePollingStatusJson | 라이브 상태 |
| recId | 클립 목록, Creator Hub 카드 |
| extras | 채팅 메시지 |
| profile | 채팅 메시지. 시스템 메시지면 `"{}"` |
| extraJson | 댓글 첨부. `PHOTO` 면 width·height, `STICKER` 면 `null` |

```python
import json
playback = json.loads(content["livePlaybackJson"])
```

***

## 식별자

| 이름 | 형태 | 설명 |
|---|---|---|
| channelId | 32자 hex | 채널 고유 식별자 |
| liveId | Int. 8자리 | 방송 세션 식별자. 방송을 켤 때마다 새로 발급 |
| chatChannelId | `N` + 5자 | 채팅방 식별자. 방송마다 변경 |
| videoNo | Int | VOD 번호. 댓글과 조회 API가 사용 |
| videoId | 36자 대문자 hex | VOD 재생용 식별자 |
| clipUID | 10자 영숫자 | 클립 식별자 (예: `L0gvjE67xM`) |
| userIdHash | 32자 hex | 사용자 해시 |
| sessionIOChannelId | `{type}@{...}` | 알림 이벤트 세션 식별자 |

### 헷갈리는 3쌍

**channelId 와 userIdHash**

두 값 모두 32자 hex로 형식이 같습니다. 스트리머 본인은 두 값이 동일합니다.

**videoNo 와 videoId**

| 식별자 | 사용처 |
|---|---|
| videoNo (Int) | VOD 상세, 다시보기 채팅, 댓글 |
| videoId (36자) | 재생 매니페스트, Creator Hub `seedMediaId` |

**clipUID 와 클립의 videoId**

클립도 두 식별자를 함께 가집니다.
댓글 조회는 `clipUID` 를, Creator Hub 카드 조회는 `videoId` 를 사용합니다.
([Clip 참조](../modules/clip.md) · [Comment 참조](../modules/comment.md#objecttype))

***

## 관련 문서

[Base URL](base-urls.md) · [필수 요청 헤더](headers.md) · [인증](auth.md)
