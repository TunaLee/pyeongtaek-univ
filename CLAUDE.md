# 평택대 · 반도체 품질데이터 분석 · 엔지니어링 (Claude Code)

1일 8교시 강의 덱. 강사는 **Claude 를 활용한 데이터 분석 강사**다 — 반도체 공정 · 이론 · 산업 통계 · 원인 매핑 장은 만들지 않는다.
데이터가 어떤 모양으로 생기는지(테스트 결과 → CSV) 정도만 둔다.

## 작업 규칙
- 답 · 진행 메시지는 한국어. 작업이 끝나면 바로 commit + push (Co-Authored-By 줄 없이).
- 덱을 고칠 때는 `lecture-deck` 스킬(~/.claude/skills/lecture-deck)의 규칙 · references/voice.md 를 따른다.
- 이 저장소는 공개다. 같은 폴더의 팀스파르타 원본 교안 · `커리큘럼_*.png` · `_raw/` 는 고객 자료라 커밋하지 않는다 (.gitignore).

## 빌드 · 검사
```
python3 src/build.py                                   # 한 파일 docs/index.html (교시를 나누지 않는다)
python3 ~/.claude/skills/lecture-deck/scripts/lint.py docs/index.html   # 금칙 0건이어야 완료
tools/shots.sh $PWD/docs/index.html <출력 폴더> [시작 장] [끝 장]        # 마지막 장면 캡처 → 시트로 눈 확인
bash ~/.claude/skills/lecture-deck/scripts/capture_anim.sh $PWD/docs/index.html <장> <초> <out.png>   # 애니메이션 6시점
```
바꾼 장은 반드시 캡처해서 본다(글자 잘림 · 내비 바 겹침 · 애니메이션 끝 장면). 캡처 출력은 스크래치 폴더에.

## 구조
- `src/build.py` 표지 · 과정 지도 → 교시마다 [간지 + `pgen.slides_for(u)`(택배 일반 예 → 반도체 적용) + `p{u}.slides()`] → 마지막 장
- `src/pkit.py` 교시 목록 UNITS · REF(labs/ref.json) · 공통 헬퍼 / `src/p1~p8.py` 교시 본문 / `src/pviz.py · pv2~pv8.py` 애니메이션(anim._D, 접두어 고유)
- 공통 모듈(deck · hx · viz2 · v1kit · v3kit · anim …)은 vibe-coding 저장소에서 복사한 것.
- `labs/make_data.py` 웨이퍼 25장 합성(시드 2611 · ETCH_03 가장자리 · W05 중복 · W11 mV · W19 결측 · W26 은 data/new) · `labs/make_general.py` 택배 25일치 · `labs/make_secom.py` UCI SECOM(CC BY 4.0)
- `labs/wafer-lab/` 수강생 실습 폴더 · `labs/solution/` 완성본 스크립트(실행 전 `cp -r ../wafer-lab/data ./data`, duckdb 는 `.venv/bin/python`)
- **화면 숫자는 손으로 적지 않는다** — ref.json · 완성본 출력 · CSV 에서 코드로 계산해 넣는다.

## 화면 문구 (사용자 반복 지적)
- 제목은 짧은 명사구. 문장형 · 질문형 · 구어체 제목 금지. 「일반 예 ·」 같은 분류 꼬리표 · 「이 강의의 선택 ·」 같은 꾸밈 금지.
- 화면엔 정보(용어 · 사실 · 수치 · 대응 · 조건)만. 설명 문장 · 하단 메모(note) · 그림 캡션 · 카드 밑 부연 · 요약 띠는 넣지 않는다. 말은 강사가 한다.
- 한 장에 정보 덩어리 하나. 넘치면 장을 나눈다. 4행 넘는 설명 표는 카드로.
- 잘 안 쓰는 말(까닭 · 품 · 몫 · 자리) · 직역투 금지. 이모지 금지. 라벨을 「~로」로 끝내지 않는다.
- 출처 줄은 외부 공식 자료를 인용한 장에만. 통계는 2026 최신 공식 자료 + 링크. CC BY 사진은 저작자 표기.
- 개념은 글보다 애니메이션. 애니메이션은 줄이지 않는다. 너무 빨리 바뀌지 않게(장면 간격 2초 이상).
- 실습 장: 순서 · 요청에 들어갈 것을 따로. 완성 요청문을 주지 않고, 요청은 개념 수준으로 짧게.
- 장을 끼워 넣으면 그 교시 순서 전체를 다시 확인한다. 장 번호는 docs/index.html 전체 기준으로 말한다.
- 「~하는 것 · 남는 것」 꼴 제목 · 라벨 금지 → 「커밋 구성」 「요청 항목」 「산출물」
