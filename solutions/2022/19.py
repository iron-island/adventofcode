import pprint

def remove_all(mylist, val):
  return [x for x in mylist if x != val]

def geode_upper_bound(curr_geodes, t, geode_rbts):

  upper_bound = curr_geodes
  for curr_t in range(1, t+1):
    upper_bound += geode_rbts
    geode_rbts += 1

  return upper_bound

def in_best_100(best_resources, best_robots, best_t, resources, robots, t):
  TOP = 1
  inserted = 0
  for idx, b in enumerate(best_resources):
    if (best_resources[idx][3] + best_t[idx]*best_robots[idx][3]) <= (resources[3] + t*robots[3]):
      best_resources.insert(idx, resources)
      best_robots.insert(idx, robots)
      best_t.insert(idx, t)
      inserted = 1
      break

  if (len(best_resources) < TOP) and not inserted:
    best_resources.append(resources)
    best_robots.append(robots)
    best_t.append(t)
    inserted = 1
  elif (len(best_resources) > TOP):
    best_resources = best_resources[:-1]
    best_robots = best_robots[:-1]
    best_t = best_t[:-1]

  return inserted

# DFS similar to day 16
cache = set()
max_geodes = 0
best_resources = (0, 0, 0, 0)
best_robots = (1, 0, 0, 0)
best_t = 0
def dfs(t, resources, robots, costs):
  global max_geodes
  global best_resources
  global best_robots
  global best_t
  global cache

  curr_ore, curr_clay, curr_obs, curr_geodes = resources
  ore_rbts, clay_rbts, obs_rbts, geode_rbts = robots
  ore_robot_cost, clay_robot_cost, obs_robot_ore_cost, obs_robot_clay_cost, geode_robot_ore_cost, geode_robot_obs_cost = costs

  if (curr_geodes > max_geodes):
    max_geodes = curr_geodes
    best_resources = resources
    best_robots = robots
    best_t = t
  elif (curr_geodes == max_geodes) and (geode_rbts >= best_robots[3]) and (t >= best_t):
    max_geodes = curr_geodes
    best_resources = resources
    best_robots = robots
    best_t = t

  if (t <= 0):
    return 0

  curr_max_possible_geodes = geode_upper_bound(curr_geodes, t, geode_rbts)
  max_lowerbound_geodes = max_geodes + best_t*best_robots[3]
  #print(f't = {t}, curr_max = {curr_max_possible_geodes}, max = {max_lowerbound_geodes}')
  if (max_lowerbound_geodes > curr_max_possible_geodes):
    return 0

  # throw away unnecessary resources
  max_ore_cost = max(ore_robot_cost, clay_robot_cost, obs_robot_ore_cost, geode_robot_ore_cost)
  max_clay_cost = obs_robot_clay_cost
  max_obs_cost = geode_robot_obs_cost
  if (curr_ore > t*max_ore_cost):
    curr_ore = t*max_ore_cost
  if (curr_clay > t*max_clay_cost):
    curr_clay = t*max_clay_cost
  if (curr_obs > t*max_obs_cost):
    curr_obs = t*max_obs_cost

  resources = (curr_ore, curr_clay, curr_obs, curr_geodes)

  if (t, resources, robots) in cache:
    return 0
  else:
    cache.add((t, resources, robots))

  #if (resources, robots, t) in visited:
  #  queue.pop(0)
  #  continue

  # build geode robot
  if (curr_ore >= geode_robot_ore_cost) and (curr_obs >= geode_robot_obs_cost):
    future_resources = (curr_ore-geode_robot_ore_cost + ore_rbts,
                        curr_clay + clay_rbts,
                        curr_obs-geode_robot_obs_cost + obs_rbts,
                        curr_geodes + geode_rbts)
    future_robots = (ore_rbts, clay_rbts, obs_rbts, geode_rbts+1)
    dfs(t-1, future_resources, future_robots, costs)
    #if (t > 1):
    #  queue.append((future_resources, future_robots, t-1))
    #else:
    #  max_geodes = max(max_geodes, curr_geodes + geode_rbts)
  elif (ore_rbts > 0) and (obs_rbts > 0):
    # wait to be able to build a geode robot
    wait_time = 0
    future_ore = curr_ore
    future_clay = curr_clay
    future_obs = curr_obs
    future_geodes = curr_geodes
    while (future_ore < geode_robot_ore_cost) or (future_obs < geode_robot_obs_cost):
      future_ore += ore_rbts
      future_clay += clay_rbts
      future_obs += obs_rbts
      future_geodes += geode_rbts
      wait_time += 1
    if (t-wait_time > 0):
      future_resources = (future_ore, future_clay, future_obs, future_geodes)
      #queue.append((future_resources, robots, t-wait_time))
      dfs(t-wait_time, future_resources, robots, costs)

  # build obsidian robot unless it is already enough
  if (obs_rbts < max_obs_cost):
    if (curr_ore >= obs_robot_ore_cost) and (curr_clay >= obs_robot_clay_cost):
      future_resources = (curr_ore-obs_robot_ore_cost + ore_rbts,
                          curr_clay-obs_robot_clay_cost + clay_rbts,
                          curr_obs + obs_rbts,
                          curr_geodes + geode_rbts)
      future_robots = (ore_rbts, clay_rbts, obs_rbts+1, geode_rbts)
      dfs(t-1, future_resources, future_robots, costs)
      #if (t > 1):
      #  queue.append((future_resources, future_robots, t-1))
      #else:
      #  max_geodes = max(max_geodes, curr_geodes + geode_rbts)
    elif (ore_rbts > 0) and (clay_rbts > 0):
      # wait to be able to build an obisidian robot
      wait_time = 0
      future_ore = curr_ore
      future_clay = curr_clay
      future_obs = curr_obs
      future_geodes = curr_geodes
      while (future_ore < obs_robot_ore_cost) or (future_clay < obs_robot_clay_cost):
        future_ore += ore_rbts
        future_clay += clay_rbts
        future_obs += obs_rbts
        future_geodes += geode_rbts
        wait_time += 1
      if (t-wait_time > 0):
        future_resources = (future_ore, future_clay, future_obs, future_geodes)
        #queue.append((future_resources, robots, t-wait_time))
        dfs(t-wait_time, future_resources, robots, costs)

  # build clay robot, unless it is already enough
  if (clay_rbts < max_clay_cost):
    if (curr_ore >= clay_robot_cost):
      future_resources = (curr_ore-clay_robot_cost + ore_rbts,
                          curr_clay + clay_rbts,
                          curr_obs + obs_rbts,
                          curr_geodes + geode_rbts)
      future_robots = (ore_rbts, clay_rbts+1, obs_rbts, geode_rbts)
      dfs(t-1, future_resources, future_robots, costs)
      #if (t > 1):
      #  queue.append((future_resources, future_robots, t-1))
      #else:
      #  max_geodes = max(max_geodes, curr_geodes + geode_rbts)
    else:
      # wait to be able to build a clay robot
      wait_time = 0
      future_ore = curr_ore
      future_clay = curr_clay
      future_obs = curr_obs
      future_geodes = curr_geodes
      while (future_ore < clay_robot_cost):
        future_ore += ore_rbts
        future_clay += clay_rbts
        future_obs += obs_rbts
        future_geodes += geode_rbts
        wait_time += 1
      if (t-wait_time > 0):
        future_resources = (future_ore, future_clay, future_obs, future_geodes)
        #queue.append((future_resources, robots, t-wait_time))
        dfs(t-wait_time, future_resources, robots, costs)

  # build ore robot, unless it is already enough
  if (ore_rbts < max_ore_cost):
    if (curr_ore >= ore_robot_cost):
      future_resources = (curr_ore-ore_robot_cost + ore_rbts,
                          curr_clay + clay_rbts,
                          curr_obs + obs_rbts,
                          curr_geodes + geode_rbts)
      future_robots = (ore_rbts+1, clay_rbts, obs_rbts, geode_rbts)
      dfs(t-1, future_resources, future_robots, costs)
      #if (t > 1):
      #  queue.append((future_resources, future_robots, t-1))
      #else:
      #  max_geodes = max(max_geodes, curr_geodes + geode_rbts)
    else:
      # wait to be able to build an ore robot
      wait_time = 0
      future_ore = curr_ore
      future_clay = curr_clay
      future_obs = curr_obs
      future_geodes = curr_geodes
      while (future_ore < ore_robot_cost):
        future_ore += ore_rbts
        future_clay += clay_rbts
        future_obs += obs_rbts
        future_geodes += geode_rbts
        wait_time += 1
      if (t-wait_time > 0):
        future_resources = (future_ore, future_clay, future_obs, future_geodes)
        #queue.append((future_resources, robots, t-wait_time))
        dfs(t-wait_time, future_resources, robots, costs)

  return 0

