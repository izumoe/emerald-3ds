"""Run the actual entity lookup with two maps sharing the same local ID."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
s=(root/'src/voxel/voxel_entities.c').read_text();a=s.index('static unsigned CameraObjectId(');b=s.index('\n/*',a)
code=r'''
#include <stdbool.h>
#include <assert.h>
#include <stdio.h>
#define OBJECT_EVENTS_COUNT 3
#define MAX_SPRITES 4
struct ObjectEvent {unsigned active,localId,mapNum,mapGroup,spriteId;float x,z;};
struct Sprite {int unused;};
struct Sprite gSprites[4];struct ObjectEvent gObjectEvents[3];
struct {unsigned objectEventId;} gPlayerAvatar={0};
struct Save {struct {unsigned mapNum,mapGroup;} location;} save={{17,0}},*gSaveBlock1Ptr=&save;
struct Map {float originX,originY;} map;
unsigned VoxelWorld_InstanceCount(void) {return 0;}
const struct Map *VoxelWorld_Instance(unsigned i) {(void)i;return &map;}
bool GetObjectWorldPos(const struct ObjectEvent *o,const struct Sprite *s,float *x,float *z) {
 (void)s;*x=o->x;*z=o->z;return true;
}
float ObjectDeck(const struct ObjectEvent *o,float x,float z) {(void)o;(void)x;(void)z;return 0;}
float VoxelRelief_LiftAt(float x,float z) {(void)x;(void)z;return 0;}
float VoxelRelief_ShiftAt(float x,float z) {(void)x;(void)z;return 0;}
'''+s[a:b]+r'''
int main(void) {
 gObjectEvents[0]=(struct ObjectEvent){1,255,17,0,0,3,4};
 gObjectEvents[1]=(struct ObjectEvent){1,2,0,0,1,5,6}; /* Wally, source Petalburg */
 gObjectEvents[2]=(struct ObjectEvent){1,2,17,0,2,8,9}; /* Route 102 local 2 */
 float x,z,g;
 assert(VoxelEntities_GetLocalWorldPos(2,&x,&z,&g));assert(x==8 && z==9);
 assert(VoxelEntities_GetLocalWorldPos(0x01000002u,&x,&z,&g));assert(x==5 && z==6);
 assert(VoxelEntities_GetLocalWorldPos(255,&x,&z,&g));assert(x==3 && z==4);
 gObjectEvents[1].active=0;assert(!VoxelEntities_GetLocalWorldPos(0x01000002u,&x,&z,&g));
 gObjectEvents[1].active=1;gObjectEvents[1].spriteId=MAX_SPRITES;
 assert(!VoxelEntities_GetLocalWorldPos(0x01000002u,&x,&z,&g));
 puts("camera actor reference: current/explicit map, retained actor, player and invalid guards passed");
}
'''
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'actors.c';out=Path(tmp)/'actors';p.write_text(code)
 subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',str(out)],check=True)
 subprocess.run([str(out)],check=True)
