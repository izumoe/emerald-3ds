# Cutscene camera prototype

Native cutscene callers include `ctr_voxel.h`. Call `CtrVoxel_PlayCameraDemo()`
for a gentle establishing pan, push-in and automatic return (6.75 seconds at
60 rendered frames per second). This is a callable example, not a replacement
for any existing story scene. Input locking and dialogue timing belong to the
caller. Poll `CtrVoxel_CameraPlaying()` for completion. A rejected start returns
false and changes nothing.

For custom shots, pass up to eight `VoxelCameraShot` entries to
`CtrVoxel_PlayCamera(shots, count, returnFrames)`. Entries are copied. Positions
are offsets from the gameplay camera target at start, clamped to +/-3 tiles;
zoom is distance relative to gameplay, clamped to 0.50..1.20. Pitch offset is
clamped to +/-8 degrees and absolute pitch to 30..55. Yaw and FOV stay unchanged.
Each shot eases from the preceding shot over `move` frames then waits `hold`
frames. Durations are rendered frames, so slowdown lengthens the sequence.
The last phase eases to the live gameplay camera, which continues following
the player independently. Non-finite values, zero movement/return duration,
and durations above 3600 are rejected.

Map changes, battles, parking and 2D swoops cancel immediately to gameplay;
manual abort uses `CtrVoxel_CancelCamera()`. No extra rendering passes or GPU
allocations are introduced. Streaming follows the shot target while active.

This prototype has no GBA script opcode, orbit or UI controls. It needs in-game checks for terrain
occlusion, streaming, sprite framing and stereo comfort. The existing blur
keeps its fixed focus band; it does not track the shot subject.

Host check: compile tests/voxel_director_test.c and src/voxel/voxel_director.c
with -Isrc/voxel -lm, or run make verify-voxel-director in a configured tree.

## Validation so far

The host sequencer check passes, including invalid input, bounded movement,
shot holds, restart rejection, live return and cancellation. The existing
voxel runtime and overlay depth checks also pass. A container with the official
devkitPro/devkitARM toolchain compiles and links the new code.

`CTR_TEST_CAMERA` is an optional capture-only game hook: it starts a new game
at frame 200 and plays the example once after 180 unlocked field frames. It
does not save. A recording setup can additionally change the generated upstream
new-game spawn to Oldale and omit the truck callback; those temporary upstream
changes are not part of this feature patch.

## NPC conversations

Direct NPC dialogue in the voxel overworld automatically frames the two speakers.
It eases for 54 rendered frames towards their midpoint, with a small southward
framing offset to leave room for the dialogue box, and a 15 percent dolly in.
Pitch and yaw stay steady. It holds while the player reads, including waits
and choices, and returns over 60 frames once the script releases field controls.
Early dismissal returns from the current displayed pose.

Signs and narration without a selected NPC are excluded. Only speakers within
two map tiles are eligible, so unrelated distant objects cannot pull the camera.
An active authored shot has priority. Set camera_dialogue=0 in settings.txt
to disable the automatic conversation framing. Moving story scenes and changes
of speaker during one locked script still need authored shots; this first pass
keeps a fixed two-person composition until the script releases control.

The optional CTR_TEST_CAMERA capture now invokes the real Oldale girl NPC script.
Its isolated capture tree spawns the player next to her at (15,11). This replaces
the earlier roaming camera demo in capture builds, and dismisses text through
the normal A-button path after a reading hold.

## Important dialogue staging preset

Ordinary dialogue defaults to 15 percent closer. Important dialogue uses one
90-frame (1.5 second at 60 Hz) easing motion: pan to the two-person composition,
dolly 20 percent closer and tilt +4 degrees concurrently. All components share
one progress value and start and finish together. There is no intermediate pose
or mid-move pause. It then holds still for reading and returns on script completion.
The earlier two-stage pan/push preset is superseded by this concurrent motion.

Settings: camera_dialogue_push=0..20 overrides the default dolly for either
style; camera_dialogue_style=0 forces steady framing, 1 selects a preliminary
character-based story preset, and 2 forces the story preset for comparison.
The prototype default is 1. Aqua and Magma grunts, Archie, Maxie, Steven, Birch,
Wally, Scott and the rival select the story preset, resolving variable graphics.
camera_dialogue_tilt=0 disables tilt. This identity heuristic is a staging aid,
not individual direction of every story scene.

The story path is sampled at 12-frame intervals, checking both sides of each
speaker's head and their torso against scenery. Rays sample at 1/32 tile using
the lighting module's terrain, building, tree and prop proxies. A blocked tilted
path tries the same shot without tilt; a blocked or unknown remaining path
leaves the gameplay camera unchanged. Missing lighting visibility support also
fails closed. This is a sampled proxy check, not pixel-perfect GPU visibility;
it does not include moving characters or continuously recheck during the hold.
It still needs hardware timing and occlusion checks in actual authored scenes.

Per-scene direction remains to be authored: speaker targets, reaction shots,
pause/choice timing, actor movement, battles and return cues. The preset is a
reusable vocabulary to build on, not a substitute for those script beats.
The 15/20 comparison previews use the same real Oldale NPC dialogue, with the
story style forced for the second take; they do not depict an authored grunt
or major story encounter.

## Scenic scripted scenes

The Oldale shop employee is now authored using real event camera macros. See
cutscene_scripts.md for commands, the walking example and limitations. The
director now interpolates yaw too; authored shots can track the selected pair
using live sub-tile positions. Routine conversation presets remain north-facing.
