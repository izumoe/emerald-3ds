"""Check first-challenge camera cues retain the original Gym battle scripts."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
names = [('DewfordTown_Gym','Brawly','BRAWLY'), ('MauvilleCity_Gym','Wattson','WATTSON'),
         ('LavaridgeTown_Gym_1F','Flannery','FLANNERY'), ('FortreeCity_Gym','Winona','WINONA')]
files = [Path('data/maps') / m / 'scripts.inc' for m, _, _ in names]
def preprocess(source, port=False):
    return subprocess.check_output(['cpp','-P','-x','c'] + (['-DPORT_BRIDGE'] if port else []) + ['-'], input=source.encode()).decode()
with tempfile.TemporaryDirectory() as tmp:
    before = Path(tmp)
    for f in files:
        (before / f).parent.mkdir(parents=True, exist_ok=True)
        (before / f).write_bytes((root/'build/upstream'/f).read_bytes())
    subprocess.run(['git','apply','--reverse',str(root/'patches/pokeemerald/0093-midgame-gym-cameras.patch')], cwd=before, check=True)
    for f, (m,n,t) in zip(files,names):
        old=(before/f).read_text();new=(root/'build/upstream'/f).read_text()
        assert preprocess(old)==preprocess(new),m
        oldlines=[x.strip() for x in preprocess(old,True).splitlines() if x.strip().startswith(('trainerbattle_', 'specialvar ', 'goto_if_', 'setflag ', 'clearflag ', 'setvar ', 'call ', 'msgbox ', 'message ', 'release', 'end'))]
        newlines=[x.strip() for x in preprocess(new,True).splitlines() if x.strip().startswith(('trainerbattle_', 'specialvar ', 'goto_if_', 'setflag ', 'clearflag ', 'setvar ', 'call ', 'msgbox ', 'message ', 'release', 'end')) and not x.strip().startswith(f'goto_if_defeated TRAINER_{t}_1, {m}_CameraOriginal')]
        assert oldlines==newlines,m
        section=new.split(f'{m}_EventScript_{n}::',1)[1].split(f'{m}_CameraOriginal{n}:',1)[0]
        assert 'camera_height 8' in section and 'camera_reveal ' in section and 'waitcamera' in section
print('PASS midgame Gyms: original GBA scripts, battle and reward actions, first-battle guards')
