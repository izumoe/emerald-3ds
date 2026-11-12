#include <assert.h>
#include <math.h>
#include <stdio.h>
#include "voxel_sprite_direction.h"
int main(void)
{
    assert(VoxelSprite_Quadrant(0,0)==0);
    assert(VoxelSprite_Quadrant(-49,0)==0);
    assert(VoxelSprite_Quadrant(-51,0)==3);
    assert(VoxelSprite_Quadrant(-43,3)==3);
    assert(VoxelSprite_Quadrant(-39,3)==0);
    assert(VoxelSprite_Quadrant(51,0)==1);
    assert(VoxelSprite_Quadrant(179,1)==2);
    assert(VoxelSprite_Quadrant(359,0)==0);
    assert(VoxelSprite_Quadrant(NAN,3)==0);
    for(unsigned d=0;d<4;++d) {
        assert(VoxelSprite_RelativeDirection(d,0)==d);
        unsigned other=VoxelSprite_RelativeDirection(d,1);
        assert(VoxelSprite_RelativeDirection(other,3)==d);
    }
    /* Camera west of pair: south-facing employee appears to face right;
     * north-facing player appears left. Mirrors must come from target art. */
    assert(VoxelSprite_RelativeDirection(0,3)==3);
    assert(VoxelSprite_RelativeDirection(1,3)==2);
    puts("camera-relative sprite directions: passed");
}
