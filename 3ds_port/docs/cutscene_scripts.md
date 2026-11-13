# Scripted camera scenes

For shot choices, composition and pacing, see the
[camera scripting lookbook](camera_lookbook.md).

The Oldale Mart employee's first guided walk is the first authored scene.
Direction lives in the existing event-script language, not C++ or a second VM.
Patch 0083 adds macros backed by eight C specials in 3ds_game_full.c. Camera math
and actor tracking stay in the voxel modules. The story's original text, actor
movement, item grant and flags remain in its script.

The polished scene uses this pattern (actual macros, excerpted):

```asm
camera_pair LOCALID_PLAYER, LOCALID_OLDALE_MART_EMPLOYEE
camera_follow TRUE
camera_offset -6, 0
camera_move 72, 110, -6, -28
waitcamera

@ The greeting starts as the camera eases closer.
camera_move 84, 70, -8, -22
msgbox OldaleTown_Text_CameraGreeting, MSGBOX_DEFAULT
msgbox OldaleTown_Text_CameraInvitation, MSGBOX_DEFAULT
closemessage

@ Camera and actors start moving together.
camera_offset 4, 6
camera_move 120, 102, -6, -28
applymovement LOCALID_OLDALE_MART_EMPLOYEE, OldaleTown_Movement_EmployeeNorth
applymovement LOCALID_PLAYER, OldaleTown_Movement_PlayerNorth
waitmovement 0
waitcamera

@ Compose the landmark, and let the employee look at it.
camera_offset 0, -20
camera_move 96, 112, -4, -30
applymovement LOCALID_OLDALE_MART_EMPLOYEE, OldaleTown_Movement_CameraLookAtMart
waitmovement 0
waitcamera
msgbox OldaleTown_Text_CameraBlueRoof, MSGBOX_DEFAULT
faceplayer
@ Goods return to a front view, then the promotion starts a slow orbit.
camera_offset 0, 4
camera_move 90, 70, -8, 0
@ ... original goods page ...
camera_offset -4, 4
camera_orbit 420, 80, 4, 150
@ ... original promotion page and item exchange ...
@ The original item, follow-up text and flags stay in the full script.
camera_return 90
waitcamera
camera_end
```

The full scene retains the original direction branches, dialogue pages,
Potion grant, inventory-full branch and release commands. The example above
shows the north-facing route used for the recording, not a replacement for all
those script branches.

## Commands

- `camera_pair a, b`: select two current-map local actor IDs; `LOCALID_PLAYER`
  is the player. Selection disables follow until explicitly enabled.
- `camera_move frames, distance, pitch, yaw`: one concurrent eased move to the
  selected pair. Distance is 50..120 percent of the independent gameplay camera
  distance, so 90 is 10% closer. Pitch is an offset of -8..8 degrees from gameplay
  (absolute camera pitch remains 30..55); yaw is -30..30 degrees from gameplay.
  Reframing always uses the gameplay baseline, avoiding compounded zoom.
- `camera_orbit frames, distance, pitch, heading`: the same concurrent move,
  with heading 30..150 degrees (90 is the front view). The Potion offer uses
  `camera_orbit 420, 65, 4, 150`: seven seconds, 35% closer, downward tilt
  and a 60-degree orbit from the preceding front view.
- `camera_offset x, z`: compose relative to the selected pair, in sixteenths
  of a world tile, clamped to +/-32 (two tiles). Positive z looks south;
  negative z composes towards the landmark north of the pair. Set before the
  next move; selection resets the offset. The same offset follows the actors.
  After `camera_anchor`, it also offsets a scenic target; each new anchor
  resets it. This allows framing between tile centres.
- `camera_height height`: aim above the actors’ ground, in sixteenths of a
  tile (0..24). Set after `camera_pair` and before a move; selecting a new pair
  resets it. This changes the look-at height, not terrain height. A queued
  `camera_reveal` retains the selected height across the transition. Try 8
  (half a tile) for a close dialogue, and check heads, feet and the text box.
- `camera_light radius`: set a minimum *visual* light-pool radius in dark
  voxel scenes, in game pixels (0..160), for the selected pair. It eases in
  with the shot and does not change the puzzle flash level. Selecting a new
  pair clears it. Use sparingly when darkness would hide a speaking character.
