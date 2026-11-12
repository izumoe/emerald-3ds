"""Keep the Mt. Chimney and Weather Institute events and rewards intact."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[2]
cases=[('data/maps/MtChimney/scripts.inc','0101-mt-chimney-camera.patch'),('data/maps/Route119_WeatherInstitute_2F/scripts.inc','0102-weather-institute-camera.patch')]
def cpp(s,port=False):return subprocess.check_output(['cpp','-P','-x','c']+(['-DPORT_BRIDGE'] if port else [])+['-'],input=s.encode()).decode()
for rel,patch in cases:
 new=(root/'build/upstream'/rel).read_text()
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp)/rel;p.parent.mkdir(parents=True);p.write_text(new)
  if 'MtChimney' in rel:
   subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0114-mt-chimney-cuts.patch')],cwd=tmp,check=True)
  subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald'/patch)],cwd=tmp,check=True);old=p.read_text()
 assert cpp(old)==cpp(new),rel
 def story(s):
  ignore=('camera_','waitcamera','@','goto_if_defeated TRAINER_SHELLY_WEATHER_INSTITUTE, WeatherInstitute_CameraOriginalShelly','WeatherInstitute_CameraOriginalShelly:')
  return [x.strip() for x in s.splitlines() if x.strip() and not x.strip().startswith(ignore)]
 a=story(cpp(old,True));b=story(cpp(new,True))
 if 'WeatherInstitute' in rel:
  # The camera prelude intentionally locks and faces the trainer before the stock battle command.
  k=b.index('Route119_WeatherInstitute_2F_EventScript_Shelly::');assert b[k+1:k+3]==['lock','faceplayer'];del b[k+1:k+3]
 assert a==b,rel
 if 'WeatherInstitute' in rel:
  assert '\tgivemon SPECIES_CASTFORM, 25, ITEM_MYSTIC_WATER\n\tgoto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY' in new
print('PASS Mt. Chimney and Weather Institute: original story actions, battle and reward branches')
