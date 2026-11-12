"""Verify the next three camera scripts preserve all original event commands."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[2]
u=root/'build/upstream'
files=['data/maps/RusturfTunnel/scripts.inc','data/maps/RustboroCity_DevonCorp_3F/scripts.inc','data/maps/GraniteCave_StevensRoom/scripts.inc']
def cpp(s,port=False):
 return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
def commands(s):
 return [l.strip() for l in s.splitlines() if l.strip() and not l.strip().startswith(('camera_','waitcamera'))]
with tempfile.TemporaryDirectory() as t:
 p=Path(t)
 for f in files:
  q=p/f;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((u/f).read_bytes())
 subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0090-rusturf-stone-steven-cameras.patch')],cwd=p,check=True)
 for f in files:
  old=(p/f).read_text();new=(u/f).read_text()
  assert cpp(old)==cpp(new),('GBA',f)
  assert commands(cpp(old,True))==commands(cpp(new,True)),('story commands',f)
 s=(u/files[2]).read_text()
 assert '\tsetvar VAR_0x8004, ITEM_LETTER\n\tcall Common_EventScript_PlayerHandedOverTheItem' in s
 # Exits settle before original movement; removal still follows waitmovement.
 for f,move in [(files[0],'RusturfTunnel_Movement_PushPlayerAsideForGrunt'),(files[0],'RusturfTunnel_Movement_PlayerWatchBrineyExit'),(files[2],'GraniteCave_StevensRoom_EventScript_StevenExitNorth')]:
  s=(u/f).read_text();before=s.split(move,1)[0].rsplit('#ifdef PORT_BRIDGE',1)[1]
  assert 'camera_pair LOCALID_PLAYER, LOCALID_PLAYER' in before and 'waitcamera' in before
 s=(u/files[1]).read_text()
 assert 'camera_pair LOCALID_PLAYER, 1' in s # visible president; local ID3 is invisible desk proxy
 assert 'camera_pair LOCALID_PLAYER, 3' not in s
print('PASS next three: exact GBA text/scripts and port story command order, handover scratch, held exits and real president actor')