- `camera_follow TRUE` / `FALSE`: smoothly follow the pair as their sprites
  walk, or freeze the current tracking offset. Positions use the same sub-tile
  movement interpolation as their billboards, followed with a small damping.
- `waitcamera`: yield until the move or return finishes. A reading hold is
  still active at arrival, so waiting does not deadlock on an open dialogue.
- `camera_return frames`: ease from the displayed pose to the live gameplay
  camera, including undoing yaw. Pair tracking stops during this return.
- `camera_end`: release script ownership. It also requests a default return if
  the author omitted one. Releasing field controls likewise restores gameplay;
  leaving the overworld cancels the camera.

These macros use temporary variables 0x8004..0x8009. Do not keep scene values
in those variables across camera commands. Existing script opcodes (`setvar`,
`special`, `waitstate`) are reused, so the script bundler needs no new opcode.
`PORT_BRIDGE` guards the macros, specials and scene additions. A vanilla GBA
build keeps the original shop scene. In a 3DS build with the voxel renderer
unavailable, camera commands fall back without blocking the story.

## Visibility and scope

An authored move preflights the same eased path it will display against scenery
proxies and skips a blocked or unknown shot. Current authored pair shots assume
both actors stand at roughly the same ground height (within a quarter tile).
The walking hold tracks interpolated positions but does not yet continuously
recheck occlusion. Roofs, thin props, missing model sides, other moving actors
and all dialogue approach directions still need scene-by-scene visual review.
The existing tilt-shift focus band remains screen-based.

Angular composition and tracking are previewed in Oldale. This is the first
small script framework and scene, not directed versions of the entire story.
Real 3DS performance and stereo comfort still need testing, and visibility
preflight still needs a hardware time budget. Optional capture builds use
CTR_TEST_CAMERA plus CTR_TEST_SHOP_CAMERA, an isolated new game beside the
employee, and normal A pulses only while field controls are locked. They do not
write a save. Capture-only spawn and truck-skip edits are not in patch 0083.

## Polished shop direction

The original greeting and Mart explanation are split at their existing page
boundaries so camera cues can follow the words. An exact-text check confirms
all five pages retain their original wording and line breaks. The travel route,
Potion grant, flags and inventory-full path are preserved. One new in-place
turn lets the employee look at the blue roof before facing the player again.

The six camera moves are: wide establish; greeting push; concurrent walking
follow; blue-roof reveal; goods reframe; promotion close-up. The shot holds for
reading and returns after the item exchange. Soft 8-pixel letterboxing fades
in over 24 rendered frames, stays outside the dialogue window, and fades away
on return. Set camera_cinema_bars=0 in settings.txt to disable it. No extra
render target is needed.

## Advancing dialogue during a move

Ordinary A presses advance text without stopping or restarting the active move.
A later camera cue retargets from the displayed pose, without queuing the old
endpoint. Easing restarts, so position is continuous but velocity can change.
Scene cleanup returns from the current pose, including an unfinished orbit.
Only explicit `waitcamera` commands gate progression; the Potion orbit has no
wait before its dialogue. A fast reader may therefore see only part of the arc.

Capture builds can set camera_test_spam=1 to pulse A every eight frames instead
of ninety, while field controls are locked. This setting has no effect in a
normal build.

## Camera-relative character sprites

Standard NPC and Brendan/May on-foot standing and walking animations now select
art relative to camera yaw. Gameplay direction, collision, script turns and
movement are unchanged. The renderer reads the corresponding animation command
at the same phase and uses its horizontal flip, so the walk cycle continues.

Four views switch at 50 degrees from the current view and switch back at
40 degrees, giving a ten-degree hysteresis band around the 45-degree boundary.
This is a discrete sprite change; there are no diagonal frames or blended art.
At the Potion orbit's 60-degree endpoint the employee and player use opposite
side views, then return to their front/back views during camera cleanup.

The first version supports the exact Standard and BrendanMayNormal animation
tables, groups 0..19 (standing and four walk speeds). Running, bikes, fishing,
surfing, affine sprites, props, custom tables and special poses retain their
normal game art. Alternate pixels are used only when the existing asset cache
has them resident; missing data falls back to the regular sprite without doing
storage I/O from the renderer. Nearby map object sheets already use the asset
read-ahead worker. Reflections use the same atlas as their characters.

Patch 0084 exposes a read-only capability query from the game engine; the view
mapping and atlas substitution live in the port. The camera script syntax and
existing scene timing are unchanged.

