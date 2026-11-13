# Main story camera checklist

Working inventory for Pokémon Emerald's main story, from moving to Littleroot
through the Hall of Fame. A checked story-scene box means its core camera pass
has been scripted and recorded, or its creative prototype was accepted. It is
a progress marker, not final sign-off: alternate approaches, scene branches,
transitions, updated geometry and hardware still need the review listed below.
Unchecked entries may still contain partial scripts or recordings. Area-reveal
boxes separately track a usable arrival sequence, including its trigger.

**Environment** is tracked independently of camera work:

- **Captured 3D**: the named scene or location was recorded with the voxel
  renderer; its exact coverage and alternate angles still need review.
- **Assets exist**: model definitions exist for at least some features in the
  area. This does not establish that the specific shot, interior or whole map
  is modelled or complete.
- **Check**: scene-specific 3D coverage has not yet been established here.
  Inspect the actual map and its relevant story state before planning a shot.

Many towns, routes and interiors are only partly modelled; consult the
map-by-map [voxel status](../../docs/VOXEL_STATUS.md) for known coverage and
faults. A flat or partly modelled scene may still support a useful composition.
Record what is missing before assigning art work. Proposed treatments are
ideas, not final direction. Consult the
[camera lookbook](camera_lookbook.md) and [script reference](cutscene_scripts.md).

## Integration and verification

The camera branch and the selected upstream geometry fixes are on the fork's
`main`. Their inclusion does not by itself approve a shot or prove the updated
models in game. Recordings made before the geometry merge describe the earlier
model state and should be revisited where the scenery changed.

- [x] Integrate the camera work and the selected upstream interior and
  underground-border fixes into the fork's `main`. See the
  [upstream PR review](../../docs/UPSTREAM_PR_REVIEW.md) for included and
  deferred work.
- [x] Run the fork's voxel runtime, draft, ground, sign, tree and lighting
  host checks on the integration branch.
- [ ] Complete the full 3DS build and scenery generation/verification after
  the geometry merge. The long-running generator was still in progress at
  the last check; record its final result before treating it as a pass.
- [ ] Recheck affected camera shots with the updated geometry, especially
  the Elite Four rooms, Weather Institute and underground locations. Confirm
  battle returns, dynamic doors, actor visibility and safe orbit paths.
- [ ] Review representative scenes on console, including stereo and the
  player's adjustable camera settings. Emulator captures do not establish
  hardware acceptance.
- [ ] Fix the existing web-builder fixture failure involving missing generated
  region data, then rerun the builder suite. It also reproduces before the
  upstream PR integration.

## Littleroot to Rustboro

First-pass direction approved for now. Checked boxes mark that creative pass;
the modelling, alternate-branch and hardware notes remain open follow-ups.

- [x] **Move to Littleroot and meet Mom** — Player's house / Littleroot. Camera:
  moving-in conversation prototype recorded for Brendan's house; remaining intro
  beats and May's house need review. Environment: Littleroot building **assets
  exist**; Brendan's house **captured 3D**, with exposed room edges. Establish home and the journey's start.
- [x] **Birch's rescue and starter choice** — Route 101 / Birch's lab. Camera:
  Route 101 rescue and lab starter handover prototypes recorded; starter selection
  UI remains original. Environment: rescue and the shown lab setup **captured
  3D**; other views **check**. Give the cry for help, chase
  and first partner choice distinct beats.
- [x] **Oldale Mart employee and Potion** — Oldale Town / Mart exterior.
  Camera: greeting, walk, static Mart reveal and promotion orbit scripted and
  recorded. Environment: shown street and Mart **captured 3D**. Recheck sprite
  facing, quick dialogue advancement and the inventory-full branch.
- [x] **First rival battle and Pokédex** — Route 103 / Birch's lab. Camera:
  Route 103 rival and lab Pokédex exchange prototypes recorded. Environment:
  Route 103 and the shown lab setup **captured 3D**. Hold the player's view
  for the rival's departure; use the shared battle push.
- [x] **Norman, Wally and the catching lesson** — Petalburg Gym / Route 102.
  Camera: introduction, walk and lesson prototype recorded. Environment:
  **captured 3D** for the shown setup. Review all entrance branches and the
  handoff into and out of the tutorial.
- [x] **Devon researcher and Aqua grunt** — Petalburg Woods. Camera: prototype
  recorded, including battle and departures. Environment: **captured 3D**.
  Check both approach paths and the hidden-then-revealed grunt.
