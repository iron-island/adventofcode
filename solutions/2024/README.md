## Day 06

- TODO: add details
- Original solution iterates through all 16900 coordinates, and runs in 27 seconds
- Optimized solution iterates only through the path (which is Part 1 answer, 5153 with my input) and gets the turns in BFS instead of getting the whole path every time an obstacle is added.

## Day 07

- Original Part 2 solution ran 4 minutes 9 seconds. But after solving, I realized that the eval() can simply be converted to normal arithmetic operations, so after modifying it and adding an early exit condition for when the test result already exceeds the expected result, runtime reduced to 37 seconds.
- After optimizing Part 2 further to a DFS with recursion and early exit conditions, runtime was reduced to just 1.7 seconds! What's surprising to me is that this was without memoization which I initially added with the `@cache` decorator. With the cache, runtime was 11.5 seconds! I guess because the DFS is already fast, the overhead of caching was probably large enough to contribute. I tried quickly changing to `@lru_cache` with low number of `maxsize` values of around 1000 to 3^10 since the cache only applies to each equation, and runtime does get down to around 2.6 seconds so the cache overhead is still large.
- An optimizationi attempt I did in Part 2 was trying a mathematical way to count the number of digits for concatenation instead of converting to string and counting via `len(str())`, after seeing a Reddit post about it. I tried `math.ceil` and `math.log10`, a loop with a divider, and f-string and they were marginally worse than the `len(str())` approach so I didn't incorporate it anymore.
- Applying the same DFS to Part 1 but with the concatenation removed, Part 1 runtime went from 3 seconds to 60ms! So combining Part 1 and Part 2 in one run where if the equation was validated in Part 1 it would be skipped in Part 2, the total runtime is now 1.6 seconds.

## Day 09

- TODO: add details
- Original Part 1 was 2 minutes 52 seconds
- Optimized Part 1 reduced to 15ms!
- Original Part 2 was 35s
- Optimized Part 2 reduced to 30ms!
- Combining Parts 1 and 2 in a single run finishes faster (35ms) compared to separate runs (45ms), this might be due to only needing to read the input and convert to integers only once.

## Day 11

- TODO: add details
- Original solution ran in 2.2s, mostly because Part 1 was brute-forced
- Optimized solution is just computing Part 1 at the 25th blink while Part 2 is running, so runtime reduced to 150ms
- Further optimized down to 80ms by replacing the deepcopy function into just the copy method

## Day 15

- TODO: add details
- Original solution with both parts runs in 9 seconds. Mostly Part 2 has the high runtime
- Removed checks and no other optimizations and reduced runtime to ~100ms

## Day 17

- TODO: add details
- Original Part 2 ran in 23.4s
- Optimized Part 2 via DFS runs in 25ms
- Combining Parts 1 and 2 in a single run is still around 25ms since Part 1 and input is small

## Day 18

- TODO: add details
- Original solution ran in 1.7s
- Optimized solution is 35ms via binary search, replacing list for searching for corruptions into sets, combining Part 1 to Part 2, and removing unnecessary data structures

## Day 19
- TODO: add details
- Original solution ran in 1.1s
- Optimized solution runs in 570ms after computing Part 1 in the same Part 1 run, and some slight optimizations that may necessarily have mattered like using `towels_list` as a global variable to prevent it needing to be an argument in the recursive `check_design2` function, and from needing to convert to a tuple.

## Day 20

- Before I thought of the solution taking advantage of the only possible path, I initially tried 2 alternatives that didn't assume a single path. Both failed even for the examples and was hard to modify and debug: Alternative 1 with BFS and then A-star where if the current tile is the starting point of the cheat, we "teleport" to the endpoint and then mark all tiles within their Manhattan distance as visited to avoid needing to traverse them. Alternative 2 is a similar BFS and A-star but before traversing, we replace all tiles between the start and end point cheats with `.` to remove walls.
- Original solution was slow since I'm finding the index `idx2 = best_path.find(cheat2)` of the endpoint `cheat2` of the path after cheating. There is actually no need to find it everytime which defeats the purpose of shrinking `cheat2_list` since it would be found at the latter ends of `best_ath`. So the difference `idx2 - idx` is just its index in `cheat2_list` + 1. This significantly lowers the runtime from around 1 minute 12 seconds to 6 seconds. I did a 2nd optimization that reduced it to 3 seconds by avoiding iterating for `idx2` which iterates 43772046 times and instead just computing the possible coordinates 20 units apart and then iterating through those coordinates to check if they lie along the path, which iterates 7868396 times.

## Day 21

- I did DFS using recursive functions and memoization, where only 2 sequence characters are sent to a function that generates the possible sequences, which then get decomposed into 2 sequence characters and then recursively checked. Only 2 characters are needed for the next call because the robot returns to 'A' on each character. Each recursive function has the sequence and depth `num_robots` as inputs, with depth decrementing on each 2 sequence character check. When the depth `num_robots = 0`, the cost is computed and returned. Depth would then be 2 and 25 for parts 1 and 2, respectively
- Although the recursive functions aren't optimized, the runtime was still surprisingly fast. It was around ~600ms and seems to stay constant even up to depth = 220. Higher depths seem to be limited by recursion depth limit which I hadn't tried to increase anymore. The function calls for part 1 goes from `dfs_key` -> `dfs_dir1_seq` -> `dfs_dir1` -> `dfs_dir2_seq` -> `dfs_dir2` and didn't use the depth yet so it wasn't actually recursive, though `dfs_dir*` functions are just copies of each other to hopefully help in debugging but luckily it immediately gave the correct answer. In part 2, I added the `num_robots` depth and `dfs_dir2` calls `dfs_dir2_seq` to actually do the recursion, and worked correctly for both part 1 and part2. It could probably handle higher depth values if I combined the `dfs_dir*_seq` and `dfs_dir*`, I'm just not sure though if it would impact the runtime as the `dfs_dir*` has a much smaller input space and probably helps to fill up its cache faster.
- I originally wrote so many other alternative solutions and helper functions to help debugging and understanding the problem, but as always these initial solutions became too complex and harder to debug. The closest I got was an iterative, greedy solution that also looks for 2 characters at a time and was able to produce valid short sequences. It was close enough to the best sequences but it doesn't look for all possible sequences so its off on some codes. In the example, it was off by 4 on code 379A.

## Day 22

- TODO: add details
- Interesting Python solution in Reddit from u/notrom11 running in 50ms: https://github.com/APMorto/aoc2024/blob/master/day_22_monkey_market/monkey_market.py
- Difficult to optimize since my original solution is already relatively fast at 6s. I was able to marginally optimize down to 3s by using bitwise operations and running both parts in the same loop.
- Tried `u/notrom11`'s approach of using Python's `array.array` and constructing the indices for the changes using 4 base-19 digits and solution went down to 1.9s
