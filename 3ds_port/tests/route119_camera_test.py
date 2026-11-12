"""Route 119 rival camera cues must preserve both approach branches and rewards."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[2]; rel=Path('data/maps/Route119/scripts.inc')
new=(root/'build/upstream'/rel).read_text()
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/rel;p.parent.mkdir(parents=True);p.write_text(new)
 subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0096-route119-rival-camera.patch')],cwd=tmp,check=True)
 old=p.read_text()
def cpp(s,port=False):
 return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
def story(s):
 return [x.strip() for x in s.splitlines() if x.strip() and not x.strip().startswith(('camera_','waitcamera','@'))]
assert cpp(old)==cpp(new)
assert story(cpp(old,True))==story(cpp(new,True))
s=new.split('Route119_EventScript_RivalExitScottArrive::',1)[1].split('\n\tend',1)[0]
assert s.index('camera_pair LOCALID_PLAYER, LOCALID_PLAYER') < s.index('Route119_EventScript_RivalExit1')
assert 'camera_reveal MAP_ROUTE119' in new
print('PASS Route 119: original scripts, both branches, held departures and queued battle return')
