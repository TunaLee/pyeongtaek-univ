"""GitHub · Vercel 배포 장 보강 — vibe-coding 1부 1-5(Git · GitHub 기초) · 1-7(배포) 장을 이 과정 예시(보고서 템플릿 wafer-report)로 옮긴 것.

배포(전 · 후) → 비유(문서 파일 → 공유 링크) → 주소별 접속 범위(파일 주소 · 배포 주소 · 이 과정은 서버 없이 HTML 파일을 바로 연다)
→ 커밋 구성 · 기록 쌓기 · Git 작업 흐름 · 요청 · 커밋 시점 · 되돌리기 · 체크포인트와 Git → GitHub · 공개 · 비공개 · gh · 올리기 요청 · 저장소 확인
→ Vercel 가져오기 · 배포 주소. 커밋 해시는 실제 git 으로 만든 값. 접두어 pg (vibe-coding 의 v1sh · v1g · v1cm 을 이름만 바꿈).
"""
import viz2
from anim import SPEED
from deck import flow, light
from hx import code, esc
from stats_hx import src
from v1kit import chat

T = "배포"
REPO = "wafer-report"
LOG = [("8ceced8", "숫자 카드 4개", "index.html 생성"), ("17ea423", "웨이퍼 맵 추가", "칩 616칸"), ("bfb3038", "불합격 차트 추가", "사유별 막대")]

GH_PLANS = ("GitHub plans", "https://docs.github.com/en/get-started/learning-about-github/githubs-plans")
GH_CLI = ("GitHub CLI", "https://cli.github.com/")
GH_REPO = ("gh repo create", "https://cli.github.com/manual/gh_repo_create")
PRO_GIT = ("Pro Git · What is Git?", "https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F")
GH_GIT = ("GitHub Docs · About Git", "https://docs.github.com/en/get-started/using-git/about-git")
CC_CP = ("Claude Code · Checkpointing", "https://code.claude.com/docs/en/checkpointing")
VC_URL = ("Vercel · Generated URLs", "https://vercel.com/docs/deployments/generated-urls")
VC_GIT = ("Vercel · Git", "https://vercel.com/docs/git")


def share():
    """비유 — 내 컴퓨터의 문서 파일(나만 열림) → 공유 링크(링크를 받은 누구나) → 문서를 고치면 링크로 보는 사람에게 바로 반영."""
    ppl = "".join(f'<span class="pgshp" style="--d:{2.6 + i * .5:.1f}s">{n}</span>' for i, n in enumerate(("팀장", "팀원", "휴대폰")))
    return ('<div class="pgsh">'
            '<div class="pgshc" style="--d:.3s"><div class="pgshh">내 컴퓨터의 문서 파일</div>'
            '<div class="pgshf"><b>회의록.docx</b><small>내 컴퓨터 · 바탕화면</small></div>'
            '<div class="pgshw">열 수 있는 사람 · 나</div><div class="pgshm">= 파일 주소 · file://</div></div>'
            '<i class="pgsha" style="--d:1.4s">→</i>'
            '<div class="pgshc on" style="--d:1.8s"><div class="pgshh">공유 링크</div>'
            '<div class="pgshl">https://… /회의록</div>'
            f'<div class="pgshps">{ppl}</div><div class="pgshm">= 배포 주소 · *.vercel.app</div></div></div>'
            '<div class="pgshu" style="--d:4.4s"><b>문서를 고치면</b><span>링크로 보는 사람에게 바로 반영</span><em>= 재배포 · push 하면 자동</em></div>')


def stack():
    """커밋이 아래에서 위로 하나씩 쌓임(v1 → v3) + 같은 기록의 터미널 출력. 해시는 실제 git 으로 만든 값."""
    cards = "".join(
        f'<div class="pgcm" style="--d:{.4 + i * .9:.1f}s"><span class="v">v{i + 1}</span><code>{h}</code><b>{m}</b><small>{d}</small></div>'
        for i, (h, m, d) in enumerate(LOG))
    term = code("터미널 · git log --oneline", esc("\n".join(f"{h} {m}" for h, m, _ in reversed(LOG))))
    return f'<div class="pgcmw"><div class="pgcms"><div class="pgcmh">기록 저장소</div>{cards}</div><div>{term}</div></div>'


