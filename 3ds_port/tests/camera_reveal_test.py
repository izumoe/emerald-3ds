"""Exercise actual queued-reveal and indoor-ray helpers with engine stubs."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
s=(root/'src/3ds_game_full.c').read_text()
def function(src,name):
 a=src.index(name+'(');a=src.rfind('\n',0,a)+1;b=src.index('{',a);n=1;i=b+1
 while n:
  n+=(src[i]=='{')-(src[i]=='}');i+=1
 return src[a:i]
a=s.index('static struct {',s.index('static bool ConversationImportant') if 'static bool ConversationImportant' in s else 0)
b=s.index('static bool sCameraScriptOwns',a)
# The reveal descriptor and setter immediately precede camera ownership.
reveal=s[a:b]
code=r'''
#include <stdbool.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
typedef short s16;
typedef unsigned char bool8;
unsigned frame;bool voxel=true;
unsigned CtrPlatform_FrameCount(void) {return frame;}
bool CtrSettings_Voxel(void) {return voxel;}
#define CTR_LOG_GAME 0
unsigned short gSpecialVar_0x8004,gSpecialVar_0x8005,gSpecialVar_0x8006,gSpecialVar_0x8007,gSpecialVar_0x8008,gSpecialVar_0x8009;
void CB2_Overworld(void) {} void CB2_OverworldBasic(void) {} void Other(void) {}
struct {void (*callback2)(void);} gMain;
struct {bool active;} gPaletteFade;
struct Save {struct {unsigned mapGroup,mapNum;} location;} save,*gSaveBlock1Ptr=&save;
bool sCameraScriptOwns,ready,accept,follow;
unsigned moves,actorA,actorB,framesSeen;int expectedYaw=-6;
bool CtrVoxel_CameraMapReady(void) {return ready;}
void CtrVoxel_ScriptPair(unsigned a,unsigned b) {actorA=a;actorB=b;}
void CtrVoxel_ScriptFollow(bool on) {follow=on;}
void CtrVoxel_GetScriptPair(unsigned *a,unsigned *b) {*a=255;*b=0x01000002u;}
bool CtrVoxel_ScriptMove(unsigned f,int d,int p,int y) {
 ++moves;framesSeen=f;assert(d==95 && p==-4 && y==expectedYaw);return accept;
}
bool CtrVoxel_ScriptOrbit(unsigned f,int d,int p,int h) { return CtrVoxel_ScriptMove(f,d,p,90-h); }
void CtrLog_Write(int c,const char *fmt,...) {(void)c;(void)fmt;}
'''+reveal+function(s,'CameraRevealTick')+function(s,'Port_CameraDeferFade')+function(s,'Port_CameraFadeReady')+function(s,'Port_CameraFadeBlocking')+r'''
void Reset(void) {
 memset(&sCameraReveal,0,sizeof(sCameraReveal));sCameraScriptOwns=false;
 moves=0;expectedYaw=-6;ready=accept=true;sCameraFadeBlocked=false;sCameraFadeWait=0;frame=0;voxel=true;gMain.callback2=CB2_Overworld;
 save.location.mapGroup=11;save.location.mapNum=3;gPaletteFade.active=true;
 gSpecialVar_0x8004=0x0b03;gSpecialVar_0x8005=255;gSpecialVar_0x8006=1;
 gSpecialVar_0x8007=95;gSpecialVar_0x8008=(unsigned short)-4;gSpecialVar_0x8009=(unsigned short)-6;
 Port_CameraReveal();
}
int main(void) {
 Reset();CameraRevealTick();assert(!moves && sCameraReveal.pending);
 gMain.callback2=Other;CameraRevealTick();assert(sCameraReveal.left);
 gMain.callback2=CB2_OverworldBasic;CameraRevealTick();assert(!moves);
 gMain.callback2=CB2_Overworld;ready=false;CameraRevealTick();assert(!moves);
 ready=true;CameraRevealTick();assert(moves==1 && framesSeen==1 && actorA==255 && actorB==0x010b0301u && follow);
 assert(sCameraScriptOwns && !sCameraReveal.pending);CameraRevealTick();assert(moves==1);
 for(int yaw=-42;yaw<=38;yaw+=80) {
  Reset();expectedYaw=yaw;gSpecialVar_0x8009=(unsigned short)yaw;Port_CameraReveal();
  sCameraReveal.left=true;CameraRevealTick();assert(moves==1 && sCameraReveal.accepted);
 }
 Reset();sCameraReveal.left=true;save.location.mapNum=9;CameraRevealTick();assert(!moves && !sCameraReveal.pending);
 Reset();sCameraReveal.left=true;ready=false;
 for(unsigned i=0;i<121;++i) { CameraRevealTick(); }
 assert(!moves && !sCameraReveal.pending);
 Reset();sCameraReveal.left=true;accept=false;CameraRevealTick();assert(moves==1 && !sCameraScriptOwns);
 Reset();save.location.mapGroup=0;save.location.mapNum=0;Port_CameraReveal();
 sCameraReveal.left=true;CameraRevealTick();assert(!moves && sCameraReveal.pending);
 save.location.mapGroup=11;save.location.mapNum=3;CameraRevealTick();assert(moves==1 && !sCameraReveal.pending);
 Reset();Port_CameraRevealSelected();sCameraReveal.left=true;CameraRevealTick();
 assert(moves==1 && actorB==0x01000002u);
 Reset();assert(!Port_CameraDeferFade());sCameraReveal.left=true;
 assert(Port_CameraDeferFade() && Port_CameraFadeBlocking());
 assert(!Port_CameraFadeReady());
 sCameraReveal.pending=false;sCameraReveal.accepted=true;sCameraReveal.poseAt=10;frame=10;
 assert(!Port_CameraFadeReady());frame=12;
 assert(Port_CameraFadeReady() && !Port_CameraFadeBlocking());
 assert(!Port_CameraDeferFade());
 Reset();sCameraReveal.left=true;voxel=false;assert(!Port_CameraDeferFade());
 Reset();sCameraReveal.left=true;assert(Port_CameraDeferFade());
 for(unsigned i=0;i<59;++i) {assert(!Port_CameraFadeReady());}
 assert(Port_CameraFadeReady() && !sCameraReveal.pending && !Port_CameraFadeBlocking());
 puts("queued reveal: leave/arrival, map readiness, one shot, mismatch, timeout and fallback passed");
}
'''
# Use the renderer's real clipping helper with a stub for known-room collision.
v=(root/'src/voxel/ctr_voxel.c').read_text(encoding='utf-8-sig')
indoor=r'''
#include <stdbool.h>
#include <assert.h>
#include <math.h>
#include <stdio.h>
#define CTR_VOXEL_LIGHTING 1
typedef struct {bool indoor;int originX,originY,width,height;} VoxelMapInstance;
VoxelMapInstance map={true,0,0,9,112};
float endZ;bool underground,blocked;
bool VoxelWorld_Underground(void) {return underground;}
const VoxelMapInstance *VoxelWorld_Instance(unsigned i) {(void)i;return &map;}
bool VoxelLighting_CameraClear(float x,float y,float z,float ex,float ey,float ez) {
 (void)x;(void)y;(void)z;(void)ex;(void)ey;endZ=ez;return !blocked && ez<112;
}
'''+function(v,'CameraActorRay')+r'''
int main(void) {
 assert(CameraActorRay(4,.9f,108,4,10,121));assert(endZ>111.9f && endZ<112);
 assert(CameraActorRay(4,.45f,111,4,9,122));
 assert(!CameraActorRay(4,.9f,108,-20,10,121));
 assert(!CameraActorRay(4,.9f,108,4,-1,121));
 map.indoor=false;assert(!CameraActorRay(4,.9f,108,4,10,121));
 underground=true;assert(CameraActorRay(4,.9f,108,4,10,121));
 assert(!CameraActorRay(4,.9f,108,-20,10,121));
 assert(!CameraActorRay(4,.9f,108,4,-1,121));
 blocked=true;assert(!CameraActorRay(4,.9f,108,4,10,121));

 puts("indoor/cave cutaway: checked room segment, front air and rejected side/below-floor exits passed");
}
'''
with tempfile.TemporaryDirectory() as tmp:
 for name,text in [('reveal',code),('indoor',indoor)]:
  p=Path(tmp)/(name+'.c');out=Path(tmp)/name;p.write_text(text)
  subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-lm','-o',str(out)],check=True)
  subprocess.run([str(out)],check=True)
