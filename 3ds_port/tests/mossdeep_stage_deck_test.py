"""Check the generated Mossdeep stage deck through the runtime lookup.

Run after generating romfs/voxel/buildings.bin from the extracted source tree.
"""
import json
import subprocess
import tempfile
from pathlib import Path

test_source = Path(__file__).with_suffix('.c').resolve()
port = Path(__file__).resolve().parents[1]
if not (port.parent / 'data/layouts/layouts.json').exists():
    port = port.parent / 'build/upstream/3ds_port'
layouts = json.loads((port.parent / 'data/layouts/layouts.json').read_text())['layouts']
layout = next(i + 1 for i, entry in enumerate(layouts)
              if entry['id'] == 'LAYOUT_MOSSDEEP_CITY_GYM')
pack = (port / 'romfs/voxel/buildings.bin').resolve()
with tempfile.TemporaryDirectory() as tmp:
    exe = Path(tmp) / 'mossdeep_deck'
    subprocess.run(['cc', '-std=c99', '-O2', '-Wall', '-Wextra', '-Werror',
                    '-Iinclude', '-Isrc/voxel', '-iquote', '../include',
                    '-D_GNU_SOURCE', '-DPORT_LOG(...)=((void)0)', '-DVOXEL_HOST_FILES',
                    f'-DMOSSDEEP_LAYOUT={layout}', f'-DVOXEL_BUILDINGS_PATH="{pack}"',
                    str(test_source), 'src/voxel/voxel_building.c',
                    'src/voxel/voxel_grade.c', 'src/3ds_video_decode.c', '-lm', '-o', str(exe)],
                   cwd=port, check=True)
    subprocess.run([str(exe)], cwd=port, check=True)