# DP
dp_obs_cache = {}
def dp_obs(t, robots, resources, cost):
  max_obs = 0

  if (t > 0):
    if (robots, resources, cost) in dp_obs_cache:
      return dp_obs_cache[(robots, resources, cost)]

    ore_robots, clay_robots, obs_robots = robots
    prev_ore_robots, prev_clay_robots, prev_obs_robots = robots
    curr_ore, curr_clay, curr_obs = resources
    ore_robot_cost, clay_robot_cost, obs_robot_ore_cost, obs_robot_clay_cost = costs

    for i in range(0, 2):
      if (i == 2) and (curr_ore >= obs_robot_ore_cost) and (curr_clay >= obs_robot_clay_cost):
        # build obsidian robot
        obs_robots += 1
        curr_ore -= obs_robot_ore_cost
        curr_clay -= obs_robot_clay_cost
      #elif (i == 1) and ((curr_ore >= clay_robot_cost) or (curr_ore >= ore_robot_cost)):
      #  curr_ore, curr_clay = dp_clay(t-1)

      # mine before updating robots
      curr_ore += prev_ore_robots
      curr_clay += prev_clay_robots
      curr_obs += prev_obs_robots

      # update
      new_robots = (ore_robots, clay_robots, obs_robots)
      new_resources = (curr_ore, curr_clay, curr_obs)
      max_obs = max(max_obs, dp_obs(t-1, new_robots, new_resources, costs) + curr_obs)

    cache[(robots, resources, cost)] = max_obs

  return max_obs

