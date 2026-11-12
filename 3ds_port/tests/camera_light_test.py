"""An authored light pool is bounded and never changes gameplay darkness."""
from pathlib import Path
import subprocess,tempfile
s=(Path(__file__).resolve().parents[1]/'src/voxel/ctr_voxel.c').read_text()
def function(name):
 a=s.rfind('\n',0,s.index(name+'('))+1;b=s.index('{',a);depth=1;i=b+1
 while depth:
  depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[a:i]
code='''#include <assert.h>\n#include <stdbool.h>\n#include <math.h>\nstatic struct {bool active; int lightRadius;} sScriptCamera;\nstatic float sCinemaBars;\n'''+function('CtrVoxel_ScriptLight')+'\n'+function('CtrVoxel_CinematicLightRadius')+'''\nint main(void) {
 CtrVoxel_ScriptLight(999); assert(sScriptCamera.lightRadius==160);
 sCinemaBars=1; assert(CtrVoxel_CinematicLightRadius()==0);
 sScriptCamera.active=true; assert(CtrVoxel_CinematicLightRadius()==160);
 sCinemaBars=0.5f; assert(fabsf(CtrVoxel_CinematicLightRadius()-80)<0.001f);
 CtrVoxel_ScriptLight(-1); assert(CtrVoxel_CinematicLightRadius()==0);
 return 0; }\n'''
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp);(p/'test.c').write_text(code)
 subprocess.run(['cc','-std=c11','-fsanitize=undefined','-o',str(p/'test'),str(p/'test.c'),'-lm'],check=True)
 subprocess.run([str(p/'test')],check=True)
print('PASS cinematic light: bounded radius, inactive gameplay, smooth fade')
