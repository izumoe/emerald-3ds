"""Preserve the Kecleon reveal, battle result and optional Steven dialogue."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[2];rel=Path('data/maps/Route120/scripts.inc')
new=(root/'build/upstream'/rel).read_text()
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/rel;p.parent.mkdir(parents=True);p.write_text(new)
 subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0099-route120-steven-camera.patch')],cwd=tmp,check=True)
 old=p.read_text()
def cpp(s,port=False):return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
def story(s):return [x.strip() for x in s.splitlines() if x.strip() and not x.strip().startswith(('camera_','waitcamera','@'))]
assert cpp(old)==cpp(new)
assert story(cpp(old,True))==story(cpp(new,True))
assert '\tsetwildbattle SPECIES_KECLEON, 30\n\tsetvar VAR_0x8009, 0\n\tsetflag FLAG_SYS_CTRL_OBJ_DELETE\n\tdowildbattle' in new
assert '\tspecialvar VAR_RESULT, GetBattleOutcome\n\tgoto_if_eq VAR_RESULT, B_OUTCOME_WON' in new
assert 'camera_reveal MAP_ROUTE120' in new
print('PASS Route 120: story, Kecleon battle setup, outcomes and camera return')