## Scenic city sequences

Patch 0085 adds `camera_scene`, `camera_anchor x, y`, and
`camera_view frames, distance, pitch, yaw`. Anchors are current-map tile
coordinates. Scenic pitch (30..55 degrees) and yaw (-60..60) are authored
absolute angles; distance (50..180 percent) uses the independent gameplay
camera distance. Each view starts at the displayed pose, so consecutive views
form a dolly/flyover path; a one-frame view cuts to its destination instead.
FOV remains fixed. Dialogue framing limits remain
unchanged.

```asm
lockall
    setvar VAR_TEMP_7, 0
    @ Let the arrival fade and initial scenery settle before taking control.
    delay 60
    camera_scene
    @ Open high over the entrance. One rendered frame establishes the view.
    camera_anchor 16, 45
    camera_view 1, 150, 55, -30
    waitcamera
    @ Descending orbit: angle, pitch and distance ease together onto the Mart.
    camera_view 180, 105, 35, 20
    waitcamera
    @ Lock off the Mart composition for two seconds; no camera movement.
    camera_hold 120
    @ Cut to the Gym, then carry the motion through Devon.
    camera_anchor 27, 19
    camera_view 1, 140, 45, 20
    waitcamera
    camera_anchor 27, 18
    camera_view 90, 130, 42, 25
    waitcamera
    camera_anchor 12, 15
    camera_view 180, 140, 45, -20
    waitcamera
    @ Climb back over the boulevard before descending towards the player.
    camera_anchor 18, 48
    camera_view 180, 150, 50, 0
    waitcamera
    camera_return 120
    waitcamera
    camera_end
    releaseall
    end
```

The Rustboro example opens high, orbits down onto the Mart, holds the blue
roof composition still for two seconds, cuts to the Gym, travels through Devon, then climbs into a
flyover back towards the player before restoring gameplay. The opening
`camera_view 1` establishes a high pose in one rendered frame; the remaining
moves take roughly fourteen and a half seconds at 60 Hz. It runs once on a first visit through the
southern entrance. The transition arms VAR_TEMP_7 only when the existing
FLAG_VISITED_RUSTBORO_CITY was unset and the arrival y is at least 52; the normal
transition still sets that visited flag. Existing saves with the city visited,
other entrances and repeat visits therefore skip the introduction. No new
persistent save flag is allocated. The on-frame script consumes the temporary
latch, locks field controls and lets the arrival fade settle for 60 frames.

B during `camera_scene` skips the whole sequence: return from the displayed
pose over 36 frames, then subsequent view/return commands become no-ops until
`camera_end`. Explicit waits resume after that short return, and the map script
releases controls. This skip behavior applies only to scenic sequences, not
ordinary conversations. Map/battle/renderer cancellation still releases camera
ownership through the existing lifecycle. Unavailable rendering or rejected
views do not block the story. Scenic views fall back when the lighting/scenery
proxy module is compiled out.

One-frame scenic views are cuts and validate the destination eye. Longer
scenic moves validate map bounds and sample the eye's swept path against the
existing terrain/scenery proxies before starting. Unlike dialogue shots, they
do not require a line of sight to a character: a landmark may legitimately
occlude part of the street. This is not a guarantee of complete scenery or
frame-perfect visibility. Streaming continues around the displayed camera;
wide views and fast travel need visual review and real hardware testing.
The live gameplay camera keeps updating independently, so cleanup restores the
player's angle and zoom, including changes made during the sequence.

### Static shots

`camera_hold frames` holds the exact displayed pose without changing its map
anchor, angles or distance. Call `waitcamera` after the arrival move, then
`camera_hold 120` for a two-second static composition. World animation keeps
running. Unlike a plain event-script `delay`, the hold participates in scenic
skip handling: B clears its timer and performs the short camera return.
The timer is bounded to 3600 game frames; it counts down after any current move
lands. Leaving camera ownership clears the timer so an interrupted script does
not keep a stale camera wait. A normal scene uses one map event script for all
shots; the macros invoke native C specials and reuse Emerald's waitstate.

## Early story interactions

Patch 0086 adds authored directions to Route 101's Birch rescue and Route 103's
first rival encounter. No new camera command is required.

