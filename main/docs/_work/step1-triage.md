# STEP 1 — 중복 / 못 쓰는 API 분류 결과

원본: `D:\test\CHZZK_UNOFFICIAL_API.md` (1120줄)
**최초 작성:** 2026-07-29
**갱신:** 2026-07-29 — 클립 HAR 1,056건 + 스튜디오 HAR 315건 + 댓글 HAR 2회 분석 반영

판정 규칙(사용자 지시):
1. **GET 전용** — POST/PUT/DELETE는 전량 버림 ← 최우선, 아래 규칙보다 우선함
2. 대체 가능하면 버림 / 대체 불가면 남김

---

## 0. 전역 규칙 — GET only

**이 문서는 읽기 전용 API만 다룹니다.** 상태를 바꾸는 요청은 대체재 유무와 무관하게 전부 제외합니다.

| 결과 | 내용 |
|---|---|
| 제외 | 서버 상태를 바꾸는 `POST` · `PUT` · `DELETE` 전량 (12건) |
| 유지 | `GET` + WebSocket **수신** + **조회용 POST 1건**(`clips/detail-bulk`) |
| 부수 효과 | 스트림 키·채널 설정 변경 사고, 시청자 수 조작(`watch-event`) **원천 차단** |

> 방금 있었던 스트림 키 노출 건을 감안하면, 읽기 전용으로 못 박는 편이 문서 자체의 위험도를 크게 낮춥니다.

**WebSocket 처리:** 핸드셰이크가 HTTP GET 업그레이드이고 소비가 수신이므로 **유지**합니다.
단 채팅 **송신** `cmd 3101 SEND_CHAT`은 쓰기이므로 cmd 표에서 제외합니다 (수신 cmd는 전부 유지).

### 조회용 POST 예외 — 1건 (사용자 판단으로 유지)

| 엔드포인트 | 성격 | 유지 근거 |
|---|---|---|
| `POST /service/v1/clips/detail-bulk` | **메서드만 POST, 실제는 조회.** 본문에 `clipUIDList[]`를 담아야 해서 GET이 아닐 뿐 | 유일한 GET 대체재 `GET /service/v1/clips/{clipUID}/detail`는 1건씩 → 클립 N개면 요청 N배. 캡처 규모(1,056건) 기준 약 10배 |

> 정확히는 규칙이 **"GET 전용"이 아니라 "읽기 전용"**입니다. 판정 기준은 메서드가 아니라 **서버 상태를 바꾸는가**입니다.
> `detail-bulk`는 조회이므로 유지, `watch-event`(집계 적재)·`live-status`(로그 적재)는 POST이자 쓰기이므로 제외.
> STEP 3 문서에는 이 엔드포인트에 **"조회용 POST — 예외"** 배지를 답니다.

---

## 0.1 갱신 요약

| 항목 | 최초 | 2차 | **읽기 전용** |
|---|---|---|---|
| 총 엔드포인트 | 89 | 약 115 | **116** (STEP 2 배치 기준 확정) |
| 중복 (정본 지정 필요) | 9건 | 12건 | 12건 |
| 버림 | 4건 | 11건 | **23건** (+12) |
| 남김 | 26건 | 18건 | **6건** |
| 판정 보류 | 4건 | 0건 | 0건 |
| 🆕 신규 미해결 | — | 2건 | 2건 |

> **총계 정정:** 최초 89건은 §8 클립 3건(`clips/{clipUID}/detail`, `detail-bulk`, `upload/enable`)을 빠뜨린 수치였습니다.
> STEP 2에서 전 엔드포인트를 모듈에 배치하며 재집계한 **116건**(이름 확인 94 + Manage 미확보 22)이 확정치입니다.

**가장 큰 변화 2가지**

1. **§12 채팅 절이 통째로 오류였습니다.** "채팅 시스템이 2개로 갈렸다"는 전제가 틀렸고(신 소켓은 채팅이 아니라 개인 알림), "서버번호 공식이 깨졌다"도 틀렸습니다(애초에 cid에서 서버를 유도하지 않음).
2. **§15의 대표 결론 "시계열 데이터가 아예 없습니다 — 가장 큰 벽"이 뒤집혔습니다.** `manage/v1/.../stats/*`가 존재합니다 (본인 채널 한정).

---

## 문서에 반드시 반영할 보안 항목

기존 §주의사항의 노출 금지 목록에 **`streamKey` / `streamUrl`을 추가**해야 합니다.