- [x] **Roxanne** — Rustboro Gym. Camera: greeting, battle transition and
  rewards prototype recorded. Environment: **captured 3D** for the shown
  approach. Review alternate approaches and fade/return.
- [x] **Rusturf rescue** — Rusturf Tunnel. Camera: confrontation, battle
  return, Peeko reunion and departures prototype recorded. Environment:
  **captured 3D**. Review alternate approaches and all exits.
- [x] **Mr. Stone's first meeting** — Devon Corp 3F. Camera: employee escort,
  desk orbit and PokéNav push prototype recorded. Environment: **captured 3D**.
  Review the complete meeting and healing fade.
- [x] **Rustboro city introduction** — Rustboro. Camera: multi-shot city
  prototype recorded. Environment: **captured 3D**; building assets exist.
  This is the same prototype tracked in Area reveals below; the checked box
  records its approved creative pass, not an implemented arrival trigger.
  Establishing orbit, static Mart, Gym/Devon and return flyover. Optional
  arrival treatment; decide when it should play and how it is skipped.

## Dewford, Slateport and Mauville

The core encounters below have staged emulator recordings. Alternate shots,
branches and transitions remain open review work even where a core pass is
checked.

- [x] **Mr. Briney's first voyage** — coast / boat / Dewford. Camera: the
  offer, boarding, boat-follow and scenic dock arrival are scripted and recorded,
  including Norman's call. Tracking crossed a connected-map seam in the staged
  run, and the arrival returned to gameplay. The close actor shot was rejected
  by dock visibility checks; the recorded arrival uses a scenic cut instead.
  Review the no-call and repeat-travel branches, other camera settings, water
  edges, and Dewford building coverage. Boat route and dock **captured 3D**.

- [x] **Steven and the Letter** — Granite Cave, Steven's room. Camera: exchange
  and exit prototype recorded. Environment: **captured 3D** for the shown
  approach. Check alternate approaches and the return to the cave camera.

- [x] **Brawly** — Dewford Gym. Camera: introduction and battle return recorded.
  Environment: **captured 3D** for the shown darkness state; check others. Frame
  the introduction and shared battle transition.

- [x] **Captain Stern and the Oceanic Museum** — Slateport harbor / museum.
  Camera: museum confrontation and battle returns recorded; harbor and alternate
  states need review. Environment: museum **captured 3D** for the shown setup;
  harbor **check**. Stage the delivery, Aqua confrontation and Archie's
  introduction.

- [x] **Rival on Route 110** — Route 110. Camera: staged encounter and departure
  recorded; alternate approaches need review. Environment: **captured 3D** for
  the shown approach. Give the meeting and battle a clear two-shot and
  transition.

- [x] **Wally challenges the Gym** — Mauville Gym exterior. Camera: staged
  encounter and departures recorded. Environment: **assets exist** for some
  Mauville buildings; exact scene **check**. Stage Wally, his uncle and the
  player, including the battle and farewell. Wally's uncle is present here;
  Norman is not part of this scene.

- [x] **Wattson** — Mauville Gym. Camera: first battle and reward recorded;
  alternate approaches need review. Environment: **check** interior and puzzle
  state. Introduce Wattson and the battle.

## Meteor Falls to Fortree

First-pass scripts include battle handoffs and character departures. The
Meteor Falls/Mt. Chimney, Flannery/gift, Weather Institute and Route 119 rival
entries remain open because an important shot is rejected, obscured or needs
recomposition. Checked scenes still need branch and transition review.

- [ ] **Meteor Falls and Mt. Chimney** — Meteor Falls / cable car / Mt. Chimney.
  Camera: Meteor Falls confrontation recorded. A revised Mt. Chimney pass cuts
  between two scenic angles for Maxie, returns to the crater after the battle,
  and cuts to Archie; one staged approach was recorded. A closer, more angled
  pass uses 50–55% scenic distance, 34° pitch and headings up to 50° to either
  side; its scenic views play in the staged approach. The Archie shot targets
  the row where the characters finish walking; a staged retest centers them
  above the dialogue box. Mountain seams remain visible and
  the shared battle push and queued actor-focused reveal are rejected by
  visibility checks. The summit uses hand-marked terraces, but the engine mesh
  scan still finds crater holes; the meteorite machine remains flat. Test both approaches,
  rapid dialogue, other camera settings, stereo and hardware; investigate the
  terrain. Cable car still needs direction. Environment: summit **captured 3D**
  for the staged view; **check** other maps and villain-team states.

