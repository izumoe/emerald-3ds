# Camera scripting lookbook

Choose the story beat first, then the shot. A conversation can share one
composition across several dialogue boxes; a new view should direct attention
to something that has changed. Use this lookbook to plan, and the
[script reference](cutscene_scripts.md) for command details. See the [main story checklist](story_camera_checklist.md) for scene and environment status.

## Choose a shot

| Shot | Use it when… | Main choice |
| --- | --- | --- |
| Establishing wide | The player enters an important place | Show the landmark and a readable route into it |
| Static landmark | A building or destination deserves attention | Arrive, settle, and hold |
| Close two-shot | Two people are having a conversation | Keep both faces readable |
| Shoulder view | One speaker has the important line | Put the listener at the edge of the foreground |
| Group composition | A third person joins or changes the conversation | Make room without returning to the full gameplay wide |
| Slow push | A request, gift or revelation gains weight | Move closer while the line plays |
| Low side angle | A character or encounter needs more presence | Lower the view and choose useful directional artwork |
| Orbit | The relationship or focus changes within a beat | Keep a readable subject throughout the arc |
| Following dolly | Characters lead, escort or walk together | Move with their interpolated positions |
| Held departure | Someone leaves the conversation | Stay with whoever remains |
| Flyover | Several landmarks form an introduction | Connect a few clear destinations, then return to the player |
| Fade and reveal | Time, place or scene state changes | Restore the image into a prepared composition |
| Battle lead-in | Dialogue turns into a fight | Give the shared battle zoom a clear subject |

## Motion during dialogue

A slow, subtle pan or orbit is a useful default during a dialogue hold. Give
the movement a clear direction and keep the important faces readable throughout.
Let a shot settle when stillness helps a landmark, reveal, entrance or departure;
use the scene’s pace and space to decide. Test quick dialogue advances so a new
cue starts cleanly from the displayed pose.

## Compose the scene

Give each shot a reason: establish who is involved, make the current speaker
readable, reveal a reaction, or follow a meaningful change. Let a clear
two-shot carry an exchange; reserve a closer angle or reverse for a new beat.
Leave the speaker looking into the frame when possible, and keep the pair on
consistent sides across cuts unless a visible move establishes the change.

Try both sides of the conversation in the actual map. A reverse angle may
reveal a more expressive sprite facing or separate the characters, but a wall,
unmodelled room edge or foreground object may make that side unusable. Review
the complete camera move and textbox, not just the starting pose. If the
preferred shot fails visibility checks, review the fallback in context rather
than assuming it is the intended composition.

## Shot cards

### Establishing wide → close conversation

**Use:** arrivals, first meetings, a new room or city.

Start wide enough to explain where the characters are. Move into the dialogue
composition once the place is understood. Keep an entrance or landmark visible
when it helps orient the player.

**Check:** the wide shot earns its duration; the move ends with readable faces.
Avoid repeating the same establishing shot for every short interaction.

### Static landmark

**Use:** a Mart, Gym, destination sign or other point of interest.

Compose the landmark, complete the move, and hold. Let the subject carry the
shot. A locked view can punctuate a sequence that otherwise moves continuously.

**Recipe:** `camera_scene` → `camera_anchor` → `camera_view` → `waitcamera`
→ `camera_hold`. A one-frame view is a cut, so review both sides of that cut.

### Close two-shot

**Use:** greetings, ordinary exchanges and the base composition for longer scenes.

Frame the speaker and listener together. Try both sides of the pair before
choosing the angle. Find the midpoint of their visible bodies, then place it
near the center of the picture left unobstructed by the dialogue box. Leave
room around both heads and feet.

**Starting point:** actor distance 50–65%, with a modest side angle. Lower distance
means closer framing; these values describe camera distance, not image scale.

**Check:** the player does not cover the speaker, and neither sprite becomes
uncomfortably large. The camera normally aims at ground height; use
`camera_height 8` as an initial aim, then adjust for the dialogue box. A lower
aim places the pair higher on screen; a negative height can be useful for a
close scenic shot. A scenic anchor can use `camera_offset` for sub-tile
adjustments. Check horizontal and vertical placement together at the beginning
and end of an orbit, with the actual dialogue box visible; aiming at the tile
or the characters' feet alone can leave the pair too low.

### Shoulder view

**Use:** advice, a challenge, a confession or an important request.

Keep the listener off-centre in the foreground and give the speaker a clear
face and silhouette. A small target offset can separate overlapping sprites.
Reverse the composition when the other character becomes the focus, if needed.

**Check:** the foreground sprite frames the speaker rather than covering them.
Keep the characters on consistent sides of the image across connected shots
unless the camera movement makes the change clear.

### Group composition and arrivals

**Use:** introductions, interruptions and a third character joining a conversation.

Make room toward the entrance before the newcomer arrives. Follow their approach
or hold the group destination, then settle into a new composition. A small widen
or target shift may be enough; preserve the intimacy of the conversation.

**Check:** each face remains distinct throughout the arrival, including while
sprites overlap. Choose the pair and offset deliberately when framing three actors.

