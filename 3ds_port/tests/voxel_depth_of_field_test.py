"""Check the depth-of-field thresholds against the PICA projection."""
from pathlib import Path
import subprocess
import tempfile


source = (Path(__file__).resolve().parents[1] / "src/3ds_video.c").read_text(encoding="utf-8-sig")
signature = "static float DofQuadDepth(float distance)"
start = source.index(signature)
end = source.index("\n}", start) + 2
code = r'''
#include <math.h>
#include <stdio.h>
''' + source[start:end] + r'''
/* World Mtx_Persp, PICA reversed depth, then Citro2D's ortho z. */
static float Project(float distance)
{
    float ndc = (distance - 200.0f) / (199.0f * distance);
    float reversed = -ndc;
    return 2.0f * reversed - 1.0f;
}
int main(void)
{
    const float distances[] = {1, 2, 4, 8, 10, 15, 30, 100, 200};
    for (unsigned i = 0; i < sizeof(distances) / sizeof(distances[0]); ++i)
    {
        float z = DofQuadDepth(distances[i]);
        if (fabsf(z - Project(distances[i])) > 0.00001f) return 1;
        if (i && z >= DofQuadDepth(distances[i - 1])) return 2;
    }
    if (DofQuadDepth(0) != DofQuadDepth(1)) return 3;
    if (DofQuadDepth(300) != DofQuadDepth(200)) return 4;
    puts("PASS depth of field: PICA thresholds, ordering, near/far limits");
    return 0;
}
'''
with tempfile.TemporaryDirectory() as temp:
    executable = Path(temp) / "dof_test"
    subprocess.run(["cc", "-std=c99", "-x", "c", "-", "-lm", "-o", str(executable)],
                   input=code, text=True, check=True)
    subprocess.run([str(executable)], check=True)
