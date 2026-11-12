"""Exercise the actual engine battle-start task with native camera stubs."""
from pathlib import Path
import subprocess,tempfile,sys
root=Path(__file__).resolve().parents[2]
upstream=Path(sys.argv[1]) if len(sys.argv)>1 else root/'build/upstream'
s=(upstream/'src/battle_setup.c').read_text()
a=s.index('static void Task_BattleStart(u8 taskId)\n{');b=s.index('\nstatic void CreateBattleStartTask',a)
code=r'''
#include <stdbool.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
typedef unsigned char u8;
typedef short s16;
#define TRUE 1
#define tState data[0]
#define tTransition data[1]
struct { s16 data[16]; } gTasks[2];
bool poison,ready,done;
unsigned began,aborted,transitioned,cleaned,destroyed;
bool FldEffPoison_IsActive(void) { return poison; }
void Port_BattleCameraBegin(void) { ++began; }
bool Port_BattleCameraReady(void) { return ready; }
void Port_BattleCameraAbort(void) { ++aborted; }
void BattleTransition_StartOnField(int kind) { assert(kind==7);++transitioned; }
void ClearMirageTowerPulseBlendEffect(void) {}
bool IsBattleTransitionDone(void) { return done; }
void CleanupOverworldWindowsAndTilemaps(void) { ++cleaned; }
void CB2_InitBattle(void) {}
void SetMainCallback2(void (*callback)(void)) { assert(callback==CB2_InitBattle); }
void RestartWildEncounterImmunitySteps(void) {}
void ClearPoisonStepCounter(void) {}
void DestroyTask(u8 id) { (void)id;++destroyed; }
'''+s[a:b]+r'''
void Reset(void) {
 memset(gTasks,0,sizeof(gTasks));gTasks[0].data[1]=7;
 poison=ready=done=false;
 began=aborted=transitioned=cleaned=destroyed=0;
}
int main(void) {
 Reset();poison=true;Task_BattleStart(0);assert(!began && !transitioned);
 poison=false;
#ifdef PORT_BRIDGE
 for(unsigned i=0;i<30;++i) Task_BattleStart(0);
 assert(began==1 && !transitioned && !aborted);
 ready=true;Task_BattleStart(0);
 assert(began==1 && transitioned==1 && gTasks[0].data[0]==1);
 Task_BattleStart(0);assert(transitioned==1 && !cleaned);
 done=true;Task_BattleStart(0);assert(cleaned==1 && destroyed==1);
 Reset();ready=true;Task_BattleStart(0);
 assert(began==1 && transitioned==1 && !aborted); /* unavailable camera */
 Reset();for(unsigned i=0;i<59;++i) Task_BattleStart(0);
 assert(began==1 && !transitioned);
 Task_BattleStart(0);assert(aborted==1 && transitioned==1);
#else
 Task_BattleStart(0);assert(!began && transitioned==1);
 done=true;Task_BattleStart(0);assert(cleaned==1 && destroyed==1);
#endif
 puts("battle start task: one-shot gate, fallback, timeout and original GBA path passed");
}
'''
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'gate.c';p.write_text(code)
 for bridge in [False,True]:
  out=Path(tmp)/('port' if bridge else 'gba')
  args=['cc','-std=c99','-Wall','-Wextra','-Werror','-fsanitize=address,undefined']
  if bridge:args+=['-DPORT_BRIDGE']
  subprocess.run(args+[str(p),'-o',str(out)],check=True)
  subprocess.run([str(out)],check=True)