### Slow push

**Use:** a gift, an offer, a warning or a line that changes the stakes.

Start from an already readable shot and move a little closer while the text
plays. A small tilt and orbit can join the push as one concurrent gesture.
Hold the resulting composition through the response.

**Starting point:** 90–180 rendered frames, moving from about 60% to 50% actor
distance. Scale the movement to the reading time and available space.

**Check:** rapid dialogue input can interrupt the move without causing a jump
or leaving the next action badly framed.

### Low side angle and orbit

**Use:** confrontations, character introductions and important exchanges.

A lower view gives sprites more presence and reveals depth in the environment.
A side angle can separate faces that overlap in a straight-on view. An orbit
can change that relationship gradually while keeping the subject anchored.

**Starting point:** 50–60% actor distance, pitch offset around -4 to -6, and
an orbit about 55° to one side. Inspect both sides; they can show different
expressions or a character's back. The directional-art mapping has hysteresis
around its 50° boundary, so do not depend on hovering exactly at the boundary.

**Check:** foreground walls, furniture, sprite backs, floor edges and background
rooms throughout the path. A large orbit draws attention to the camera; give
that movement enough time and a clear story purpose.

### Following dolly

**Use:** an escort, a guided walk or two characters moving together.

Select the actors, enable follow, and start the camera move alongside the
original movement commands. Leave space in the direction of travel. Settle
and disable follow when the group reaches its destination.

**Check:** corners, pauses and uneven actor speeds. Use `waitmovement` and
`waitcamera` where the next beat needs both walking and framing to finish.

### Held departure

**Use:** a defeated enemy fleeing, a farewell or an NPC going to fetch someone.

Prepare a player-only composition before the walk begins, then keep it steady.
Choose an angle where the departing character crosses the frame edge. A route
away into the distance may leave them visible until the script removes them.

**Recipe:** `camera_pair LOCALID_PLAYER, LOCALID_PLAYER` → offset and move
→ `waitcamera` → original departure movement → short hold → gameplay return.

**Check:** every departing actor is fully outside the image before removal.
Review the entire walk, including small companions and the return to gameplay.

### Landmark sequence and flyover

**Use:** a city's first introduction or an approach to a major destination.

Plan a small sequence of distinct beats: descending establishing orbit → static
landmark → second landmark → travelling view → player. Link destinations with
deliberate changes in anchor, height and angle. Let some shots remain still.

**Check:** map streaming, exposed map edges, buildings crossing the view, and
whether the final return makes the player's position clear. Scenic commands
use different distance and angle conventions from actor commands; see below.

### Fade and reveal

**Use:** healing, elapsed time, a location change or a substantial reframing.

Fade out, prepare the next composition, and reveal it when the map and actors
are ready. Use the queued reveal commands for supported transitions rather
than trying to time a camera move against loading by eye.

**Check:** who owns each fade, what happens on early input, and whether every
branch restores the picture and player control. Keep original story fades
unless the scene explicitly needs different timing.

### Battle lead-in and return

**Use:** a conversation becomes an encounter.

Compose the confrontation so the shared battle zoom has a clear subject. Plan
the post-battle view separately: the defeated character may speak, flee or
change position. Prepare any held departure before that movement starts.

**Check:** the actual battle transition and actual return, including fades.
A standalone conversation preview does not exercise this boundary.

## Command conventions

- Actor shots use `camera_pair`, `camera_move` and `camera_orbit`. Distance is
  50–120% of gameplay distance; pitch is an offset from gameplay pitch.
- `camera_move` yaw is a relative offset limited to ±30°. `camera_orbit` uses
  heading 30–150, with 90 as the front view. Heading 145 gives a -55° yaw;
  heading 35 gives +55°.
- Scenic shots use `camera_scene`, `camera_anchor` and `camera_view`. Scenic
  distance is 50–180%; pitch and yaw are absolute angles. Do not copy actor
  pitch or orbit heading numbers directly into a scenic view.
- `camera_offset` uses sixteenths of a tile. Selecting a pair or scenic anchor
  resets the offset; selecting a pair also disables follow. Set them again when
  the next shot requires them.
- Durations are rendered frames: 60 frames is about one second at 60 fps.
  Slowdown lengthens the movement.
- Use the actual macro `waitcamera` when a completed move is required. Without
  a wait, dialogue can advance during the tween. A replacement move begins
  from the displayed pose; review its path under rapid input.

## Finish and review

Return to gameplay deliberately with `camera_return`, `waitcamera` and
`camera_end`. Preserve original movement, text, rewards and quest branches.
Camera macros use scratch variables; consult the reference before placing them
between an existing variable assignment and the command that consumes it.

Review each scene at normal reading speed, with rapid A presses, and through
supported skip/alternate branches. Check faces, tween midpoints, actor exits,
obstructions, battle returns and fades. Visibility checks can reject a shot;
test the fallback as well as the intended composition.

Leave a short purpose comment beside each cue, such as “hold player while
grunt escapes” or “push during the offer.” It should explain the story beat
so later tuning preserves the intent.
