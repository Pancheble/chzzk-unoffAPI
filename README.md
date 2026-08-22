# 치지직 비공식 API

치지직 웹에서 HAR 떠서 정리한 내부 API 문서임. **115개** 들어있다.

## 구조

```
docs/   문서 25개
book/   docs/ 를 site.html 한 파일로 묶는 생성기
```

`book/site.html` 열면 사이드바 달린 사이트로 볼 수 있다 ㅇㅇ

| | |
|---|---|
| [`docs/core/`](docs/core/) | 호스트, 필수 헤더, 응답 봉투, 식별자 |
| [`docs/modules/`](docs/modules/) | 기능별 API 12개 |
| [`docs/reference/`](docs/reference/) | 엔드포인트 색인, Enum, 애널리틱스, 제외·정정 이력 |

## 읽기 전에 알아둘 것

**HTTP 200 이 성공이 아니더라** 그런데 ㅅㅂ 호스트마다 성공 조건도 다름.

| 봉투 | 호스트 | 성공 |
|---|---|---|
| A형 | `api.chzzk.naver.com` 등 | `code == 200` |
| B형 | `creatorhub-api.naver.com` | `header.code == 0` |

**커스텀 헤더 없으면 상당수가 그냥 실패함** `deviceId` 는 클라이언트가 만드는 UUID 인데
한 번 만들어서 계속 써야 됨 -> [필수 요청 헤더](docs/core/headers.md)

**읽기 전용만 있음.** 방송 설정 변경, 제재, 금지어 편집 같은 쓰기 API 는 일부러 뺐음 귀찮기도 하고
왜 없는지는 [제외된 API](docs/reference/deprecated.md) 에 정리해뒀으니까 알아서 읽어라.

## 이 문서가 왜 있냐

기존 라이브러리랑 실측이 다른 데가 ㅈㄴ 있었음. 그거 바로잡으려고 만든 거임.

| 알려진 것 | 실제 |
|---|---|
| 채팅 서버번호 `sum(charCodes) % 9 + 1` | 공식 자체가 없음. 풀에서 아무 서버나 됨 |
| 채팅 CONNECT `ver: "2"` | `ver: "3"` |
| `ssio{N}.nchat` 이 신규 채팅 | 채팅 아님. 개인 알림 채널 |
| `POST /service/live-status` 가 라이브 상태 | 행동 로그 수집기 |
| `GET /polling/live-detail` 이 라이브 상세 | A/B 테스트 배정 조회 |
| 대댓글 경로 `.../replies` | `replyComments` |

시계열 데이터는 없다 본인 채널은 `manage/v1/.../stats/*` 로 됨

그래서 각 항목에 **어디까지 확인했는지** 같이 적어놨음.
`실측` / `스키마 미상` / `경로만 확인` / `추정` 넷으로 구분함. 추정을 사실처럼 적어두면
이 문서 만든 의미가 없어서.

전체 정정 내역 -> [정정된 사실](docs/reference/deprecated.md#잘못-알려져-있던-사실)

## 고치거나 추가할 때

```bash
python book/build.py        # 사이트 다시 생성
python book/check-links.py  # 링크 검사 <- 이거 필수다
```

목차는 `docs/` 폴더 구조에서 자동으로 나옴. 파일 넣으면 뜨고 지우면 사라진다 ㅇㅇ

`book/site.html` 이랑 `docs/SUMMARY.md` 는 생성물임. 직접 고쳐도 빌드하면 덮임.

## 주의

- 누가 읽을지는 모르겠는데 상업적으로 쓸 거면 [치지직 개발자센터](https://developers.chzzk.naver.com) 공식 API 써라.
- 요청 간격 둬야한다. 몰아서 때리면 IP 차단됨
- **`streamKey` / `accTkn` 같은 건 확인하고 PR땡겨라.**
  크롬 sanitized HAR 은 쿠키랑 요청 헤더만 지우고 **응답 본문은 그대로**
- 댓글, 채팅 응답에 남의 닉네임이랑 `userIdHash` 들어있다 그런데 알빠노

## License
Do What The Fuck You Want To Public License  
당신 좆대로 하세요 공중 라이선스  

See [LICENSE](./LICENSE) file.
