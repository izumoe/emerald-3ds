#include <assert.h>
#include <stdio.h>
#include "voxel_shaft_profiles.h"

static void Check(int group, int map, size_t count, float width, float height)
{
    const VoxelShaftProfile *profile = VoxelShaft_Profile(group, map);
    assert(profile && profile->count == count && count <= 14);
    for (size_t i = 0; i < profile->count; ++i)
    {
        const VoxelShaft *shaft = &profile->shafts[i];
        assert(shaft->x >= 0 && shaft->x < width && shaft->z >= 0 && shaft->z < height);
        assert(shaft->height > 0 && shaft->height < 8 && shaft->width > 0 && shaft->width < 2);
        assert(shaft->strength > 0 && shaft->strength <= 0.5f);
    }
}

int main(void)
{
    Check(24, 10, 1, 15, 14);
    Check(24, 4, 3, 36, 24);
    Check(24, 11, 14, 48, 44);
    assert(VoxelShaft_Profile(24, 9) == NULL);
    assert(VoxelShaft_Profile(0, 11) == NULL);
    puts("PASS light shafts: map selection, counts, bounds and intensity");
    return 0;
}
