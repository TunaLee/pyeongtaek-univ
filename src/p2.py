"""2교시 웨이퍼 데이터 · 집계 자동화 · CLAUDE.md.

도입(웨이퍼와 칩 · 엑셀 행과 맵 칸) → 설명(같은 질문 세 가지 도구 · 수율 계산 · 사과 집계 표 · 칩 집계 표(시트 세 장)
· 엑셀과 CSV · 새 대화의 시작 · CLAUDE.md · 확인할 수 있는 문장 · 숫자 대조)
→ 적용(실습 2-1 웨이퍼 데이터 읽기 · 차트(1교시 순서 그대로) → 2-2 집계 엑셀 · CSV(사과 · 웨이퍼)).
웨이퍼 열 목록(18개 묶음)은 보여 주지 않는다 — 측정값 이름은 몰라도 됨.
"""
import p0
import psim
import sk
import viz2
from deck import lab, light
from hx import code, esc, photo
from pkit import LAB, brief, chat, tag

T = tag("2")
WN, DN = sk.WN, sk.DN
TOP = max(DN["reason"], key=DN["reason"].get)
TOPK = sk.D_KO[TOP]
WTOP = max(WN["reason"], key=WN["reason"].get)
IO_LIM = sk.SIM["wafer"]["spec"]["ioff_na"]["hi"]                    # 누설전류 합격선(기준표)
IO_LOW = (sk.W07["ioff_na"] < 5).mean() * 100
IO_OVER = int((sk.W07["ioff_na"] > IO_LIM).sum())
CSS = """
  .p2eq{font-size:40px; font-weight:800; color:#16233A; text-align:center; margin:30px 0 26px;}
  .p2eq em{font-style:normal; color:#F28C28;}
  .p2wb{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; align-items:start; margin-top:6px;}
  .p2wb .p0x{opacity:0; animation:p2In .5s var(--d) forwards;}
  .p2wb .p0x td{font-size:15px; padding:7px 10px;} .p2wb .p0x tr.h td{font-size:13.5px;}
  .p2wb .p0x tr.top td{background:#FFF3E6; font-weight:800;}
  .p2wb .tabs{display:flex; border-top:1px solid #DADCE0; background:#F8F9FA; font-size:12.5px;}
  .p2wb .tabs span{padding:5px 12px; color:#5F6368; border-right:1px solid #DADCE0;}
  .p2wb .tabs span.on{background:#fff; color:#1D6F42; font-weight:800; border-bottom:2px solid #1D6F42;}
  @keyframes p2In{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.p2wb .p0x{animation:none; opacity:1}}
"""


def workbook(name, sheets):
    """엑셀 파일 하나 · 시트 세 장을 나란히 — sheets=[(탭, 머리 행, 행들, 강조 행 번호)] · 2초 간격."""
    tabs = [t for t, *_ in sheets]
    out = ""
    for i, (tab, head, rows, top) in enumerate(sheets):
        hr = '<tr class="h">' + "".join(f"<td>{h}</td>" for h in head) + "</tr>"
        body = "".join(f'<tr class="{"top" if j == top else ""}">' + "".join(
            f'<td class="{"n" if k else ""}">{v}</td>' for k, v in enumerate(r)) + "</tr>" for j, r in enumerate(rows))
        tb = "".join(f'<span class="{"on" if t == tab else ""}">{t}</span>' for t in tabs)
        out += (f'<div class="p0x" style="--d:{.3 + i * 2:.1f}s"><div class="bar">{name}.xlsx · {tab}</div>'
                f'<table>{hr}{body}</table><div class="tabs">{tb}</div></div>')
    return f'<div class="p2wb">{out}</div>'


def _zones(df, col, ok, keys, ko=None):
    """위치별 시트 행 (위치 · 전체 · 합격 · 비율) 과 비율이 가장 낮은 행 번호."""
    g = df.groupby(col)
    rows = [((ko or {}).get(k, k), len(g.get_group(k)), int((g.get_group(k)[ok[0]] == ok[1]).sum())) for k in keys]
    low = min(range(len(rows)), key=lambda i: rows[i][2] / rows[i][1])
    return [(z, n, k, f"{k / n * 100:.2f}%") for z, n, k in rows], low


