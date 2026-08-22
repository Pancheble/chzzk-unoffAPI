# STEP 2 — 모듈 경계 설계

전제: STEP 1([step1-triage.md](step1-triage.md)) 분류 결과 반영
대상: ~~116건 (이름 확인 94 + Manage 미확보 22)~~ → **115건** (이름 확인 95 + Manage 미확보 20)
규칙: **읽기 전용** — 서버 상태를 바꾸는 요청은 문서에 싣지 않음

> **집계 정정 (STEP 3):** 설계 시점의 116건은 Manage 배분을 잘못 센 값이었습니다.
> 모듈별 실측: manage.md 23 + stats.md 3 + notification.md 1 = **47** (사용자 제공 실측치와 일치).
> 따라서 manage.md는 44가 아니라 **43**(이름 확인 23 / 미확보 20), 총계는 **115건**입니다.

---

## 1. 파일 트리

> **STEP 3 실행 시 변경 3가지**
> 1. 원본 `CHZZK_UNOFFICIAL_API.md`는 인덱스로 축소했다가 **삭제**했습니다. 고유 내용이 구 절 번호 매핑표뿐이라 이전이 끝난 뒤엔 쓸모가 없었습니다.
> 2. **`CLAUDE.md`를 루트에 추가**했습니다. Claude Code가 자동 로드하는 진입점이 필요했습니다.
> 3. **`reference/endpoints.md`를 추가**했습니다. 12개 모듈을 뒤지지 않고 경로를 찾을 평면 인덱스가 없었습니다.

```
D:\test\
├─ CLAUDE.md                      에이전트 진입점 · 금지 값 · 통념 정정표   🆕
└─ docs\
   ├─ README.md                  인덱스 · 모듈 맵 · 이름 함정 · 빠른 시작
   ├─ core\
   │   ├─ base-urls.md           호스트 7종
   │   ├─ headers.md             필수 헤더 · deviceId · CORS
   │   ├─ conventions.md         응답 봉투 3형 · 페이지네이션 3종 · 문자열 JSON · 식별자
   │   └─ auth.md                쿠키 · 권한 3단계
   ├─ modules\
   │   ├─ channel.md       (15)  채널 조회 · data?fields · my-info · 팔로잉
   │   ├─ live.md           (5)  라이브 상세/상태 · 폴링
   │   ├─ video.md          (3)  VOD 상세 · 다시보기 채팅 · 재생 매니페스트
   │   ├─ clip.md           (6)  클립 목록/상세/벌크 · 원본 영상 매핑
   │   ├─ comment.md        (4)  댓글 · 대댓글 · 스티커
   │   ├─ chat.md           (3)  실시간 채팅 (수신 전용)
   │   ├─ notification.md   (4)  개인 알림 소켓 · 이벤트 세션 9종      🆕
   │   ├─ discovery.md     (11)  홈 · 카테고리 · 배너 · 검색
   │   ├─ commerce.md      (12)  후원 · 미션 · 상점 · 광고 · 유료상품
   │   ├─ user.md           (6)  사용자 상태 · 차단 · 배지 · 닉네임
   │   ├─ manage.md        (43)  스튜디오 조회 (읽기 전용)             
   │   └─ stats.md          (3)  채널 통계                          🆕
   ├─ reference\
   │   ├─ endpoints.md    (115)  전체 평면 인덱스 — 검색용             🆕
   │   ├─ enums.md               Enum 전량
   │   ├─ deprecated.md          버림 23건 + 사실 오류 정정 이력
   │   └─ analytics.md           본인 채널 / 타 채널 2트랙 레시피
   └─ _work\
       ├─ step1-triage.md        중복·제외 분류 근거
       └─ step2-modules.md       이 문서
```

**총 22개 파일** (CLAUDE.md 1 + README 1 + core 4 + modules 12 + reference 4)
※ `_work/` 2개는 작업 노트라 집계에서 제외. 원본 인덱스는 삭제됨.

---

## 2. 엔드포인트 → 모듈 배치표

