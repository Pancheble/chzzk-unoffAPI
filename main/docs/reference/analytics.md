# 채널 애널리틱스

채널 지표를 수집하는 방법을 정리한 문서입니다.\
본인 채널인지 타 채널인지에 따라 사용할 수 있는 API가 완전히 달라집니다.\
본인 채널은 API가 과거 데이터를 제공하고, 타 채널은 공개 지표를 직접 축적해야 합니다.

| | |
|---|---|
| 트랙 A | 본인 채널. 채널 권한 필요 |
| 트랙 B | 타 채널. 인증 불필요 |
| 관련 문서 | [Stats](../modules/stats.md) · [Live](../modules/live.md) · [Video](../modules/video.md) |

| 항목 | 트랙 A — 본인 채널 | 트랙 B — 타 채널 |
|---|---|---|
| 과거 데이터 | API가 제공 | 직접 축적해야 함 |
| 평균·최고 동시 시청자 | `avgCv`, `peakCv` 제공 | 폴링으로 근사 |
| 시청 유지율 | `avgKeepWatchingRate` 제공 | 얻을 수 없음 |
| 필요 조건 | 본인 채널 로그인 | 없음 |

치지직에는 시계열 데이터가 없다고 알려져 있으나 이는 타 채널에 한한 이야기입니다.

***

## 트랙 A — 본인 채널

```
GET /manage/v1/channels/{channelId}/stats/lives?from=YYYY-MM-DD&to=YYYY-MM-DD
GET /manage/v1/channels/{channelId}/stats/videos?from=YYYY-MM-DD&to=YYYY-MM-DD
GET /manage/v1/channels/{channelId}/stats/recent-live
```

쿠키와 본인 채널 권한이 필요합니다. ([Stats 참조](../modules/stats.md))

### 얻을 수 있는 지표

| 지표 | Field |
|---|---|
| 조회수 | pv |
| 순 방문자 수 | uv |
| 평균 동시 시청자 수 | avgCv |
| 최고 동시 시청자 수 | peakCv |
| 총 시청 지속시간 | totalKeepWatchingTime |
| 평균 시청 지속시간 | avgKeepWatchingTime |
| 평균 시청 유지율 | avgKeepWatchingRate |

폴링 없이 과거 데이터를 그대로 조회할 수 있습니다.

### 함께 사용하는 API

| 목적 | 엔드포인트 |
|---|---|
| 팔로워 목록 | `GET /manage/v1/channels/{id}/followers` ([Manage 참조](../modules/manage.md)) |
| 구독자 목록 | `GET /manage/v1/channels/{id}/subscribers?sortType=RECENT` |
| 비공개 포함 VOD 목록 | `GET /manage/v1/channels/{id}/videos` |

### 현재 한계

