"""수율 도구 — data/ 엑셀 한 개의 행 수 · 합격(상품) · 불합격(불량) · 수율(상품률)을 계산해 돌려준다 (MCP · stdio).

실습 「수율 도구 만들기」 완성본. Python 3.10 이상 · pip install mcp pandas openpyxl (mcp 2.x · FastMCP → MCPServer).
연결: 프로젝트 맨 위 .mcp.json → Claude Code 를 다시 열고 /mcp 에서 yield-tools 확인.
"""
from pathlib import Path

import pandas as pd
from mcp.server.mcpserver import MCPServer

server = MCPServer("yield-tools")
DATA = Path(__file__).resolve().parent.parent / "data"   # 스크립트 위치 기준 · 작업 폴더와 상관없음


@server.tool()
def yield_of(file: str) -> dict:
    """data/ 엑셀 한 개의 행 수 · 합격 · 불합격 · 수율(%) — 웨이퍼 pass_fail=PASS · 사과 등급=상품"""
    df = pd.read_excel(DATA / Path(file).name)
    n = len(df)
    ok = int((df["pass_fail"] == "PASS").sum()) if "pass_fail" in df else int((df["등급"] == "상품").sum())
    return {"파일": Path(file).name, "행": n, "합격": ok, "불합격": n - ok, "수율": round(ok / n * 100, 2)}


if __name__ == "__main__":
    server.run()
