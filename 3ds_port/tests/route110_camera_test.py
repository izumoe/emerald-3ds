"""Route 110 must preserve its approach selector across camera commands and battle."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[2];rel=Path('data/maps/Route110/scripts.inc')
new=(root/'build/upstream'/rel).read_text()
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/rel;p.parent.mkdir(parents=True);p.write_text(new)
 subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0097-route110-rival-camera.patch')],cwd=tmp,check=True)
 old=p.read_text()
def cpp(s,port=False):return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
def story(s):return [x.strip() for x in s.splitlines() if x.strip() and not x.strip().startswith(('camera_','waitcamera','copyvar VAR_TEMP_6, VAR_0x8008','copyvar VAR_0x8008, VAR_TEMP_6','@'))]
assert cpp(old)==cpp(new)
assert story(cpp(old,True))==story(cpp(new,True))
start=new.split('Route110_EventScript_RivalScene::',1)[1].split('\n\tend',1)[0]
assert start.index('copyvar VAR_TEMP_6, VAR_0x8008') < start.index('camera_pair') < start.index('copyvar VAR_0x8008, VAR_TEMP_6') < start.index('checkplayergender',start.index('camera_pair'))
end=new.split('Route110_EventScript_RivalExit::',1)[1].split('\n\tend',1)[0]
assert end.index('waitcamera') < end.index('copyvar VAR_0x8008, VAR_TEMP_6') < end.index('Route110_EventScript_MoveRival1')
print('PASS Route 110: original scripts, three approach selectors and held exit')
