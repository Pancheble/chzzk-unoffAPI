# 치지직(CHZZK) 비공식 API 문서

네이버 치지직 웹 프론트엔드가 사용하는 내부 API를 캡처하여 정리한 비공식 문서입니다.\
공식 문서가 아니며, 네이버는 이 API들의 하위 호환성을 보장하지 않습니다.\
상업적 서비스를 개발하는 경우 [치지직 개발자센터](https://developers.chzzk.naver.com)의 공식 API를 사용합니다.

| | |
|---|---|
| 수록 엔드포인트 | 115건. 이름 확인 95건 + [미확보 20건](modules/manage.md#미수록-경로) ([전체 목록](reference/endpoints.md)) |
| 캡처 기준일 | 2026-07-25 (클립·웹) · 2026-07-29 (스튜디오·댓글) |
| 범위 | 읽기 전용. `GET`, WebSocket 수신, [조회용 `POST` 1건](reference/deprecated.md#예외--조회용-post-1건) |
| 인증 | 공개 조회는 불필요. 일부 API만 쿠키 필요 ([인증 참조](core/auth.md)) |
| 응답 봉투 | 3형이 혼재하며 성공 조건이 다릅니다 ([응답 봉투 참조](core/conventions.md#응답-봉투)) |

서버 상태를 변경하는 요청(`POST`, `PUT`, `DELETE`)은 수록하지 않았습니다.
방송 설정 변경, 제재 관리, 금지어 편집, 시청 이벤트 전송 등이 해당합니다.
제외 목록과 사유는 [제외된 API](reference/deprecated.md)에 있습니다.

***

## 빠른 시작

인증 없이 호출할 수 있습니다.
다만 커스텀 헤더가 없으면 상당수의 API가 실패합니다. ([필수 헤더 참조](core/headers.md))

```python
import requests

BASE = "https://api.chzzk.naver.com"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://chzzk.naver.com",
    "Referer": "https://chzzk.naver.com/",
    "front-client-platform-type": "PC",
    "front-client-product-type": "web",
    "deviceId": "00000000-0000-4000-8000-000000000000",  # UUID v4 하나를 고정해 사용
}

cid = "<32자 channelId>"

# 채널 기본 정보
ch = requests.get(f"{BASE}/service/v1/channels/{cid}", headers=HEADERS).json()
print(ch["content"]["channelName"], ch["content"]["followerCount"])

# 라이브 상태
st = requests.get(
    f"{BASE}/polling/v3.1/channels/{cid}/live-status",
    params={"includePlayerRecommendContent": "false"}, headers=HEADERS,
).json()
print(st["content"]["status"], st["content"]["concurrentUserCount"])
```

***

## 오류 처리

HTTP 상태 코드가 200이어도 실패일 수 있습니다. 응답 봉투 안의 코드로 판정합니다.\
호스트마다 봉투 형태와 성공 조건이 다릅니다.

| 봉투 | 호스트 | 성공 조건 | 실패 시 |
|---|---|---|---|
| A형 | `api.chzzk.naver.com` · `comm-api` · `nng_comment_api` | `code == 200` | `message` 에 사유 |
| B형 | `creatorhub-api.naver.com` | `header.code == 0` | `header.message` 에 사유 |
| XML | `apis.naver.com/neonplayer` | 봉투 없음 (DASH MPD) | — |

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

봉투가 성공을 반환하면서 내용이 비어 있는 경우가 있습니다.

| 상황 | 판정 방법 |
|---|---|
| 존재하지 않는 채널 | `code: 200` 이면서 `channelId` 가 `null` ([참조](modules/channel.md#채널-기본-정보-조회)) |
| 데이터가 없는 스튜디오 통계 | 빈 배열 또는 `null` ([참조](modules/stats.md#미확인--일별-배열-항목-구조)) |
| 쿠키 만료 | HTTP 401이 아니라 `loggedIn: false` ([참조](modules/user.md#로그인-상태-조회)) |

전체 규약은 [응답 봉투](core/conventions.md#응답-봉투)에 있습니다.

***

## 요청 제한

공식적으로 문서화된 rate limit은 없습니다. 아래는 관측값과 안전 마진을 기준으로 한 권장 사항입니다.

| 상황 | 권장 |
|---|---|
| 방송 중 라이브 폴링 | 응답의 `livePollingStatusJson.callPeriodMilliSecond` 를 따름. 관측값 10000ms |
| 대량 수집 (클립·VOD·채팅) | 요청 사이에 간격을 둠. 배치 작업이라도 몰아서 호출하면 IP 차단 위험 |
| 재시도 | `429` 와 `5xx` 에만 지수 백오프. 나머지 `4xx` 는 재시도해도 결과가 같음 |

권장 주기보다 자주 호출하면 IP 차단이나 계정 보호조치로 이어질 수 있습니다.
[클립 뷰어 카드 조회](modules/clip.md#클립-뷰어-카드-조회)는 벌크 조회가 없어 클립 한 개당 한 번씩 호출해야 하므로 특히 주의가 필요합니다.

***

## 민감 정보

아래 값은 공유하거나 저장소에 커밋해서는 안 됩니다.

| 값 | 출처 | 위험 |
|---|---|---|
| streamKey · streamUrl | [스트리밍 정보 조회](modules/manage.md#스트리밍-정보-조회) | 제3자가 해당 채널로 송출 가능 |
| accTkn | [액세스 토큰 발급](modules/chat.md#액세스-토큰-발급) | 채팅 계정 도용 |
| liveTokenList | [라이브 상태 조회](modules/live.md#라이브-상태-조회) | 시청 이벤트 위조 |
| extraToken | [채팅 메시지 extras](modules/chat.md#extras) | 시청 이벤트 위조 |
| Socket.IO auth | [알림 소켓 URL 발급](modules/notification.md#알림-소켓-url-발급) | 개인 알림 수신 |
| NID_AUT · NID_SES | 브라우저 쿠키 | 계정 자격증명 |

크롬의 sanitized HAR 내보내기는 쿠키와 요청 헤더만 제거하며 응답 본문은 지우지 않습니다.
스튜디오 화면을 캡처하면 `streamKey` 가 평문으로 HAR에 남습니다.
HAR을 공유하거나 커밋하기 전에 응답 본문까지 제거하는 별도 스크럽이 필요합니다.

댓글과 채팅 응답에는 다른 이용자의 닉네임과 `userIdHash` 가 포함됩니다. 수집·보관 시 개인정보 취급에 유의합니다.

***

## 이름과 기능이 다른 엔드포인트

경로 이름만으로 기능을 판단하면 잘못된 API를 호출하게 되는 경우가 있습니다.

| 경로 | 실제 기능 |
|---|---|
| `POST /service/live-status` | 라이브 상태가 아니라 행동 로그 수집기. 이 문서에서 제외 |
| `GET /polling/live-detail` | 라이브 상세가 아니라 [A/B 테스트 배정 조회](modules/live.md#ab-테스트-배정-조회) |
| `GET /polling/v3.1/.../live-status` | [라이브 상태 조회](modules/live.md#라이브-상태-조회) |
| `GET /service/v3.3/.../live-detail` | [라이브 상세 조회](modules/live.md#라이브-상세-조회) |
| `GET /service/v1/personal/session-url` | 개인 데이터가 아니라 [알림 소켓 URL 발급](modules/notification.md#알림-소켓-url-발급) |
| `wss://ssio{N}.nchat.naver.com` | 채팅이 아니라 [개인 알림 채널](modules/notification.md) |

정정 내역 전체는 [정정된 사실](reference/deprecated.md#잘못-알려져-있던-사실)에 있습니다.

***

## 문서 구성

**요청 규약**

| 문서 | 내용 |
|---|---|
| [Base URL](core/base-urls.md) | 호스트 7종과 용도 |
| [필수 요청 헤더](core/headers.md) | 커스텀 헤더. 없으면 상당수가 실패 |
| [공통 규칙](core/conventions.md) | 응답 봉투 3형, 페이지네이션 3종, 식별자 |
| [인증](core/auth.md) | 쿠키 인증과 권한 3단계 |

**기능 모듈**

| 문서 | 건수 | 내용 |
|---|---|---|
| [Channel](modules/channel.md) | 15 | 채널 조회, 부가 데이터, 팔로잉 |
| [Live](modules/live.md) | 5 | 라이브 상세·상태, 폴링 |
| [Video](modules/video.md) | 3 | VOD 상세, 다시보기 채팅, 재생 매니페스트 |
| [Clip](modules/clip.md) | 6 | 클립 목록·상세·벌크, 원본 영상 매핑 |
| [Comment](modules/comment.md) | 4 | 댓글, 대댓글, 스티커 |
| [Chat](modules/chat.md) | 3 | 실시간 채팅. 수신 전용 |
| [Notification](modules/notification.md) | 4 | 개인 알림 소켓, 이벤트 세션 9종 |
| [Discovery](modules/discovery.md) | 11 | 홈, 카테고리, 배너, 검색 |
| [Commerce](modules/commerce.md) | 12 | 후원, 미션, 상점, 광고 |
| [User](modules/user.md) | 6 | 사용자 상태, 차단, 배지 |
| [Manage](modules/manage.md) | 43 | 스튜디오 조회. 본인 채널 권한 필요 |
| [Stats](modules/stats.md) | 3 | 채널 통계. 본인 채널 권한 필요 |

각 모듈은 엔드포인트마다 같은 순서로 작성합니다.
HTTP Request, Request Param, Response Body, 예제 순입니다.

**레퍼런스**

| 문서 | 내용 |
|---|---|
| [엔드포인트 전체 목록](reference/endpoints.md) | 115건 평면 인덱스. 경로로 찾을 때 사용 |
| [Enum 레퍼런스](reference/enums.md) | 확인된 Enum 전량 |
| [채널 애널리틱스](reference/analytics.md) | 본인 채널과 타 채널의 수집 방법 |
| [제외된 API · 정정된 사실](reference/deprecated.md) | 제외 23건, 정정 7건 |

***

## 목적별 진입점

| 목적 | 문서 |
|---|---|
| 시청자 수 추적 | [라이브 상태 조회](modules/live.md#라이브-상태-조회), [채널 애널리틱스](reference/analytics.md) |
| 채팅 로그 전량 수집 | [다시보기 채팅 조회](modules/video.md#다시보기-채팅-조회). WebSocket 불필요 |
| 실시간 채팅 수신 | [Chat](modules/chat.md) |
| 클립의 원본 방송 위치 | [클립 뷰어 카드 조회](modules/clip.md#클립-뷰어-카드-조회) |
| 채널 개설일과 누적 방송시간 | [채널 부가 데이터 조회](modules/channel.md#채널-부가-데이터-조회) |
| 본인 채널 시계열 통계 | [Stats](modules/stats.md) |
| 타 채널 분석 | [트랙 B](reference/analytics.md#트랙-b--타-채널) |
| 후원 알림 오버레이 | [Notification](modules/notification.md) |

***

## 상태 표기

각 엔드포인트에는 확인 수준을 함께 적습니다.

| 표기 | 의미 |
|---|---|
| 실측 | 경로, 파라미터, 응답을 모두 확인 |
| 스키마 미상 | 경로와 인증은 확정. 응답 스키마는 빈 배열이나 `null` 로만 관측 |
| 경로만 확인 | 파라미터 미검증 |
| 추정 | 실측 근거 없음 |
| 조회용 POST | 메서드는 `POST` 이나 서버 상태를 변경하지 않음 |

인증이 필요한 API에는 인증 필요, 민감 정보를 포함하는 응답에는 민감 정보 포함을 함께 적습니다.

***

## 주의 사항

비공식 API입니다. 네이버가 사용을 허가한 것이 아니며 예고 없이 변경될 수 있습니다.
응답 파싱은 필드 누락에 관대하게 작성하는 편이 안전합니다.

## 참고

- [치지직 공식 개발자 문서](https://chzzk.gitbook.io/chzzk)
- [awesome-chzzk](https://github.com/dokdo2013/awesome-chzzk)
- [kimcore/chzzk](https://github.com/kimcore/chzzk) · [gunyu1019/chzzkpy](https://github.com/gunyu1019/chzzkpy) · [R2turnTrue/chzzk4j](https://github.com/R2turnTrue/chzzk4j)

## 문서에 기여하기

새 엔드포인트를 추가하거나 오류를 수정할 때는 [문서 규약](CONTRIBUTING.md)을 따릅니다.