dp_clay_cache = {}
def dp_clay(t, robots, resources, costs):
  max_clay = 0
  curr_ore = 0
  ore_robots = 1
  clay_robots = 0

  if (t > 0):
    if (robots, resources, costs) in dp_clay_cache:
      return dp_clay_cache[(robots, resources, costs)]

    ore_robots, clay_robots = robots
    prev_ore_robots, prev_clay_robots = robots
    curr_ore, curr_clay = resources
    ore_robot_cost, clay_robot_cost = costs
    for i in range(0, 3):
      if (i == 2) and (curr_ore >= clay_robot_cost):
        # build clay robot
        clay_robots += 1
        curr_ore -= clay_robot_cost
      elif (i == 1) and (curr_ore >= ore_robot_cost):
        # build ore robot
        ore_robots += 1
        curr_ore -= ore_robot_cost

      # mine before updating robots
      curr_ore += prev_ore_robots
      curr_clay += prev_clay_robots

      # update
      new_robots = (ore_robots, clay_robots)
      new_resources = (curr_ore, curr_clay)
      max_clay = max(max_clay, dp_clay(t-1, new_robots, new_resources, costs) + curr_clay)
      #mined_ore, mined_clay, built_ore_rbts, built_clay_rbts = dp_clay(t-1, new_robots, new_resources, costs)
      #if (mined_clay + curr_clay) > max_clay:
      #  max_clay = mined_clay + curr_clay
      #  curr_ore = mined_ore
      #  ore_robots = built_ore_rbts
      #  clay_robots = built_clay_rbts

  #dp_clay_cache[(robots, resources, costs)] = (curr_ore, max_clay, ore_robots, clay_robots)
  #return (curr_ore, max_clay, ore_robots, clay_robots)
  dp_clay_cache[(robots, resources, costs)] = max_clay
  return max_clay

# initialize variables
input_file = "../../inputs/2022/input19.txt"
#input_file = "example19.txt"

blueprints = {}
PART1 = 0

