#include "voxel_director.h"
#include <math.h>
#include <string.h>
static float Clamp(float x, float a, float b) { return x < a ? a : x > b ? b : x; }
static float Mix(float a, float b, float t) { return a + (b-a)*t; }
bool VoxelDirector_Begin(VoxelDirector *d, const VoxelCamera *camera,
                         const VoxelCameraShot *shots, unsigned count, unsigned returnFrames)
{
    if (!shots || !count || count > VOXEL_DIRECTOR_SHOTS || !returnFrames || d->active)
        return false;
    for (unsigned i=0; i<count; ++i)
        if (!shots[i].move || shots[i].move > 3600 || shots[i].hold > 3600
            || !isfinite(shots[i].x) || !isfinite(shots[i].z)
            || !isfinite(shots[i].zoom) || !isfinite(shots[i].pitch) || !isfinite(shots[i].yaw)) return false;
    if (returnFrames > 3600) return false;
    memset(d, 0, sizeof(*d));
    memcpy(d->shots, shots, count * sizeof(*shots));
    d->anchor = d->from = *camera;
    d->count = count;
    d->returnFrames = returnFrames;
    d->active = true;
    return true;
}
void VoxelDirector_Cancel(VoxelDirector *d) { d->active = false; }
void VoxelDirector_Hold(VoxelDirector *d) { if (d->active) d->holdLast = true; }
void VoxelDirector_Track(VoxelDirector *d, float dx, float dz, float groundDelta)
{
    if (isfinite(dx) && isfinite(dz) && isfinite(groundDelta))
    { d->trackX = dx; d->trackZ = dz; d->trackGround = groundDelta; }
}
bool VoxelDirector_Moving(const VoxelDirector *d)
{
    if (!d->active) return false;
    return d->index >= d->count || d->frame < d->shots[d->index].move;
}
void VoxelDirector_Release(VoxelDirector *d, const VoxelCamera *current)
{
    if (!d->active || !d->holdLast) return;
    d->holdLast = false;
    d->from = *current;
    d->index = d->count;
    d->frame = 0;
}
void VoxelDirector_Step(VoxelDirector *d, const VoxelCamera *follow, VoxelCamera *out)
{
    VoxelCamera target = *follow;
    unsigned duration = d->returnFrames, hold = 0;
    *out = *follow;
    if (!d->active) return;
    if (d->index < d->count) {
        const VoxelCameraShot *s = &d->shots[d->index];
        target = d->anchor;
        target.targetX += Clamp(s->x, -3, 3) + d->trackX;
        target.targetZ += Clamp(s->z, -3, 3) + d->trackZ;
        target.ground += d->trackGround;
        target.yaw += Clamp(s->yaw, -60, 60);
        target.distance *= Clamp(s->zoom, 0.50f, 1.20f);
        target.pitch = Clamp(target.pitch + Clamp(s->pitch, -8, 8), 30, 55);
        duration = s->move;
        hold = s->hold;
    }
    float t = Clamp((float)++d->frame / duration, 0, 1);
    t = t*t*(3-2*t);
    *out = target;
    out->targetX = Mix(d->from.targetX, target.targetX, t);
    out->targetZ = Mix(d->from.targetZ, target.targetZ, t);
    out->ground = Mix(d->from.ground, target.ground, t);
    out->focusHeight = Mix(d->from.focusHeight, target.focusHeight, t);
    out->pitch = Mix(d->from.pitch, target.pitch, t);
    out->yaw = Mix(d->from.yaw, target.yaw, t);
    out->distance = Mix(d->from.distance, target.distance, t);
    float pitch = out->pitch * (3.14159265358979323846f/180);
    float yaw = out->yaw * (3.14159265358979323846f/180);
    out->x = out->targetX + sinf(yaw)*out->distance;
    out->y = out->ground + out->focusHeight + tanf(pitch)*out->distance;
    out->z = out->targetZ + cosf(yaw)*out->distance;
    out->targetY = out->ground + out->focusHeight;
    if (d->holdLast && d->index + 1 == d->count && d->frame >= duration) {
        d->frame = duration; /* Bound the counter during an arbitrarily long read. */
        return;
    }
    if (d->frame >= duration + hold) {
        d->from = *out;
        d->frame = 0;
        if (++d->index > d->count) d->active = false;
    }
}
