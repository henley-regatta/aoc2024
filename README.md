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