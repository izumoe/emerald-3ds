/* Camera-relative four-direction art; independent of game-facing state. */
#ifndef VOXEL_SPRITE_DIRECTION_H
#define VOXEL_SPRITE_DIRECTION_H
#include <math.h>
/* Keep the current quadrant within 50 degrees: five degrees of hysteresis
 * either side of the nearest-view boundary. Quadrants increase S,E,N,W. */
static inline int VoxelSprite_Quadrant(float yaw, int previous)
{
    if (!isfinite(yaw)) return 0;
    yaw = fmodf(yaw, 360.0f);
    float delta = yaw - previous * 90.0f;
    while (delta > 180.0f) delta -= 360.0f;
    while (delta < -180.0f) delta += 360.0f;
    if (fabsf(delta) <= 50.0f) return previous;
    int nearest = (int)floorf((yaw + 45.0f) / 90.0f);
    return (nearest % 4 + 4) % 4;
}
static inline unsigned VoxelSprite_RelativeDirection(unsigned direction, int quadrant)
{
    static const unsigned toAngle[4] = {0,2,3,1}; /* S,N,W,E */
    static const unsigned toDirection[4] = {0,3,1,2};
    return toDirection[(toAngle[direction & 3] - quadrant + 4) % 4];
}
#endif