def _claude_md():
    """sim-lab/CLAUDE.md 에서 10줄 — 제목 · 만드는 것 · 작업 규칙 셋 · 정답 숫자."""
    t = [x for x in (LAB / "sim-lab" / "CLAUDE.md").read_text(encoding="utf-8").split("\n") if x.strip()]
    i = t.index("## 작업 규칙")
    j = t.index(next(x for x in t if x.startswith("## 정답 숫자")))
    return "\n".join([t[0], t[1], t[2], t[i], t[i + 1], t[i + 3], t[i + 5], t[j], t[j + 1], t[j + 2]])


def slides():
    return [
        # ── 도입 · 웨이퍼 데이터
        light("웨이퍼와 칩", f'<div class="phmap v3ph">{photo("wafer_photo.webp", "웨이퍼")}' + viz2.maprows([
            ("칩", "웨이퍼 위 네모 한 칸", f"한 장에 {WN['rows']}개"), ("합격 · 불합격", "칩마다 검사 결과", "PASS · FAIL"),
            ("수율", "합격 칩 ÷ 전체 칩", f"W07 · {WN['yield']}%")], "용어", "뜻") + "</div>", T),
        light("엑셀 행과 맵 칸", psim.row_to_cell(), T),
        # ── 설명 · 집계
        light("같은 질문, 세 가지 도구", p0.three_tools(), T),
        light("수율 계산", f'<div class="p2eq">수율 = <em>합격 {WN["pass"]}</em> ÷ 전체 {WN["rows"]} = <em>{WN["yield"]}%</em></div>'
              + viz2.tiles([("사과 상품률", f"상품 {DN['pass']} ÷ 전체 {DN['rows']} = {DN['rate']}%"),
                            ("같은 계산", "조건에 맞는 행 수 ÷ 전체 행 수")], 2), T),
        light("사과 집계 표", workbook("apple_summary", [
            ("요약", ["항목", "값"], [("전체", DN["rows"]), ("상품", DN["pass"]), ("불량", DN["fail"]), ("상품률", f"{DN['rate']}%")], 3),
            ("사유별", ["불량 사유", "개수"], [(sk.D_KO[k], v) for k, v in sorted(DN["reason"].items(), key=lambda x: -x[1])], 0),
            ("위치별", ["위치", "전체", "상품", "상품률"], *_zones(sk.D07, "위치", ("등급", "상품"), sk.AREA))]), T),
        light("칩 집계 표", workbook("yield_summary", [
            ("요약", ["항목", "값"], [("전체", WN["rows"]), ("합격", WN["pass"]), ("불합격", WN["fail"]), ("수율", f"{WN['yield']}%")], 3),
            ("사유별", ["불합격 사유", "칩 수"], [(sk.KO[k], v) for k, v in sorted(WN["reason"].items(), key=lambda x: -x[1])], 0),
            ("위치별", ["위치", "전체", "합격", "합격률"], *_zones(sk.W07, "zone", ("pass_fail", "PASS"), ("center", "mid", "edge"), sk.ZONE_KO))]), T),
        light("엑셀과 CSV", p0.excel_vs_csv(sk.D07.head(4)[["날짜", "사과번호", "가로칸", "세로칸", "위치", "품종", "무게", "당도", "등급"]],
                                          full=sk.D07.columns), T),
        # ── 설명 · CLAUDE.md
        light("새 대화의 시작", viz2.pair(
            "CLAUDE.md 없음", [("새 대화", "폴더 · 규칙 · 정답 숫자를 모름"), ("사람", "대화마다 같은 설명 반복"),
                              ("결과", "원본 수정 · 낯선 용어 · 다른 숫자")],
            "CLAUDE.md 있음", [("새 대화", "CLAUDE.md 부터 읽고 시작"), ("사람", "한 번 적어 두고 필요할 때 고침"),
                              ("결과", "같은 규칙 · 같은 정답 숫자")]), T),
        light("CLAUDE.md", '<div class="twocol w"><div>' + code("sim-lab/CLAUDE.md", esc(_claude_md())) + "</div><div>"
              + viz2.tiles([("위치", "sim-lab/CLAUDE.md · 폴더 맨 위"), ("내용", "만드는 것 · 폴더 · 데이터 · 작업 규칙 · 정답 숫자"),
                            ("고치는 때", "같은 말을 두 번 하게 될 때")], 1) + "</div></div>", T),
        light("확인할 수 있는 문장", viz2.pair(
            "흐린 규칙", [("말투", "「친절하게 답해」"), ("결과", "「깔끔하게 만들어」"), ("숫자", "「정확하게 계산해」")],
            "확인할 수 있는 규칙", [("말투", "「반도체 용어를 새로 꺼내지 않는다」"), ("결과", "「output/simulator.html 한 파일」"),
                              ("숫자", f"「정답은 {WN['rows']} · {WN['pass']} · {WN['fail']} · {WN['yield']}%」")]), T),
        light("숫자 맞춰 보기", viz2.maprows([
            ("Claude 보고", f"합격 {WN['pass']}", "요청 결과"), ("엑셀 필터", f"pass_fail = PASS · {WN['pass']}행", "사람이 직접"),
            ("다르면", "어느 쪽이 맞는지 행 단위로 확인 요청", "그대로 넘어가지 않음")], "확인", "W07"), T),
        # ── 적용
        lab("2-1", "웨이퍼 데이터 읽기 · 차트", T, "1교시 순서 그대로 W07 을 요약하고 누설전류 분포 · 사유별 불합격 막대 · 웨이퍼 맵을 그린다",
            ["W07 요약 요청", "누설전류 분포 요청", "사유별 불합격 막대 요청", "웨이퍼 맵 요청"],
            [f"{WN['rows']}행 · 합격 {WN['pass']} · 불합격 {WN['fail']} · 수율 {WN['yield']}%", f"불합격 1위 {sk.KO[WTOP]} {WN['reason'][WTOP]}개",
             "output/charts/ HTML 세 장"], files="data/wafer_test_W07.xlsx"),
        light("웨이퍼 차트 결과", sk.trio([("sim/chart_wafer_hist.webp", "누설전류 분포"), ("sim/chart_wafer_reason.webp", "사유별 불합격"),
                                        ("sim/chart_wafer_map.webp", "웨이퍼 맵")]), T),
        light("웨이퍼 차트에서 읽은 사실", viz2.tiles([
            ("누설전류 분포", f"{IO_LOW:.0f}% 가 5 nA 아래에 몰림 · {IO_LIM} nA 넘는 칩 {IO_OVER}개가 멀리 떨어짐"),
            ("사유별 불합격", f"{sk.KO[WTOP]} {WN['reason'][WTOP]}개 · 불합격 {WN['fail']}개의 {WN['reason'][WTOP] / WN['fail'] * 100:.0f}%"),
            ("웨이퍼 맵", f"{sk.KO[WTOP]} 칸이 대각선 한 줄로 이어짐")], 3), T),
        lab("2-2", "집계 엑셀 · CSV", T, "사과 · 웨이퍼를 사유별 · 위치별로 집계해 엑셀 시트 세 장과 CSV 로 저장한다",
            ["CLAUDE.md 정답 숫자 확인", "사과 집계 · CSV 요청", "웨이퍼 집계 · CSV 요청", "엑셀 필터로 대조"],
            [f"사과 상품률 {DN['rate']}% · 웨이퍼 수율 {WN['yield']}%", "apple_summary.xlsx · yield_summary.xlsx (시트 3장)",
             "apple_A07.csv · wafer_test_W07.csv"], files="data/apple_A07.xlsx · data/wafer_test_W07.xlsx"),
        brief("2-2", T,
              ["CLAUDE.md 정답 숫자 확인", "사과 집계 · CSV", "웨이퍼 집계 · CSV", "엑셀 필터로 대조"],
              [("목표", "요약 · 사유별 · 위치별 집계"), ("입력", "apple_A07.xlsx · wafer_test_W07.xlsx"),
               ("산출물", "집계 엑셀 2개(시트 3장) · CSV 2개"), ("하지 말 것", "data/ 원본 수정")],
              [], [f"상품 {DN['pass']} · 합격 {WN['pass']}", "사유별 합 = 불량 · 불합격 수"], ""),
        light("실습 2-2 확인", chat([
            ("me", "yield_summary.xlsx 의 사유별 시트 합계가 불합격 수와 같은지 확인해 줘."),
            ("ai", f"사유별 합계 {sum(WN['reason'].values())} · 불합격 {WN['fail']} · 같음\n"
                   + " · ".join(f"{sk.KO[k]} {v}" for k, v in WN["reason"].items()))], "확인 대화 예"), T),
    ]