### `core/` — 엔드포인트 없음 (규약만)

### `modules/channel.md` — 15

| 경로 | 인증 |
|---|---|
| `GET /service/v1/channels/{channelId}` | |
| `GET /service/v1/channels/{channelId}/data?fields=` **정본** | |
| `GET /service/v1.1/channels/{channelId}/my-info` | |
| `GET /service/v1/channels/{channelId}/videos` **정본** | |
| `GET /service/v1/channels/{channelId}/chat-rules` | |
| `GET /service/v1/channels/{channelId}/announcements` | |
| `GET /service/v1/channels/{channelId}/live-schedule` | |
| `GET /service/v1/channels/{channelId}/live-recommended` | |
| `GET /service/v1/channels/{channelId}/follow` | |
| `GET /service/v1/channels/{channelId}/cafe-connection` | |
| `GET /service/v1/channels/{channelId}/achievement-badges` | |
| `GET /service/v1/channels/{channelId}/party-donation-info` | |
| `GET /service/v1/channels/{channelId}/log-power/prediction` | |
| `GET /service/v1/channels/followings` | |
| `GET /service/v1/channels/followings/live` | |

> `channels/{id}/clips`는 여기 두지 않고 요약표에 **`clip.md` 링크 1행**만 둡니다.
> `chat-rules`·`videos`는 `manage.md`에 동명 경로가 있으므로 **혼동 주의 박스** 삽입.

### `modules/live.md` — 5

| 경로 | 비고 |
|---|---|
| `GET /service/v3.3/channels/{channelId}/live-detail` **정본** | v1/v2 아님 |
| `GET /polling/v3.1/channels/{channelId}/live-status` **정본** | 시청자 트래킹은 이것 |
| `GET /polling/live-detail?entityId=&abTestNoList=` | 이름 함정 (A/B 배정) |
| `GET /service/v1/lives/{liveId}/ads/current` | |
| `GET /service/v1/live/{liveId}/auto-play-info` | |

### `modules/video.md` — 3

| 경로 | 비고 |
|---|---|
| `GET /service/v3/videos/{videoNo}` **정본** | `inKey` · `prevVideo`/`nextVideo` 체인 |
| `GET /service/v1/videos/{videoNo}/chats` **정본** | HTTP만으로 채팅 전량 수집 |
| `GET .../neonplayer/vodplay/v3/playback/{videoId}` **정본** | DASH MPD(XML), `key`=`inKey` |

### `modules/clip.md` — 6

| 경로 | 비고 |
|---|---|
| `GET /service/v1/channels/{channelId}/clips` **정본** | 커서 = `clipUID` |
| `GET /service/v1/clips/{clipUID}/detail` | `optionalProperties` 반복 파라미터 |
| `POST /service/v1/clips/detail-bulk` | **조회용 POST — 예외** |
| `GET /service/v1/clips/upload/enable` | |
| `GET /api/v5.0/clipviewer/cards` | 봉투 B형 |
| `GET /api/v5.0/clipviewer/card` **정본** | 클립→원본 매핑 (구 §16 전량) |

### `modules/comment.md` — 4

| 경로 | 비고 |
|---|---|
| `GET /v1/type/{objectType}/id/{objectId}/comments` | objectType 3종 확정 |
| `GET /v1/type/{objectType}/id/{objectId}/comments/{commentId}/replyComments` | `replies` 아님 |
| `GET /api/v4.0/comment/sticker/pack?stickerServiceCode=chzzk` | 호스트: CREATOR, 봉투 B형 |
| `GET /api/v4.0/comment/sticker?packCode=&stickerServiceCode=` | 〃 |

> 스티커 2건은 호스트가 다르지만 **기능이 댓글 첨부**라 여기 배치. 호스트·봉투 차이는 박스로 경고.

### `modules/chat.md` — 3 · **수신 전용**

