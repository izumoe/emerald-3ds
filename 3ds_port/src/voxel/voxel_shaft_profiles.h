/* Authored sunlight shafts, in the map's local tile coordinates.
 * The ends are suggestions of openings, not simulated light sources: they
 * are depth-tested against geometry but do not trace a path back to the sky. */
#ifndef VOXEL_SHAFT_PROFILES_H
#define VOXEL_SHAFT_PROFILES_H

#include <stddef.h>

typedef struct
{
    float x, z, height, width, leanX, leanZ, strength;
} VoxelShaft;

typedef struct
{
    int group, map;
    int forest;
    const VoxelShaft *shafts;
    size_t count;
} VoxelShaftProfile;

static const VoxelShaft kShaftSteven[] = {
    {6.0f, 4.8f, 3.4f, 0.75f, -0.55f, -0.35f, 0.32f},
};
static const VoxelShaft kShaftTunnel[] = {
    {8.5f, 5.5f, 3.6f, 0.70f, -0.45f, -0.30f, 0.28f},
    {21.5f, 5.5f, 3.8f, 0.80f, -0.45f, -0.30f, 0.25f},
    {30.0f, 9.0f, 3.6f, 0.65f, -0.45f, -0.30f, 0.22f},
};
static const VoxelShaft kShaftWoods[] = {
    {15.0f, 35.0f, 5.0f, 0.85f, -0.8f, -0.5f, 0.34f},
    {18.0f, 33.0f, 4.5f, 0.65f, -0.8f, -0.5f, 0.31f},
    {21.5f, 28.0f, 4.8f, 0.85f, -0.8f, -0.5f, 0.35f},
    {25.5f, 24.0f, 4.6f, 0.75f, -0.8f, -0.5f, 0.32f},
    {22.5f, 25.0f, 4.5f, 0.75f, -0.8f, -0.5f, 0.32f},
    {27.0f, 22.0f, 4.5f, 0.70f, -0.8f, -0.5f, 0.30f},
    {17.0f, 24.0f, 4.7f, 0.85f, -0.8f, -0.5f, 0.34f},
    {13.5f, 19.0f, 4.6f, 0.70f, -0.8f, -0.5f, 0.30f},
    {9.5f, 15.0f, 4.8f, 0.80f, -0.8f, -0.5f, 0.32f},
    {11.0f, 9.5f, 4.6f, 0.70f, -0.8f, -0.5f, 0.31f},
    {16.5f, 7.5f, 5.0f, 0.85f, -0.8f, -0.5f, 0.35f},
    {31.0f, 6.5f, 4.7f, 0.75f, -0.8f, -0.5f, 0.32f},
    {35.0f, 22.5f, 4.7f, 0.75f, -0.8f, -0.5f, 0.31f},
    {34.5f, 31.0f, 4.6f, 0.80f, -0.8f, -0.5f, 0.32f},
};

/* Emerald's map IDs (group 24): tunnel 4, Steven's room 10, woods 11. */
static const VoxelShaftProfile kShaftProfiles[] = {
    {24, 10, 0, kShaftSteven, sizeof(kShaftSteven) / sizeof(kShaftSteven[0])},
    {24, 4, 0, kShaftTunnel, sizeof(kShaftTunnel) / sizeof(kShaftTunnel[0])},
    {24, 11, 1, kShaftWoods, sizeof(kShaftWoods) / sizeof(kShaftWoods[0])},
};

static inline const VoxelShaftProfile *VoxelShaft_Profile(int group, int map)
{
    for (size_t i = 0; i < sizeof(kShaftProfiles) / sizeof(kShaftProfiles[0]); ++i)
        if (kShaftProfiles[i].group == group && kShaftProfiles[i].map == map)
            return &kShaftProfiles[i];
    return NULL;
}

#endif
