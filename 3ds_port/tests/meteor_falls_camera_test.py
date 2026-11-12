"""Keep the Meteor Falls confrontation and its two departures intact."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[2];rel=Path('data/maps/MeteorFalls_1F_1R/scripts.inc');new=(root/'build/upstream'/rel).read_text()
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/rel;p.parent.mkdir(parents=True);p.write_text(new)
 subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0100-meteor-falls-camera.patch')],cwd=tmp,check=True);old=p.read_text()
def cpp(s,port=False):return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
def story(s):return [x.strip() for x in s.splitlines() if x.strip() and not x.strip().startswith(('camera_','waitcamera','@'))]
assert cpp(old)==cpp(new)
assert story(cpp(old,True))==story(cpp(new,True))
for movement in ['MeteorFalls_1F_1R_Movement_PushPlayerOutOfWay','MeteorFalls_1F_1R_Movement_ArchieExit']:
 before=new.split(movement,1)[0].rsplit('#ifdef PORT_BRIDGE',1)[1]
 assert 'camera_pair LOCALID_PLAYER, LOCALID_PLAYER' in before and 'waitcamera' in before
print('PASS Meteor Falls: original story and held Magma/Aqua departures')