| 경로 | 비고 |
|---|---|
| `wss://kr-ss{N}.chat.naver.com/chat` | 서버번호 **풀 내 임의** · `ver: "3"` |
| `GET /v1/chats/access-token?channelId=&chatType=STREAMING` | comm-api |
| `GET /v1/chats/{chatChannelId}/users/{userIdHash}/profile?chatType=&streamingChannelId=` | `profile-card` 아님 |

포함: v3 CONNECT 바디 · `bdy.sid` 재사용 규칙 · **수신 cmd 표** · `messageTypeCode` · `extras`/`profile` 파싱
제외: `cmd 3101 SEND_CHAT` (송신)

### `modules/notification.md` 🆕 — 4

| 경로 | 비고 |
|---|---|
| `GET /service/v1/personal/session-url` | **알림 소켓 URL 전체를 서버가 반환** |
| `GET /manage/v1/alerts/{sessionIOChannelId}/session-url` | 응답 `url`·`app` 공백 (미해결) |
| `wss://ssio{N}.nchat.naver.com/socket.io/?auth=&EIO=3&transport=websocket` | **채팅 아님** · `nng@glive` |
| `GET /v1/notification/new` | comm-api |

포함: 이벤트 세션 9종(`donation@` `subscription@` `newsfeed@` `video@` `mission@` `gift@` `partydonation@` `studio@` `streamershop@`)

### `modules/discovery.md` — 11

`topics` · `topics/HOME/sub-topics/HOME/main` · `categories/live` · `banners` · `home/skins` ·
`client-config` · `program-schedules/coming` · `streamer-partners/recommended` ·
`v2/search/lounges` · `v2/search/lounges/auto-complete` · `v1/lounge/loungeEvent/chzzk`

### `modules/commerce.md` — 12

`donations/chat-setting` · `donations/video-setting` · `donations/mission-setting` ·
`v2/.../donations/missions` · `commercial/v1/streamer-shop/{id}/products` ·
`streamer-shop/{id}/notifiable` · `commercial/v1/channels/{id}/donation-campaigns` ·
`cheat-key/status` · `cheat-key/promotion-status` · `offerwall/total-reward` ·
`service/v1/paid-product/init` · `service/v1/ad/display-status`

### `modules/user.md` — 6

`GET /v1/user/getUserStatus` · `GET /v1/privateUserBlocks/allUserIdHash` ·
`GET /service/v1/personal/personal-data?fields=` · `GET /service/v2/nickname/color/codes` ·
`GET /service/v1/badge-awards/unread` · `GET /service/v1/badges/assets/last-updated?badgeType=`

### `modules/manage.md` — 44 (실측 47 − stats 3)

**이름 확인 22 / 미확보 22**

| 확인된 경로 | 상태 |
|---|---|
| `/channels/{id}/streaming-info` | `streamKey`·`streamUrl` 포함 |
| `/channels/{id}/streams` | 실사용은 `streaming-info` |
| `/channels/{id}/live-setting/normal` `/chat` `/chat-mode` `/chat-condition` | (4) |
| `/channels/{id}/my-role` · `/my-status` | (2) |
| `/channels/{id}/chat-rules` | |
| `/channels/{id}/chats/prohibit-words` | |
| `/channels/{id}/restrict-users` · `/restrict-release-requests` | 경로 / 스키마 빈 응답 |
| `/channels/{id}/streaming-roles` | |
| `/channels/{id}/followers` · `/subscribers` · `/videos` · `/clips` · `/clips/make-clips` · `/news-feeds` · `/party/summary` | 경로 / 스키마 빈 응답 |
| `/auto-complete/categories?keyword=` | 미포착 |
| `/channels/{id}/users/{targetId}/chat-activity-count` | 미포착 |
| `manage/v2/channels/{id}/center-status` | **v2** |

> 미확보 22개는 **`## 미수록 경로` 절**을 만들어 자리를 비워둡니다. 목록 받는 즉시 채웁니다.

### `modules/stats.md` 🆕 — 3

