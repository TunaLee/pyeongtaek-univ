"""2교시 데이터 정제 · 검증.

배경(지저분한 이유 · SECOM 실측) → 비유(택배 검수) → 원시 파일 속 문제(애니) → 정제 단계(애니) → 중복 · 단위 함정(애니) · 결측
→ 검증 규칙(애니) · 검증 보고서 → 원본은 읽기만 → Claude Code 에 맡기기 → 실습 2.
숫자는 labs/wafer-lab/data · labs/solution/scripts(clean.py) 를 직접 돌려 얻는다.
"""
import sys

import pandas as pd

import pv2
import viz2
from deck import lab, light
from hx import code, esc, note
from pkit import LAB, REF, SOL, W, brief, chat, codemap, tag
from stats_hx import big, hbars, src

sys.path.insert(0, str(SOL / "scripts"))
from clean import clean, validate  # noqa: E402
from common import rejudge  # noqa: E402

T = tag("2")
RAW = LAB / "wafer-lab" / "data" / "raw"
SEC = REF["secom"]
SECOM_SRC = ("UCI ML Repository · SECOM (McCann & Johnston, 2008) · CC BY 4.0 · doi:10.24432/C54305",
             "https://archive.ics.uci.edu/dataset/179/secom")


def _raw(w):
    return pd.read_csv(RAW / f"wafer_test_W{w}.csv")


R05, R11, R19 = _raw("05"), _raw("11"), _raw("19")
C05, I05 = clean(R05)
C11, I11 = clean(R11)
C19, I19 = clean(R19)
N_DUP = len(R05) - len(C05)
N_NA = int(R19.ioff_na.isna().sum())
TRAP = rejudge(R11)                                    # 단위 확인 없이 판정
N_TRAP = int((TRAP.fail_type == "vth_shift").sum())
Y11 = (C11.pass_fail == "PASS").mean() * 100
Y19 = (C19.pass_fail == "PASS").mean() * 100
RULES = [r for r, _ in validate(C11)]
QC11 = "\n".join(x for x in (SOL / "output" / "qc_W11.md").read_text(encoding="utf-8").split("\n") if x.strip())


def _secom_cols():
    """SECOM 열 590개 중 결측 · 상수 없이 그대로 쓸 수 있는 열 수."""
    X = pd.read_csv(LAB / "wafer-lab" / "data" / "secom" / "secom.csv").drop(columns=["timestamp", "result"])
    return int(((X.isna().sum() == 0) & (X.nunique() > 1)).sum())


SEC_OK = _secom_cols()


def _rows(df, idx):
    return [(str(df.die_x[i]), str(df.die_y[i]), f"{df.vth_v[i]:g}", "" if pd.isna(df.ioff_na[i]) else f"{df.ioff_na[i]:g}") for i in idx]


def _show05():
    """중복 한 쌍이 1 · 3 번째 줄에 오도록 고른 다섯 줄."""
    dup = R05[R05.duplicated(["die_x", "die_y"], keep="last")].index[0]
    twin = R05[(R05.die_x == R05.die_x[dup]) & (R05.die_y == R05.die_y[dup])].index
    a, b = twin[0], twin[-1]
    return _rows(R05, [0, a, 1, b, 2])


def _show19():
    na = R19[R19.ioff_na.isna()].index[0]
    return _rows(R19, [na - 2, na - 1, na, na + 1, na + 2])