`liveStatList` 와 `videoStatList` 의 항목 구조가 확인되지 않았습니다.
방송 이력이 없는 채널에서 캡처하여 배열이 비어 있었습니다. ([미확인 항목 참조](../modules/stats.md#미확인--일별-배열-항목-구조))

***

## 트랙 B — 타 채널

공개 지표를 조회하고 시계열은 직접 축적합니다.

### 인증 없이 얻을 수 있는 지표

| 지표 | 엔드포인트 | Field |
|---|---|---|
| 현재 팔로워 수 | [채널 기본 정보 조회](../modules/channel.md#채널-기본-정보-조회) | followerCount |
| 채널 개설일 | [채널 부가 데이터 조회](../modules/channel.md#채널-부가-데이터-조회) | channelHistory.firstLiveDate |
| 누적 방송시간 | [채널 부가 데이터 조회](../modules/channel.md#채널-부가-데이터-조회) | channelHistory.totalLiveHours |
| 현재 동시 시청자 수 | [라이브 상태 조회](../modules/live.md#라이브-상태-조회) | concurrentUserCount |
| 방송 제목·카테고리·태그 | [라이브 상태 조회](../modules/live.md#라이브-상태-조회) | liveTitle, liveCategory, tags |
| VOD 목록 | [VOD 목록 조회](../modules/channel.md#vod-목록-조회) | |
| VOD별 생방송 시청자 수 | [VOD 객체](../modules/video.md#vod-객체) | livePv |
| VOD별 다시보기 조회수 | [VOD 객체](../modules/video.md#vod-객체) | readCount |
| 방송 실제 시작 시각 | [VOD 객체](../modules/video.md#vod-객체) | liveOpenDate |
| 클립 목록과 조회수 | [채널 클립 목록 조회](../modules/clip.md#채널-클립-목록-조회) | readCount |
| 채팅 로그 전량 | [다시보기 채팅 조회](../modules/video.md#다시보기-채팅-조회) | |
| 댓글 전량 | [Comment](../modules/comment.md) | |

### 시계열 축적

```
팔로워 추이  → GET /service/v1/channels/{id}                 1시간 주기 폴링 → followerCount 적재
시청자 추이  → GET /polling/v3.1/channels/{id}/live-status   방송 중 10초 주기 → concurrentUserCount 적재
```

폴링 주기는 응답의 `livePollingStatusJson.callPeriodMilliSecond` 를 따릅니다. 관측값은 10000ms입니다.
이보다 자주 호출하면 IP 차단으로 이어질 수 있습니다.

```python
import json, time

def track_viewers(channel_id, headers, sink):
    while True:
        c = unwrap(requests.get(
            f"{BASE}/polling/v3.1/channels/{channel_id}/live-status",
            params={"includePlayerRecommendContent": "false"}, headers=headers))
        if c["status"] != "OPEN":
            return
        sink(time.time(), c["concurrentUserCount"])
        time.sleep(json.loads(c["livePollingStatusJson"])["callPeriodMilliSecond"] / 1000)
```

### VOD 전수 수집

`nextVideo.videoNo` 를 따라가면 채널의 모든 VOD를 순회할 수 있습니다.
목록 API의 페이지네이션보다 누락이 적습니다. ([VOD 체인 참조](../modules/video.md#vod-체인))

***

## 수집 시 주의할 필드

### accumulateCount 는 항상 0입니다

`live-status` 와 `live-detail` 양쪽 모두 0으로 관측됐습니다. 필드 자체가 채워지지 않습니다.

| 필요한 값 | 대체 |
|---|---|
| 방송 종료 후 누적 시청자 | VOD의 `livePv` |
| 방송 중 누적 시청자 | `concurrentUserCount` 를 직접 집계 |

### concurrentUserCount 가 API마다 다릅니다

| 엔드포인트 | 관측값 |
|---|---|
| `polling/v3.1/.../live-status` | 1926 |
| `service/v3.3/.../live-detail` | 4866 |

캡처 시점 차이일 가능성이 있으나 확인되지 않았습니다.
시계열로 축적할 때는 한쪽 API로 통일합니다. 폴링 비용이 낮은 `live-status` 를 권장합니다.

### livePv 와 readCount 는 다른 값입니다

| Field | 의미 |
|---|---|
| livePv | 생방송 당시 시청자 수 |
| readCount | VOD 다시보기 조회수 |

모집단이 다르므로 합산하거나 혼용하지 않습니다.

***

## 타 채널에서 얻을 수 없는 지표

아래 지표는 스튜디오 전용이며 타 채널에서는 어떤 방법으로도 조회할 수 없습니다.

시청 지속시간, 유입 경로, 시청자 연령과 성별, 팔로워 증감 상세, 정산과 수익입니다.

타 채널 분석은 위에 정리한 공개 지표와 자체 폴링이 한계입니다.

***

## 수집 시 주의

댓글과 채팅 응답에는 다른 이용자의 닉네임과 `userIdHash` 가 포함됩니다. 개인정보 취급에 유의합니다.

요청 사이에 간격을 둡니다. 과도한 폴링은 IP 차단으로 이어집니다.

스튜디오를 캡처하는 경우 `streaming-info` 의 스트림 키가 응답에 포함됩니다. ([스트리밍 정보 조회 참조](../modules/manage.md#스트리밍-정보-조회))
