_Lung = const(81)

def _tick_lung(self, t, i):
    x = self.x[i]
    tape = self._tp
    if tape.player.x > x+300:
        self._tids[i] = 0
    data = self.data
    if data[0]: return
    self.y[i] = 105
    if tape.player.x > x-17:
        self.bsync = 1
    if self.bsync or self.omons.bsync:
        data[0] = 1
        self.reactions = [
"|Lung: Umby! Glow!",
"|Well if it isn't the wormy duo!",
"^: Lung?",
"@: Lung! What are you doing here?!",
"|Lung: Well, as you can see, I'm not a particularly welcome guest.",
"^: We've been feeling the same way.",
"@: What happened? How did you get here?",
"|Lung: Same reason as you, by the looks of it.",
"|I hitched a ride on one of those floating skulls. They might just be heads, but they have a pretty cosy respiratory system. My plan was to see if I could hunt down the swarm's hive mind.",
"^: You've been trying to take down these aliens too?!",
"|Lung: Trying, yes. Succeeding? No.",
"^: We tried to take down their mainframe.",
"|Lung: Well that won't work.",
"|Their whole ship is a bio-computer.",
"@: Did you find their hive mind?",
"|Lung: Sadly, no, and I've seen enough to know that they don't even work as a collective.",
"@: What do you mean?",
"|Lung: Well, they really like to barter...",
"|In a big way.",
"@: Barter???",
"|Lung: Yep! It's their main invasion strategy...",
"|Find the owners, buy them out.",
"^: But nobody owns the planet!",
"|Lung: Well the aliens think they do now.",
"@: Who did they buy it from?!",
"|Lung: The dolphins.",
"^: The dolphins?!??!!!!",
"|Lung: Yep, the dolphins. Who else would they go to?",
"|The most intelligent species are the Worms, but they love earth, earth is like their favourite thing, they would never sell it.",
"|Next up were Humans, but the aliens didn't think they were valid owners...",
"|They never took care of the place.",
"@: True.",
"^: Yep.",
"|Lung: That left the Octopus, and the Dolphins... and the Dolphins were only too keen to sell the place.",
"@: What did they sell it for?!",
"|Lung: Mock tuna.",
"|Well, mock tuna and a really really giant tank.",
"|They are on board this ship now...",
"@: Wait. Two things...",
"@: Firstly, they already had those things - actual tuna, and the entire ocean!",
"|Lung: Kind of... there hasn't been much tuna since the humans got to it. Here, they have synthesisers. They can have as much mock tuna as they want!",
"@: Fair enough. But secondly, are you saying there is a really really giant tank on board, with enough salty water to destroy even the largest bio-computer?",
"|Lung: That... that might actually work!",
"^: What?",
"@: We smash the tank, then flood the ship.",
"^: Where is the tank?",
"|Lung: If you keep going straight ahead, you'll come up underneath it, where all the support structures are.",
"@: This is amazing! We finally have a real plan!",
"^: What about you, Lung?",
"|Lung: Me? I'll have the best chance if you can disable all their systems.",
"|You pull this off, and I'm sure I'll find a way out.",
"@: Alright, Lung. Good luck then.",
"|Lung: Same goes to the both of you!"]

mons.ticks = {_Lung: _tick_lung}