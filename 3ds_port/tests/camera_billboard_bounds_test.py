"""Exercise the actual render-base helper and camera bounds with known OBJ pixels."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1];s=(root/'src/voxel/voxel_entities.c').read_text()
def fn(name):
 a=s.index(name+'(');a=s.rfind('\n',0,a)+1;b=s.index('{',a);n=1;i=b+1
 while n:n+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[a:i]
code=r'''
#include <stdbool.h>
#include <math.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define OBJECT_EVENTS_COUNT 3
#define MAX_SPRITES 4
#define VOXEL_PIXELS_PER_TILE 16.0f
typedef struct {float pitch,yaw,lay;} VoxelCamera;
typedef struct {bool valid,flipX,flipY,color256;int width,height,footPad;unsigned sourceBytes;unsigned char source[4096];const void *footPadImages;} VoxelSpriteSlot;
struct ObjectEvent {unsigned active,localId,mapNum,mapGroup,spriteId,graphicsId;float x,z;};
struct Sprite {int unused;} gSprites[4];struct ObjectEvent gObjectEvents[3];
struct {unsigned objectEventId;} gPlayerAvatar={0};
struct Save {struct {unsigned mapNum,mapGroup;} location;} save={{4,24}},*gSaveBlock1Ptr=&save;
struct Map {float originX,originY;} map;
struct ObjectEventGraphicsInfo {const void *images;} infos[3];
const struct ObjectEventGraphicsInfo *GetObjectEventGraphicsInfo(unsigned id) {return &infos[id];}
VoxelSpriteSlot sSlots[3];unsigned sSlotEffect[3];float deck,push,model;
unsigned VoxelWorld_InstanceCount(void) {return 0;}
const struct Map *VoxelWorld_Instance(unsigned i) {(void)i;return &map;}
bool GetObjectWorldPos(const struct ObjectEvent *o,const struct Sprite *sp,float *x,float *z) {(void)sp;*x=o->x;*z=o->z;return true;}
float ObjectDeck(const struct ObjectEvent *o,float x,float z) {(void)o;(void)x;(void)z;return deck;}
float VoxelRelief_LiftAt(float x,float z) {(void)x;(void)z;return 1;}
float VoxelRelief_ShiftAt(float x,float z) {(void)x;(void)z;return 1;}
float CardPush(float x,float z,float w,float h) {(void)x;(void)z;(void)w;(void)h;return push;}
float ModelPush(float x,float z,float w) {(void)x;(void)z;(void)w;return model;}
'''+''.join(fn(n) for n in ['CameraObjectId','VisibleRows','BillboardBase','OpaqueTop','VoxelEntities_GetCameraBounds'])+r'''
void Near(float a,float b) {assert(fabsf(a-b)<0.0001f);}
void Pixel(VoxelSpriteSlot *slot,unsigned x,unsigned y) {
 unsigned tile=(y/8)*(slot->width/8)+x/8,p=(y%8)*8+x%8;
 if(slot->color256)slot->source[tile*64+p]=1;
 else slot->source[tile*32+p/2]|=1u<<((p&1)*4);
}
int main(void) {
 infos[1].images=&infos[1];infos[2].images=&infos[2];
 gObjectEvents[0]=(struct ObjectEvent){1,255,4,24,0,1,13,4};
 VoxelSpriteSlot *slot=&sSlots[0];slot->valid=true;slot->width=16;slot->height=32;slot->footPad=2;slot->sourceBytes=256;slot->footPadImages=infos[1].images;
 for(unsigned y=6;y<30;++y)for(unsigned x=2;x<14;++x)Pixel(slot,x,y);
 assert(OpaqueTop(slot,30)==6);
 VoxelCamera camera={0,90,0};float x,y,z,w,h;push=2;model=1;
 assert(VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));
 Near(x,15.5f);Near(y,3);Near(z,5.5f);Near(w,.5f);Near(h,1.5f);
 /* A model push wins by maximum, not addition; decks disable both pushes. */
 push=0;assert(VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));Near(x,14.5f);Near(y,2);
 deck=1;assert(VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));Near(x,13.5f);Near(y,2);Near(z,6.5f);
 deck=0;push=2;camera.yaw=0;camera.pitch=60;
 assert(VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));Near(x,13.5f);Near(z,7.5f);Near(w,.3535534f);Near(h,2.1213203f);
 /* A small Pokemon has its own opaque height, not a human-sized probe. */
 memset(slot->source,0,sizeof(slot->source));slot->height=16;slot->footPad=1;slot->sourceBytes=128;
 gObjectEvents[0].graphicsId=2;slot->footPadImages=infos[2].images;
 for(unsigned row=4;row<15;++row)Pixel(slot,8,row);
 camera.pitch=0;assert(VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));Near(h,.6875f);
 slot->flipY=true;assert(OpaqueTop(slot,15)==1);slot->flipY=false;
 slot->color256=true;slot->sourceBytes=256;memset(slot->source,0,sizeof(slot->source));Pixel(slot,8,3);assert(OpaqueTop(slot,15)==3);
 memset(slot->source,0,sizeof(slot->source));assert(!VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));
 Pixel(slot,8,3);slot->footPadImages=NULL;assert(!VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));slot->footPadImages=infos[2].images;
 camera.lay=1;assert(!VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));camera.lay=0;
 sSlotEffect[0]=1;assert(!VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));sSlotEffect[0]=0;
 gObjectEvents[0].spriteId=MAX_SPRITES;assert(!VoxelEntities_GetCameraBounds(255,&camera,&x,&y,&z,&w,&h));
 puts("billboard camera bounds: cell centres, shared render push, deck, opaque/trimmed heights, transforms and invalid cache guards passed");
}
'''
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'bounds.c';out=Path(tmp)/'bounds';p.write_text(code)
 subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-lm','-o',str(out)],check=True)
 subprocess.run([str(out)],check=True)