| 경로 | 상태 |
|---|---|
| `GET /manage/v1/channels/{id}/stats/lives?from=&to=` | 경로 / `liveStatList[]` 빈 배열 |
| `GET /manage/v1/channels/{id}/stats/videos?from=&to=` | 경로 / `summaryVideoStat` 확보 |
| `GET /manage/v1/channels/{id}/stats/recent-live` | 경로 / `null` |

`manage.md`에서 분리하는 이유: **§15의 핵심 결론을 뒤집은 엔드포인트**라 44개 목록에 묻히면 안 됨.

---

## 3. 모듈 문서 템플릿

모든 `modules/*.md`가 동일한 뼈대를 따릅니다.

```markdown
# {모듈명}

> 한 줄 요약

**Base:** `{host}` · **인증:** {불필요 | 쿠키 | 채널 권한}
**관련:** [channel](../modules/channel.md) · [live](../modules/live.md)

## 엔드포인트 요약

| 상태 | Method | 경로 | 설명 |
|---|---|---|---|

## {엔드포인트명}

​```
GET /path/{param}?query=
​```

**요청 파라미터**
| 이름 | 필수 | 값 | 설명 |

**응답 주요 필드**
| 필드 | 타입 | 설명 |

**주의** — 함정이 있을 때만

<details><summary>Response 예시</summary>
​```json
​```
</details>

## 미수록 / 미검증
```

**규칙**
- 요약표 → 상세 순서 고정 (기존 문서의 좋은 패턴 유지)
- 응답 예시는 **항상 `<details>` 안에** — 스크롤 지옥 방지
- 값이 확인된 필드만 표에, 추정은 달아 별도 행

---

## 4. 상태 마커 규약

기존 3종()이 "경로 확인"과 "스키마 확인"을 구분 못 해서 혼선이 있었습니다. 5종으로 분리합니다.

| 마커 | 의미 |
|---|---|
| 실측 | 경로 + 파라미터 + 응답 전부 실측 |
| 스키마 미상 | **경로·인증 확정 / 응답 스키마 미상** (빈 배열·null로 관측) |
| 경로만 확인 | 경로만 확인, 파라미터 미검증 |
| 추정 | 추정 |
| 조회용 POST | 조회용 POST 예외 (`clips/detail-bulk` 전용) |

부가 배지: 인증 필요 · 민감정보 포함 · 애널리틱스 핵심

> 가 새로 필요한 이유: Manage 11건이 "경로는 확실한데 채널에 데이터가 없어 응답이 비었다" 상태입니다. 도 도 정확하지 않습니다.

---

## 5. 링크 규약

| 대상 | 표기 |
|---|---|
| 모듈 간 | `[live-status](../modules/live.md#라이브-상태-조회)` — 상대경로 |
| 중복 정본 | 요약표 행에 `→ [clip.md](../modules/clip.md#채널-클립-목록-조회)` 만 두고 본문 서술 없음 |
| core 참조 | `[응답 봉투](../core/conventions.md#응답-봉투)` |

**기존 `§6.4` 같은 번호 참조는 전량 제거합니다.** 절 번호가 바뀌면 즉시 깨지는 참조라 이번 재편의 주요 정리 대상입니다.

> **STEP 3에서 추가된 규칙:** 제목 맨 앞에 이모지를 두지 않습니다.
> `## streaming-info`의 앵커가 `#-streaming-info`가 되어 링크가 깨졌습니다 (5건 발생).
> 이모지는 제목 뒤에 붙이거나 본문으로 내립니다. 렌더러마다 처리가 달라 앞에 두면 불안정합니다.

---

## 6. README.md 구성

1. **이 문서는 읽기 전용 API만 다룹니다** — 범위를 최상단에 못 박음
2. 보안 — `streamKey`/`streamUrl`/`accTkn`/`liveTokenList` 노출 금지 + **크롬 sanitized HAR은 응답 본문을 안 지움**
3. **이름 함정 표** (구 §4 + `personal/session-url` 추가) ← 제일 먼저 읽어야 할 것
4. 모듈 맵 (12개 링크 + 한 줄 설명 + 엔드포인트 수)
5. 빠른 시작 (헤더 → 채널 조회 → 라이브 상태)
6. 목적별 진입점: "시청자 수 추적하려면" / "채팅 로그 받으려면" / "내 채널 통계 보려면"

