# Cribbage Conundrum (working title)

Every time I play crib, I seem to find myself in a situation where I'm unsure of what cards to put into the crib vs keep in my hand. I feel like the general rule of thumb for most of the game is to optimize for the maximum possible number of points during the ["show"](https://en.wikipedia.org/wiki/Cribbage#Show). However, perhaps near the end of the game if you only need a handful of points, you can optimize for the highest expected value of your hand, which could differ. There are additional nuances of course (i.e. whether it's yours or your opponent's crib, optimizing for the [play](https://en.wikipedia.org/wiki/Cribbage#Play), etc.) but for now let's just focus on the basics.

If you've ever played [crib](https://en.wikipedia.org/wiki/Cribbage) before, I'm sure you've found yourself in the situation where you're unsure of what cards to put into the crib vs keep in your hand. While you can do some simple mental math to determine the maximum basic expected value of your hand based on what you discard and what the cut card will be, 

## Skeleton 

- Background
  - Outline example hand where you could optimize for max points or max expected val
- Outline problem/idea
  - See if there's a difference in "strategy" (what cards you put into the crib vs what you keep in your hand) based on whether you want to optimize for max potential points or max expected val
- Methodology
  - Points reference
    - Get all possible crib hands (4 card hands)
    - For each hand, get all possible cut cards
    - Get the points for each hand and cut card combination
    - ~13 million rows of data
    - s/o this guy for the API: https://github.com/dkackman/CribbageCounter (run it locally so you don't spam his API)
    - Could certainly be more efficient, but this brute force way worked. 
      - Could generalize to ignore suits when not relevant/needed (see wiki crib stats page)
  - With the points ref out of the way, 
  - Sorted list of hands where avg ev hand is slightly greater than max val hand, but max val hand has much higher upside. So it's not necessarily bad to keep the max val hand in your hand.