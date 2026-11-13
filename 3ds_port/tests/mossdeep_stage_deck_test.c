/* Exercise the packed stage heights through the same lookup used by actors. */
#include <math.h>
#include <stdio.h>
#include <string.h>

#include "voxel_building.h"
#include "voxel_relief.h"

void VoxelBuilder_Tri(VoxelBuilder *b, const VoxelVertex *a, const VoxelVertex *c,
                      const VoxelVertex *d) { (void)b; (void)a; (void)c; (void)d; }
void VoxelBuilder_Quad(VoxelBuilder *b, const VoxelVertex *a, const VoxelVertex *c,
                       const VoxelVertex *d, const VoxelVertex *e)
{ (void)b; (void)a; (void)c; (void)d; (void)e; }
float VoxelBuilder_StretchZ(const VoxelBuilder *b, float z) { (void)b; return z; }
float VoxelRelief_CellLift(const VoxelMapInstance *i, int x, int y)
{ (void)i; (void)x; (void)y; return 0; }
float VoxelRelief_CellShift(const VoxelMapInstance *i, int x, int y)
{ (void)i; (void)x; (void)y; return 0; }
int VoxelWorld_GetMetatileId(int x, int y) { (void)x; (void)y; return 0x20a; }

int main(void)
{
    VoxelMapInstance inst;
    float lift;
    memset(&inst, 0, sizeof(inst));
    inst.layoutId = MOSSDEEP_LAYOUT;
    inst.originX = 10; inst.originY = 20;
    inst.width = 27; inst.height = 34;
    if (!VoxelBuildings_Init()) return 1;
    /* The twins stand at (23,7)/(24,7); either front tile can hold the player. */
    for (int x = 23; x <= 24; ++x)
        for (int y = 7; y <= 8; ++y)
            if (!VoxelBuildings_DeckAt(&inst, 10+x+0.5f, 20+y+0.5f, 0, &lift)
                || fabsf(lift - 0.75f) > 0.001f) return 2;
    if (VoxelBuildings_DeckAt(&inst, 33.5f, 29.5f, 0, &lift)) return 3;
    VoxelBuildings_Shutdown();
    puts("PASS Mossdeep: twins and player stand on the stage; adjacent floor stays level");
    return 0;
}