def gitflow():
    """작업 폴더 → (add) 스테이징 → (commit) 로컬 저장소 → (push) GitHub · (pull) 되돌아옴. 구조는 Pro Git 「세 가지 상태」 + 원격."""
    K = 2.2

    def chip(t, d, o=None, cls=""):
        st = f"--d:{d * K:.2f}s" + (f"; --o:{o * K * SPEED:.2f}s" if o else "")   # --d 는 build 가 SPEED 를 곱함 · 나머지는 여기서
        return f'<div class="pggc {cls}{" o" if o else ""}" style="{st}">{t}</div>'

    def cm(h, m, d, cls=""):
        return f'<div class="pggk {cls}" style="--d:{d * K:.2f}s">{f"<tt>{h}</tt>" if h else ""}<b>{m}</b></div>'

    def pill(cmd, d1, d2=None):
        an = f"--d1:{d1 * K * SPEED:.2f}s; --d2:{(d2 if d2 else d1) * K * SPEED:.2f}s"
        return f'<div class="pggp" style="{an}"><tt>{cmd}</tt><i>→</i></div>'

    (h1, m1, _), (h2, m2, _), (h3, m3, _) = LOG
    wd = chip("index.html · 맵 추가", 1.0, 2.0) + chip("index.html · 차트 추가", 6.0, 6.8) + chip("index.html · 문구 바뀜", 11.6, cls="pl")
    stg = chip("index.html", 2.2, 3.4) + chip("index.html", 7.0, 7.8)
    loc = cm(h1, m1, .2) + cm(h2, m2, 3.6) + cm(h3, m3, 8.0) + cm("", "문구 수정 · 받아 옴", 11.2, "pl")
    rem = cm(h1, m1, .2) + cm(h2, m2, 5.0) + cm(h3, m3, 9.0) + cm("", "문구 수정 · 다른 컴퓨터", 10.0, "pl")

    def col(name, en, body, cls=""):
        return f'<div class="pggz {cls}"><div class="pggzh"><b>{name}</b><small>{en}</small></div><div class="pggzb">{body}</div></div>'
    return ('<div class="pgg"><div class="pggtop"><span class="me">내 컴퓨터</span><span class="net">인터넷</span></div>'
            '<div class="pggrow">'
            + col("작업 폴더", "working directory · 파일 수정", wd) + pill("git add", 1.8, 6.6)
            + col("스테이징 영역", "staging area · 커밋할 파일", stg) + pill("git commit", 3.2, 7.6)
            + col("로컬 저장소", "repository · 커밋 기록", loc) + pill("git push", 4.6, 8.6)
            + col("GitHub", "remote · 원격 저장소", rem, "rm")
            + f'</div><div class="pggpull" style="--d1:{10.8 * K * SPEED:.2f}s; --d2:{10.8 * K * SPEED:.2f}s"><i>←</i><tt>git pull</tt><span>원격의 새 커밋을 받아 내 폴더에 합침</span></div></div>')