Birch starts with the off-screen call for help framed around the entrance.
The camera moves towards the action with the actors, then follows the Birch /
Zigzagoon pair during the existing chase. Tracking stops and the view settles
before his plea. The bag cue uses the original text's page break, pans towards
the bag, and restores gameplay before field controls are released. Starter
selection and the rescue battle are separate existing interactions and remain
unchanged by this scene patch.

The Route 103 rival opens in a wider angled composition, reframes during the
turn and recognition, then pushes 15% closer with a small orbit for the battle
challenge. The shared battle-start rule takes over the displayed challenge pose and
pushes into the battle transition without returning to gameplay first.
The post-battle dialogue begins with a fresh wider pair shot; the departure
camera selects the player alone and pushes to 80% distance while the rival
walks out of frame. A northward two-tile composition offset keeps the rival
fully beyond the lower edge at the end of the walk. It holds for 45 frames, removes the rival off-screen, then
returns before the remaining story flags are changed. Both May and Brendan branches and all six starter-dependent
battle branches retain their original logic.

Dialogue views remain held until another cue or cleanup. Ordinary advancement
retargets from the displayed pose; short explicit waits finish important arrival
or return moves. There is no scenic B-skip across these story conversations.
Movement paths, text, flags, rewards and battle opponents are preserved. As
elsewhere, unknown/blocked pair views fall back instead of blocking the script;
walking visibility still requires scene review.

`tests/early_story_scripts_test.py` compares the unported scripts, original
story-action order, rival text and exact Birch page split against the baseline
recovered from patch 0086. Run it after bootstrap, or pass an upstream tree.
Optional isolated captures reuse CTR_TEST_CAMERA / CTR_TEST_CITY_CAMERA with
camera_test_early=1 (Birch) or 2 (rival). The rival capture gives a level-20
Treecko solely to shorten the real battle. Capture-only spawn/intro edits live
in the temporary upstream tree and are excluded from the feature patch.

## Shared battle transition push

Patch 0087 hooks the engine's common overworld Task_BattleStart path, used by
normal wild and trainer battles. It requests the push once after the existing
poison-effect gate, waits for it to land, then starts the stock field battle
transition. A 60-game-frame watchdog prevents a stalled renderer blocking the
battle. Unavailable/unsafe framing falls back immediately to the original flow.
The GBA path is guarded out with PORT_BRIDGE.

The native push begins at the displayed pose, keeps its angles and FOV, and
moves over 30 rendered frames (nominally half a second). A current trainer may
supply the pair midpoint; otherwise the target is the player. The target
distance is min(current distance, gameplay distance * 0.80), so an existing
close shot is never zoomed out or multiplied into a larger push. The settled
pose remains owned through CB2_OverworldBasic while the stock field effect
plays; ownership clears on leaving the field under that effect. Special flows
that bypass the common field task are outside this hook.

`tests/battle_camera_gate_test.py` runs the actual task with native stubs in
both port and GBA modes: one request per task, readiness, immediate fallback,
watchdog, poison gating and normal transition completion. The script wait
harness also checks that battle ownership survives the field effect callback
and clears when the battle starts.

## Woods, Roxanne and Wally

Patch 0088 adds the Petalburg Woods researcher/Aqua encounter, Roxanne's first
challenge and rewards, and Wally's Gym introduction / walk / catching tutorial /
return. Original battle opponents, rewards, movement routes and story actions
are retained. Roxanne's introduction is split only at its original page breaks;
the original trainerbattle_single and rematch handling remain in place.

Roxanne's first greeting adds a short stock `fadescreenspeed` fade to black,
sets the opening pose under black, then fades up. Challenge motion flows into
the shared battle push. The existing post-battle fade reveals the badge pose;
there is no extra fade between the badge fanfare and TM handoff. Bag-full and
repeat-visit branches clean up without replaying the introduction.

Wally's three-character indoor views are tighter and more downward-facing to
keep the adjacent Gym rooms out of the cinematic composition. The doorway pan,
request, loan and walk use normal actor movement. The outdoor walk crosses from
Petalburg into Route 102; actor references and a tracking camera rebase across
that connected-map boundary. The original catching battle and party save/load
remain intact. The existing Gym exit and return fades hide arrival poses.

New commands:

