# aoc2024

[2024 Advent Of Code](https://adventofcode.com/2024) - My solutions

Eh why not

## Python
  - `python/day1part1.py`  - They're toying with us, this is just list sorting and absolute math
  - `python/day1part2.py`  - It's a simple solution that won't scale, but with only 1000 numbers in it doesn't matter
  - `python/day2part1.py`  - Shockingly mechanical. I mean completely just plow through the test conditions, bob's yer uncle
  - `python/day2part2.py`  - Spent more time fighting python's list mechanics and reference-not-copy behaviour than tackling the core problem
  - `python/day3part1.py`  - A quick refresher course required on python's Regular Expression handling. And let's nest them, why not?
  - `python/day3part2.py`  - If you can do alternatives in RE's and you've caught on to backslash plague, this was a surprisingly easy elaboration
  - `python/day4part1.py`  - This is actually my 2nd (working) attempt; my thought-i'd-been-clever approach of comparing ALL X,S positions is combinatorialy bad. This approach is approx 100x quicker...
  - `python/day4part2.py`  - Ah yes, this is where that lesson comes in immediately useful. Compare-from-start only is immediately the right approach to a speedy part 2 solution.
  - `python/day5part1.py`  - The fairly-naieve algorithm appears to be good enough as well as finding the right answer. What horrors await in part two???
  - `python/day5part2.py`  - The horror was trying to be clever against an unproven assumption of global rule consistency, when a simple looping reorder until consistency worked well enough
  - `python/day6part1.py`  - Luvs me 2d arrays. Luvs me simple IF statements. Luvs Iterative solutions. Luvs map updates. Simple as.
  - `python/day6part2.py`  - Clearly I'm still too brute-force even with optimisations; took 15 minutes after making the obvious optimisations. Right answer, clearly the wrong algorithm...
    - `python/day6part2_threaded.py`  - various optimisations (slow `Enum`? Strings!) but the only one that works is `ProcessPoolExecutor` with n tuned to CPU and reasonable slice size
  - `python/day7part1.py`  - Look, it's a fairly simple permutations problem, and `itertools` is part of the base library so why the hell shouldn't I use it, eh?
  - `python/day7part2.py`  - Ah the old permutation explosion complication trick. Luckily for me neither the increase in permutations NOR the size of the result required any special handling; brute force gives an acceptable result in less time than day6part2 so hooray and move on
  - `python/day8part1.py`  - Another permutations problem but with some bounds-checking going on. Wasted 20 minutes looking for an off-by-one error which turned out to be input related.
  - `python/day8part2.py`  - OK, just re-permutate the permutations; the map's fairly small so the additional complexity doesn't do much for the O(n) calculations, answer comes out fairly quickly with the force of brute. 
  - `python/day9part1.py`  - Spent more time on trying to visualise and then worrying about sparse datastructures before summing the actual data and finding a simple pre-allocated array would do. After that, brute force mechanistic rules the day again
  - `python/day9part2.py`  - OK, so some of my simplifying assumptions were too simple, a bit more grind required. Lots of off-by-one and too-soon terminations but going back to basics worked out OK
  - `python/day10part1.py` - So the algorithm sorts for the number of paths to the summits, not the total summits available so there's a _lot_ of post-processing aggro to dedup to get to the sum of the summits but oh lord it works OK.
  - `python/day10part2.py` - ARGHGHGHGHH, so yes just like the boy I solved part 2 before part 1 and the part 2 solution REMOVES code/complexity from the part one.
  - `python/day11part1.py` - Before I even read Part 2 I know I've made a simplifying assumption in Part 1 that won't hold. Also, I need to learn better map/list comprehension because I'm writing functions and loops for everything here and this is Not the Python Way
  - `python/day11part2.py` - GET IN! No, I made the *correct* simplifying assumption in part one (actually tracking stone order _doesn't matter_ just the number of stones). I blame previous year's AoC experience for letting me solve that one. A simple 1-char change to the code and bob's yer uncle