def slides():
    return [
        # ── 도입 · 배포란 · 비유 · 주소
        light("배포", viz2.pair(
            "배포 전", [("주소", "file:///…/index.html · 내 컴퓨터 안"), ("열 수 있는 사람", "나 혼자"), ("컴퓨터를 끄면", "못 엶")],
            "배포 후", [("주소", f"{REPO}.vercel.app 형식"), ("열 수 있는 사람", "주소를 받은 누구나"), ("컴퓨터를 끄면", "그대로 열림")]), T),
        light("문서 파일과 공유 링크", share(), T),
        light("주소별 접속 범위", viz2.maprows([
            ("file:///…/index.html", "이 컴퓨터만", "만들며 확인 · 파일을 두 번 클릭"),
            (f"{REPO}.vercel.app", "인터넷의 누구나", "공유 · PC · 휴대폰")], "주소", "열리는 범위"), T),
        # ── 설명 · Git
        light("커밋 구성", viz2.tiles([
            ("바뀐 내용", "어느 파일의 어느 줄"), ("메시지", f"「{LOG[1][1]}」"),
            ("시각 · 작성자", "언제 · 누가"), ("고유 번호", f"{LOG[1][0]} 같은 해시")], 4), T),
        light("커밋 기록 쌓기", stack(), T),
        light("Git 작업 흐름", gitflow() + src(PRO_GIT, GH_GIT), T),
        light("Git 작업 요청", viz2.maprows([
            ("「지금 상태 커밋해 줘」", "git add · git commit", "메시지도 Claude 가 씀"),
            ("「커밋 기록 보여 줘」", "git log", "시점 · 메시지 목록"),
            ("「방금 고친 거 취소해 줘」", "git restore", "커밋 전 수정 버림"),
            ("「마지막 커밋 되돌려 줘」", "git revert", "되돌리는 새 커밋")], "Claude Code 에 하는 말", "실행되는 명령"), T),
        light("커밋 시점", viz2.tiles([
            ("기능 하나가 됐을 때", "「웨이퍼 맵 동작」"), ("크게 바꾸기 전", "화면 배치를 갈아엎기 전"),
            ("확인이 끝났을 때", "브라우저로 보고 숫자 맞음")], 3)
              + flow([("요청", "기능 하나"), ("확인", "브라우저 · 숫자"), ("커밋", "세이브"), ("다음 요청", "")], hl=2), T),
        light("Git으로 되돌리기", flow([
            ("수정 요청", "화면 배치 변경"), ("확인", "전보다 나빠짐"), ("「마지막 커밋 상태로 되돌려 줘」", ""), ("다시 요청", "더 작게 나눠서")], hl=2)
              + chat([("me", "방금 바꾼 배치가 전보다 별로야. 마지막 커밋 상태로 되돌려 줘."),
                      ("ai", f"마지막 커밋(「{LOG[2][1]}」) 뒤에 고친 index.html 을 되돌렸다.")], "되돌리기 대화 예"), T),
        light("체크포인트와 Git", viz2.pair(
            "체크포인트 (/rewind · Esc 두 번)", [("남는 때", "요청마다 자동"), ("되감기", "코드 · 대화 · 둘 다"),
                                              ("못 잡는 것", "Bash 명령으로 바뀐 파일 · Claude Code 밖에서 고친 파일")],
            "Git 커밋", [("남는 때", "내가 「커밋해 줘」 한 시점"), ("보관", "지우기 전까지 · GitHub 에도"), ("배포", "커밋을 가져가 공개")], hl="r")
              + src(CC_CP), T),
        # ── 설명 · GitHub
        light("GitHub", viz2.pair(
            "Git", [("어디에", "내 컴퓨터"), ("하는 일", "저장 시점 기록 · 되돌리기"), ("없으면", "기록이 이 컴퓨터에만")],
            "GitHub", [("어디에", "인터넷 · 원격 저장소"), ("하는 일", "기록 보관 · 공유 · 다른 컴퓨터에서 받기"), ("배포", "Vercel 과 연결")])
              + src(GH_PLANS), T),
        light("공개 · 비공개 저장소", viz2.pair(
            "공개 (public)", [("누가 보나", "인터넷의 누구나 코드를 봄"), ("맞는 경우", "공개해도 되는 연습 코드")],
            "비공개 (private)", [("누가 보나", "나와 초대한 사람만"), ("맞는 경우", "회사 업무 · 이 실습")], hl="r")
              + viz2.tiles([("GitHub Free", "비공개 저장소도 개수 제한 없음 · 일부 기능만 유료")], 1)
              + src(GH_PLANS), T),
        light("GitHub CLI (gh)", viz2.tiles([
            ("gh", "GitHub 공식 명령 도구 · 저장소 만들기 · 올리기"), ("설치", "Claude Code 에 「GitHub CLI 설치해 줘」"),
            ("명령 암기", "필요 없음 · 실행은 Claude Code")], 3)
              + '<div class="twocol"><div>' + code("Claude Code 가 실행 · macOS 예", esc("brew install gh")) + "</div><div>"
              + code("Claude Code 가 실행 · Windows 예", esc("winget install --id GitHub.cli --source winget")) + "</div></div>"
              + src(GH_CLI), T),
        light("GitHub 업로드 요청", chat([
            ("me", f"이 폴더를 GitHub 비공개 저장소 {REPO} 로 올려 줘"),
            ("ai", f"gh repo create {REPO} --private --source=. --push 를 실행해도 될까요?"),
            ("me", "응"),
            ("ai", f"완료 · https://github.com/내계정/{REPO}")], "Claude Code 대화")
              + viz2.tiles([("Claude 가 쓰는 명령", "gh repo create · 원격 저장소 만들기 + 지금까지의 커밋 올리기")], 1)
              + src(GH_REPO), T),
        light("업로드한 저장소 확인", '<div class="twocol"><div>'
              + code(f"github.com/내계정/{REPO} · 예", esc(f"{REPO}/\n├── index.html\n├── CLAUDE.md\n├── .claude/\n└── .gitignore      data/ 는 올리지 않음"))
              + "</div><div>" + viz2.tiles([
                  ("파일 목록", "내 폴더와 같음 · data/ 제외"), ("커밋 기록", "기능마다 남긴 커밋"), ("자물쇠 표시", "비공개 저장소")], 1)
              + "</div></div>", T),
        # ── 설명 · Vercel
        light("Vercel 프로젝트 가져오기", flow([
            ("Vercel 로그인", "GitHub 계정"), ("새 프로젝트", "Git 저장소 가져오기"), (f"{REPO} 선택", "저장소 접근 허용"),
            ("Deploy", "설정은 기본값"), ("주소 발급", "1분 안팎")], hl=2)
              + viz2.tiles([("저장소가 안 보이면", "GitHub 쪽에서 Vercel 에 그 저장소 접근 허용"),
                            ("설정", "HTML 한 파일 · 빌드 설정을 바꿀 것 없음")], 2)
              + src(VC_GIT), T),
        light("배포 주소", viz2.tiles([
            ("프로젝트 기본 주소", "프로젝트명.vercel.app · 다시 배포해도 같음"), ("배포마다 고유 주소", "버전마다 따로 생김")], 2)
              + code("배포 완료 · 예", esc(f"✓ Production   https://{REPO}.vercel.app\n  이번 배포     https://{REPO}-a1b2c3.vercel.app"))
              + src(VC_URL), T),
    ]