- `camera_reveal map, actor1, actor2, distance, pitch, yaw` queues a held actor
  composition for the next battle/map return to that destination. It uses source
  actors from the destination map, waits for the renderer's map cache to match,
  then requests a one-frame pose during the existing reveal. Patch 0089 briefly
  holds the existing black fade until that pose has rendered; it adds no second
  fade. A 60-frame fallback prevents waiting indefinitely. A wrong destination or 120-frame field timeout
  discards the request. The origin map may remain live during a warp; it is
  waited out rather than mistaken for a wrong arrival.
- `camera_pair_map actor1, actor2, source_map` selects retained actors by their
  original map IDs. The player remains LOCALID_PLAYER regardless of map. This
  avoids confusing Wally with a Route 102 NPC using the same local ID.
- `camera_reveal_selected map, distance, pitch, yaw` queues the currently
  selected (possibly foreign-map) pair for the next reveal.

These commands share scratch variables 0x8004..0x8009. Wally's original approach
branch uses 0x8008 across many calls, so each indoor helper saves it to otherwise
unused VAR_TEMP_E and restores it before returning. Do not remove that wrapper.

Following cameras now retain their director state on a genuine connected-map
crossing: anchor, start pose and tracked coordinates shift by the renderer's
existing map rebase. Warps and non-following scenes still cancel normally.
Indoor actor rays check the known room segment up to its front cutaway edge;
empty space beyond that south edge is allowed. Side exits, below-floor eyes,
unknown outdoor coverage and room obstructions still fail closed.

Isolated capture modes are camera_test_early=3 (Woods), 4 (Roxanne), 5 (Wally),
under CTR_TEST_CAMERA and CTR_TEST_CITY_CAMERA. Temporary spawn/intro setup is
excluded from the feature patch. The capture party shortens ordinary battles;
Wally's tutorial loads/restores the original scripted party.

Patch 0089 gates the engine FadeInFromBlack only when a matching queued reveal
is pending. It retains black palettes, leaves normal weather/script fade waits
blocked, and starts the original fade after the pose has had two frame boundaries
to render. Missing/disabled voxel rendering bypasses the gate; a 60-frame timeout
releases it safely. All other fades retain their original path. Palette-fade
`active` may be false during this short black hold; the reveal log's fade field
alone is therefore not evidence that a reposition was visible.

### Tighter dialogue framing

Authored dialogue uses 50–75% of gameplay distance, with Norman at 50% and Roxanne at 55%. Walking, entrances and establishing shots retain wider framing. The closer range is available to scripted shots and still uses the existing visibility checks; the adjustable gameplay camera remains the baseline. The shared battle cue preserves an already closer dialogue pose instead of pulling back to its 80% limit.

### Woods entrance and exit revision

The Woods opening uses 60% distance and the existing `hideobjectat`/`showobjectat` event commands inside `PORT_BRIDGE`: the grunt is hidden during the researcher chat, then shown before his original entrance movement. Both approaches restore him before the confrontation. Before each departure, the camera settles on the player alone at 60% distance with a one-tile southward target offset. Both the grunt and researcher then run north out of this held shot. The researcher view starts before his original walk, and stays held through removal; it no longer reframes after he has finished walking. The help/reward shots also use 60% distance, and the confrontation biases its target north to reduce crowding from the researcher behind the player. No story actor is removed early.

### Clear dialogue angles

Dialogue shots use authored three-quarter views (26–30 degrees to the side) rather than the player-to-NPC axis. The Woods researcher uses the left-side view, the grunt confrontation the right-side view, with a northward target bias to give the player and grunt more room. The departures retain a static, slightly angled player composition. Norman, Wally and Roxanne use the same angled two-shot approach; entrance/tracking views retain their original wider poses. The native visibility sweep still validates each eased path.

### Lower, closer Wally and Roxanne views

Wally/Norman dialogue uses `camera_orbit` headings 50/135 (40–45 degrees to the side), pitch offset -6 and 50% distance. Wally's entrance uses a following 60% shot at heading 125 (35 degrees), keeping it close as he walks in. Roxanne uses headings 42/138 (48 degrees), pitch -6 and 55% distance. Queued fade reveals use the orbit path as well, preserving these wider side angles under the existing visibility checks. At the capture gameplay pitch of 40 degrees, dialogue settles at 34 degrees. The detached upper Gym rooms may enter the background at these lower angles; the framing prioritizes the actors and close side view.

### Wally side artwork