def slides():
    return [
        # ── 배경
        light("공정 데이터가 지저분한 이유", viz2.tiles([
            ("장비 · 프로그램 차이", "테스터마다 단위 · 열 이름이 다름"), ("재측정 · 재전송", "같은 다이 결과가 두 번 들어옴"),
            ("측정 실패", "접촉 불량 · 장비 정지 → 빈칸"), ("사람 손", "엑셀에서 열고 저장하며 형식이 바뀜")], 2), T),
        light("실제 공정 데이터 · UCI SECOM", big([
            (f"{SEC['rows']:,}", "행", "생산 단위 (2008년 7~10월)"), (f"{SEC['features']}", "열", "공정 센서 값 · 이름 비공개"),
            (f"{SEC['fail']}", "건", "불량 (FAIL)", True)], 3)
              + src(SECOM_SRC), T),
        light("SECOM 의 결측 · 상수 열", hbars([
            ("결측이 하나라도 있는 열", SEC["cols_any_missing"], True, f"{SEC['cols_any_missing']} / {SEC['features']}"),
            ("값이 하나뿐인 열", SEC["cols_constant"], False, f"{SEC['cols_constant']}"),
            ("결측 50% 넘는 열", SEC["cols_missing_over50"], False, f"{SEC['cols_missing_over50']}"),
            ("그대로 쓸 수 있는 열", SEC_OK, False, f"{SEC_OK}")], top=SEC["features"])
              + src(SECOM_SRC), T),
        light("비유 · 택배 분류장 검수", viz2.maprows([
            ("같은 상자 두 번 스캔", "중복 행", "한 번만 남김"), ("무게 g · kg 섞임", "단위 오류", "한 단위로 통일"),
            ("주소 빈칸", "결측", "따로 표시 · 재확인"), ("검수 통과 도장", "검증 규칙", "통과한 것만 출고")], "분류장", "데이터"), T),
        # ── 원시 파일 속 문제
        light("원시 파일 속 문제", pv2.raw_issues(_show05(), _rows(R11, range(5)), _show19()), T),
        light("정제 단계", pv2.clean_steps(len(R05), N_DUP, N_NA, len(C05)), T),
        light("중복 기준", codemap([
            ('df.drop_duplicates(subset=["wafer_id", "die_x", "die_y"])', "같은 웨이퍼 · 같은 좌표면 한 줄만"),
            ("len(raw) - len(df)", f"지운 줄 수 · W05 = {N_DUP}"),
            ('df.duplicated(["die_x", "die_y"]).any()', "남은 중복이 있나 · False 여야 함")],
            ask="같은 다이가 두 번 들어온 줄을 지워 줘", title="clean.py"), T),
        light("단위 오류의 함정 · W11", pv2.unit_trap(int(R11.vth_v[0]), N_TRAP, Y11), T),
        light("결측 처리 세 가지", viz2.pair(
            "지우기 · 채우기", [("지우기", "다이 수가 줄어 수율 분모가 바뀜"), ("평균으로 채우기", "측정하지 않은 값을 만듦")],
            "표시하기", [("RETEST", "측정값이 빈 다이는 재측정 대상"), ("수율", "PASS 로 세지 않음 · 개수는 보고서에")]), T),
        light("W19 결측 처리 결과", big([
            (f"{N_NA}", "개", "ioff_na 빈 다이 → RETEST"), (f"{W('W19')['yield']}", "%", "테스터 판정 수율"),
            (f"{Y19:.2f}", "%", "다시 판정한 수율", True)], 3), T),
        # ── 검증
        light("검증 규칙", pv2.gate(RULES), T),
        light("검증 보고서", '<div class="twocol w"><div>' + code("output/qc_W11.md", esc(QC11)) + "</div><div>"
              + viz2.tiles([("발견한 문제", "무엇을 · 몇 개 · 어떻게 고쳤나"), ("검증 규칙", "통과 · 실패 체크"),
                            ("쓰는 곳", "파이프라인 기록 · 분석 요약의 근거")], 1) + "</div></div>", T),
        light("원본 보존", viz2.pair(
            "원본 직접 수정", [("data/raw/", "W11 의 vth_v 를 직접 수정"), ("다음 날", "무엇을 바꿨는지 알 수 없음")],
            "정제본 별도 저장", [("data/raw/", "테스터가 준 그대로"), ("output/clean/", "clean.py 가 매번 새로 만듦")]), T),
        light("Claude Code 에 정제 맡기기", chat([
            ("me", "data/raw 의 W05 · W11 · W19 를 검사해 줘. 고치지 말고 문제만 보고."),
            ("ai", f"W05 · 같은 좌표 {N_DUP}줄 중복 ({len(R05)}행)\nW11 · vth_v 중앙값 {R11.vth_v.median():g} → mV 로 보임\n"
                   f"W19 · ioff_na 빈칸 {N_NA}개")], "검사 대화 예"), T),
        # ── 실습
        lab("2-2", "정제 · 검증 스크립트", T, "원시 파일의 문제를 찾고 clean.py · 검증 보고서를 만든다",
            ["W05 · W11 · W19 문제 검사 요청", "처리 방법 정하기 (중복 · 단위 · 결측)", "clean.py 작성 요청", "검증 규칙 추가 요청",
             "세 파일 실행 · 보고서 확인"],
            [f"W05 {len(R05)} → {len(C05)}행", f"W11 수율 {Y11:.2f}% (0% 아님)", f"W19 RETEST {N_NA}개 · 검증 규칙 {len(RULES)}개 통과"],
            files="data/raw/wafer_test_W05 · W11 · W19.csv"),
        brief("2-2", T,
              ["문제 검사 요청 (고치지 말고 보고)", "처리 방법 정하기", "clean.py 요청", "검증 규칙 · 보고서 요청", "세 파일 실행"],
              [("목표", "원시 CSV 한 장 → 정제본 + 검증 보고서"), ("입력", "data/raw/ · spec.csv"),
               ("산출물", "scripts/clean.py · output/qc_W05 · W11 · W19.md"), ("하지 말 것", "data/raw/ 수정 · 결측을 평균으로 채우기")],
              [], [f"W11 수율 {Y11:.2f}%", f"W19 RETEST {N_NA}개"], ""),
        light("실습 2-2 확인", viz2.maprows([
            ("W05", f"{len(R05)}행 → {len(C05)}행", f"중복 {N_DUP}줄 삭제"), ("W11", "vth_v ÷ 1000", f"수율 {Y11:.2f}%"),
            ("W19", f"RETEST {N_NA}개", f"수율 {Y19:.2f}%"), ("검증", f"규칙 {len(RULES)}개", "세 파일 모두 통과")], "파일", "결과"), T),
    ]