CSS = r"""
  /* 배포 · 문서 파일과 공유 링크 (pgsh) */
  .pgsh{display:grid; grid-template-columns:1fr 50px 1fr; gap:12px; align-items:stretch; margin:4px 0 16px;}
  .pgshc{border:2px solid #C9D6E6; border-radius:16px; background:#fff; padding:18px 22px; display:flex; flex-direction:column; gap:12px;
    opacity:0; animation:pgIn .6s var(--d) forwards;}
  .pgshc.on{border-color:#F28C28; background:#FFF8F0;}
  .pgshh{font-size:22px; font-weight:800; color:#16233A;}
  .pgshf{display:flex; flex-direction:column; gap:2px; border-left:6px solid #2B579A; background:#F4F6F9; border-radius:8px; padding:10px 14px;}
  .pgshf b{font-size:19px; color:#16233A;} .pgshf small{font-size:14px; color:#6B7785;}
  .pgshl{font-family:var(--mono); font-size:16px; font-weight:700; color:#1F3A5F; background:#EAF0F7; border-radius:20px; padding:9px 16px;}
  .pgshw{font-size:17px; color:#3A4657; font-weight:600;}
  .pgshps{display:flex; gap:10px;}
  .pgshp{font-size:15px; font-weight:700; color:#fff; background:#1F3A5F; border-radius:16px; padding:6px 14px; opacity:0; animation:pgIn .5s var(--d) forwards;}
  .pgshm{margin-top:auto; font-size:17px; font-weight:800; color:#E07A12;}
  .pgsha{font-style:normal; align-self:center; text-align:center; font-size:34px; font-weight:800; color:#F28C28; opacity:0; animation:pgIn .5s var(--d) forwards;}
  .pgshu{display:flex; gap:16px; align-items:baseline; border:2px dashed #F28C28; border-radius:14px; padding:14px 22px; opacity:0; animation:pgIn .6s var(--d) forwards;}
  .pgshu b{font-size:20px; color:#16233A;} .pgshu span{font-size:18px; color:#3A4657;} .pgshu em{margin-left:auto; font-style:normal; font-size:17px; font-weight:800; color:#E07A12;}
  @keyframes pgIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  /* Git 작업 흐름 (pgg) */
  .pggtop{display:grid; grid-template-columns:3fr 1fr; gap:10px; margin-bottom:8px;}
  .pggtop span{font-size:14px; font-weight:800; text-align:center; padding:5px 0; border-radius:8px;}
  .pggtop .me{background:#EAF0F7; color:#16233A;} .pggtop .net{background:#16233A; color:#fff;}
  .pggrow{display:grid; grid-template-columns:1fr 86px 1fr 96px 1fr 86px 1fr; align-items:stretch;}
  .pggz{border:2px solid #C9D6E6; border-radius:14px; background:#F7F8FA; display:flex; flex-direction:column; min-height:300px;}
  .pggz.rm{border-color:#16233A;}
  .pggzh{padding:10px 10px 8px; border-bottom:1.5px solid #D9DDE3; text-align:center;}
  .pggzh b{display:block; font-size:19px; color:#16233A;} .pggzh small{font-size:12px; color:#6B7785;}
  .pggzb{flex:1; display:flex; flex-direction:column-reverse; justify-content:flex-end; gap:7px; padding:10px;}
  .pggc{background:#FFF1E2; border:2px solid #F28C28; border-radius:9px; padding:8px 9px; font-size:15px; font-weight:700; color:#16233A; text-align:center;
    opacity:0; animation:pggIn .6s var(--d) forwards;}
  .pggc.o{animation:pggIn .6s var(--d) forwards, pggOut .6s var(--o) forwards;}
  .pggk{background:#fff; border:2px solid #1F3A5F; border-radius:9px; padding:7px 9px; opacity:0; animation:pggIn .4s var(--d) forwards;}
  .pggk tt{display:block; font-family:var(--mono); font-size:12.5px; color:#6B7785; background:none; padding:0;}
  .pggk b{font-size:15px; color:#16233A;}
  .pggk.pl,.pggc.pl{border-color:#2E7D5B; background:#EAF6EF;}
  .pggp{display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px;}
  .pggp tt{font-family:var(--mono); font-size:13.5px; font-weight:700; color:#16233A; background:#EAF0F7; border-radius:14px; padding:5px 8px; white-space:nowrap;
    animation:pggHi 2.4s var(--d1), pggHi 2.4s var(--d2);}
  .pggp i{font-style:normal; font-size:26px; font-weight:800; color:#F28C28;}
  .pggpull{margin-top:12px; display:flex; align-items:center; gap:12px; justify-content:center; border:2px dashed #2E7D5B; border-radius:12px; padding:9px;
    opacity:0; animation:pggIn .4s var(--d1) forwards;}
  .pggpull i{font-style:normal; font-size:24px; font-weight:800; color:#2E7D5B;}
  .pggpull tt{font-family:var(--mono); font-size:15px; font-weight:700; color:#fff; background:#2E7D5B; border-radius:14px; padding:5px 12px;}
  .pggpull span{font-size:16px; color:#16233A; font-weight:600;}
  @keyframes pggIn{from{opacity:0; transform:translateY(-8px)} to{opacity:1; transform:none}}
  @keyframes pggOut{from{opacity:1} to{opacity:0; height:0; padding:0; margin:0; border-width:0}}
  @keyframes pggHi{0%,100%{background:#EAF0F7; color:#16233A} 15%,75%{background:#F28C28; color:#fff}}
  /* 커밋 기록 쌓기 (pgcm) */
  .pgcmw{display:grid; grid-template-columns:1.1fr 1fr; gap:26px; align-items:center;}
  .pgcms{display:flex; flex-direction:column-reverse; gap:10px; border:2px dashed #D9DDE3; border-radius:16px; padding:18px 18px 14px; background:#F7F8FA; min-height:280px; justify-content:flex-start;}
  .pgcmh{order:-1; font-size:14px; font-weight:800; color:#6B7785; text-align:center; margin-top:6px;}
  .pgcm{display:grid; grid-template-columns:44px 84px 1fr; align-items:baseline; gap:8px; padding:12px 16px; border-radius:12px; background:#fff; border:2px solid #1F3A5F;
        opacity:0; animation:pgcmIn .5s ease-out var(--d) forwards;}
  .pgcm:last-of-type{border-color:#F28C28; background:#FFF8F0;}
  .pgcm .v{font-weight:900; color:#F28C28; font-size:18px;} .pgcm code{font-family:var(--mono); font-size:15px; color:#6B7785; background:none;}
  .pgcm b{font-size:19px; color:#16233A;} .pgcm small{grid-column:3; font-size:14.5px; color:#6B7785;}
  @keyframes pgcmIn{from{opacity:0; transform:translateY(-24px)} to{opacity:1; transform:none}}
  @media print{.pgshc,.pgshp,.pgsha,.pgshu,.pggc,.pggk,.pggpull,.pgcm{opacity:1; animation:none} .pggc.o{display:none} .pggp tt{animation:none}}
"""