- [ ] **Flannery and the Go-Goggles** — Lavaridge Gym / town. Camera: first
  battle recorded, but heavy steam obscures the shot. The rival gift completes
  in gameplay view after the terrain check rejects the close camera. Both a
  normal scenic anchor and a closer scenic test were rejected as well; the
  experiments were discarded and the safe fallback remains. Environment:
  **assets exist** for the shared Gym exterior;
  Gym interior and rival scene **check**. Separate the victory from the gift.

- [x] **Norman's Gym battle and Surf** — Petalburg Gym / Wally's house. Camera:
  battle, post-battle exchange and Surf gift recorded. Environment: both
  rooms **captured 3D** for the shown setups; review alternate entrances and
  the transition to the house.

- [ ] **Weather Institute takeover** — Route 119 / Weather Institute. Camera:
  administrator and rescue scripted; battle transition and return recorded.
  A staged retest after the interior fixes shows a black floor gap beneath the
  player on the battle return and throughout the rescue dialogue. Investigate
  the room's floor geometry before approving the shots. Environment: interior
  **captured 3D** after the geometry merge; the exterior building remains flat.
  **Check** weather and alternate approaches.

- [ ] **Route 119 rival battle** — bridge south of Fortree. Camera: opening
  angle and revised battle return recorded. The battle push is rejected by the
  terrain check, and alternate approaches need review. Environment: **captured
  3D** for the shown approach. Keep the player framed as the rival departs.

- [x] **Steven and the unseen obstacle** — Route 120. Camera: encounter
  recorded through the Kecleon reveal, battle return and departure. Environment:
  **captured 3D** for the shown setup; review alternate approaches and choices.
  The 3D renderer suppresses the bridge shadow to preserve the surprise.

- [x] **Winona** — Fortree Gym. Camera: first battle and reward recorded;
  alternate approaches and puzzle state need review. Environment: **check**
  exterior, interior and puzzle state. Establish her introduction and battle.

## Lilycove to the weather crisis

Lilycove, Mt. Pyre and the twins have staged emulator captures. Several
other encounters have partial scripts but still need major story beats;
checked captures also need branch, model and hardware review.

- [x] **Lilycove rival farewell** — Lilycove Department Store exterior. Camera:
  conversation, battle return and held departure recorded. Environment:
  **captured 3D** for the shown approach; check alternate interactions.
- [x] **Mt. Pyre and the stolen orbs** — Mt. Pyre summit. Camera: first pass.
  Environment: summit **captured 3D** for one staged approach, with heavy fog;
  check other approaches. The confrontation and explanation are recorded.
- [ ] **Magma Hideout at Mt. Chimney** — hideout / Groudon chamber. Camera:
  first Maxie battle script; awakening needs direction and visual review.
  Environment: **check**. Stage Maxie's awakening attempt, battle and
  Groudon's departure, with clear views of the legendary Pokémon.
- [ ] **Slateport submarine theft** — harbor. Camera: Stern and Archie dialogue scripted. Environment: **check** harbor
  and submarine; check all four approaches and the escape. Stage Stern, the crowd, Archie and
  the getaway as a short sequence.
- [ ] **Aqua Hideout** — Lilycove hideout / submarine bay. Camera: Matt's battle
  scripted. Environment: **check** interiors and moving actors; submarine
  escape composition still needs review. Build toward the
  administrator encounter and submarine escape.
- [ ] **Mossdeep Space Center** — Space Center. Camera: Steven's initial
  dialogue scripted. Environment: **check** exterior, interiors and team
  positions; the multi-battle and aftermath need direction. Introduce the
  attack, Steven's partnership and the battle with Maxie and Tabitha.
- [x] **Tate and Liza** — Mossdeep Gym. Camera: group shot and battle return
  recorded for one approach; the one-Pokémon branch keeps the original view.
  Environment: shown platform **captured 3D**, but most of the room appears
  black and needs modelling; review the other speaking position and puzzle.
- [ ] **Seafloor Cavern** — cavern / Kyogre chamber. Camera: Archie battle
  scripted. Environment: **check** underwater approach and chamber; the
  awakening retains the original camera and needs direction. Stage Archie,
  Kyogre's awakening and the transition to the weather crisis.

## Sootopolis and the League

Juan, Victory Road Wally, Sidney and the Champion sequence have staged
emulator captures. The Elite Four entry remains open as a group because only
Sidney was recorded; legendary sequences, other League rooms, transitions and
branches still need review.