# read input file
with open(input_file, 'r') as txtfile:
  txtfile_line = txtfile.readline()

  while txtfile_line:
    # parse
    txtfile_line = txtfile_line.strip()
    parsed_line = txtfile_line.split(" ")

    # process
    if PART1 or (len(blueprints) < 3):
      ore_robot_cost = int(parsed_line[6])
      clay_robot_cost = int(parsed_line[12])
      obs_robot_ore_cost = int(parsed_line[18])
      obs_robot_clay_cost = int(parsed_line[21])
      geode_robot_ore_cost = int(parsed_line[27])
      geode_robot_clay_cost = int(parsed_line[30])

      blueprints[parsed_line[1][:-1]] = (ore_robot_cost,
                                        clay_robot_cost,
                                        obs_robot_ore_cost,
                                        obs_robot_clay_cost,
                                        geode_robot_ore_cost,
                                        geode_robot_clay_cost)

    # read next line
    txtfile_line = txtfile.readline() 

print(blueprints)

sum_quality = 0
BFS = 0
DFS = 1
DP = 0
GREEDY = 0
max_geodes_list = []
part2_ans = 1
for b in blueprints:
  # BFS
  if BFS:
    print(f'BFS for blueprint {b}...')
    ore_robot_cost, clay_robot_cost, obs_robot_ore_cost, obs_robot_clay_cost, geode_robot_ore_cost, geode_robot_obs_cost = blueprints[b]
    queue = []
    visited = set()
    best_robots = (1, 0, 0, 0)
    best_resources = (0, 0, 0, 0)
    best_t = 24
    if PART1:
      queue.append(((0, 0, 0, 0), (1, 0, 0, 0), 24))
    else:
      queue.append(((0, 0, 0, 0), (1, 0, 0, 0), 32))
    max_geodes = 0
    max_possible_geodes = geode_upper_bound(0, 24, 0)
    print(max_possible_geodes)
    max_possible_geodes = 0
    while len(queue):
      resources, robots, t = queue[0]

      curr_ore, curr_clay, curr_obs, curr_geodes = resources
      ore_rbts, clay_rbts, obs_rbts, geode_rbts = robots

      if (curr_geodes > max_geodes):
        max_geodes = curr_geodes
        best_resources = resources
        best_robots = robots
        best_t = t
      elif (curr_geodes == max_geodes) and (geode_rbts >= best_robots[3]) and (t >= best_t):
        max_geodes = curr_geodes
        best_resources = resources
        best_robots = robots
        best_t = t

      if (t <= 0):
        queue.pop(0)
        continue

      curr_max_possible_geodes = geode_upper_bound(curr_geodes, t, geode_rbts)
      max_lowerbound_geodes = max_geodes + best_t*best_robots[3]
      print(f'Blueprint {b}, t = {t} with {len(queue)} queue, curr_max = {curr_max_possible_geodes}, max = {max_lowerbound_geodes}')
      if (max_lowerbound_geodes > curr_max_possible_geodes):
        queue.pop(0)
        print("continue")
        continue

      # throw away unnecessary resources
      max_ore_cost = max(ore_robot_cost, clay_robot_cost, obs_robot_ore_cost, geode_robot_ore_cost)
      max_clay_cost = obs_robot_clay_cost
      max_obs_cost = geode_robot_obs_cost
      if (curr_ore > t*max_ore_cost):
        curr_ore = t*max_ore_cost
      if (curr_clay > t*max_clay_cost):
        curr_clay = t*max_clay_cost
      if (curr_obs > t*max_obs_cost):
        curr_obs = t*max_obs_cost

      resources = (curr_ore, curr_clay, curr_obs, curr_geodes)

      if (resources, robots, t) in visited:
        queue.pop(0)
        continue

      # build geode robot
      if (curr_ore >= geode_robot_ore_cost) and (curr_obs >= geode_robot_obs_cost):
        future_resources = (curr_ore-geode_robot_ore_cost + ore_rbts,
                            curr_clay + clay_rbts,
                            curr_obs-geode_robot_obs_cost + obs_rbts,
                            curr_geodes + geode_rbts)
        future_robots = (ore_rbts, clay_rbts, obs_rbts, geode_rbts+1)
        if (t > 1):
          queue.append((future_resources, future_robots, t-1))
        else:
          max_geodes = max(max_geodes, curr_geodes + geode_rbts)
      elif (ore_rbts > 0) and (obs_rbts > 0):
        # wait to be able to build a geode robot
        wait_time = 0
        future_ore = curr_ore
        future_clay = curr_clay
        future_obs = curr_obs
        future_geodes = curr_geodes
        while (future_ore < geode_robot_ore_cost) or (future_obs < geode_robot_obs_cost):
          future_ore += ore_rbts
          future_clay += clay_rbts
          future_obs += obs_rbts
          future_geodes += geode_rbts
          wait_time += 1
        if (t-wait_time > 0):
          future_resources = (future_ore, future_clay, future_obs, future_geodes)
          queue.append((future_resources, robots, t-wait_time))

      # build obsidian robot unless it is already enough
      if (obs_rbts < max_obs_cost):
        if (curr_ore >= obs_robot_ore_cost) and (curr_clay >= obs_robot_clay_cost):
          future_resources = (curr_ore-obs_robot_ore_cost + ore_rbts,
                              curr_clay-obs_robot_clay_cost + clay_rbts,
                              curr_obs + obs_rbts,
                              curr_geodes + geode_rbts)
          future_robots = (ore_rbts, clay_rbts, obs_rbts+1, geode_rbts)
          if (t > 1):
            queue.append((future_resources, future_robots, t-1))
          else:
            max_geodes = max(max_geodes, curr_geodes + geode_rbts)
        elif (ore_rbts > 0) and (clay_rbts > 0):
          # wait to be able to build an obisidian robot
          wait_time = 0
          future_ore = curr_ore
          future_clay = curr_clay
          future_obs = curr_obs
          future_geodes = curr_geodes
          while (future_ore < obs_robot_ore_cost) or (future_clay < obs_robot_clay_cost):
            future_ore += ore_rbts
            future_clay += clay_rbts
            future_obs += obs_rbts
            future_geodes += geode_rbts
            wait_time += 1
          if (t-wait_time > 0):
            future_resources = (future_ore, future_clay, future_obs, future_geodes)
            queue.append((future_resources, robots, t-wait_time))

      # build clay robot, unless it is already enough
      if (clay_rbts < max_clay_cost):
        if (curr_ore >= clay_robot_cost):
          future_resources = (curr_ore-clay_robot_cost + ore_rbts,
                              curr_clay + clay_rbts,
                              curr_obs + obs_rbts,
                              curr_geodes + geode_rbts)
          future_robots = (ore_rbts, clay_rbts+1, obs_rbts, geode_rbts)
          if (t > 1):
            queue.append((future_resources, future_robots, t-1))
          else:
            max_geodes = max(max_geodes, curr_geodes + geode_rbts)
        else:
          # wait to be able to build a clay robot
          wait_time = 0
          future_ore = curr_ore
          future_clay = curr_clay
          future_obs = curr_obs
          future_geodes = curr_geodes
          while (future_ore < clay_robot_cost):
            future_ore += ore_rbts
            future_clay += clay_rbts
            future_obs += obs_rbts
            future_geodes += geode_rbts
            wait_time += 1
          if (t-wait_time > 0):
            future_resources = (future_ore, future_clay, future_obs, future_geodes)
            queue.append((future_resources, robots, t-wait_time))

      # build ore robot, unless it is already enough
      if (ore_rbts < max_ore_cost):
        if (curr_ore >= ore_robot_cost):
          future_resources = (curr_ore-ore_robot_cost + ore_rbts,
                              curr_clay + clay_rbts,
                              curr_obs + obs_rbts,
                              curr_geodes + geode_rbts)
          future_robots = (ore_rbts+1, clay_rbts, obs_rbts, geode_rbts)
          if (t > 1):
            queue.append((future_resources, future_robots, t-1))
          else:
            max_geodes = max(max_geodes, curr_geodes + geode_rbts)
        else:
          # wait to be able to build an ore robot
          wait_time = 0
          future_ore = curr_ore
          future_clay = curr_clay
          future_obs = curr_obs
          future_geodes = curr_geodes
          while (future_ore < ore_robot_cost):
            future_ore += ore_rbts
            future_clay += clay_rbts
            future_obs += obs_rbts
            future_geodes += geode_rbts
            wait_time += 1
          if (t-wait_time > 0):
            future_resources = (future_ore, future_clay, future_obs, future_geodes)
            queue.append((future_resources, robots, t-wait_time))

      # don't build, but explore branch only if it can still possibly beat the current best
      #if (curr_geodes + t*geode_rbts) >= (best_resources[3] + best_t*best_robots[3]):
      #  resources = (curr_ore + ore_rbts,
      #               curr_clay + clay_rbts,
      #               curr_obs + obs_rbts,
      #               curr_geodes + geode_rbts)
      #  robots = (ore_rbts, clay_rbts, obs_rbts, geode_rbts)
      #  if (t > 1):
      #    queue.append((resources, robots, t-1))
      #  else:
      #    max_geodes = max(max_geodes, curr_geodes + geode_rbts)
    
      visited.add((resources, robots, t)) 
      queue.pop(0)

    print(f'Resources: {best_resources})')
    print(f'Robots: {best_robots}')
    print(f't: {best_t}')
    print(max_geodes)
    max_geodes_list.append(max_geodes)
    sum_quality += int(b)*max_geodes
    part2_ans = part2_ans*max_geodes

  # DFS
  elif (DFS):
    print(f'DFS for blueprint {b}...')
    robots = (1, 0, 0, 0)
    resources = (0, 0, 0, 0)
    costs = blueprints[b]
    max_geodes = 0
    cache = set()
    if PART1:
      dfs(24, resources, robots, costs)
    else:
      dfs(32, resources, robots, costs)
    quality = int(b)*max_geodes
    print(quality)
    sum_quality += quality
    max_geodes_list.append(max_geodes)
    part2_ans = part2_ans*max_geodes
  # DP
  elif (DP):
    robots = (1, 0)
    resources = (0, 0)
    costs = (blueprints[b][0], blueprints[b][1])
    dp_clay(24, robots, resources, costs)
  # GREEDY
  elif (GREEDY):
    ore_rbt_cost, clay_rbt_cost, obs_rbt_ore_cost, obs_rbt_clay_cost, geode_rbt_ore_cost, geode_rbt_obs_cost  = blueprints[b]
    curr_ore = 0
    curr_clay = 0
    curr_obs = 0
    curr_geode = 0
    ore_rbts = 1
    clay_rbts = 0
    obs_rbts = 0
    geode_rbts = 0
    for t in range(24, 0, -1):
      prev_ore_rbts = ore_rbts
      prev_clay_rbts = clay_rbts
      prev_obs_rbts = obs_rbts
      prev_geode_rbts = geode_rbts

      # build
      #if (curr_obs >= geode_rbt_obs_cost):
      #  if (curr_ore >= geode_rbt_ore_cost):
      #    curr_ore -= geode_rbt_ore_cost
      #    curr_obs -= geode_rbt_obs_cost
      #    geode_rbts += 1
      #  else:
      #    # build/wait for ores
      #else:
      #  # build obsidian robots if obsidian is bottleneck
      #  if (curr_clay >= obs_rbt_clay_cost):
      #    if (curr_ore >= obs_rbt_ore_cost):
      #      curr_ore -= obs_rbt_ore_cost
      #      curr_clay -= obs_rbt_clay_cost
      #      obs_rbts += 1
      #  else:
      #    # build clay robots if clay is bottleneck

      # mine
      curr_ore += prev_ore_rbts
      curr_clay += prev_clay_rbts
      curr_obs += prev_obs_rbts
      curr_geode += prev_geode_rbts
      if (b == '1'):
        print((curr_ore, curr_clay, curr_obs, curr_geode))

    quality = curr_geode*int(b)
    print(quality)
    sum_quality = sum_quality + quality
  
#pretty_print = pprint.PrettyPrinter()
#pretty_print.pprint()

# print answer
print(max_geodes_list)
ans1 = sum_quality
ans2 = part2_ans
print("First star: %d" % (ans1))
print("Second star: %d" % (ans2))
