"""7교시 조절 바 전체 · Skill.

도입(조절 바 설계표) → 설명(왼쪽 조절 · 오른쪽 결과 · 처음 값과 원본 대비 · 숫자 점검 · 컨텍스트 · 비우기와 요약 · Skill · Skill 폴더)
→ 적용(실습 7-1 사과 조절 바 전체 → 7-2 웨이퍼 조절 바 8종).
"""
import psim
import sk
import viz2
from deck import lab, light
from hx import code, esc
from pkit import brief, tag
from stats_hx import src

T = tag("7")
WN, DN = sk.WN, sk.DN
CSS = ""

WS, DS = sk.SIM["wafer"], sk.SIM["apple"]
UNIT = {"rc_ohm": "Ω", "ioff_na": "nA", "vth_v": "V", "particle_cnt": "개", "idsat_ma": "mA", "ox_thk_nm": "nm", "radius_mm": "mm"}


SKILL = """---
name: sim-check
description: 시뮬레이터 숫자를 점검할 때. 조절 바를
  움직인 뒤 카드 · 맵 · 차트 숫자를 대조한다.
---
1. 조절 바 네 가지를 정답표.md 순서로 움직인다
2. 카드 · 맵 · 차트 · 분포 숫자를 기록한다
3. 정답표와 다르면 다른 곳만 표로 보고한다"""


def _design():
    rows = []
    for c, v in WS["spec"].items():
        if "on" in v:
            rows.append((sk.COL_KO[c], c, "체크 · 판정 켜기"))
            continue
        lo, hi, u = v.get("lo"), v.get("hi"), UNIT[c]
        cond = f"{lo:g} ~ {hi:g} {u}" if lo is not None and hi is not None else (f"{lo:g} {u} 이상" if lo is not None else f"{hi:g} {u} 이하")
        rows.append(("중심에서 거리", c, cond + " · 집계 범위") if c == "radius_mm" else (sk.COL_KO[c], c, cond))
    return viz2.tiles([(name, f"{col} · {cond}") for name, col, cond in rows], 4)


def slides():
    chk = WS["s7_checks"]
    return [
        # ── 도입
        light("조절 바 설계표", _design(), T),
        # ── 설명
        light("왼쪽 조절 · 오른쪽 결과", sk.duo("sim/wafer_s7.webp", "sim/wafer_s7_moved.webp", "처음 값", "누설전류 상한 5 nA"), T),
        light("처음 값과 원본 대비", viz2.tiles([
            ("처음 값 버튼", "조절 바 8개를 기준표 값으로"), ("원본 대비", f"엑셀 원본 수율 {WN['yield']}% 와 차이 · 예 {chk[0]['delta_pp']:+.2f}%p"),
            ("걸림 수", "조절 바마다 그 기준에 걸린 칩 수")], 3), T),
        light("숫자 점검 항목", viz2.maprows([(c["op"], f"수율 {c['rate']:.2f}%", f"합격 {c['pass']} / {c['total']} · {c['delta_pp']:+.2f}%p") for c in chk], "조작", "기대 숫자"), T),
        # ── 설명 · 컨텍스트 · Skill
        light("컨텍스트", psim.context_fill()
              + src(("Claude Code 문서 · Context window", "https://code.claude.com/docs/en/context-window")), T),
        light("비우기와 요약", viz2.tiles([
            ("/clear", "대화를 비움 · CLAUDE.md 는 다시 읽음"), ("/compact", "지금까지를 요약해 이어 감"),
            ("쓰는 때", "교시가 바뀔 때 · 다른 일로 넘어갈 때"), ("남기는 법", "결정 · 숫자는 파일로(docs/)")], 2)
              + src(("Claude Code 문서 · Commands", "https://code.claude.com/docs/en/commands")), T),
        light("매번 같은 설명", viz2.pair(
            "요청마다 설명", [("1교시", "「숫자 보고할 때 네 가지 다」"), ("6교시", "「상한 5 · 20 숫자도」"), ("7교시", "「여덟 개 다 · 같은 형식」")],
            "Skill 한 번", [("저장", ".claude/skills/sim-check/SKILL.md"), ("부르기", "「숫자 점검해 줘」"), ("결과", "매번 같은 순서 · 같은 표")]), T),
        light("Skill 이 열리는 단계", psim.skill_trigger()
              + src(("Claude Code 문서 · Skills", "https://code.claude.com/docs/en/skills")), T),
        light("SKILL.md", '<div class="twocol w"><div>' + code(".claude/skills/sim-check/SKILL.md", esc(SKILL)) + "</div><div>"
              + viz2.tiles([("name", "Skill 이름 · 폴더 이름과 같게"), ("description", "언제 쓰는지 · Claude 가 고르는 기준"),
                            ("본문", "단계 · 산출물 형식")], 1) + "</div></div>", T),
        # ── 적용
        lab("7-1", "사과 조절 바 6종", T, "판정 4종(멍 · 벌레 체크 · 무게 하한 · 당도 하한)과 집계 범위 2종(중심에서 거리 · 지름) 조절 바를 만들고 두 칸으로 배치한다",
            ["조절 바 설계표 요청", "조절 바 전체 · 처음 값 버튼", "두 칸 배치", "sim-check Skill 로 숫자 점검"],
            [f"{DS['s7_checks'][0]['op']} → {DS['s7_checks'][0]['rate']:.2f}%", f"{DS['s7_checks'][1]['op']} → {DS['s7_checks'][1]['rate']:.2f}%", "처음 값 버튼 → 원래 숫자"], files="output/apple_sim.html"),
        light("사과 조절 바 6종 결과", sk.one("sim/apple_s7.webp", "사과 조절 바 6종"), T),
        lab("7-2", "조절 바 8종", T, "기준표 일곱 측정값 + 집계 범위(중심에서 거리)에 조절 바를 만들고 처음 값 · 원본 대비를 넣는다",
            ["조절 바 설계표 요청", "조절 바 8종 · 분포 · 합격선", "왼쪽 조절 · 오른쪽 결과", "처음 값 · 원본 대비", "숫자 점검 항목"],
            ["점검 네 가지 · " + " · ".join(f"{c['rate']:.2f}%" for c in chk), f"처음 값 → {WN['yield']}%"], files="output/simulator.html"),
        brief("7-2", T,
              ["설계표", "조절 바 8종", "배치", "처음 값 · 원본 대비", "숫자 점검"],
              [("목표", "기준표 전 항목 조절 바"), ("입력", "합격기준표.md"),
               ("산출물", "simulator.html 왼쪽 조절 · 오른쪽 결과"), ("하지 말 것", "판정 순서 바꾸기 · 기존 화면 지우기")],
              [], [f"처음 값 → {WN['yield']}%", "네 가지 점검 숫자 일치"], ""),
    ]
