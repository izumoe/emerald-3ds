"""Ensure museum cinematics preserve both battles and the item handover."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[2];rel=Path('data/maps/SlateportCity_OceanicMuseum_2F/scripts.inc')
new=(root/'build/upstream'/rel).read_text()
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/rel;p.parent.mkdir(parents=True);p.write_text(new)
 subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0098-oceanic-museum-camera.patch')],cwd=tmp,check=True)
 old=p.read_text()
def cpp(s,port=False):return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
def story(s):return [x.strip() for x in s.splitlines() if x.strip() and not x.strip().startswith(('camera_','waitcamera','@'))]
assert cpp(old)==cpp(new)
assert story(cpp(old,True))==story(cpp(new,True))
assert '\tsetvar VAR_0x8004, ITEM_DEVON_GOODS\n\tcall Common_EventScript_PlayerHandedOverTheItem' in new
assert new.count('camera_reveal MAP_SLATEPORT_CITY_OCEANIC_MUSEUM_2F')==2
print('PASS museum: original story, both battles, Devon Goods scratch handover')