```
GET /manage/v1/channels/{channelId}/streaming-info
→ "streamKey": "<32자>", "streamUrl": "rtmp://global-rtmp.lip2.navercorp.com:8080/relay"
```

> **크롬 sanitized HAR 내보내기는 응답 본문을 지우지 않습니다.** 쿠키·헤더만 제거합니다.
> 이 경고문을 문서에 넣어야 같은 사고가 재발하지 않습니다.

기존 목록: `liveTokenList` · `extraToken` · Socket.IO `auth` · 스트림 키
→ 갱신: `liveTokenList` · `extraToken` · `accTkn` · Socket.IO `auth` · **`streamKey`** · **`streamUrl`**

---

## A. 중복 — 정본 1곳 지정, 나머지는 링크로 대체

### A-1. 절이 달라서 흩어진 중복 (12건)

| # | 엔드포인트 | 현재 위치 | 정본(STEP 2 기준) |
|---|---|---|---|
| 1 | `GET /polling/v3.1/channels/{id}/live-status` | §6.2 · §7 · §15 (3곳) | `modules/live.md` |
| 2 | `GET /service/v1/channels/{id}/clips` | §6.1 표 · §8 상세 | `modules/clip.md` |
| 3 | `GET /api/v5.0/clipviewer/card` | §11 표 · §16 전체 파라미터 | `modules/clip.md` |
| 4 | `GET /service/v3/videos/{videoNo}` | §6.4 · §15 표 3행 | `modules/video.md` |
| 5 | `GET /service/v1/videos/{videoNo}/chats` | §6.4 · §15 · §12.5 팁 (3곳) | `modules/video.md` |
| 6 | VOD 재생 매니페스트 | §1 Base URL 표 · §6.4 | `modules/video.md` |
| 7 | `GET /service/v1/channels/{id}/data?fields=` | §6.1 · §15 2행 | `modules/channel.md` |
| 8 | `GET /service/v1/channels/{id}` | §6.1 표 · §15 표 | `modules/channel.md` |
| 9 | `GET /service/v1/channels/{id}/videos` | §6.1 표 · §15 표 | `modules/channel.md` |
| **10** 🆕 | **`GET /service/v1/personal/session-url`** | §6.7 "기타" 표 1행 · §12.3 "`auth` 토큰 발급 경로 " | `modules/notification.md` |
| **11** 🆕 | manage 통계 ↔ §15 폴링 수집 서술 | §13(미기재) · §15 "직접 쌓는 수밖에" | `reference/analytics.md` (본인/타 채널 분기) |
| **12** 🆕 | `GET /manage/v1/channels/{id}/streams` ↔ `/streaming-info` | §13 표 | `modules/manage.md` (실사용 = `streaming-info`) |

> **#10이 가장 뼈아픈 중복입니다.** §6.7 "기타" 표에 무심하게 한 줄 있던 `personal/session-url`이, §12.3에서 "다음 캡처 과제"로 찾던 바로 그 경로였습니다. 문서 양쪽 끝에 떨어져 있어서 연결이 안 됐습니다. **모듈화가 왜 필요한지 보여주는 직접 사례**라 STEP 3 README에 남길 만합니다.

### A-2. 중복 아님 — 유지 (표 + 바로 아래 상세 패턴)

`my-info` · `channels/followings` · `topics/HOME/.../main` · `categories/live`

### A-3. 중복 아님 — 동명이경, 구분 명시 필요 (2건 → **5건**)

| 경로 | service (공개) | manage (스튜디오) |
|---|---|---|
| `chat-rules` | `GET /service/v1/channels/{id}/chat-rules` | `GET/PUT /manage/v1/channels/{id}/chat-rules` |
| `videos` | `GET /service/v1/channels/{id}/videos` | `GET /manage/v1/channels/{id}/videos` |
| **`clips`** 🆕 | `GET /service/v1/channels/{id}/clips` | `GET /manage/v1/channels/{id}/clips` |
| **`followers`** 🆕 | (없음 — `followerCount`만) | `GET /manage/v1/channels/{id}/followers` |
| **`live-setting`** 🆕 | (없음) | `/live-setting/{normal\|chat\|chat-mode\|chat-condition}` |

### A-4. 이름 ≠ 기능 (§4) — 함정 인덱스, README로 승격

