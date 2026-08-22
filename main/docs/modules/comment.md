# Comment

댓글 API로 VOD, 채널 게시글, 클립에 달린 댓글과 대댓글을 조회할 수 있습니다.\
세 대상이 같은 엔드포인트를 사용하며 `objectType` 으로 구분합니다.\
인증이 필요하지 않습니다.

| | |
|---|---|
| Base URL | `https://apis.naver.com/nng_main/nng_comment_api` · `https://creatorhub-api.naver.com` |
| 응답 봉투 | A형. `code == 200`. 스티커 2건만 B형 `header.code == 0` |
| 관련 문서 | [Video](video.md) · [Clip](clip.md) |

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /v1/type/{objectType}/id/{objectId}/comments** | [댓글 목록 조회](#댓글-목록-조회) |
| 실측 | **GET /v1/type/{objectType}/id/{objectId}/comments/{commentId}/replyComments** | [대댓글 조회](#대댓글-조회) |
| 실측 | **GET /api/v4.0/comment/sticker/pack** | [스티커 조회](#스티커-조회) |
| 실측 | **GET /api/v4.0/comment/sticker** | [스티커 조회](#스티커-조회) |

스티커 2건은 `https://creatorhub-api.naver.com` 을 사용하며 응답 봉투가 B형입니다.
기능이 댓글 첨부이므로 이 문서에 수록합니다. ([응답 봉투 참조](../core/conventions.md#b형--creator-hub-계열))

***

## objectType

댓글 대상은 세 가지이며 타입마다 `objectId` 의 체계가 다릅니다.

| objectType | objectId | 형태 | 대상 |
|---|---|---|---|
| STREAMING_VIDEO | videoNo | Int | VOD 댓글 |
| CHANNEL_POST | channelId | 32자 hex | 채널 커뮤니티 게시글 댓글 |
| CLIP | clipUID | 10자 | 클립 댓글 |

`CLIP` 의 `objectId` 는 `clipUID` 이며 36자 `videoId` 가 아닙니다.
`CHANNEL_POST` 의 `objectId` 도 게시글 번호가 아니라 `channelId` 입니다.

***

## 댓글 객체

목록 조회와 대댓글 조회가 공통으로 반환하는 객체입니다.

| Field | Type | Description |
|---|---|---|
| comment.commentId | Int | 댓글 식별자 |
| comment.commentType | String | `COMMENT` 또는 `REPLY` |
| comment.content | String | 본문. 스티커만 첨부한 경우 빈 문자열 |
| comment.replyCount | Int | 대댓글 수 ([아래 참조](#replycount-를-신뢰해도-됩니다)) |
| comment.parentCommentId | Int | 부모 댓글 식별자. 최상위 댓글은 0 |
| comment.mentionedUserIdHash | String | 답글 대상 사용자 해시 |
| comment.mentionedUserNickname | String | 답글 대상 닉네임 |
| comment.secret | Boolean | 비밀 댓글 여부 |
| comment.hideByCleanBot | Boolean | 클린봇 자동 숨김 여부 |
| comment.deleted | Boolean | 삭제 여부 |
| comment.createdDate | String | 작성 일시. `YYYYMMDDHHmmss` 형식 |
| comment.attaches | Object[] | [첨부 목록](#첨부) |
| comment.objectType | String | 댓글 대상 종류 |
| comment.objectId | String | 댓글 대상 식별자 |
| comment.childObjectCount | Int | 대댓글 수. `replyCount` 와 별도로 존재하며 차이는 미확인 |
| comment.childCommentActive | Boolean | 대댓글 허용 여부 |
| user.userIdHash | String | 작성자 해시. 개인정보 |
| user.userNickname | String | 작성자 닉네임. 개인정보 |
| user.userRoleCode | String | 작성자 역할 (예: `common_user`) |
| user.writer | Boolean | 영상 작성자 본인 여부 |
| user.privateUserBlock | Boolean | 차단한 사용자 여부 ([차단 목록 조회 참조](user.md#차단-목록-조회)) |
| buffNerf.buffCount | Int | 추천 수 |
| buffNerf.nerfCount | Int | 비추천 수 |

### 첨부

| Field | Type | Description |
|---|---|---|
| attachType | String | `PHOTO` 또는 `STICKER` |
| attachValue | String | 이미지 URL 또는 스티커 코드 |
| extraJson | String | `PHOTO` 면 width와 height, `STICKER` 면 `null`. 문자열로 감싸진 JSON |
| order | Int | 표시 순서 |
| createdDate | String | 첨부 일시. ISO 8601 형식 |

***

## 댓글 목록 조회

대상에 달린 댓글 목록을 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /v1/type/{objectType}/id/{objectId}/comments** | 댓글 목록 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| objectType | String | * | 댓글 대상 종류. [3종](#objecttype) |
| objectId | String | * | 댓글 대상 식별자. 타입마다 체계가 다름 |
| limit | Int | * | 조회할 댓글 개수. 30 확인 |
| offset | Int | * | 조회 시작 위치. 0부터 시작 ([참조](../core/conventions.md#페이지네이션--3가지-혼재)) |
| orderType | String | * | 정렬 방식. `POPULAR` 인기순, `DESC` 최신순, `ASC` 오래된순 |
| pagingType | String | * | `PAGE` |

최신순 값이 `NEW` 가 아니라 `DESC` 입니다.

**Response Body**

| Field | Type | Description |
|---|---|---|
| commentActive | Boolean | 댓글 허용 여부 |
| totalCount | Int | 전체 댓글 수 |
| commentCount | Int | 전체 댓글 수. `totalCount` 와 병존하는 이유는 미확인 |
| comments.page | Object | 페이지 정보 |
| comments.data | Object[] | [댓글 객체](#댓글-객체) 목록 |

<details><summary>응답 예시</summary>

```json
{
  "code": 200,
  "content": {
    "comments": {
      "page": { "next": null, "prev": null },
      "data": [{
        "comment": {
          "commentId": 27576679,
          "commentType": "COMMENT",
          "replyCount": 0,
          "parentCommentId": 0,
          "content": "댓글 내용",
          "mentionedUserIdHash": null,
          "mentionedUserNickname": null,
          "secret": false,
          "hideByCleanBot": false,
          "deleted": false,
          "createdDate": "20260724191415",
          "attaches": [{
            "commentId": 27576679,
            "attachType": "PHOTO",
            "attachValue": "https://nng-phinf.pstatic.net/...",
            "extraJson": "{\"width\":360,\"height\":194}",
            "order": 1,
            "createdDate": "2026-07-24T10:56:45.000+00:00"
          }],
          "objectType": "STREAMING_VIDEO",
          "objectId": "14350160",
          "loungeId": null,
          "onlyOneEmoji": false,
          "childObjectCount": 0,
          "childCommentActive": true
        },
        "user": {
          "userIdHash": "<hash>",
          "userNickname": "<nickname>",
          "profileImageUrl": "...",
          "userLevel": 0,
          "writer": false,
          "badge": null,
          "title": null,
          "userRoleCode": "common_user",
          "secretOpen": false,
          "buffnerf": null,
          "privateUserBlock": false,
          "verifiedMark": false,
          "activatedChannelBadgeIds": []
        },
        "buffNerf": { "buffCount": 2, "nerfCount": 0 }
      }]
    }
  }
}
```
</details>

### 날짜 형식이 두 가지입니다

| 위치 | 형식 |
|---|---|
| comment.createdDate | `YYYYMMDDHHmmss` |
| attaches.createdDate | ISO 8601 |

```python
from datetime import datetime
dt = datetime.strptime(c["comment"]["createdDate"], "%Y%m%d%H%M%S")
```

***

## 대댓글 조회

특정 댓글에 달린 대댓글 목록을 조회할 수 있습니다.

경로가 `replies` 가 아니라 `replyComments` 입니다.

| HTTP Request | Description |
|---|---|
| **GET /v1/type/{objectType}/id/{objectId}/comments/{commentId}/replyComments** | 대댓글 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| objectType | String | * | 댓글 대상 종류 |
| objectId | String | * | 댓글 대상 식별자 |
| commentId | Int | * | 부모 댓글 식별자 |
| offset | Int | * | 조회 시작 위치. 0부터 시작. `limit` 은 없음 |

**Response Body**

[댓글 객체](#댓글-객체)와 같으며 아래 필드의 값이 다릅니다.

| Field | 최상위 댓글 | 대댓글 |
|---|---|---|
| commentType | `COMMENT` | `REPLY` |
| parentCommentId | 0 | 부모 댓글 식별자 |
| mentionedUserNickname · mentionedUserIdHash | `null` | 답글 대상 정보가 채워짐 |
| commentCount | 반환됨 | 반환되지 않음 |
| totalCount | 전체 댓글 수 | 대댓글 총 개수 |

### replyCount 를 신뢰해도 됩니다

부모 댓글의 `replyCount` 와 대댓글 응답의 `totalCount` 가 일치하는 것을 확인했습니다. 3건과 8건 두 사례에서 모두 일치했습니다.
따라서 `replyCount` 가 0이면 대댓글 조회를 생략할 수 있습니다.

**예제**

```python
def collect_all(object_type, object_id, headers):
    for item in iter_comments(object_type, object_id, headers):
        yield item
        if item["comment"]["replyCount"] > 0:      # 0이면 요청 생략
            yield from iter_replies(
                object_type, object_id, item["comment"]["commentId"], headers)
```

***

## 스티커 조회

댓글에 첨부된 스티커 정보를 조회할 수 있습니다.\
`attaches` 의 `attachType` 이 `STICKER` 인 항목을 해석할 때 사용합니다.\
이 API는 `https://creatorhub-api.naver.com` 을 사용하며 응답 봉투가 B형입니다.

| HTTP Request | Description |
|---|---|
| **GET /api/v4.0/comment/sticker/pack** | 스티커 팩 목록 조회 |
| **GET /api/v4.0/comment/sticker** | 팩 내 스티커 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| stickerServiceCode | String | * | `chzzk`. 두 API 공통 |
| packCode | String | * | 스티커 팩 코드. `/sticker` 에만 사용 |

성공 조건이 `header.code == 0` 입니다. A형과 같은 방식으로 판정하면 정상 응답을 실패로 처리하게 됩니다. ([응답 봉투 참조](../core/conventions.md#응답-봉투))

***

## 개인정보

댓글 응답에는 다른 이용자의 닉네임과 `userIdHash` 가 포함됩니다. 수집·보관 시 개인정보 취급에 유의합니다.

***

## 관련 문서

[Video](video.md) · [Clip](clip.md) · [User](user.md) · [공통 규칙](../core/conventions.md) · [엔드포인트 목록](../reference/endpoints.md)