> 4번 모듈 맵에 **`personal/session-url` 사례**를 각주로 남깁니다. "기타" 표에 묻혀 있던 한 줄이 다른 절의 미해결 과제였던 건이라, 모듈화의 근거로 실물이 있는 편이 낫습니다.

---

## 7. reference/ 구성

| 파일 | 내용 |
|---|---|
| `endpoints.md` 🆕 | **115건 평면 인덱스.** 호스트·접두사별 표 + 모듈 링크. 경로 검색 전용 |
| `enums.md` | 기존 전량 + 신규 7종(`ASC` `REPLY` `STREAMER` `permissions` 8값 `dateFilter` `orderFilter` `sortType` `streamerCurrentGrade`) |
| `deprecated.md` | 버림 23건. **왜 버렸는지**와 대체재를 표로. 사실 오류 7건은 "이렇게 알려져 있었으나 실제는 —" 형식 |
| `analytics.md` | **2트랙 재작성** — ① 본인 채널: `stats/*` ② 타 채널: 공개 지표 + 폴링. 구 §15의 "시계열 없음" 결론 정정 명시 |

> `endpoints.md`는 설계 시점에 없었습니다. 모듈화로 개별 문서는 짧아졌지만 **"이런 엔드포인트가 있나?"에 답하려면 12개 파일을 뒤져야 하는** 역효과가 생겨서 STEP 3에서 추가했습니다.

---

## 8. 결정 사항 요약

| # | 결정 | 근거 |
|---|---|---|
| 1 | 12개 기능 모듈 + core 4 + reference 4 | 모듈당 3~15건, 최대 manage 43 |
| 2 | `notification.md` 신설 | `ssio{N}`이 채팅이 아님이 밝혀져 §12에서 분리 |
| 3 | `stats.md` 독립 | manage 43개에 묻히면 안 되는 항목 |
| 4 | `donation` → `commerce`로 확장 | 후원·상점·광고·유료상품이 전부 상업 기능 |
| 5 | 상태 마커 3종 → 5종 | "경로 확정 / 스키마 미상"을 표현할 수단이 없었음 |
| 6 | 절 번호 참조 전량 → 상대경로 링크 | 재편마다 깨지는 참조 제거 |
| ~~7~~ | ~~원본 파일은 인덱스로 축소~~ → **삭제** | 매핑표 외 고유 내용이 없었음. 이전 완료 후 가치 소멸 |
| 8 🆕 | `CLAUDE.md` 루트 추가 | `docs/`는 자동 로드되지 않음. 에이전트 진입점 + 통념 정정표 필요 |
| 9 🆕 | `endpoints.md` 추가 | 모듈화의 역효과(경로 검색 비용) 상쇄 |
| 10 🆕 | 제목 앞 이모지 금지 | 앵커가 `#-제목`이 되어 링크 5건 깨짐 |

---

## 9. STEP 3 결과

**완료.** 22개 파일 생성, 내부 링크 346개 전량 검증 통과 (깨진 파일 0 · 앵커 0).

### 미해결로 남긴 것

설계 시점에 "없으면 로 표기하고 자리만 만들어둔다"고 한 항목들입니다. 그대로 적용됐습니다.

| 항목 | 현재 상태 |
|---|---|
| Manage 실측 47개 전체 목록 | **20개 미확보** → `manage.md`의 `## 미수록 경로` 절에 표 형식 주석으로 자리 확보 |
| `stats/*` 응답 전문 | — `summaryVideoStat` 필드만 확보, 배열 항목 구조 미상 |
| `manage/v2/.../center-status` 응답 | 경로만, 응답 예시 없음 |
| `streaming-info` 나머지 필드 | — 키 2개 외 구조 미확보 |

해결 방법은 저장소의 `CLAUDE.md` 「미해결」 절에 정리했습니다.
