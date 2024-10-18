# HackyFactorioQualityCalculator
A half-assed attempt to model how quality, productivity, and recycler feedback loops interact in Factorio: Space Age.

![alt text](https://github.com/csp256/HackyFactorioQualityCalculator/blob/main/example.gif) 

This Python script calculates the output distribution of quality along a single branch of the production chain. It has support for varying quality and productivity bonuses per input rarity (quality level) for each stage of production.

It does not model speed, power, pollution, or anything like that. It also has no support for actual item recipes: it assumes all other ingredients are trivially available. But it can be useful to evaluate the best way to get a target rarity of a specific item. 

Should you prioritize increasing your module rarity, or scale horizontally with more resource outposting? Where should your best modules go? How does productivity interact with recycler loops? Is it more efficient to set up a chain of moderate rarity interemediate items, or should you try to roll for high rarities from lower rarity inputs? Etc. 
