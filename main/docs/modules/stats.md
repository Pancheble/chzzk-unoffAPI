# Stats

통계 API로 본인 채널의 방송별 통계와 VOD별 통계를 조회할 수 있습니다.\
이 API를 호출하려면 본인 채널 권한이 필요합니다.\
타 채널의 통계는 조회할 수 없습니다.

| | |
|---|---|
| Base URL | `https://api.chzzk.naver.com/manage/v1` |
| 응답 봉투 | A형. `code == 200` ([참조](../core/conventions.md#응답-봉투)) |
| 관련 문서 | [Manage](manage.md) · [채널 애널리틱스](../reference/analytics.md) |

치지직 API에는 시계열 데이터가 없어 직접 폴링해서 축적해야 한다고 알려져 있으나, 이는 타 채널에 한한 이야기입니다.
본인 채널은 이 API로 과거 통계를 조회할 수 있습니다.
폴링 수집은 타 채널을 분석할 때만 필요합니다. ([채널 애널리틱스 참조](../reference/analytics.md))

***

## 엔드포인트

| 상태 | HTTP Request | Description |
|---|---|---|
| 스키마 미상 | **GET /channels/{channelId}/stats/lives** | [방송별 통계 조회](#방송별-통계-조회) |
| 스키마 미상 | **GET /channels/{channelId}/stats/videos** | [VOD별 통계 조회](#vod별-통계-조회) |
| 스키마 미상 | **GET /channels/{channelId}/stats/recent-live** | [최근 방송 통계 조회](#최근-방송-통계-조회) |

경로, 인증, 파라미터는 확정됐으나 배열 항목의 구조는 확인되지 않았습니다. ([아래 참조](#미확인--일별-배열-항목-구조))

***

## 방송별 통계 조회

기간 내 방송별 통계를 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /channels/{channelId}/stats/lives** | 방송별 통계 조회 |

**Request Param**

| Field | Type | required | Description |
|---|---|---|---|
| channelId | String | * | 본인 채널 식별자 |
| from | String | * | 조회 시작일. `YYYY-MM-DD` |
| to | String | * | 조회 종료일. `YYYY-MM-DD` |

**Response Body**

| Field | Type | Description |
|---|---|---|
| liveStatList | Object[] | 방송별 통계 목록. 항목 구조 미확인 |
| summaryLiveStat | Object | 요약. 스키마 미확인 |

***

## VOD별 통계 조회

기간 내 VOD별 통계를 조회할 수 있습니다.\
이 모듈에서 요약 스키마가 확정된 유일한 API입니다.

| HTTP Request | Description |
|---|---|
| **GET /channels/{channelId}/stats/videos** | VOD별 통계 조회 |

**Request Param**

[방송별 통계 조회](#방송별-통계-조회)와 같습니다.

**Response Body**

| Field | Type | Description |
|---|---|---|
| videoStatList | Object[] | VOD별 통계 목록. 항목 구조 미확인 |
| summaryVideoStat | Object | 요약. 필드 의미 확정 |

**summaryVideoStat**

| Field | Type | Description |
|---|---|---|
| pv | Int | 조회수 |
| uv | Int | 순 방문자 수 |
| avgCv | Int | 평균 동시 시청자 수 |
| peakCv | Int | 최고 동시 시청자 수 |
| totalKeepWatchingTime | Int | 총 시청 지속시간 |
| avgKeepWatchingTime | Int | 평균 시청 지속시간 |
| avgKeepWatchingRate | Number | 평균 시청 유지율 |
| duration | Int | 길이 |
| date | String | 날짜 |

`avgCv`, `peakCv`, `avgKeepWatchingRate` 는 공개 API로는 얻을 수 없는 값입니다.
공개 API의 `concurrentUserCount` 는 특정 시점의 스냅샷이고 `livePv` 는 누적 조회수이므로 대체할 수 없습니다.

***

## 최근 방송 통계 조회

가장 최근 방송의 통계를 조회할 수 있습니다.

| HTTP Request | Description |
|---|---|
| **GET /channels/{channelId}/stats/recent-live** | 최근 방송 통계 조회 |

요청 파라미터가 없습니다. 캡처에서 응답 전체가 `null` 로 관측됐습니다.

***

## 미확인 — 일별 배열 항목 구조

캡처한 채널에 방송 이력이 없어 배열이 모두 비어 있었습니다.

| 응답 필드 | 관측값 |
|---|---|
| liveStatList | 빈 배열 |
| videoStatList | 빈 배열 |
| summaryLiveStat | `null` |
| recent-live 전체 | `null` |

확인되지 않은 사항은 다음과 같습니다.

- `liveStatList` 항목 하나의 필드 구성
- `videoStatList` 항목이 `summaryVideoStat` 과 같은 필드를 사용하는지 여부
- `summaryLiveStat` 이 `summaryVideoStat` 과 같은 스키마인지 여부
- 일별 집계인지 방송별 집계인지 여부

본인 채널로 방송을 진행한 뒤 다음 날 스튜디오를 재캡처하면 일괄 확인할 수 있습니다.
같은 캡처로 [Manage의 스키마 미상 11건](manage.md#응답-스키마-미상--11건)도 함께 확인됩니다.

재캡처 시 응답 본문까지 스크럽해야 합니다. 같은 세션에 `streaming-info` 의 스트림 키가 포함됩니다. ([스트리밍 정보 조회 참조](manage.md#스트리밍-정보-조회))

***

## 본인 채널 한정

타 채널의 통계는 이 API로 조회할 수 없습니다.

| 대상 | 방법 |
|---|---|
| 본인 채널 | 이 문서의 API로 과거 데이터 조회 |
| 타 채널 | 공개 지표와 자체 폴링 ([트랙 B 참조](../reference/analytics.md#트랙-b--타-채널)) |

시청 지속시간, 유입 경로, 시청자 연령과 성별, 팔로워 증감 상세, 정산과 수익은 모두 스튜디오 전용입니다.

***

## 관련 문서

[Manage](manage.md) · [채널 애널리틱스](../reference/analytics.md) · [공통 규칙](../core/conventions.md) · [엔드포인트 목록](../reference/endpoints.md)
