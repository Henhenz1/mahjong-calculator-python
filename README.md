# mahjong-calculator-python

well, might as well use this place for thoughts and todo for now

sets are actually pretty useful. maybe find ways of implementing for sanankou, ii/ryanpeikou, sankantsu possibly more

sets are close to absolutely necessary. managed some good work today 3/3/17 but gonna need to go back through and make everything work with sets
    ...or maybe not? i'm not sure
    never mind, both are necessary since set doesn't support indexing b/c unordered

    need specific checks for honroutou and tanyao for chiitoitsu

already have daisharin, daichisei, and paarenchan   
    add sanrenkou/suurenkou? ideally we can have settings to enable/disable uncommon yaku

chiitoitsu pairs must be distinct: make sure to add this somewhere

CAN'T USE .count() WITH SET - GO BACK AND FIND ERRORS

just realized that the strategy of "finding number tile values by truncating the first index of the tile list" doesn't work if the meld is of honors....did we check for that? go through and make sure

can we make code more efficient by using all([]) instead of linked 'and' chains?

is shousuushi easier to check using sets?
