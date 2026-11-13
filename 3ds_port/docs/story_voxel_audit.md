# Story environment voxel audit

Use this alongside the [story camera checklist](story_camera_checklist.md)
and the map-by-map [voxel status](../../docs/VOXEL_STATUS.md). A camera
recorded with the voxel renderer is not evidence that its environment is
modelled: an unmodelled wall or object can still be drawn flat. The status
document is itself under review; these entries are a triage of its existing
evidence, not a completed visual inspection of every map.

The status inventory scores 656 building and terrain items; 90 are marked
reviewed on a console. The remaining items range from unstarted to modelled
with known faults. Shared layouts and connected map seams need to be checked
as a group. Do not treat a checked camera scene as geometry sign-off.

## Main-story environment priorities

| Story area | Known state | Work before approving wider shots |
|---|---|---|
| Petalburg Woods | Buildings and terrain unstarted in the inventory; generic trees exist. | Inspect the entrance, canopy, ground and encounter path in the engine and on hardware. |
| Granite Cave, including Steven | Two rock clusters in Steven's room have a first model; its walls and remaining rocks are flat. The three approach floors are unstarted in the inventory. | Model the remaining room without closing its entrance or walkable cells; then cover the approach floors and darkness states. |
| Oceanic Museum | Both museum floors unstarted. | Model walls and exhibits around the Stern confrontation and preserve the battle and NPC paths. |
| Meteor Falls | First-floor terrain has reported height and texture faults; other cave rooms are unstarted. | Repair the story approach and waterfall, then inspect adjacent rooms and transitions. |
| Mt. Chimney | Station exists; summit terraces have visible seams and holes and some objects remain flat. | Complete crater terrain and missing props, then retry lower and wider story shots. |
| Weather Institute | Both floors have models with reported visual faults. | Repair and recheck the floor shadow, furniture and NPC placement before camera approval. |
| Mt. Pyre | Indoor floors unstarted; exterior and summit have known terrain faults and need elevated decks. | Model the story path and summit, including fog, memorials and the orb encounter. |
| Magma Hideout | Several machine models exist; cave rock and lava remain unmodelled, and some rooms are unstarted. | Model the cave and Groudon chamber; recheck reported flat machines and story actors. |
| Aqua Hideout | Partitions and some equipment exist; rock banks and multiple props remain flat. | Complete the route and submarine bay, checking water, moving actors and warp states. |
| Mossdeep Space Center | Both floors unstarted. | Model the story rooms and equipment; check the Steven and team battle staging. |
| Seafloor Cavern | Underwater approach, entrance and all nine rooms unstarted. | Model the approach and Kyogre chamber with water, terrain and battle staging. |
| Cave of Origin | Entrance, 1F and B1F unstarted. | Model the story route and inspect its lighting and boundaries. |
| Sky Pillar | Floors have models with reported side-wall flicker; entrance and summit unstarted. | Fix the walls and model the summit for Rayquaza; preserve the changing floor states. |
| Victory Road | All three floors unstarted. | Model the cave and check Wally's encounter and the League approach. |

Also review the remaining Gym, city, League and area-reveal locations against
their individual rows in the status inventory. A row can move to reviewed only
after checking the actual game on a console, including entrances, actor
occlusion, collision, stereo, story states and the camera paths used there.
