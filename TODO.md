- bins remove balls and apply modifiers to next shots
- obstacles apply modifiers to the balls that hit them
- invert gravity modifier per ball
- physics/restitution modifier per ball
- make pegs have a non collision regenerating state
- variable power should be a modifier, default fixed power
-

Bugs:
- explosions reproc when still within lifetime and another bomb goes off (probably a list resize during iteration bug)
- more hit sounds than hits, or phantom hits after balls should have been removed by bin hits
- along with the phantom hits, pegs sometimes disappear when they shouldn't because of this
