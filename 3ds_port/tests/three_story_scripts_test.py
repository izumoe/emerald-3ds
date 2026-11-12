"""Verify the new story scenes retain original text, actions and GBA scripts."""
from pathlib import Path
import tempfile,subprocess,re,sys
root=Path(__file__).resolve().parents[2]
u=Path(sys.argv[1]) if len(sys.argv)>1 else root/'build/upstream'
files=['data/specials.inc','asm/macros/event.inc','data/maps/PetalburgWoods/scripts.inc','data/maps/RustboroCity_Gym/scripts.inc','data/maps/PetalburgCity_Gym/scripts.inc','data/maps/PetalburgCity/scripts.inc']
def cpp(s,port=False):
 return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
def text(s,label):
 body=s.split(label+':',1)[1];body=re.split(r'(?m)^[A-Za-z_]\w*:',body)[0]
 return ''.join(re.findall(r'\.string "(.*)"',body)).removesuffix('$')
with tempfile.TemporaryDirectory() as tmp:
 b=Path(tmp)
 for n in files:
  p=b/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((u/n).read_bytes())
 subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0088-woods-roxanne-wally-cameras.patch')],cwd=b,check=True)
 for n in files:
  old=(b/n).read_text();new=(u/n).read_text()
  assert cpp(old)==cpp(new),n
  if '/maps/' not in n:continue
  for label in re.findall(r'(?m)^([A-Za-z_]\w*):\n\s*\.string',old):
   assert text(old,label)==text(new,label),(n,label)
  pattern=r'(?m)^\s*(?:setflag|clearflag|giveitem|addvar|warp|trainerbattle_\w+|setvar VAR_(?!0x800)[^\n]+|special (?:SavePlayerParty|LoadPlayerParty|LoadWallyZigzagoon|StartWallyTutorialBattle|InitBirchState))\b[^\n]*'
  def actions(s):return [x.strip().replace('RustboroCity_Gym_Text_CameraChallenge,','RustboroCity_Gym_Text_RoxanneIntro,') for x in re.findall(pattern,cpp(s,True))]
  assert actions(old)==actions(new),n
 s=(u/files[3]).read_text()
 assert text(s,'RustboroCity_Gym_Text_RoxanneIntro').split(r'\p')==[text(s,'RustboroCity_Gym_Text_CameraIntroduction'),text(s,'RustboroCity_Gym_Text_CameraSchool'),text(s,'RustboroCity_Gym_Text_CameraChallenge')]
 s=(u/files[4]).read_text()
 helpers=re.findall(r'(?ms)^PetalburgCity_Gym_Camera\w+:\n(.*?)(?=\n\n)',s)
 assert len(helpers)==6
 for body in helpers:
  lines=body.strip().splitlines()
  assert lines[0].strip()=='copyvar VAR_TEMP_E, VAR_0x8008'
  assert lines[-2].strip()=='copyvar VAR_0x8008, VAR_TEMP_E'
print('PASS three scenes: GBA preservation, original text/action order, Roxanne pages and Wally direction scratch')

# The pre-ambush grunt is hidden in both approaches and shown before his walk.
s=(u/'data/maps/PetalburgWoods/scripts.inc').read_text()
for approach in ['Left','Right']:
 body=s.split('PetalburgWoods_EventScript_DevonResearcher'+approach+'::',1)[1].split('\n\tend',1)[0]
 assert body.index('hideobjectat LOCALID_PETALBURG_WOODS_GRUNT') < body.index('call PetalburgWoods_EventScript_DevonResearcherIntro')
 assert body.index('showobjectat LOCALID_PETALBURG_WOODS_GRUNT') < body.index('applymovement LOCALID_PETALBURG_WOODS_GRUNT, PetalburgWoods_Movement_AquaEntrance')
body=s.split('PetalburgWoods_EventScript_DevonResearcherIntro::',1)[1]
exit=body.split('PetalburgWoods_Movement_AquaRunAway',1)[0].rsplit('#ifdef PORT_BRIDGE',1)[1]
assert 'camera_pair LOCALID_PLAYER, LOCALID_PLAYER' in exit
assert 'camera_follow TRUE' not in exit and 'waitcamera' in exit
print('PASS Woods: hide/reveal ordering and held survivor shot before grunt exit')

for approach in ['Left','Right']:
 body=s.split('PetalburgWoods_EventScript_DevonResearcher'+approach+'::',1)[1].split('\n\tend',1)[0]
 departure=body.split('applymovement LOCALID_PLAYER, PetalburgWoods_Movement_WatchResearcherLeave',1)[0].rsplit('#ifdef PORT_BRIDGE',1)[1]
 assert 'camera_pair LOCALID_PLAYER, LOCALID_PLAYER' in departure
 assert 'camera_offset 0, 16' in departure and 'waitcamera' in departure
print('PASS Woods: both researcher exits start with a held close player shot')
