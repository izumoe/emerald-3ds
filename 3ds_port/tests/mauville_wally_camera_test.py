"""Verify camera direction does not change Wally's original event commands."""
from pathlib import Path
import subprocess
import tempfile
root=Path(__file__).resolve().parents[2]
rel=Path('data/maps/MauvilleCity/scripts.inc')
new=(root/'build/upstream'/rel).read_text()
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/rel;p.parent.mkdir(parents=True);p.write_text(new)
    subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0095-mauville-wally-camera.patch')],cwd=tmp,check=True)
    old=p.read_text()
def cpp(s,port=False):
    return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
def story(s):
    return [x.strip() for x in s.splitlines() if x.strip() and not x.strip().startswith(('camera_','waitcamera','@'))]
assert cpp(old)==cpp(new)
assert story(cpp(old,True))==story(cpp(new,True))
assert '\tcall_if_eq VAR_RESULT, YES, MauvilleCity_EventScript_BattleWally\n\tgoto_if_eq VAR_RESULT, NO, MauvilleCity_EventScript_DeclineWallyBattle' in new
for direction in ['North','East']:
    s=new.split(f'MauvilleCity_EventScript_WallyAndUncleExit{direction}::',1)[1].split('\n\tend',1)[0]
    assert 'camera_pair LOCALID_PLAYER, LOCALID_PLAYER' in s and 'waitcamera' in s
print('PASS Mauville Wally: original script, choice handoff, both held departures')
