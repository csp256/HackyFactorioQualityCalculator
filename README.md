# HackyFactorioQualityCalculator
A half-assed attempt to model how quality, productivity, and recycler feedback loops interact in Factorio: Space Age

![alt text](https://github.com/csp256/HackyFactorioQualityCalculator/blob/main/example.gif) 

Does not account for branching dependency chains. Instead, it calculates the output distribution of quality along a single branch of the production chain. It has support for varying quality and productivity bonuses per quality level per stage of the production chain.

Adding productivity to a stage of the production chain does not automatically add the quality penalty caused by speed modules. Remember, garbage in, garbage out.

It does not model speed, power, pollution, or anything like that. It also has no support for actual item recipes. 

But it can be useful to evaluate the best way to get a target rarity. 
