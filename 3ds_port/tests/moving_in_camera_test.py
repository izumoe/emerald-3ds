"""The moving-in camera must not disturb either house's shared event variables."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
files = [Path(f'data/maps/LittlerootTown_{name}House_1F/scripts.inc') for name in ('Brendans', 'Mays')]
files.append(Path('data/scripts/players_house.inc'))
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    for f in files:
        dest = tmp / f
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((root / 'build/upstream' / f).read_bytes())
    subprocess.run(['git', 'apply', '--reverse', str(root / 'patches/pokeemerald/0092-moving-in-camera.patch')], cwd=tmp, check=True)
    for f in files:
        old = (tmp / f).read_bytes()
        new = (root / 'build/upstream' / f).read_bytes()
        cpp = lambda x: subprocess.check_output(['cpp', '-P', '-x', 'c', '-'], input=x)
        assert cpp(old) == cpp(new), f
        oldport = subprocess.check_output(['cpp', '-P', '-DPORT_BRIDGE', '-x', 'c', '-'], input=old).decode()
        newport = subprocess.check_output(['cpp', '-P', '-DPORT_BRIDGE', '-x', 'c', '-'], input=new).decode()
        def story(s):
            return [line.strip() for line in s.splitlines() if line.strip() and not line.strip().startswith(('camera_', 'waitcamera', '@'))]
        assert story(oldport) == story(newport), f
    for f in files[:2]:
        s = (root / 'build/upstream' / f).read_text()
        section = s.split('_EventScript_EnterHouseMovingIn::', 1)[1].split('\n\tend', 1)[0]
        assert section.index('waitcamera') < section.index('setvar VAR_0x8004') < section.index('setvar VAR_0x8005')
print('PASS moving-in: both vanilla variants, story order and shared scratch variables')
