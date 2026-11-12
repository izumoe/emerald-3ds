#include "voxel_director.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
static void Near(float a, float b) { assert(fabsf(a-b)<0.0001f); }
int main(void)
{
    VoxelDirector d = {0};
    VoxelCamera follow = {.targetX=10, .targetZ=20, .ground=1, .pitch=40, .distance=13, .fov=35};
    VoxelCamera out;
    VoxelCameraShot shots[] = {{100,-100,0.01f,100,60,30,0}, {1,0,1,0,60,0,0}};
    assert(!VoxelDirector_Begin(&d,&follow,shots,0,60));
    assert(!VoxelDirector_Begin(&d,&follow,shots,2,0));
    shots[0].x = NAN;
    assert(!VoxelDirector_Begin(&d,&follow,shots,2,60));
    shots[0].x = 100;
    assert(VoxelDirector_Begin(&d,&follow,shots,2,60));
    assert(!VoxelDirector_Begin(&d,&follow,shots,2,60));
    for (unsigned i=0;i<60;++i) {
        VoxelDirector_Step(&d,&follow,&out);
        assert(out.distance >= 13*0.50f);
        assert(out.targetX>=10 && out.targetX<=13);
        assert(isfinite(out.y));
    }
    Near(out.targetX,13); Near(out.targetZ,17); Near(out.pitch,48);
    Near(out.distance,13*0.50f);
    for (unsigned i=0;i<30;++i) VoxelDirector_Step(&d,&follow,&out);
    Near(out.targetX,13);
    for (unsigned i=0;i<60;++i) VoxelDirector_Step(&d,&follow,&out);
    Near(out.targetX,11); Near(out.distance,13);
    /* Gameplay moves during the return: land on its current pose exactly. */
    for (unsigned i=0;i<60;++i) {
        follow.targetX += 0.01f;
        VoxelDirector_Step(&d,&follow,&out);
    }
    assert(!d.active); Near(out.targetX,follow.targetX);
    Near(out.distance,follow.distance); Near(out.pitch,follow.pitch);
    assert(VoxelDirector_Begin(&d,&follow,shots,2,60));
    VoxelDirector_Cancel(&d);
    VoxelDirector_Step(&d,&follow,&out);
    Near(out.targetX,follow.targetX);
    /* A conversation must last as long as reading, not a preset timeout. */
    VoxelCameraShot talk = {0.5f, 0.7f, 0.92f, 0, 54, 0,0};
    assert(VoxelDirector_Begin(&d,&follow,&talk,1,60));
    VoxelDirector_Hold(&d);
    for (unsigned i=0; i<12000; ++i) VoxelDirector_Step(&d,&follow,&out);
    assert(d.active); assert(d.frame == 54);
    Near(out.distance,follow.distance*0.92f);
    VoxelDirector_Release(&d,&out);
    for (unsigned i=0; i<60; ++i) VoxelDirector_Step(&d,&follow,&out);
    assert(!d.active); Near(out.targetX,follow.targetX);
    /* Dismiss before arrival: return from the displayed pose, with no snap. */
    assert(VoxelDirector_Begin(&d,&follow,&talk,1,60));
    VoxelDirector_Hold(&d);
    for (unsigned i=0; i<10; ++i) VoxelDirector_Step(&d,&follow,&out);
    float before = out.targetX;
    VoxelDirector_Release(&d,&out);
    VoxelDirector_Step(&d,&follow,&out);
    assert(fabsf(out.targetX-before) < 0.001f);
    for (unsigned i=1; i<60; ++i) VoxelDirector_Step(&d,&follow,&out);
    assert(!d.active); Near(out.distance,follow.distance);
    /* Authored multi-shot sequences still hold only their final shot. */
    VoxelCameraShot story[] = {{0.6f,0.9f,0.95f,2,3,1,0},{0,0.7f,0.80f,4,3,0,0}};
    assert(VoxelDirector_Begin(&d,&follow,story,2,60));
    VoxelDirector_Hold(&d);
    for (unsigned i=0;i<100;++i) VoxelDirector_Step(&d,&follow,&out);
    assert(d.active && d.index == 1);
    Near(out.distance,follow.distance*0.80f);
    Near(out.pitch,follow.pitch+4);
    VoxelDirector_Release(&d,&out);
    for (unsigned i=0;i<60;++i) VoxelDirector_Step(&d,&follow,&out);
    assert(!d.active); Near(out.pitch,follow.pitch);
    /* Story arrival: all components reach halfway together, then hold. */
    VoxelCameraShot together = {1.0f,0.7f,0.80f,4,90,0,0};
    assert(VoxelDirector_Begin(&d,&follow,&together,1,60));
    VoxelDirector_Hold(&d);
    for (unsigned i=0;i<45;++i) VoxelDirector_Step(&d,&follow,&out);
    Near(out.targetX,follow.targetX+0.5f);
    Near(out.targetZ,follow.targetZ+0.35f);
    Near(out.distance,follow.distance*0.90f);
    Near(out.pitch,follow.pitch+2);
    for (unsigned i=45;i<200;++i) VoxelDirector_Step(&d,&follow,&out);
    assert(d.active && d.index == 0 && d.frame == 90);
    Near(out.distance,follow.distance*0.80f);
    Near(out.pitch,follow.pitch+4);
    VoxelDirector_Release(&d,&out);
    for (unsigned i=0;i<60;++i) VoxelDirector_Step(&d,&follow,&out);
    assert(!d.active); Near(out.pitch,follow.pitch);
    /* Angled tracking: yaw eases with the move, held framing follows actors,
     * waitcamera finishes at arrival, and return restores gameplay yaw. */
    VoxelCameraShot scenic = {0,0.7f,0.90f,-6,60,0,-24};
    assert(VoxelDirector_Begin(&d,&follow,&scenic,1,60));
    VoxelDirector_Hold(&d);
    assert(VoxelDirector_Moving(&d));
    for (unsigned i=0;i<30;++i) VoxelDirector_Step(&d,&follow,&out);
    Near(out.yaw,-12);
    for (unsigned i=30;i<60;++i) VoxelDirector_Step(&d,&follow,&out);
    assert(!VoxelDirector_Moving(&d) && d.active);
    VoxelDirector_Track(&d,2,-7,0);
    VoxelDirector_Step(&d,&follow,&out);
    Near(out.targetX,follow.targetX+2);
    Near(out.targetZ,follow.targetZ+0.7f-7);
    Near(out.yaw,-24);
    VoxelDirector_Release(&d,&out);
    assert(VoxelDirector_Moving(&d));
    for (unsigned i=0;i<60;++i) VoxelDirector_Step(&d,&follow,&out);
    assert(!VoxelDirector_Moving(&d)); Near(out.yaw,follow.yaw);
    /* Script endpoints use gameplay distance and absolute actor positions,
     * even when retargeting from a closer shot on the other side. */
    VoxelCamera from=follow; from.distance*=0.8f; from.yaw=-24;
    VoxelCameraShot reframe={0,0,1.2f,0,60,0,24};
    assert(VoxelDirector_Begin(&d,&from,&reframe,1,60));
    d.anchor=follow; d.anchor.targetX+=8;
    VoxelDirector_Hold(&d);
    for (unsigned i=0;i<30;++i) VoxelDirector_Step(&d,&follow,&out);
    Near(out.yaw,0); Near(out.distance,follow.distance);
    for (unsigned i=30;i<60;++i) VoxelDirector_Step(&d,&follow,&out);
    Near(out.yaw,24); Near(out.distance,follow.distance*1.2f);
    Near(out.targetX,follow.targetX+8);
    VoxelDirector_Cancel(&d);
    /* A slow orbit remains active across ordinary text advances; replacing it
     * or returning early starts at the displayed pose rather than its endpoint. */
    VoxelCameraShot orbit={0,0,0.80f,4,420,0,-60};
    assert(VoxelDirector_Begin(&d,&follow,&orbit,1,90));
    VoxelDirector_Hold(&d);
    for (unsigned i=0;i<40;++i) VoxelDirector_Step(&d,&follow,&out);
    assert(VoxelDirector_Moving(&d));
    VoxelCamera displayed=out;
    VoxelDirector_Cancel(&d);
    VoxelCameraShot next={0,0,0.9f,0,90,0,0};
    assert(VoxelDirector_Begin(&d,&displayed,&next,1,90));
    d.anchor=follow;
    VoxelDirector_Hold(&d);
    VoxelDirector_Step(&d,&follow,&out);
    assert(fabsf(out.yaw-displayed.yaw)<0.1f);
    assert(fabsf(out.x-displayed.x)<0.05f);
    assert(fabsf(out.y-displayed.y)<0.05f);
    assert(fabsf(out.z-displayed.z)<0.05f);
    displayed=out;
    VoxelDirector_Release(&d,&displayed);
    VoxelDirector_Step(&d,&follow,&out);
    assert(fabsf(out.yaw-displayed.yaw)<0.1f);
    for (unsigned i=1;i<90;++i) VoxelDirector_Step(&d,&follow,&out);
    assert(!d.active); Near(out.yaw,follow.yaw);
    assert(VoxelDirector_Begin(&d,&follow,&orbit,1,90));
    VoxelDirector_Hold(&d);
    for (unsigned i=0;i<500;++i) VoxelDirector_Step(&d,&follow,&out);
    Near(out.yaw,-60); Near(out.pitch,follow.pitch+4);
    assert(!VoxelDirector_Moving(&d) && d.active);
    VoxelDirector_Cancel(&d);
    /* Scenic views use a fixed map anchor with authored absolute angles and
     * a wider distance, but return to the live adjustable gameplay camera. */
    VoxelCamera custom=follow;
    custom.pitch=48; custom.distance=7.25f;
    VoxelCameraShot landmark={0,0,1,0,180,0,0};
    assert(VoxelDirector_Begin(&d,&custom,&landmark,1,36));
    d.anchor=custom;
    d.anchor.targetX=27.5f; d.anchor.targetZ=19.5f;
    d.anchor.pitch=55; d.anchor.yaw=-25; d.anchor.distance=custom.distance*1.8f;
    VoxelDirector_Hold(&d);
    for(unsigned i=0;i<180;++i) VoxelDirector_Step(&d,&custom,&out);
    Near(out.targetX,27.5f); Near(out.targetZ,19.5f);
    Near(out.pitch,55); Near(out.yaw,-25); Near(out.distance,custom.distance*1.8f);
    displayed=out;
    VoxelDirector_Release(&d,&displayed);
    VoxelDirector_Step(&d,&custom,&out);
    assert(fabsf(out.targetX-displayed.targetX)<0.1f);
    /* Gameplay settings may change while the cinematic owns the view. */
    custom.pitch=43; custom.distance=8.5f;
    for(unsigned i=1;i<36;++i) VoxelDirector_Step(&d,&custom,&out);
    assert(!d.active); Near(out.pitch,43); Near(out.distance,8.5f);
    Near(out.targetX,custom.targetX); Near(out.yaw,custom.yaw);
    /* A one-frame scenic cut lands on its anchor; the subsequent descending
     * orbit starts from that exact displayed view rather than gameplay. */
    VoxelCameraShot cutShot={0,0,1,0,1,0,0};
    assert(VoxelDirector_Begin(&d,&custom,&cutShot,1,36));
    d.anchor=custom; d.anchor.pitch=55; d.anchor.yaw=-40;
    d.anchor.distance=custom.distance*1.7f;
    d.anchor.targetX=16.5f; d.anchor.targetZ=45.5f;
    VoxelDirector_Hold(&d);
    VoxelDirector_Step(&d,&custom,&out);
    Near(out.yaw,-40); Near(out.pitch,55); Near(out.targetZ,45.5f);
    assert(!VoxelDirector_Moving(&d));
    displayed=out; VoxelDirector_Cancel(&d);
    landmark.move=180;
    assert(VoxelDirector_Begin(&d,&displayed,&landmark,1,36));
    d.anchor=custom; d.anchor.pitch=32; d.anchor.yaw=15;
    d.anchor.distance=custom.distance*1.1f;
    d.anchor.targetX=16.5f; d.anchor.targetZ=45.5f;
    VoxelDirector_Hold(&d);
    VoxelDirector_Step(&d,&custom,&out);
    assert(fabsf(out.yaw-displayed.yaw)<0.01f);
    for(unsigned i=1;i<180;++i) VoxelDirector_Step(&d,&custom,&out);
    Near(out.yaw,15); Near(out.pitch,32); Near(out.distance,custom.distance*1.1f);
    VoxelDirector_Cancel(&d);
    /* Raise the aim without changing physical ground; release smoothly to gameplay. */
    VoxelCamera base = {.targetX=3,.targetZ=4,.ground=2,.pitch=40,.distance=8,.fov=35};
    VoxelCameraShot heightShot={0,0,1,0,60,0,0};
    assert(VoxelDirector_Begin(&d,&base,&heightShot,1,60));
    d.anchor.focusHeight=0.5f;
    VoxelDirector_Hold(&d);
    for (unsigned i=0;i<30;++i) VoxelDirector_Step(&d,&base,&out);
    Near(out.ground,2); Near(out.focusHeight,0.25f); Near(out.targetY,2.25f);
    for (unsigned i=30;i<60;++i) VoxelDirector_Step(&d,&base,&out);
    Near(out.focusHeight,0.5f); Near(out.targetY,2.5f);
    VoxelDirector_Release(&d,&out);
    for (unsigned i=0;i<60;++i) VoxelDirector_Step(&d,&base,&out);
    assert(!d.active); Near(out.focusHeight,0); Near(out.ground,2); Near(out.targetY,2);
    puts("voxel director: passed");
}
