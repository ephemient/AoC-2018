# --- Day 4: Repose Record ---
# You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

# As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

# For example, consider the following records, which have already been organized into chronological order:

# [1518-11-01 00:00] Guard #10 begins shift
# [1518-11-01 00:05] falls asleep
# [1518-11-01 00:25] wakes up
# [1518-11-01 00:30] falls asleep
# [1518-11-01 00:55] wakes up
# [1518-11-01 23:58] Guard #99 begins shift
# [1518-11-02 00:40] falls asleep
# [1518-11-02 00:50] wakes up
# [1518-11-03 00:05] Guard #10 begins shift
# [1518-11-03 00:24] falls asleep
# [1518-11-03 00:29] wakes up
# [1518-11-04 00:02] Guard #99 begins shift
# [1518-11-04 00:36] falls asleep
# [1518-11-04 00:46] wakes up
# [1518-11-05 00:03] Guard #99 begins shift
# [1518-11-05 00:45] falls asleep
# [1518-11-05 00:55] wakes up
# Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

# Visually, these records show that the guards are asleep at these times:

# Date   ID   Minute
#             000000000011111111112222222222333333333344444444445555555555
#             012345678901234567890123456789012345678901234567890123456789
# 11-01  #10  .....####################.....#########################.....
# 11-02  #99  ........................................##########..........
# 11-03  #10  ........................#####...............................
# 11-04  #99  ....................................##########..............
# 11-05  #99  .............................................##########.....
# The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

# Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

# If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

# Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

# In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

# While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

# What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)

from collections import Counter, defaultdict
import operator

with open('day4.txt') as puzzle_file:
    puzzle_input = sorted(line.strip() for line in puzzle_file)

def organize_by_day(entries):
    logs_by_day = []
    day_log = []
    for entry in entries:
        if 'Guard' in entry and day_log:
            logs_by_day.append(day_log)
            day_log = []
        day_log.append(entry)
    if day_log:
        logs_by_day.append(day_log)
    return logs_by_day

def organize_by_guard(entries_by_day):
    guard_sleep_logs = defaultdict(list)
    for day in entries_by_day:
        guard = int(day[0].split()[3].lstrip('#'))
        for entry in day[1:]:
            guard_sleep_logs[guard].append(int(entry[15:17]))
    return guard_sleep_logs

def find_guard_mins_asleep(guards):
    guards_mins_asleep = {}
    for guard, times in guards.items():
        guards_mins_asleep[guard] = sum(end - start for start, end in zip(times[0::2], times[1::2]))
    return guards_mins_asleep

def find_guard_most_asleep(guards):
    return max(guards.items(), key=operator.itemgetter(1))

def find_min_most_likely_asleep(times):
    counter = Counter()
    for start, end in zip(times[0::2], times[1::2]):
        counter.update(range(start, end))
    return next(iter(counter.most_common(1)), (0, 0))

guards_sleep_logs = organize_by_guard(organize_by_day(puzzle_input))
guards_mins_asleep = find_guard_mins_asleep(guards_sleep_logs)
guard_of_choice, mins_asleep = find_guard_most_asleep(guards_mins_asleep)
min_of_choice, times_asleep = find_min_most_likely_asleep(guards_sleep_logs[guard_of_choice])

print guard_of_choice * min_of_choice # Your puzzle answer was 12504.

# --- Part Two ---
# Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

# In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

# What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)

def strategy_2(guard_log):
    guard_of_choice = None
    min_of_choice = None
    times_asleep = 0
    for guard, sleep_log in guard_log.items():
        minute, times = find_min_most_likely_asleep(sleep_log)
        if times > times_asleep:
            times_asleep = times
            guard_of_choice = guard
            min_of_choice = minute
    return guard_of_choice * min_of_choice
        
print strategy_2(guards_sleep_logs) # Your puzzle answer was 139543.