`POST /service/live-status` · `GET /polling/live-detail` · `GET /polling/v3.1/.../live-status` · `GET /service/v3.3/.../live-detail`
🆕 추가: **`GET /service/v1/personal/session-url`** — "personal"이라는 이름 때문에 알림 소켓 발급 경로임을 놓치기 쉬움

---

## B. 버림 — 24건

### B-0. 🆕 GET only 규칙 위반 — 13건

메서드가 `GET`이 아니라는 이유만으로 버립니다. 대체재 유무를 따지지 않습니다.

| # | 엔드포인트 | Method | 이전 판정 | 비고 |
|---|---|---|---|---|
| 12 | `/polling/v1/watch-event/live` | POST | 남김 | 애초에 호출 금지였음 |
| 13 | `/polling/v1/watch-event/video` | POST | 남김 | 〃 |
| 14 | `/polling/v1/watch-event/clip` | POST | 남김 | 〃 |
| 15 | `/manage/v1/channels/{id}/live-setting/*` | PUT | 남김 | GET은 유지 |
| 16 | `/manage/v1/channels/{id}/chats/prohibit-words` | POST | 남김 | GET은 유지 |
| 17 | `/manage/v1/channels/{id}/chats/prohibit-words/{no}` | DELETE·PUT | 남김 | **경로 자체 삭제** |
| 18 | `/manage/v1/channels/{id}/restrict-users` | POST | 남김 | GET은 유지 |
| 19 | `/manage/v1/channels/{id}/restrict-users/{targetId}` | DELETE | 남김 | **경로 자체 삭제** |
| 20 | `/manage/v1/channels/{id}/restrict-users/{targetId}/validate` | POST | 남김 | **경로 자체 삭제** |
| 21 | `/manage/v1/channels/{id}/temporary-restrict-users` | POST | 남김 | **경로 자체 삭제** |
| 22 | `/manage/v1/channels/{id}/restrict-release-requests/{no}/reject` | POST | 남김 | **경로 자체 삭제** |
| 23 | `/manage/v1/channels/{id}/streaming-roles[/{targetId}]` | PUT·DELETE | 남김 | GET은 유지 / `{targetId}` 경로 삭제 |
| 24 | `/manage/v1/channels/{id}/donations/mission/{approve,reject}` | POST | 남김 | **경로 자체 삭제** |

> `POST /service/v1/clips/detail-bulk`는 **조회용 POST라 예외로 유지**합니다 (§0 참조).

**경로 자체가 사라지는 것 8개** (쓰기 전용): `prohibit-words/{no}` · `restrict-users/{targetId}` · `validate` · `temporary-restrict-users` · `reject` · `mission/approve` · `mission/reject` · `streaming-roles/{targetId}`

> 이 8개는 애초에 **라이브러리 소스 기준 기재**였고 스튜디오 실측 47개(전부 GET)에도 없었습니다.
> 즉 GET only 규칙으로 문서에서 사라지는 실측 경로는 **0개**입니다 — 검증된 것은 하나도 잃지 않습니다.

**§12.4 cmd 표에서 제외:** `3101 SEND_CHAT` (송신). 수신 cmd(`93101` `93102` `93006` `94005` `94006` `94008` `94010` `94015`)와 `0`/`100`/`5101` 계열은 유지.

### B-1. 구버전·불필요 (기존 4건, 유지)

| 버리는 것 | 대체재 | 남길 흔적 |
|---|---|---|
| `POST /service/live-status` (텔레메트리) | `polling/v3.1/.../live-status` | 함정 표 1행. 요청 본문 JSON 블록 삭제 |
| `live-detail` v1/v2 | **v3.3** | 마이그레이션 1줄 |
| `donations/missions` v1 | **v2** | 마이그레이션 1줄 |
| `profile-card` | `/profile` + `streamingChannelId` | 마이그레이션 1줄 |

### B-2. 🆕 사실 오류 서술 — 전면 삭제·재작성 (7건)

기존에 "남김"으로 분류했던 것 중 **틀린 내용으로 밝혀져 버리는 것들**입니다.
대체재는 "정정된 사실" 그 자체입니다.

