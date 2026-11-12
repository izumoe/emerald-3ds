"""Run the actual native script-wait helpers with engine/camera stubs."""
from pathlib import Path
import subprocess, tempfile
root = Path(__file__).resolve().parents[1]
source = (root / 'src/3ds_game_full.c').read_text()
def function(name):
    start = source.index(name + '(')
    start = source.rfind('\n', 0, start) + 1
    brace = source.index('{', start)
    depth = 1
    end = brace + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]
code = r'''
#include <stdbool.h>
#include <assert.h>
#include <stdio.h>
#define B_BUTTON 2
#define CTR_LOG_GAME 0
static bool sCameraScriptOwns, sCameraScriptWait, sCameraScene, sCameraSceneSkipped;
static unsigned sCameraScriptHold;
static bool sBattleCameraPush;
static unsigned sCameraRevealGrace;
static struct {bool active;} gPaletteFade;
static bool sCameraFadeBlocked;
static unsigned short gSpecialVar_0x8006;
static void CB2_Overworld(void) {}
static void OtherScene(void) {}
static void CB2_OverworldBasic(void) {}
static struct { void (*callback2)(void); unsigned newKeys; } gMain;
static bool moving, locked;
static unsigned resumed, returned;
bool CtrVoxel_ScriptMoving(void) { return moving; }
void CtrVoxel_ScriptReturn(unsigned frames) { returned=frames; moving=true; }
void CtrVoxel_CancelCamera(void) { moving=false; }
static bool ArePlayerFieldControlsLocked(void) { return locked; }
static void ScriptContext_Enable(void) { ++resumed; }
static void CtrLog_Write(int category,const char *message) { (void)category;(void)message; }
'''
code += function('Port_CameraHold') + '\n' + function('CameraScriptTick')
code += r'''
static void Reset(void) {
 sCameraScriptOwns=sCameraScene=true;
 sCameraScriptWait=sCameraSceneSkipped=false;
 sCameraScriptHold=resumed=returned=0;
 moving=false;locked=true;sBattleCameraPush=false;
 sCameraRevealGrace=0;gPaletteFade.active=false;sCameraFadeBlocked=false;
 gMain.callback2=CB2_Overworld;gMain.newKeys=0;
}
int main(void) {
 Reset();gSpecialVar_0x8006=120;Port_CameraHold();
 for(unsigned i=0;i<119;++i) CameraScriptTick();
 assert(resumed==0 && sCameraScriptHold==1);
 CameraScriptTick();assert(resumed==1 && !sCameraScriptWait);
 Reset();gSpecialVar_0x8006=120;Port_CameraHold();moving=true;
 for(unsigned i=0;i<20;++i) CameraScriptTick();
 assert(sCameraScriptHold==120 && resumed==0);
 moving=false;CameraScriptTick();assert(sCameraScriptHold==119);
 gMain.newKeys=B_BUTTON;CameraScriptTick();
 assert(sCameraSceneSkipped && sCameraScriptHold==0 && returned==36 && resumed==0);
 gMain.newKeys=0;CameraScriptTick();assert(resumed==0);
 moving=false;CameraScriptTick();assert(resumed==1);
 Port_CameraHold();assert(sCameraScriptHold==0);
 CameraScriptTick();assert(resumed==2);
 Reset();gSpecialVar_0x8006=120;Port_CameraHold();
 gMain.callback2=OtherScene;CameraScriptTick();
 assert(!sCameraScriptOwns && sCameraScriptHold==0 && resumed==1);
 Reset();gSpecialVar_0x8006=65535;Port_CameraHold();assert(sCameraScriptHold==3600);
 Reset();sBattleCameraPush=true;gMain.callback2=CB2_OverworldBasic;
 CameraScriptTick();assert(sCameraScriptOwns && sBattleCameraPush);
 gMain.callback2=OtherScene;CameraScriptTick();
 assert(!sCameraScriptOwns && !sBattleCameraPush);
 Reset();locked=false;sCameraRevealGrace=8;gPaletteFade.active=true;
 CameraScriptTick();assert(sCameraScriptOwns && sCameraRevealGrace==8);
 gPaletteFade.active=false;
 for(unsigned i=0;i<7;++i) {CameraScriptTick();assert(sCameraScriptOwns);}
 locked=true;CameraScriptTick();assert(sCameraScriptOwns && !sCameraRevealGrace);
 puts("camera script hold: timing, movement wait, B skip and cancellation passed");
}
'''
with tempfile.TemporaryDirectory() as tmp:
    src=Path(tmp)/'wait.c';exe=Path(tmp)/'wait'
    src.write_text(code)
    subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(src),'-o',str(exe)],check=True)
    subprocess.run([str(exe)],check=True)
