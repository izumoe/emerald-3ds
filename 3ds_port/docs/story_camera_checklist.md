# Main story camera checklist

Working inventory for Pokémon Emerald's main story, from moving to Littleroot
through the Hall of Fame. Tick a box only when the scene's direction, relevant
branches and transitions have been reviewed. A prototype is a starting point,
not a claim that every approach and gameplay camera setting is finished.

**Environment** is tracked independently of camera work:

- **Captured 3D**: the named scene or location was recorded with the voxel
  renderer; its exact coverage and alternate angles still need review.
- **Assets exist**: model definitions exist for at least some features in the
  area. This does not establish that the specific shot, interior or whole map
  is modelled or complete.
- **Check**: scene-specific 3D coverage has not yet been established here.
  Inspect the actual map and its relevant story state before planning a shot.

The upstream README describes many towns and routes as partly modelled, with
large areas and most interiors still flat. A flat or partly modelled scene may
still support a useful composition. Record what is missing before assigning art
work. Proposed treatments are ideas, not final direction. Consult the
[camera lookbook](camera_lookbook.md) and [script reference](cutscene_scripts.md).

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
  Establishing orbit, static Mart, Gym/Devon and return flyover. Optional
  arrival treatment; decide when it should play and how it is skipped.

## Dewford, Slateport and Mauville

First-pass scripts are in progress. Briney, Wally, Brawly, Wattson, the Route
110 rival and the museum have staged emulator recordings; the remaining shots,
branches and map transitions need visual review. Checkboxes remain open pending
that review.

- [ ] **Mr. Briney's first voyage** — coast / boat / Dewford. Camera: first
  offer and departure recorded; voyage and arrival still need camera direction.
  Environment: **check** scene maps; Dewford building assets exist. Establish
  the departure and destination; consider whether travel needs a full sequence.

- [ ] **Steven and the Letter** — Granite Cave, Steven's room. Camera: exchange
  and exit prototype recorded. Environment: **captured 3D** for the shown
  approach. Check alternate approaches and the return to the cave camera.

- [ ] **Brawly** — Dewford Gym. Camera: introduction and battle return recorded.
  Environment: **captured 3D** for the shown darkness state; check others. Frame
  the introduction and shared battle transition.

- [ ] **Captain Stern and the Oceanic Museum** — Slateport harbor / museum.
  Camera: museum confrontation and battle returns recorded; harbor and alternate
  states need review. Environment: museum **captured 3D** for the shown setup;
  harbor **check**. Stage the delivery, Aqua confrontation and Archie's
  introduction.

- [ ] **Rival on Route 110** — Route 110. Camera: staged encounter and departure
  recorded; alternate approaches need review. Environment: **captured 3D** for
  the shown approach. Give the meeting and battle a clear two-shot and
  transition.

- [ ] **Wally challenges the Gym** — Mauville Gym exterior. Camera: staged
  encounter and departures recorded. Environment: **assets exist** for some
  Mauville buildings; exact scene **check**. Stage Wally, his uncle and the
  player, including the battle and farewell. Wally's uncle is present here;
  Norman is not part of this scene.

- [ ] **Wattson** — Mauville Gym. Camera: first battle and reward recorded;
  alternate approaches need review. Environment: **check** interior and puzzle
  state. Introduce Wattson and the battle.

## Meteor Falls to Fortree

First-pass scripts are in progress, including the battle handoffs and character
departures. Meteor Falls, Route 119, Route 120, Flannery and Winona have staged
emulator captures; the remaining shots, branches, map transitions and
visibility need visual review. Checkboxes remain open pending that review.

- [ ] **Meteor Falls and Mt. Chimney** — Meteor Falls / cable car / Mt. Chimney.
  Camera: Meteor Falls confrontation recorded; summit opening rejected by
  terrain visibility checks, as did the battle return; both need recomposition.
  Cable car still needs
  direction. Environment: **check** each map and villain-team state. Stage the
  Meteorite theft, opposing teams, ascent, Maxie battle and recovery.

- [ ] **Flannery and the Go-Goggles** — Lavaridge Gym / town. Camera: first
  battle recorded, but heavy steam obscures the shot. The rival gift completes
  in gameplay view after the terrain check rejects the close camera; it needs
  recomposition. Environment: **assets exist** for the shared Gym exterior;
  Gym interior and rival scene **check**. Separate the victory from the gift.

- [ ] **Norman's Gym battle and Surf** — Petalburg Gym / Wally's house. Camera:
  battle, post-battle exchange and Surf gift recorded. Environment: both
  rooms **captured 3D** for the shown setups; review alternate entrances and
  the transition to the house.

