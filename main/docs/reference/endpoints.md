# 엔드포인트 전체 목록

경로로 찾는 평면 인덱스입니다.파라미터와 응답 구조는 각 모듈 문서에 있습니다.

| | |
|---|---|
| 수록 | 115건. 이름 확인 95건 + [미확보 20건](../modules/manage.md#미수록-경로) |
| 범위 | 읽기 전용. 제외된 쓰기 API는 [제외된 API](deprecated.md)에 있습니다 |
| 상태 표기 | 실측 · 스키마 미상 · 경로만 확인 · 추정 · 조회용 POST |
| 부가 표기 | 인증 필요 · 민감 정보 · 애널리틱스 핵심 |
| 갱신 | 엔드포인트를 추가하면 [집계](#집계)의 건수도 함께 수정합니다 |

---

## `api.chzzk.naver.com` — `/service` (43)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 경로만 확인 | `GET /service/v1/ad/display-status` | [commerce](../modules/commerce.md) — 광고 노출 상태 (pgId, pgType — 파라미터 미검증) |
| 실측 · 인증 필요 | `GET /service/v1/badge-awards/unread` | [user](../modules/user.md) — 안 읽은 배지 획득 알림 |
| 실측 | `GET /service/v1/badges/assets/last-updated` | [user](../modules/user.md) — 배지 이미지 에셋 갱신 시각 (badgeType) |
| 실측 | `GET /service/v1/banners` | [discovery](../modules/discovery.md) — 배너 목록 (deviceType, positionsIn) |
| 실측 | `GET /service/v1/categories/live` | [discovery](../modules/discovery.md) — 카테고리별 라이브 (size, 커서 페이지네이션) |
| 실측 · 인증 필요 | `GET /service/v1/channels/followings` | [channel](../modules/channel.md) — 팔로잉 목록 (page, size, sortType) |
| 실측 · 인증 필요 | `GET /service/v1/channels/followings/live` | [channel](../modules/channel.md) — 방송 중인 팔로잉만 |
| 실측 | `GET /service/v1/channels/{channelId}` | [channel](../modules/channel.md) — 채널 기본 정보 |
| 실측 | `GET /service/v1/channels/{channelId}/achievement-badges` | [channel](../modules/channel.md) — 업적 배지 |
| 실측 | `GET /service/v1/channels/{channelId}/announcements` | [channel](../modules/channel.md) — 채널 공지 |
| 실측 | `GET /service/v1/channels/{channelId}/cafe-connection` | [channel](../modules/channel.md) — 카페 연동 정보 |
| 실측 | `GET /service/v1/channels/{channelId}/chat-rules` | [channel](../modules/channel.md) — 채팅 규칙 (읽기, 공개) |
| 실측 | `GET /service/v1/channels/{channelId}/clips` | [clip](../modules/clip.md) — 채널 클립 목록 (filterType, orderType, size, clipUID 커서) |
| 실측 · 애널리틱스 핵심 | `GET /service/v1/channels/{channelId}/data` | [channel](../modules/channel.md) — 채널 부가 데이터 — 개설일·누적 방송시간 (fields) |
| 실측 | `GET /service/v1/channels/{channelId}/donations/chat-setting` | [commerce](../modules/commerce.md) — 채팅 후원 설정 |
| 실측 | `GET /service/v1/channels/{channelId}/donations/mission-setting` | [commerce](../modules/commerce.md) — 미션 후원 설정 |
| 실측 | `GET /service/v1/channels/{channelId}/donations/video-setting` | [commerce](../modules/commerce.md) — 영상 후원 설정 |
| 실측 | `GET /service/v1/channels/{channelId}/follow` | [channel](../modules/channel.md) — 팔로우 정보 |
| 실측 | `GET /service/v1/channels/{channelId}/live-recommended` | [channel](../modules/channel.md) — 추천 라이브 |
| 실측 | `GET /service/v1/channels/{channelId}/live-schedule` | [channel](../modules/channel.md) — 방송 예정 일정 |
| 실측 | `GET /service/v1/channels/{channelId}/log-power/prediction` | [channel](../modules/channel.md) — 로그파워 예측 |
| 실측 | `GET /service/v1/channels/{channelId}/party-donation-info` | [channel](../modules/channel.md) — 파티 후원 정보 |
| 실측 | `GET /service/v1/channels/{channelId}/videos` | [channel](../modules/channel.md) — VOD 목록 — 공개분만 (page, size) |
| 실측 | `GET /service/v1/client-config` | [discovery](../modules/discovery.md) — 클라이언트 설정 + 이벤트 배너 |
| 실측 | `GET /service/v1/clips/upload/enable` | [clip](../modules/clip.md) — 클립 업로드 가능 여부 |
| 실측 | `GET /service/v1/clips/{clipUID}/detail` | [clip](../modules/clip.md) — 클립 상세 (optionalProperties 반복 파라미터) |
| 조회용 POST | `POST /service/v1/clips/detail-bulk` | [clip](../modules/clip.md) — 클립 벌크 조회 — 조회용 POST 예외 (body: clipUIDList[]) |
| 실측 | `GET /service/v1/home/skins` | [discovery](../modules/discovery.md) — 홈 스킨 (이벤트 테마) |
| 경로만 확인 | `GET /service/v1/live/{liveId}/auto-play-info` | [live](../modules/live.md) — 자동재생 정보 (경로만 확인) |
| 경로만 확인 | `GET /service/v1/lives/{liveId}/ads/current` | [live](../modules/live.md) — 현재 광고 (경로만 확인) |
| 경로만 확인 | `GET /service/v1/paid-product/init` | [commerce](../modules/commerce.md) — 유료상품 초기화 (경로만 확인) |
| 실측 · 인증 필요 | `GET /service/v1/personal/personal-data` | [user](../modules/user.md) — 개인 설정 데이터 (fields) |
| 실측 · 인증 필요 · 민감 정보 | `GET /service/v1/personal/session-url` | [notification](../modules/notification.md) — 개인 알림 소켓 URL 발급 (경로만 확인 이름과 달리 '개인 데이터' 아님) |
| 실측 | `GET /service/v1/program-schedules/coming` | [discovery](../modules/discovery.md) — 편성표 |
| 실측 | `GET /service/v1/streamer-partners/recommended` | [discovery](../modules/discovery.md) — 추천 파트너 스트리머 |
| 실측 | `GET /service/v1/topics` | [discovery](../modules/discovery.md) — 토픽 목록 |
| 실측 | `GET /service/v1/topics/HOME/sub-topics/HOME/main` | [discovery](../modules/discovery.md) — 홈 메인 피드 (slotSize) |
| 실측 · 애널리틱스 핵심 | `GET /service/v1/videos/{videoNo}/chats` | [video](../modules/video.md) — 다시보기 채팅 — WebSocket 불필요 (playerMessageTime, previousVideoChatSize) |
| 실측 · 인증 필요 | `GET /service/v1.1/channels/{channelId}/my-info` | [channel](../modules/channel.md) — 내 정보 (팔로우/구독/제재/권한) |
| 실측 | `GET /service/v2/channels/{channelId}/donations/missions` | [commerce](../modules/commerce.md) — 미션 목록 — v2 (filterStatus, page, size) |
| 실측 | `GET /service/v2/nickname/color/codes` | [user](../modules/user.md) — 닉네임 색상 코드 |
| 실측 | `GET /service/v3/videos/{videoNo}` | [video](../modules/video.md) — VOD 상세 — v3 (dt) |
| 실측 | `GET /service/v3.3/channels/{channelId}/live-detail` | [live](../modules/live.md) — 라이브 상세 — v3.3 (cu, dt, tm) |

## `api.chzzk.naver.com` — `/polling` (2)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 실측 | `GET /polling/live-detail` | [live](../modules/live.md) — 경로만 확인 이름 함정: 라이브 상세 아님 — A/B 테스트 배정 (entityId, abTestNoList) |
| 실측 · 애널리틱스 핵심 · 민감 정보 | `GET /polling/v3.1/channels/{channelId}/live-status` | [live](../modules/live.md) — 라이브 상태 — 진짜 시청자 수 폴링용 (includePlayerRecommendContent) |

## `api.chzzk.naver.com` — `/commercial` (6)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 실측 | `GET /commercial/v1/channels/{channelId}/donation-campaigns` | [commerce](../modules/commerce.md) — 후원 캠페인 |
| 실측 | `GET /commercial/v1/cheat-key/promotion-status` | [commerce](../modules/commerce.md) — 치트키 프로모션 상태 |
| 실측 | `GET /commercial/v1/cheat-key/status` | [commerce](../modules/commerce.md) — 치트키 사용 상태 |
| 실측 | `GET /commercial/v1/offerwall/total-reward` | [commerce](../modules/commerce.md) — 오퍼월 누적 리워드 (clientPlatformType) |
| 실측 | `GET /commercial/v1/streamer-shop/{channelId}/notifiable` | [commerce](../modules/commerce.md) — 스트리머 상점 알림 가능 여부 |
| 실측 | `GET /commercial/v1/streamer-shop/{channelId}/products` | [commerce](../modules/commerce.md) — 스트리머 상점 상품 (catalogType) |

## `api.chzzk.naver.com` — `/manage`. 인증 필요 (27)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 경로만 확인 · 인증 필요 | `GET /manage/v1/auto-complete/categories` | [manage](../modules/manage.md) — 카테고리 자동완성 (keyword) |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/alerts/{sessionIOChannelId}/session-url` | [notification](../modules/notification.md) — 이벤트 세션 접속 URL 발급 (9종 — 응답 스키마 미상) |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/chat-rules` | [manage](../modules/manage.md) — 채팅 규칙 (스튜디오) |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/chats/prohibit-words` | [manage](../modules/manage.md) — 금지어 목록 |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/channels/{channelId}/clips` | [manage](../modules/manage.md) — 클립 목록 — 스튜디오 (dateFilter, orderFilter) |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/channels/{channelId}/clips/make-clips` | [manage](../modules/manage.md) — 내가 만든 클립 |
| 스키마 미상 · 인증 필요 · 애널리틱스 핵심 | `GET /manage/v1/channels/{channelId}/followers` | [manage](../modules/manage.md) — 팔로워 목록 — 공개 API에는 없음 |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/live-setting/chat` | [manage](../modules/manage.md) — 채팅 설정 |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/live-setting/chat-condition` | [manage](../modules/manage.md) — 채팅 조건 |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/live-setting/chat-mode` | [manage](../modules/manage.md) — 채팅 모드 |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/live-setting/normal` | [manage](../modules/manage.md) — 방송 기본 설정 |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/my-role` | [manage](../modules/manage.md) — 내 역할 (userRole, permissions) |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/my-status` | [manage](../modules/manage.md) — 내 상태 |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/channels/{channelId}/news-feeds` | [manage](../modules/manage.md) — 뉴스피드 |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/channels/{channelId}/party/summary` | [manage](../modules/manage.md) — 파티 요약 |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/channels/{channelId}/restrict-release-requests` | [manage](../modules/manage.md) — 제한 해제 요청 목록 |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/channels/{channelId}/restrict-users` | [manage](../modules/manage.md) — 활동 제한 사용자 목록 |
| 스키마 미상 · 인증 필요 · 애널리틱스 핵심 | `GET /manage/v1/channels/{channelId}/stats/lives` | [stats](../modules/stats.md) — 방송별 통계 시계열 (from, to — 일별 항목 구조 미상) |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/channels/{channelId}/stats/recent-live` | [stats](../modules/stats.md) — 최근 방송 통계 |
| 스키마 미상 · 인증 필요 · 애널리틱스 핵심 | `GET /manage/v1/channels/{channelId}/stats/videos` | [stats](../modules/stats.md) — VOD별 통계 시계열 (from, to) — avgCv/peakCv/avgKeepWatchingRate |
| 실측 · 인증 필요 · 민감 정보 | `GET /manage/v1/channels/{channelId}/streaming-info` | [manage](../modules/manage.md) — 민감 정보 스트림 키 평문 포함 — streamKey/streamUrl |
| 실측 · 인증 필요 | `GET /manage/v1/channels/{channelId}/streaming-roles` | [manage](../modules/manage.md) — 매니저 목록 |
| 경로만 확인 · 인증 필요 | `GET /manage/v1/channels/{channelId}/streams` | [manage](../modules/manage.md) — 스트림 목록 (실사용은 streaming-info 권장) |
| 스키마 미상 · 인증 필요 · 애널리틱스 핵심 | `GET /manage/v1/channels/{channelId}/subscribers` | [manage](../modules/manage.md) — 구독자 목록 (sortType=RECENT) |
| 경로만 확인 · 인증 필요 | `GET /manage/v1/channels/{channelId}/users/{targetId}/chat-activity-count` | [manage](../modules/manage.md) — 사용자 채팅 활동 횟수 |
| 스키마 미상 · 인증 필요 | `GET /manage/v1/channels/{channelId}/videos` | [manage](../modules/manage.md) — VOD 목록 — 비공개 포함 (스튜디오) |
| 실측 · 인증 필요 | `GET /manage/v2/channels/{channelId}/center-status` | [manage](../modules/manage.md) — 크리에이터 센터 상태 — v2 |
| 추정 ×20 | **미확보** — 실측 47개 중 경로명 미확인 | [manage](../modules/manage.md#미수록-경로) |

## `comm-api.game.naver.com/nng_main` (8)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 실측 · 인증 필요 · 민감 정보 | `GET /v1/chats/access-token` | [chat](../modules/chat.md) — 채팅 액세스 토큰 발급 (channelId, chatType=STREAMING) |
| 실측 · 인증 필요 | `GET /v1/chats/{chatChannelId}/users/{userIdHash}/profile` | [chat](../modules/chat.md) — 채팅 사용자 프로필 (chatType, streamingChannelId) |
| 실측 | `GET /v1/lounge/loungeEvent/chzzk` | [discovery](../modules/discovery.md) — 라운지 이벤트 |
| 실측 · 인증 필요 | `GET /v1/notification/new` | [notification](../modules/notification.md) — 새 알림 여부 (소켓 없이 폴링 확인용) |
| 실측 · 인증 필요 | `GET /v1/privateUserBlocks/allUserIdHash` | [user](../modules/user.md) — 차단 사용자 목록 |
| 실측 · 인증 필요 | `GET /v1/user/getUserStatus` | [user](../modules/user.md) — 로그인 상태 확인 (쿠키 유효성 검사용) |
| 실측 | `GET /v2/search/lounges` | [discovery](../modules/discovery.md) — 라운지 검색 (offset, size) |
| 실측 | `GET /v2/search/lounges/auto-complete` | [discovery](../modules/discovery.md) — 라운지 검색 자동완성 |

## `apis.naver.com/nng_main/nng_comment_api` (2)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 실측 | `GET /v1/type/{objectType}/id/{objectId}/comments` | [comment](../modules/comment.md) — 댓글 목록 (limit, offset, orderType, pagingType=PAGE) |
| 실측 | `GET /v1/type/{objectType}/id/{objectId}/comments/{commentId}/replyComments` | [comment](../modules/comment.md) — 대댓글 (offset만, limit 없음) |

## `creatorhub-api.naver.com` — 응답 봉투 B형 (4)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 실측 | `GET /api/v4.0/comment/sticker` | [comment](../modules/comment.md) — 팩 내 스티커 목록 (packCode, stickerServiceCode) |
| 실측 | `GET /api/v4.0/comment/sticker/pack` | [comment](../modules/comment.md) — 스티커 팩 목록 (stickerServiceCode=chzzk) |
| 실측 · 애널리틱스 핵심 | `GET /api/v5.0/clipviewer/card` | [clip](../modules/clip.md) — 클립 원본 영상 매핑 — extraLinks에 원본 VOD/오프셋 (seedType, seedMediaId 등) |
| 실측 | `GET /api/v5.0/clipviewer/cards` | [clip](../modules/clip.md) — 클립 뷰어 추천 피드 (무한스크롤) |

## `apis.naver.com/neonplayer` (1)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 실측 | `GET /neonplayer/vodplay/v3/playback/{videoId}` | [video](../modules/video.md) — VOD 재생 매니페스트 — 응답 XML(DASH MPD) (key=inKey 등) |

## WebSocket (2)

| 상태 | 경로 | 모듈 |
|---|---|---|
| 실측 · 인증 필요 | `wss://kr-ss{N}.chat.naver.com/chat` | [chat](../modules/chat.md) — 실시간 채팅 수신. {N}은 서버 풀 내 임의 번호 — 공식 없음 |
| 실측 · 인증 필요 · 민감 정보 | `wss://ssio{N}.nchat.naver.com/socket.io/?auth=&EIO=3&transport=websocket` | [notification](../modules/notification.md) — 개인 알림 채널 (Engine.IO v3). URL 전체를 session-url 응답이 반환 |

---

## 집계

| 호스트 / 접두사 | 건수 |
|---|---|
| `api.chzzk.naver.com` — `/service` | 43 |
| `api.chzzk.naver.com` — `/polling` | 2 |
| `api.chzzk.naver.com` — `/commercial` | 6 |
| `api.chzzk.naver.com` — `/manage`. 인증 필요 | 27 + **미확보 20** |
| `comm-api.game.naver.com/nng_main` | 8 |
| `apis.naver.com/nng_main/nng_comment_api` | 2 |
| `creatorhub-api.naver.com` — 응답 봉투 B형 | 4 |
| `apis.naver.com/neonplayer` | 1 |
| WebSocket | 2 |
| **합계** | **95 + 20 = 115** |