- [ ] **Weather crisis and Sootopolis confrontation** — routes / Sootopolis.
  Camera: Steven's escort scripted; legendary confrontation needs direction.
  Environment: **assets exist** for some Sootopolis buildings;
  weather effects, legendary actors and exact viewpoints **check**. Establish
  the abnormal weather, Groudon and Kyogre, then Wallace and Steven.
- [ ] **Cave of Origin and Sky Pillar** — Cave of Origin / Sky Pillar summit.
  Camera: Cave of Origin and Sky Pillar Wallace dialogue scripted; original
  shake and camera effects retained. Environment: **check** both interiors
  and summit. The underground-border fix is merged but needs visual review
  on the affected Sky Pillar floors. Give Wallace's request and Rayquaza's
  awakening distinct beats; preserve player control on the climb.
- [ ] **Rayquaza and the aftermath** — Sootopolis. Camera: plan. Environment:
  **check** crisis and restored-weather states. Give the descent, confrontation,
  departure and leaders' reactions room to read.
- [x] **Juan** — Sootopolis Gym. Camera: introduction, battle return and reward
  recorded for one approach. Environment: **captured 3D** for the shown setup;
  review the puzzle state and alternate approaches.
- [x] **Wally's last challenge** — Victory Road. Camera: entrance challenge
  and battle return recorded with the side angle. Environment:
  **captured 3D** for the shown approach; check the other approach and flags.
- [ ] **Pokémon League and Elite Four** — Ever Grande / League rooms. Camera:
  first dialogue and battle-return scripts for all four; Sidney recorded.
  Environment: Sidney's room **captured 3D** before the geometry merge;
  assets exist for all four rooms and their wall, lintel and dynamic-door
  fixes need fresh visual review. Check the exterior, each door and light
  state, and the other rooms. Use individual framing for each introduction.
- [x] **Champion Wallace and Hall of Fame** — Champion room / Hall of Fame.
  Camera: Wallace battle, Champion procession and Hall of Fame recorded for
  one staged run, including return to the original recording effect.
  Environment: both rooms **captured 3D** for the shown setup; check credits
  and alternate party and rival states.
  Give the Champion entrance, victory and final procession a full sequence.
- [ ] **Return home after the credits** — Littleroot / house. Camera: plan.
  Environment: Littleroot building **assets exist**; interior **check**.
  Review whether a quiet closing view serves the existing scene.

## Area reveals

These are separate from character scenes: a reveal introduces a place and
returns the camera to the player. Triggers and shot ideas below are proposals,
not implemented features. Prefer a first meaningful arrival, a skippable
sequence and a clear return to the player's position. Check alternate entrances,
revisits, story flags, saves and map transitions before choosing the trigger.
Do not play a reveal over an existing event without coordinating ownership.

- [ ] **Littleroot — a new home.** Trigger: first outdoor arrival after moving
  in. Shot: a gentle look across the houses and lab, ending at the player.
  Environment: **assets exist** for houses and lab; exact views **check**.
- [ ] **Petalburg — the first Gym.** Trigger: first arrival from Route 101/102.
  Shot: establish the town, then a brief static Gym composition and return.
  Environment: Gym exterior **assets exist**; approach and full view **check**.
- [ ] **Petalburg Woods — entering the forest.** Trigger: first entrance.
  Shot: a restrained view along the tree-lined path, preserving the sense of
  enclosure. Environment: story encounter **captured 3D**; entrance and
  canopy views **check**.
- [ ] **Rustboro — city and Devon.** Trigger: first suitable city arrival.
  Shot: descending orbit, static Mart, Gym to Devon, then a flyover to the
  player. Environment: **captured 3D** for the existing prototype; other
  approaches **check**. The existing city-introduction entry above tracks this
  same prototype; do not implement a second competing trigger.
- [ ] **Dewford — arrival by sea.** Trigger: first arrival with Briney. Shot:
  sea and shoreline, settle on the small town and return to the dock.
  Environment: town building **assets exist**; boat, water and dock **check**.
- [ ] **Granite Cave — the descent.** Trigger: first entrance or arrival at a
  suitable opening. Shot: hold on the cave mouth or a safe interior vista.
  Environment: Steven's room **captured 3D**; entrance, darkness and other
  floors **check**. Avoid revealing areas through walls or spoiling navigation.
- [ ] **Slateport — the harbor.** Trigger: first landfall on the beach or first
  city entrance. Shot: coast to harbor and shipyard, ending at the player.
  Environment: **check** beach, harbor, water, crowds and story-dependent ships.
