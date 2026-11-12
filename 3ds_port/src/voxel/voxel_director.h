/* Bounded, allocation-free cutscene camera. No SDK dependencies. */
#ifndef VOXEL_DIRECTOR_H
#define VOXEL_DIRECTOR_H
#include <stdbool.h>
#include "voxel_camera.h"
#define VOXEL_DIRECTOR_SHOTS 8
/* Offsets in world tiles from the gameplay target when Begin is called.
 * move/hold are rendered frames (normally 60 Hz), move must be nonzero.
 * zoom is distance relative to gameplay: clamped to 0.50..1.20.
 * pitch is an offset in degrees, clamped to +/-8 and absolute 30..55.
 * FOV stays unchanged; yaw follows the same easing as the other components. */
typedef struct {
    float x, z, zoom, pitch;
    unsigned move, hold;
    float yaw; /* delta from the starting yaw, clamped to +/-60 degrees */
} VoxelCameraShot;
typedef struct {
    VoxelCameraShot shots[VOXEL_DIRECTOR_SHOTS];
    VoxelCamera anchor, from;
    unsigned count, index, frame, returnFrames;
    bool active, holdLast;
    float trackX, trackZ, trackGround;
} VoxelDirector;
bool VoxelDirector_Begin(VoxelDirector *d, const VoxelCamera *camera,
                         const VoxelCameraShot *shots, unsigned count, unsigned returnFrames);
void VoxelDirector_Cancel(VoxelDirector *d);
/* Hold the final shot until Release, including while the player reads. */
void VoxelDirector_Hold(VoxelDirector *d);
void VoxelDirector_Track(VoxelDirector *d, float dx, float dz, float groundDelta);
bool VoxelDirector_Moving(const VoxelDirector *d);
/* Return from the currently displayed pose, even during the arrival. */
void VoxelDirector_Release(VoxelDirector *d, const VoxelCamera *current);
/* Follow keeps updating independently. Last phase blends to its live pose. */
void VoxelDirector_Step(VoxelDirector *d, const VoxelCamera *follow, VoxelCamera *out);
#endif
