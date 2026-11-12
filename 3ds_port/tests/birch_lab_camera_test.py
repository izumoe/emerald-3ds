"""Verify the lab camera cues preserve the original story scripts."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
rel = Path('data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc')
new = (root / 'build/upstream' / rel).read_text()
with tempfile.TemporaryDirectory() as tmp:
    target = Path(tmp) / rel
    target.parent.mkdir(parents=True)
    target.write_text(new)
    subprocess.run(['git', 'apply', '--reverse', str(root / 'patches/pokeemerald/0091-birch-lab-camera.patch')], cwd=tmp, check=True)
    old = target.read_text()

def preprocess(source, port=False):
    args = ['cpp', '-P', '-x', 'c'] + (['-DPORT_BRIDGE'] if port else []) + ['-']
    return subprocess.check_output(args, input=source.encode()).decode()

def story_lines(source):
    return [line.strip() for line in source.splitlines()
            if line.strip() and not line.strip().startswith(('camera_', 'waitcamera', '@'))]

assert preprocess(old) == preprocess(new)
assert story_lines(preprocess(old, True)) == story_lines(preprocess(new, True))
# Gender selection and conditional calls must stay adjacent: camera macros use scratch vars.
assert '\tcheckplayergender\n\tcall_if_eq VAR_RESULT, MALE, LittlerootTown_ProfessorBirchsLab_EventScript_MayGivePokeBalls' in new
print('PASS lab: vanilla output, story order and gender-dependent handover')