| # | 버리는 서술 | 왜 틀렸나 | 대체 |
|---|---|---|---|
| 5 | **§12.1 "채팅 시스템이 2개로 갈렸습니다"** 비교표 전체 | `ssio{N}`은 채팅이 아니라 **개인 알림 채널**(`nng@glive`). WS 프레임 8개가 전부 핸드셰이크·하트비트, 채팅 페이로드 0건 | 채팅은 1종뿐 → §12 재작성 + 알림은 `notification.md`로 분리 |
| 6 | **§12.2 "서버 번호 공식이 깨졌습니다"** 절 전체 | modulus가 바뀐 게 아니라 **cid에서 서버를 유도한다는 전제 자체가 무효**. 동일 cid `N2dc9q`가 `kr-ss24`·`kr-ss35` 양쪽 접속 성공(`retCode 0`) | "풀 내 아무 서버나 접속" 1줄 |
| 7 | §12.2 "다음 캡처 최우선 과제" 액션 아이템 | 해결됨 | 삭제 |
| 8 | **§12.4 CONNECT `ver: "2"`** | 실제 **`ver: "3"`**, `bdy` 확장(`libVer` `windowId` `timezone` `devName` 등). 응답 `cmd:10100`의 `bdy.sid`를 이후 전 요청에 포함 | v3 바디 전문으로 교체 |
| 9 | **§9 대댓글 추정 경로 `.../replies`** | 실제는 **`replyComments`** | 확정 경로로 교체, 제거 |
| 10 | **§15 "#1 시계열 데이터가 아예 없습니다 — 가장 큰 벽"** | `manage/v1/.../stats/{lives,videos,recent-live}` 존재 | **본인 채널 = stats API / 타 채널 = 폴링**으로 분기 재작성 |
| 11 | §15 "#2 `accumulateCount` — live-detail과 대조하세요" 액션 | 양쪽 다 `0`. **필드 자체가 무효** | "누적은 VOD `livePv` 사용" 결론으로 교체 |

> **§15 "#3 스트리머 인증이 필요한 것들 — 어떤 방법으로도 접근 불가"는 절반만 유지됩니다.**
> 본인 채널은 `stats/*`로 접근 가능해졌습니다. **타 채널 분석에는 폴링이 여전히 유일**하다는 부분만 남깁니다.

### B-3. 🆕 마커 제거 (보류 4건 전건 해결)

| 위치 | 이전 | 확정 |
|---|---|---|
| §6.1 `data?fields` 표 | `description` | **유효** — 응답에 `description` 반환 |
| §9 objectType 표 | 클립 | **`CLIP`**, `objectId` = **`clipUID`**(10자) |
| §9 대댓글 | `replies` | **`replyComments`**, `offset`만 (limit 없음) |
| §15 #2 | `accumulateCount` 대조 필요 | **무효 필드** 확정 |

---

## C. 남김 — 6건

### C-1. 채팅 — 1건 · 💀 → 판정 변경

`wss://kr-ss{N}.chat.naver.com/chat` — **접속 가능.** 서버번호는 풀 내 임의.
대체 불가(실시간 채팅 유일 경로) + 핸드셰이크가 HTTP GET 업그레이드 → 유지.
**수신 전용으로 문서화합니다.** 송신(`cmd 3101`)은 §B-0에서 제외.

잔여 경미 미검증: 유효 서버번호 범위 · `auth:"READ"`로 `uid` 없이 접속 가능 여부 · `libVer`/`windowId` 필수 여부

### ~~C-2. Manage 쓰기 계열 — 9건~~ → **§B-0으로 이동 (GET only)**

### C-3. GET 미포착 — 2건

`/auto-complete/categories?keyword=` (카테고리 검색창 타이핑) · `/channels/{id}/users/{targetId}/chat-activity-count` (시청자 클릭)

### C-4. 🆕 신규 미해결 — 2건

| # | 항목 | 막힌 지점 |
|---|---|---|
| N-1 | `manage/v1/channels/{id}/stats/{lives,videos,recent-live}` | 스키마 일부만 확보(`summaryVideoStat`). `liveStatList[]`·`videoStatList[]` 빈 배열, `summaryLiveStat`·`recent-live` `null` → **일별 배열 항목 구조 미상** |
| N-2 | `manage/v1/alerts/{sessionIOChannelId}/session-url` + 이벤트 세션 9종 | 응답 `url`·`app` 공백. 각 채널 페이로드 구조 전량 미확인 |

이벤트 세션 9종: `donation@` `subscription@` `newsfeed@` `video@` `mission@` `gift@` `partydonation@` `studio@` `streamershop@`

### C-5. 조사 대상 아님 — 1건 (4건 → 1건)

`GET /polling/live-detail?entityId=&abTestNoList=` 이름 함정 근거로만 보존
(진짜 상세는 `GET /service/v3.3/.../live-detail`)