The close Norman, Wally request and Pokémon loan shots orbit to heading 145 (55 degrees from the front), beyond the sprite quadrant's 50-degree hysteresis boundary. This makes the standard side artwork appear through the existing camera-relative direction mapping. Small one-tile lateral target offsets keep the camera on a clear path through the Gym. Actor facing/movement state is unchanged. The entrance remains at heading 125 so it can approach smoothly before the dialogue orbit.

Wally’s request and loan exchange stay on the speaker-facing side, showing his face over Norman’s shoulder. The player uses side artwork at this angle; Norman also uses side artwork while facing the player, then turns naturally as the original script addresses Wally.

## Rusturf rescue, Mr. Stone and Steven

Patch 0090 authors three more early story scenes with the existing commands:

- Rusturf Tunnel: close grunt/Peeko confrontation, queued post-battle reveal,
  held player shot for the grunt's escape, a softer Briney/Peeko reunion and
  another held player shot while both leave. The earlier backing-up taunt also
  has its own short camera cue and cleanup before controls return.
- Devon Corp 3F: employee greeting, a player hold while the employee leaves and
  returns, following dolly during the escort, then a desk-side orbit and slow
  push for the letter/PokeNav handover. The original healing fade remains.
  Actor 1 is the visible president; actor 3 is an invisible interaction proxy.
- Steven's room: a quiet paired side view for the letter and TM, a slow closer
  move for the Champion/registration dialogue, and a player-only hold while
  Steven follows his original exit route. The Letter handover keeps its
  original VAR_0x8004 assignment and call together, without camera scratch
  commands between them.

All camera commands are guarded by PORT_BRIDGE. The scene test compares the
entire original GBA output and all non-camera commands in the port, including
text, movement, rewards, flags, calls and warps. Capture modes 6/7/8 route to
Rusturf / the original auto-start Devon map script / Steven respectively, and
are compiled only with CTR_TEST_CITY_CAMERA. Temporary startup spawn/quest-flag staging is kept
outside the production source patch; test-only party/Letter setup is guarded
in the capture helper.

Cave camera visibility now clips only the segment beyond the finite map’s front edge, as for indoor cutaways. Terrain inside that edge is still traced; side exits, below-floor paths and obstructed known segments remain rejected. The reveal/cutaway harness covers both room and cave cases. Rusturf’s reunion first reframes using the still-visible player, then selects Briney and Peeko once the view clears the foreground ledge. This avoids asking a new subject to be visible from the earlier escape shot.

Scripted visibility probes now use the actor's rendered upright billboard bounds:
cell centre, relief/model push, standing foot trim and opaque sprite height. The
base transform is shared with EmitBillboard, keeping the checks aligned with
what is drawn. This matters on cave ledges and for mixed-size pairs such as
Briney and Peeko. Cached art must match the active object; missing or stale bounds
reject the move. The bounds harness exercises centre/push/deck transforms,
human/Pokemon heights, 4/8-bit pixels, flipped frames and invalid cache guards.

## Littleroot opening and lab pass

The moving-in scene selects the player and Mom before the gender-specific
wrapper initializes `VAR_0x8004` and `VAR_0x8005`. The shared event uses those
variables for its original facing and movement calls, so it does not issue
camera commands again until those uses are complete. The camera then returns
before the event releases control. Both house variants preserve their original
commands; the Brendan-house capture is the visually reviewed setup.

The lab starter handover frames Birch and the player, then reselects them after
the nickname branch because naming leaves the overworld. The Pokédex handover
shifts focus from Birch to the rival after the rival approaches. Gender checks
and conditional item calls remain adjacent. These additions are guarded by
`PORT_BRIDGE`; the original dialogue, choice branches, gifts and flags remain.

The Route 101 chase and plea use closer framing. The Route 103 rival scene uses
stronger side angles to separate the actors and retains the held player view for
the departure. Test captures use isolated scene setups, not a continuous save;
other approaches, the May-house view and nickname/skip branches still require
visual review. Small rooms can expose unmodelled space at their edges.

The lab conversation uses 1,320-frame (about 22 seconds at 60 fps) lateral
and orbital moves during the starter and Pokédex dialogue. The Pokédex framing
uses offsets to centre the three-person group, then shifts its target toward the
rival and drifts during the Poké Ball offer.
These are continuous camera moves; the renderer does not implement a true
crossfade between live views. The cues are allowed to be interrupted by dialogue
advances and the next cue starts from the displayed pose.