- [ ] **Mauville — crossroads and Gym.** Trigger: first arrival. Shot: show the
  crossroads and a static Gym view before returning to the entrance.
  Environment: some town buildings **assets exist**; scene and entrances **check**.
- [ ] **Meteor Falls — waterfall and cave.** Trigger: first approach to the
  entrance or first safe viewpoint inside. Shot: reveal the falls, then settle
  near the player; coordinate with the story encounter. Environment: **check**
  terrain, water, cave edges and villain-team state.
- [ ] **Mt. Chimney — ascent and summit.** Trigger: first cable-car arrival.
  Shot: reveal the crater and opposing teams from a safe angle, then return
  before the encounter. Environment: **check** cable car, summit, smoke and
  actor states; avoid exposing unloaded edges.
- [ ] **Lavaridge — mountain town.** Trigger: first arrival from the mountain.
  Shot: a short descending view toward town and the Gym. Environment: Gym
  exterior **assets exist**; approach, terrain and town **check**.
- [ ] **Fortree — city in the trees.** Trigger: first arrival from Route 119.
  Shot: move through or above the canopy to reveal raised walkways, then return
  to the player. Environment: **check** treehouses, bridges, canopy and depth.
- [ ] **Lilycove — city and coastline.** Trigger: first arrival from Route 121.
  Shot: city and Department Store, then coast/harbor, ending at the player.
  Environment: some building **assets exist**; coastline and proposed camera
  path **check**. Coordinate with the rival encounter near the store.
- [ ] **Mt. Pyre — mountain of memorials.** Trigger: first view from the water
  or first entrance; select one after scouting both. Shot: a slow, quiet reveal
  of the mountain and approach, with a separate summit composition if the story
  calls for it. Environment: **check** exterior, water, summit, fog and
  memorials. Preserve the atmosphere and avoid previewing the orb theft.
- [ ] **Mossdeep — island and Space Center.** Trigger: first arrival from the
  sea. Shot: establish the shoreline, then the Space Center and Gym before
  returning to the landing. Environment: shared Gym exterior **assets exist**;
  island, Space Center, water and arrival approaches **check**.
- [ ] **Seafloor Cavern — submerged entrance.** Trigger: first suitable approach
  or surfacing inside. Shot: a restrained reveal of the entrance or chamber.
  Environment: **check** underwater rendering, submarine, chamber and terrain.
  Keep the route and Kyogre reveal for their own story beats.
- [ ] **Sootopolis — crater city.** Trigger: first arrival, accounting for
  underwater and airborne approaches and the weather-crisis story state. Shot:
  reveal the crater walls and city, then descend to the player; a crisis arrival
  may need a distinct composition coordinated with the legendary confrontation.
  Environment: some buildings **assets exist**; crater, water, weather and
  legendary actors **check**. Avoid playing the normal reveal over the crisis.
- [ ] **Sky Pillar — tower and summit.** Trigger: first approach to the tower;
  consider a separate summit shot before Rayquaza's awakening. Shot: reveal
  the tower from the sea, then reserve the summit's focus for the story.
  Environment: floor assets exist; the merged underground-border fix needs
  visual review. **Check** tower exterior, sea, upper floors and summit.
- [ ] **Ever Grande — waterfall and Pokémon League.** Trigger: first arrival at
  a viewpoint that can show the approach; consider a second reveal at the League
  entrance after Victory Road. Shot: waterfall and island first, then a held
  League facade and return to the player. Environment: **check** waterfall,
  exterior, map boundaries and League approach. Treat the two arrivals as
  separate candidates, not one presumed continuous camera path.
- [ ] **Victory Road — final approach.** Trigger: first entrance or a suitable
  view near the exit. Shot: a brief cavern composition that leads into Wally's
  encounter without revealing his position too early. Environment: **check**
  cave, lighting, terrain and story actor states.

For every reveal, record the exact maps and approach, one-time flag or replay
policy, story-state variants, skip behavior, shot path, model/flat coverage,
streaming and map-edge findings, and how gameplay control is restored. A
missing model is an environment task; a shot that exposes a flat background
may instead be composed differently. Evaluate scope and art needs after scouting.

## Before final sign-off

A checked first-pass box is not final sign-off. Record the exact map and story state, what is modelled or flat, missing assets,
proposed framing, relevant script branches, and a recording or review reference.
Check actor visibility, rapid dialogue input, exits, battle/fade transitions,
return to gameplay, and alternate approach directions. Verify on real hardware
and stereo separately from emulator captures. Keep story actions, rewards and
flags intact. Track optional content and the postgame in a separate inventory.
