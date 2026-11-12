"""Check the additional story scripts retain their original actions and choices."""
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
cases = [
    ('data/maps/PetalburgCity_Gym/scripts.inc', '0103-norman-surf-camera.patch'),
    ('data/maps/PetalburgCity_WallysHouse/scripts.inc', '0103-norman-surf-camera.patch'),
    ('data/maps/LavaridgeTown/scripts.inc', '0104-lavaridge-rival-camera.patch'),
    ('data/maps/Route104_MrBrineysHouse/scripts.inc', '0105-briney-voyage-camera.patch'),
    ('data/maps/Route104/scripts.inc', '0113-briney-voyage-camera.patch'),
]

def cpp(text, port=False):
    args = ['cpp', '-P', '-x', 'c'] + (['-DPORT_BRIDGE'] if port else []) + ['-']
    return subprocess.check_output(args, input=text.encode()).decode()

def story(text):
    ignored = ('camera_', 'waitcamera', '@', 'copyvar VAR_TEMP_6, VAR_0x8008',
               'copyvar VAR_0x8008, VAR_TEMP_6', 'copyvar VAR_TEMP_6, VAR_RESULT',
               'copyvar VAR_RESULT, VAR_TEMP_6')
    return [line.strip() for line in text.splitlines()
            if line.strip() and not line.strip().startswith(ignored)]

for rel, patch_name in cases:
    patch = root / 'patches/pokeemerald' / patch_name
    new = (root / 'build/upstream' / rel).read_text()
    with tempfile.TemporaryDirectory() as directory:
        for line in patch.read_text().splitlines():
            if line.startswith('+++ b/'):
                name = line[6:]
                dest = Path(directory) / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(root / 'build/upstream' / name, dest)
        subprocess.run(['git', 'apply', '--reverse', str(patch)], cwd=directory, check=True)
        old = (Path(directory) / rel).read_text()
    assert cpp(old) == cpp(new), rel
    assert story(cpp(old, True)) == story(cpp(new, True)), rel
    if 'LavaridgeTown' in rel:
        assert new.index('copyvar VAR_TEMP_6, VAR_0x8008') < new.index('camera_pair LOCALID_PLAYER, LOCALID_LAVARIDGE_RIVAL')
        assert new.count('copyvar VAR_0x8008, VAR_TEMP_6') == 2
    if rel == 'data/maps/Route104/scripts.inc':
        for label in ('Route104_EventScript_DeliverLetterReminder::',
                      'Route104_EventScript_LandedInDewford::'):
            block = new.split(label, 1)[1].split('\n\tend', 1)[0]
            assert block.index('camera_return 60') < block.index('releaseall')
    if 'BrineysHouse' in rel:
        assert (new.index('MSGBOX_YESNO') < new.index('copyvar VAR_TEMP_6, VAR_RESULT')
                < new.index('camera_return 60') < new.index('copyvar VAR_RESULT, VAR_TEMP_6')
                < new.index('goto_if_eq VAR_RESULT, NO'))
print('PASS Norman, Surf, Go-Goggles and Briney: story actions and choice handoffs')
