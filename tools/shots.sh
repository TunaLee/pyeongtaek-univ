#!/bin/bash
# 덱 장을 마지막 장면(t=25s)으로 캡처 → 6장씩 시트. 사용: tools/shots.sh <html 절대경로> <출력 폴더> [시작 장] [끝 장]
SRC=$1; O=$2; mkdir -p $O; rm -f $O/s*.png $O/sheet*.png
N=$(grep -c '<section class="slide' $SRC)
for n in $(seq ${3:-1} ${4:-$N}); do
  python3 - "$SRC" "$O/p.html" "$n" <<'PY'
import sys, os
s = open(sys.argv[1]).read(); n = sys.argv[3]
css = (f'<base href="file://{os.path.dirname(sys.argv[1])}/"><style>.slide{{display:none!important}} '
       f'section.slide:nth-of-type({n}){{display:flex!important}} .stage{{padding:0!important;display:block!important}} '
       f'.scaler{{transform:none!important}} body{{background:#fff!important}} '
       f'.progress,.nav,.controls,#jumpHint,.toolbar{{display:none!important}}</style></head>')
js = ('<script>addEventListener("load",()=>setTimeout(()=>{for(const a of document.getAnimations()){a.pause();a.currentTime=25000;}},50));</script></body>')
open(sys.argv[2], 'w').write(s.replace('</head>', css, 1).replace('</body>', js, 1))
PY
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars \
    --window-size=1280,720 --virtual-time-budget=4000 --screenshot=$O/s$n.png file://$O/p.html 2>/dev/null
done
python3 - "$O" <<'PY'
import sys, glob
from PIL import Image, ImageDraw
O = sys.argv[1]
fs = sorted(glob.glob(f'{O}/s*.png'), key=lambda f: int(f.split('/s')[-1][:-4]))
for k in range(0, len(fs), 6):
    ims = [Image.open(f).convert('RGB').resize((640, 360)) for f in fs[k:k + 6]]
    S = Image.new('RGB', (1280, 360 * ((len(ims) + 1) // 2)), 'white')
    d = ImageDraw.Draw(S)
    for i, im in enumerate(ims):
        S.paste(im, ((i % 2) * 640, (i // 2) * 360)); d.rectangle(((i % 2) * 640, (i // 2) * 360, (i % 2) * 640 + 40, (i // 2) * 360 + 22), fill='black'); d.text(((i % 2) * 640 + 6, (i // 2) * 360 + 4), str(k + i + 1), fill='yellow')
    S.save(f'{O}/sheet{k // 6}.png')
print(len(fs), 'slides')
PY