- [ ] **Weather Institute takeover** — Route 119 / Weather Institute. Camera:
  administrator and rescue scripted; battle return recorded. Rescue framing
  exposes a dark floor gap; shorter orbits clear in a staged retest. Environment:
  interior **captured 3D** with that issue; **check** exterior and weather.
  Stage the Aqua encounter, administrator battle and rescue.

- [ ] **Route 119 rival battle** — bridge south of Fortree. Camera: opening
  angle and revised battle return recorded. The battle push is rejected by the
  terrain check, and alternate approaches need review. Environment: **captured
  3D** for the shown approach. Keep the player framed as the rival departs.

- [ ] **Steven and the unseen obstacle** — Route 120. Camera: encounter
  recorded through the Kecleon reveal, battle return and departure. Environment:
  **captured 3D** for the shown setup; review alternate approaches and choices.
  The 3D renderer suppresses the bridge shadow to preserve the surprise.

- [ ] **Winona** — Fortree Gym. Camera: first battle and reward recorded;
  alternate approaches and puzzle state need review. Environment: **check**
  exterior, interior and puzzle state. Establish her introduction and battle.

## Lilycove to the weather crisis

- [ ] **Lilycove rival farewell** — Lilycove Department Store exterior. Camera:
  plan. Environment: **assets exist** for some Lilycove buildings; exact
  location **check**. Give the final rival encounter a distinct closing beat.
- [ ] **Mt. Pyre and the stolen orbs** — Mt. Pyre summit. Camera: plan.
  Environment: **check** summit, fog and characters. Stage the theft, the
  teams' departures and the elderly couple's explanation.
- [ ] **Magma Hideout at Mt. Chimney** — hideout / Groudon chamber. Camera:
  plan. Environment: **check**. Stage Maxie's awakening attempt, battle and
  Groudon's departure, with clear views of the legendary Pokémon.
- [ ] **Slateport submarine theft** — harbor. Camera: plan. Environment:
  **check** harbor and submarine. Stage Stern, the crowd, Archie and the
  getaway as a short sequence.
- [ ] **Aqua Hideout** — Lilycove hideout / submarine bay. Camera: plan.
  Environment: **check** interiors and moving actors. Build toward the
  administrator encounter and submarine escape.
- [ ] **Mossdeep Space Center** — Space Center. Camera: plan. Environment:
  **check** exterior, interiors and team positions. Introduce the attack,
  Steven's partnership and the battle with Maxie and Tabitha.
- [ ] **Tate and Liza** — Mossdeep Gym. Camera: plan. Environment: **check**
  interior and puzzle state. Compose both leaders for the double battle.
- [ ] **Seafloor Cavern** — cavern / Kyogre chamber. Camera: plan. Environment:
  **check** underwater approach and chamber. Stage Archie, Kyogre's awakening
  and the transition to the weather crisis.

## Sootopolis and the League

- [ ] **Weather crisis and Sootopolis confrontation** — routes / Sootopolis.
  Camera: plan. Environment: **assets exist** for some Sootopolis buildings;
  weather effects, legendary actors and exact viewpoints **check**. Establish
  the abnormal weather, Groudon and Kyogre, then Wallace and Steven.
- [ ] **Cave of Origin and Sky Pillar** — Cave of Origin / Sky Pillar summit.
  Camera: plan. Environment: **check** both interiors and summit. Give Wallace's
  request and Rayquaza's awakening distinct beats; preserve player control on
  the climb.
- [ ] **Rayquaza and the aftermath** — Sootopolis. Camera: plan. Environment:
  **check** crisis and restored-weather states. Give the descent, confrontation,
  departure and leaders' reactions room to read.
- [ ] **Juan** — Sootopolis Gym. Camera: plan. Environment: **check** interior
  and puzzle state. Introduce the final Gym battle and reward.
- [ ] **Wally's last challenge** — Victory Road. Camera: plan. Environment:
  **check** cave and entrance routes. Give the reunion, battle and farewell a
  character-focused treatment.
- [ ] **Pokémon League and Elite Four** — Ever Grande / League rooms. Camera:
  plan. Environment: **check** exterior and each room. Establish the approach;
  use a consistent battle-introduction pattern with individual framing.
- [ ] **Champion Wallace and Hall of Fame** — Champion room / Hall of Fame.
  Camera: plan. Environment: **check** rooms and battle/credits transitions.
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
  Environment: **check** tower exterior, sea, upper floors and summit.
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

## Before marking a scene complete

Record the exact map and story state, what is modelled or flat, missing assets,
proposed framing, relevant script branches, and a recording or review reference.
Check actor visibility, rapid dialogue input, exits, battle/fade transitions,
return to gameplay, and alternate approach directions. Verify on real hardware
and stereo separately from emulator captures. Keep story actions, rewards and
flags intact. Track optional content and the postgame in a separate inventory.
