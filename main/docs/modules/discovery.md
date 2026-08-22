# Discovery

디스커버리 API로 홈 피드, 카테고리별 라이브, 배너, 라운지 검색 결과를 조회할 수 있습니다.\
인증이 필요하지 않습니다.\
특정 채널이 아니라 서비스 전체를 대상으로 하는 API 묶음입니다.

| | |
|---|---|
| Base URL | `https://api.chzzk.naver.com` · `https://comm-api.game.naver.com/nng_main` |
| 응답 봉투 | A형. `code == 200` ([참조](../core/conventions.md#응답-봉투)) |
| 관련 문서 | [Live](live.md) · [Channel](channel.md) |

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 실측 | **GET /service/v1/topics/HOME/sub-topics/HOME/main** | [홈 메인 피드 조회](#홈-메인-피드-조회) |
| 실측 | **GET /service/v1/categories/live** | [카테고리별 라이브 조회](#카테고리별-라이브-조회) |
| 실측 | **GET /service/v1/topics** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/banners** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/home/skins** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/client-config** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/program-schedules/coming** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /service/v1/streamer-partners/recommended** | [부가 엔드포인트](#부가-엔드포인트) |
| 실측 | **GET /v2/search/lounges** | [라운지 검색](#라운지-검색) |
| 실측 | **GET /v2/search/lounges/auto-complete** | [라운지 검색](#라운지-검색) |
| 실측 | **GET /v1/lounge/loungeEvent/chzzk** | [라운지 검색](#라운지-검색) |

***

## 홈 메인 피드 조회

치지직 홈 첫 화면의 콘텐츠를 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/topics/HOME/sub-topics/HOME/main** | 홈 메인 피드 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| slotSize | Int | * | 슬롯 개수. 5 확인 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| topLives | Object[] | 상위 라이브 목록 |
| topLives.trackingParams | Object | 통계용 파라미터. 조회 결과에 영향 없음 |

***

## 카테고리별 라이브 조회

카테고리를 동시 시청자 수 순으로 조회할 수 있습니다.\
커서 방식으로 페이징합니다.

| HTTP Request | Description |
|---|---|
| **GET /service/v1/categories/live** | 카테고리별 라이브 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| size | Int | * | 조회할 카테고리 개수. 6 확인 |
| concurrentUserCount | Int | optional | 커서. 첫 요청은 생략 |
| openLiveCount | Int | optional | 커서 |
| categoryId | String | optional | 커서 |

**Response Body**

| Field | Type | Description |
|---|---|---|
| data | Object[] | 카테고리 목록 |
| data.categoryType | String | `GAME`, `SPORTS`, `ETC` ([Enum 참조](../reference/enums.md)) |
| data.categoryId | String | 카테고리 코드 (예: `Lost_Ark`) |
| data.categoryValue | String | 카테고리 표시명 |
| data.posterImageUrl | String | 포스터 이미지 URL |
| data.openLiveCount | Int | 해당 카테고리의 방송 수 |
| data.concurrentUserCount | Int | 해당 카테고리의 합산 시청자 수 |
| data.newCategory | Boolean | 신규 카테고리 여부 |
| data.dropsCampaignNos | Int[] | 드롭스 캠페인 번호 |
| page.next | Object | 다음 커서. 마지막 페이지면 `null` |

### 커서가 3개로 구성됩니다

정렬 기준 세 필드가 함께 커서를 구성합니다. ([커서 페이지네이션 참조](../core/conventions.md#커서-방식이-특이합니다))

```json
"page": { "next": { "concurrentUserCount": 7307, "openLiveCount": 172, "categoryId": "Lost_Ark" } }
```

```
?concurrentUserCount=7307&openLiveCount=172&categoryId=Lost_Ark
```

`page.next` 를 그대로 파라미터에 병합합니다. 키를 하나라도 누락하면 정렬 위치가 어긋납니다.

***

## 라운지 검색

네이버 게임 라운지를 검색할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET https://comm-api.game.naver.com/nng_main/v2/search/lounges** | 라운지 검색 |
| **GET https://comm-api.game.naver.com/nng_main/v2/search/lounges/auto-complete** | 라운지 자동완성 |
| **GET https://comm-api.game.naver.com/nng_main/v1/lounge/loungeEvent/chzzk** | 라운지 이벤트 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| offset | Int | * | 조회 시작 위치 ([참조](../core/conventions.md#페이지네이션--3가지-혼재)) |
| size | Int | * | 조회할 개수 |

응답의 `page.next.offset` 을 다음 요청에 사용합니다.

라운지는 네이버 게임 커뮤니티 개념이며 치지직 채널과 1:1로 대응하지 않습니다.
채널 검색이 목적이라면 이 경로가 적합하지 않을 수 있습니다.
채널 검색 전용 경로는 이번 캡처에서 확인되지 않았습니다.

***

## 부가 엔드포인트

경로와 응답 형태는 확인했으나 쿼리 파라미터 조합은 대부분 검증되지 않았습니다.

| 경로 | 내용 | 파라미터 |
|---|---|---|
| `GET /service/v1/topics` | 토픽 목록. 홈 피드의 `HOME/HOME` 외 다른 토픽 존재 | 없음 |
| `GET /service/v1/banners` | 배너 | `deviceType`, `positionsIn` |
| `GET /service/v1/home/skins` | 홈 스킨. 이벤트 테마 | 미검증 |
| `GET /service/v1/client-config` | 클라이언트 설정과 이벤트 배너 | 미검증 |
| `GET /service/v1/program-schedules/coming` | 방송 예정 편성표 | 미검증 |
| `GET /service/v1/streamer-partners/recommended` | 추천 파트너 스트리머 | 미검증 |

***

## 관련 문서

[Live](live.md) · [Channel](channel.md) · [공통 규칙](../core/conventions.md) · [엔드포인트 목록](../reference/endpoints.md)
