"""Check late-story camera cues preserve the original event actions."""
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
patches = ['0106-late-story-camera-pass.patch', '0107-league-hideouts-camera-pass.patch', '0108-harbor-space-pillar-cameras.patch', '0109-mossdeep-twins-camera.patch', '0110-seafloor-cavern-camera.patch', '0111-finale-conversations-camera.patch', '0112-champion-procession-camera.patch']

def cpp(text, port=False):
    return subprocess.check_output(['cpp', '-P', '-x', 'c'] + (['-DPORT_BRIDGE'] if port else []) + ['-'], input=text.encode()).decode()

def events(text):
    ignored = ('camera_', 'waitcamera', '@', 'copyvar VAR_TEMP_6, VAR_0x8008',
               'copyvar VAR_0x8008, VAR_TEMP_6',
               'goto_if_defeated TRAINER_JUAN_1, SootopolisGym_CameraOriginalJuan',
               'SootopolisGym_CameraOriginalJuan:',
               'goto_if_defeated TRAINER_MATT, AquaHideout_CameraOriginalMatt',
               'AquaHideout_CameraOriginalMatt:',
               'goto_if_defeated TRAINER_TATE_AND_LIZA_1, MossdeepGym_CameraOriginalTwins',
               'special HasEnoughMonsForDoubleBattle',
               'goto_if_ne VAR_RESULT, PLAYER_HAS_TWO_USABLE_MONS, MossdeepGym_CameraOriginalTwins',
               'MossdeepGym_CameraOriginalTwins:',
               'setvar VAR_0x8004, LOCALID_SEAFLOOR_CAVERN_ARCHIE',
               'setvar VAR_0x8005, LOCALID_SEAFLOOR_CAVERN_MAXIE',
               'setvar VAR_0x8006, LOCALID_SEAFLOOR_CAVERN_GRUNT_1',
               'setvar VAR_0x8007, LOCALID_SEAFLOOR_CAVERN_GRUNT_2')
    return [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith(ignored)]

for filename in patches:
    patch = root/'patches/pokeemerald'/filename
    paths = [line[6:] for line in patch.read_text().splitlines() if line.startswith('+++ b/')]
    with tempfile.TemporaryDirectory() as tmp:
        for rel in paths:
            dst=Path(tmp)/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy(root/'build/upstream'/rel,dst)
        subprocess.run(['git','apply','--reverse',str(patch)],cwd=tmp,check=True)
        for rel in paths:
            old=(Path(tmp)/rel).read_text(); new=(root/'build/upstream'/rel).read_text()
            assert cpp(old)==cpp(new),rel
            before=events(cpp(old,True));after=events(cpp(new,True))
            if rel.endswith('SootopolisCity_Gym_1F/scripts.inc'):
                k=after.index('SootopolisCity_Gym_1F_EventScript_Juan::'); assert after[k+1:k+3]==['lock','faceplayer'];del after[k+1:k+3]
            if rel.endswith('AquaHideout_B2F/scripts.inc'):
                k=after.index('AquaHideout_B2F_EventScript_Matt::');assert after[k+1:k+3]==['lock','faceplayer'];del after[k+1:k+3]
            if rel.endswith('MossdeepCity_Gym/scripts.inc'):
                k=after.index('MossdeepCity_Gym_EventScript_TateAndLiza::');assert after[k+1:k+3]==['lock','faceplayer'];del after[k+1:k+3]
            assert before==after,rel
            if 'MossdeepCity_Gym/scripts.inc' in rel:
                assert new.index('special HasEnoughMonsForDoubleBattle') < new.index('goto_if_ne VAR_RESULT, PLAYER_HAS_TWO_USABLE_MONS') < new.index('camera_reveal MAP_MOSSDEEP_CITY_GYM')
            if 'SeafloorCavern_Room9' in rel:
                for name in ('ARCHIE', 'MAXIE', 'GRUNT_1', 'GRUNT_2'):
                    line = f'LOCALID_SEAFLOOR_CAVERN_{name}'
                    assert new.count(line) == old.count(line) + (4 if name == "ARCHIE" else 2), name
                assert new.index('camera_end', new.index('camera_reveal MAP_SEAFLOOR_CAVERN_ROOM9')) < new.index('special DoOrbEffect')
                battle = new.index('trainerbattle_no_intro TRAINER_ARCHIE')
                cue = new.index('camera_reveal MAP_SEAFLOOR_CAVERN_ROOM9')
                assert cue < new.index('setvar VAR_0x8004, LOCALID_SEAFLOOR_CAVERN_ARCHIE', cue) < battle
                after_return = new.index('camera_end', battle)
                assert after_return < new.index('setvar VAR_0x8004, LOCALID_SEAFLOOR_CAVERN_ARCHIE', after_return) < new.index('special DoOrbEffect')
            if 'SlateportCity_Harbor' in rel:
                stored = new.index('copyvar VAR_TEMP_6, VAR_0x8008')
                exit_cue = new.index('camera_pair LOCALID_PLAYER, LOCALID_PLAYER', stored)
                restored = new.index('copyvar VAR_0x8008, VAR_TEMP_6', exit_cue)
                approach = new.index('call_if_eq VAR_0x8008, 0, SlateportCity_Harbor_EventScript_SternApproachPlayer0', restored)
                assert stored < exit_cue < restored < approach
            if 'VictoryRoad_1F' in rel:
                assert new.index('copyvar VAR_TEMP_6, VAR_0x8008') < new.index('camera_pair LOCALID_PLAYER, LOCALID_VICTORY_ROAD_ENTRANCE_WALLY')
                assert new.index('copyvar VAR_0x8008, VAR_TEMP_6') < new.index('copyvar VAR_VICTORY_ROAD_1F_STATE, VAR_0x8008')
            if 'MtPyre_Summit' in rel:
                assert new.index('copyvar VAR_0x8008, VAR_TEMP_6') < new.index('call_if_eq VAR_0x8008, 0, MtPyre_Summit_EventScript_OldLadyApproachPlayer0')
print('PASS late-story scripts: original actions, choice and approach selectors')
