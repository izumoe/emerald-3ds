"""Authored cameras accept modest relief only after path visibility succeeds."""
from pathlib import Path
import subprocess,tempfile
s=(Path(__file__).resolve().parents[1]/'src/voxel/ctr_voxel.c').read_text()
a=s.rfind('\n',0,s.index('ScriptMove('))+1;b=s.index('{',a);n=1;i=b+1
while n:n+=(s[i]=='{')-(s[i]=='}');i+=1
actual=s[a:i]
code=r'''
#include <stdbool.h>
#include <math.h>
#include <assert.h>
#include <stdarg.h>
typedef struct {float targetX,targetZ,ground,focusHeight,yaw;} VoxelCamera;
typedef struct {float x,z,zoom,pitch;unsigned move,hold;float yaw;} VoxelCameraShot;
typedef struct {bool active;VoxelCamera anchor;} VoxelDirector;
static VoxelCamera sCamera,sFollowCamera; static VoxelDirector sDirector;
static struct {bool on;} sBattle;static float sSwoop;
static struct {unsigned a,b;bool active,returning;float x,z,ground,smoothX,smoothZ,smoothGround;int height16;} sScriptCamera;
static float gap;static bool clear,found=true;static int checks;
#define CTR_LOG_VIDEO 0
bool CtrSettings_Voxel(void){return true;} bool CtrVoxel_IsAvailable(void){return true;}
bool ScriptPairPosition(float*x,float*z,float*g){*x=*z=0;*g=gap/2;return true;}
bool VoxelEntities_GetLocalWorldPos(unsigned a,float*x,float*z,float*g){*x=*z=0;*g=a==1?gap:0;return found;}
bool ConversationPathClear(const VoxelCameraShot*s,float x,float z,float dx,float dz,const VoxelCamera*a,const unsigned*ids){(void)s;(void)x;(void)z;(void)dx;(void)dz;(void)a;assert(ids[0]==0 && ids[1]==1);++checks;return clear;}
void CtrLog_Write(int c,const char *f,...){(void)c;(void)f;}
bool VoxelDirector_Moving(VoxelDirector*d){(void)d;return false;}
void VoxelDirector_Cancel(VoxelDirector*d){d->active=false;}
bool VoxelDirector_Begin(VoxelDirector*d,const VoxelCamera*c,const VoxelCameraShot*s,unsigned n,unsigned r){(void)c;(void)s;(void)n;(void)r;d->active=true;return true;}
void VoxelDirector_Hold(VoxelDirector*d){(void)d;}
'''+actual+r'''
int main(void){sScriptCamera.a=0;sScriptCamera.b=1;sScriptCamera.height16=8;
 gap=.5f;clear=true;assert(ScriptMove(60,55,-4,-35,60));assert(checks==1);assert(sDirector.anchor.focusHeight==.5f);
 sDirector.active=false;clear=false;assert(!ScriptMove(60,55,-4,-35,60));assert(checks==2);
 gap=1.01f;clear=true;assert(!ScriptMove(60,55,-4,-35,60));assert(checks==2);
 gap=.5f;found=false;assert(!ScriptMove(60,55,-4,-35,60));assert(checks==2);
}
'''
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp);(p/'test.c').write_text(code);subprocess.run(['cc','-std=c11','-fsanitize=undefined','-o',str(p/'test'),str(p/'test.c'),'-lm'],check=True);subprocess.run([str(p/'test')],check=True)
print('PASS authored camera: modest relief requires a clear path; large gaps and missing actors reject')
