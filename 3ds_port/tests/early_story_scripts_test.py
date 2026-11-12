"""Check new camera cues preserve original event behavior and dialogue."""
from pathlib import Path
import re, subprocess, tempfile, sys, json
root=Path(__file__).resolve().parents[2]
upstream=Path(sys.argv[1]) if len(sys.argv)>1 else root/'build/upstream'
files=['data/maps/Route101/scripts.inc','data/maps/Route103/scripts.inc']
with tempfile.TemporaryDirectory() as tmp:
    before=Path(tmp)
    for name in files:
        p=before/name;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes((upstream/name).read_bytes())
    subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0086-early-story-cameras.patch')],cwd=before,check=True)
    for name in files:
        old=(before/name).read_text();new=(upstream/name).read_text()
        map_info=json.loads((upstream/Path(name).parent/'map.json').read_text())
        layouts=json.loads((upstream/'data/layouts/layouts.json').read_text())['layouts']
        layout=next(x for x in layouts if x['id']==map_info['layout'])
        for x,z in re.findall(r'camera_anchor (\d+), (\d+)',new):
            assert 0<=int(x)<layout['width'] and 0<=int(z)<layout['height'],(name,x,z)
        def gba(s):return subprocess.check_output(['cpp','-P','-x','c','-'],input=s.encode())
        assert gba(old)==gba(new),name
        # Story actions retain their original order on the port too.
        pattern=r'(?m)^\s*(?:applymovement|waitmovement|trainerbattle_no_intro|setflag|clearflag|removeobject|setvar VAR_(?!0x800)[^\n]+|warp)\b[^\n]*'
        def actions(s):return [x.strip() for x in re.findall(pattern,s)]
        assert actions(old)==actions(new),name
        if 'Route103' in name:
            assert re.findall(r'\.string "(.*)"',old)==re.findall(r'\.string "(.*)"',new)
        else:
            def text(label):
                body=new.split(label+':',1)[1]
                body=re.split(r'(?m)^[A-Za-z_]\w*:',body)[0]
                return ''.join(re.findall(r'\.string "(.*)"',body)).removesuffix('$')
            assert text('Route101_Text_PleaseHelp').split(r'\p')==[text('Route101_Text_CameraPleaseHelp'),text('Route101_Text_CameraBag')]
print('PASS early story: GBA scripts, story action order, rival dialogue and exact Birch page split')