> `watch-event` 3건은 GET only 규칙으로 §B-0에서 제외됐습니다. 호출 금지 경고문도 함께 삭제 — 문서에 없는 API를 경고할 이유가 없습니다.

---

## D. 🆕 신규 반영 대상

### D-1. Manage 경로 정정 — 문서 기재가 실제와 다름

| 문서 기재 | 실제 |
|---|---|
| `/channels/{id}/streams` | 유효하나 실사용은 **`/streaming-info`** |
| `/channels/{id}/live-setting` | **4개로 분리** — `/normal` `/chat` `/chat-mode` `/chat-condition` |
| (없음) | **`manage/v2/channels/{id}/center-status`** — v2 존재 |
| (없음) | `/my-role` `/my-status` `/stats/*` `/streaming-info` `/clips` `/clips/make-clips` `/news-feeds` `/party/summary` `/alerts/{id}/session-url` 등 |

### D-2. Enum 추가 (§14)

| Enum | 추가 값 |
|---|---|
| `orderType` (댓글) | `POPULAR` · `DESC` · **`ASC`** |
| `commentType` | `COMMENT` · **`REPLY`** |
| `userRole` | `USER` · **`STREAMER`** (확정, 제거) |
| `permissions` 🆕 | `VIDEO_DELETE` `VIDEO_HIDE` `LIVE_CREATE` `CHANNEL_MANAGE` `CHAT_MANAGE` `CHAT_BLIND` `SETTLEMENT_MANAGE` `PAID_WATCH_PARTY_SOURCE_PLAY` |
| `dateFilter` / `orderFilter` (클립) 🆕 | `ALL` / `LATEST` |
| `sortType` (구독자) 🆕 | `RECENT` |
| `streamerCurrentGrade` 🆕 | `GRADE_3` |

### D-3. 응답이 비어 항목 구조 미확인인 Manage GET — 11건

`clips` · `clips/make-clips` · `followers` · `news-feeds` · `party/summary` ·
`restrict-release-requests` · `restrict-users` · `stats/lives` · `stats/videos` ·
`subscribers` · `videos`

> 경로·인증은 확정. **응답 스키마만 미상**이므로 "경로 확정 / 스키마 "로 표기하고 남깁니다.

### D-4. 신규 (경미)

- 댓글 응답 최상위에 `totalCount`와 `commentCount`가 **병존**하는 이유 미확인
- `concurrentUserCount`가 `live-status`(1926)와 `live-detail`(4866)에서 크게 다름 — 캡처 시점 차이 추정이나 **애널리틱스에서는 한쪽으로 통일 필요**

---

## E. STEP 2에 미치는 영향

| 변경 | 내용 |
|---|---|
| 🆕 모듈 추가 | **`modules/notification.md`** — `personal/session-url` + `alerts/{id}/session-url` + 이벤트 세션 9종. §12에서 분리 |
| 🆕 모듈 추가 | **`modules/stats.md`** — `manage/v1/.../stats/*`. manage에 섞기엔 가치가 커서 독립 |
| 대폭 확장 | `modules/manage.md` — 20 → 47경로 |
| 전면 재작성 | `reference/analytics.md` — **본인 채널(stats API) / 타 채널(폴링)** 2트랙 |
| 대폭 축소 | `modules/chat.md` — §12.1·12.2 삭제, ver 3으로 교체, **수신 전용** |
| 🆕 대폭 축소 | `modules/manage.md` — 쓰기 계열 제거로 **읽기 전용 스튜디오 조회** 모듈이 됨 |
| 🆕 삭제 | `watch-event` 절 (§7 하위) 통째로 제거 |
| 🆕 README | 상단에 **"이 문서는 GET 전용"** 명시 — 범위를 먼저 못 박아야 읽는 사람이 헷갈리지 않음 |

---

## F. STEP 3 진행에 필요한 것

문서를 쓰려면 아래가 필요합니다. 없으면 해당 부분만 "경로 확정 / 스키마 미상"으로 남깁니다.

- [ ] **Manage 실측 47개 GET 경로 전체 목록** — 현재 이름을 확인한 것은 25개뿐입니다
- [ ] `summaryVideoStat` 외 `stats/*` 응답 전문 (빈 배열이어도 봉투 구조 필요)
- [ ] `manage/v2/channels/{id}/center-status` 응답 예시
- [ ] `streaming-info` 응답에서 **`streamKey`·`streamUrl` 제거한** 나머지 필드 구조
