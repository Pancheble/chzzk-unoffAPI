# Enum 레퍼런스

요청 파라미터와 응답 필드에 사용되는 값의 목록입니다.\
관측된 값만 수록하며, 존재가 추정되나 캡처되지 않은 값은 미확인으로 표기합니다.

| | |
|---|---|
| 관련 문서 | [엔드포인트 전체 목록](endpoints.md) · [식별자](../core/conventions.md#식별자) |

***

## 콘텐츠

| Enum | 값 |
|---|---|
| categoryType | `GAME` · `SPORTS` · `ETC` |
| status (라이브) | `OPEN` · `CLOSE` |
| videoType | `REPLAY` · `UPLOAD` |
| vodStatus | `ABR_HLS` |
| mediaType | `SHORT_FORM` |
| cardType | `CONTENT` |
| mediaScaleType | `CROP` |
| 화질 트랙 | `144p` · `360p` · `480p` · `720p` · `1080p` · `alow.stream` |

***

## 채팅

| Enum | 값 |
|---|---|
| chatAvailableGroup | `ALL` · `FOLLOWER` · `MANAGER` · `SUBSCRIBER` |
| chatAvailableCondition | `NONE` · `REAL_NAME` |
| messageTypeCode | `1` TEXT · `2` IMAGE · `3` STICKER · `4` VIDEO · `5` RICH · `10` DONATION · `11` SUBSCRIPTION · `30` SYSTEM_MESSAGE |
| messageStatusType | `NORMAL` |
| chatType | `STREAMING` |
| CONNECT auth | `SEND`. `READ` 는 미확인 |
| CONNECT ver | `3`. 공개 라이브러리에 알려진 `2` 는 구버전 |

### cmd 코드

수신에 사용되는 코드입니다. 송신 코드 `3101 SEND_CHAT` 은 이 문서의 범위 밖입니다.

| cmd | 이름 |
|---|---|
| 0 / 10000 | PING / PONG |
| 100 / 10100 | CONNECT / CONNECTED |
| 5101 / 15101 | REQUEST_RECENT_CHAT / RECENT_CHAT |
| 93101 | CHAT |
| 93102 | DONATION |
| 93006 | EVENT |
| 94005 / 94006 / 94008 | KICK / BLOCK / BLIND |
| 94010 / 94015 | NOTICE / PENALTY |

***

## 사용자 · 권한

| Enum | 값 |
|---|---|
| userRole | `USER` · `STREAMER`. `MANAGER` 는 미확인 |
| userRoleCode | `common_user`. `streamer` 와 `manager` 는 미확인 |
| userAdultStatus | `AGE_RESTRICTION` · `null` |
| restrictReleaseState | `NONE`. 그 외 값은 미확인 |
| streamerCurrentGrade | `GRADE_3` |

### permissions

스트리머 본인일 때 반환되는 권한 값입니다.

`VIDEO_DELETE` · `VIDEO_HIDE` · `LIVE_CREATE` · `CHANNEL_MANAGE` ·
`CHAT_MANAGE` · `CHAT_BLIND` · `SETTLEMENT_MANAGE` · `PAID_WATCH_PARTY_SOURCE_PLAY`

***

## 댓글

| Enum | 값 |
|---|---|
| objectType | `STREAMING_VIDEO` · `CHANNEL_POST` · `CLIP` |
| commentType | `COMMENT` · `REPLY` |
| orderType | `POPULAR` · `DESC` · `ASC` |
| pagingType | `PAGE` |
| attachType | `PHOTO` · `STICKER` |

`objectType` 마다 `objectId` 의 형식이 다릅니다. ([objectType 참조](../modules/comment.md#objecttype))

***

## 클립

| Enum | 값 | 사용처 |
|---|---|---|
| orderType | `RECENT`. `POPULAR` 는 미확인 | 공개 API |
| filterType | `ALL`. 그 외 값은 미확인 | 공개 API |
| dateFilter | `ALL` | 스튜디오 |
| orderFilter | `LATEST` | 스튜디오 |
| optionalProperties | `COMMENT` · `PRIVATE_USER_BLOCK` · `PENALTY` · `MAKER_CHANNEL` · `OWNER_CHANNEL` | 반복 파라미터 |
| seedType | `SPECIFIC` | Creator Hub |
| serviceType | `CHZZK` | Creator Hub |
| recType | `CHZZK` | Creator Hub |
| panelType | `sdk_chzzk` | Creator Hub |
| deviceType | `html5_mo` | Creator Hub |
| extraLinks.type | `TEXT` · `GENRE` | Creator Hub |

***

## 채널 · 기타

| Enum | 값 |
|---|---|
| sortType (팔로잉) | `FOLLOW`. 그 외 값은 미확인 |
| sortType (구독자) | `RECENT` |
| tvAppViewingPolicyType | `ALLOWED` |
| catalogType (상점) | 미확인 |
| serviceId (Creator Hub) | `2113`. 치지직 클립 고정값으로 보이나 미확인 |

***

## 알림 세션 타입

`donation@` · `subscription@` · `gift@` · `partydonation@` · `mission@` ·
`newsfeed@` · `video@` · `studio@` · `streamershop@`

([이벤트 세션 9종 참조](../modules/notification.md#이벤트-세션-9종))

***

## 제외된 Enum

읽기 전용 범위 밖이라 수록하지 않은 값입니다.

| Enum | 사유 |
|---|---|
| watchEventType (`WATCH_STARTED` 등) | `watch-event` 가 제외됨 ([제외된 API 참조](deprecated.md)) |
