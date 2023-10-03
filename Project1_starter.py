import re
from datetime import datetime, timedelta

def string_to_time_object(time_str):
    return datetime.strptime(time_str, '%H:%M')

def time_object_to_string(time_obj):
    return time_obj.strftime('%H:%M')

# Bubble sort algorithm to sort the merged algorithm 
def sort_and_merge(sched1, sched2):
    merged_arry = sched1 + sched2

    for i in range(len(merged_arry)-1):
        for j in range(0, len(merged_arry)-i-1):
            # Convert to time objects to compare the time
            time_place_1 = string_to_time_object(merged_arry[j][0])
            time_place_2 = string_to_time_object(merged_arry[j + 1][0])

            if time_place_1 > time_place_2:
                # Swap places if larger.
                merged_arry[j], merged_arry[j+1] = merged_arry[j+1], merged_arry[j]

    return merged_arry
            

# Main Algorithm
def find_meeting_schedule(person1_busy_schedule, person1_work_hours, person2_busy_Schedule, person2_work_hours, duration_of_meeting):
    p1_work_start, p1_work_end = string_to_time_object(person1_work_hours[0]), string_to_time_object(person1_work_hours[1])
    p2_work_start, p2_work_end = string_to_time_object(person2_work_hours[0]), string_to_time_object(person2_work_hours[1])
        

    # Combine busy schedules of both persons and sort using the first time in the time slot.
    unavailability_sched = sort_and_merge(person1_busy_schedule, person2_busy_Schedule)

    # Initialize the available time slots list
    available_slots = []

    # Set the starting current time to the person who starts work the latest.
    curr_time = max(p1_work_start, p2_work_start)

    for busy_start_time, busy_end_time in unavailability_sched:
        # Convert the current iteration variables to time objects
        busy_start_time = string_to_time_object(busy_start_time)
        busy_end_time = string_to_time_object(busy_end_time)

        # Check if current time is less than the start time
        if curr_time < busy_start_time:
            # If it is, find the minimum available end
            avail_end = min(busy_start_time, p1_work_end, p2_work_end)
            # If the available end - current time is greater or equal to the duration of meeting
            # then append it to the available_slots
            if (avail_end - curr_time) >= timedelta(minutes=duration_of_meeting):
                available_slots.append([time_object_to_string(curr_time), time_object_to_string(avail_end)])
            # If not, then set the end time of that slot to current time to indicate to keep going throughout the day.
            curr_time = busy_end_time
        # If the current time is less than the busy start time, check if the current time is larger 
        # or equal too the busy end time, if it is then skip.
        elif curr_time >= busy_end_time:
            continue
        # If curr_time is not smaller than busy start time or bigger than busy end time, then set it equal
        # to busy end time to continue passing the time.
        else:
            curr_time = busy_end_time

    # This part is to catch the end time of the shift at the end of the day.
    # First find the minimum end time of both people.
    total_end =  min(p1_work_end, p2_work_end)
    # Check if current time is less than the total end
    if curr_time < total_end:
        # If the total end minus current time is large enough for a meeting, then add it to the available slots.
        if (total_end - curr_time) >= timedelta(minutes=duration_of_meeting):
             available_slots.append([time_object_to_string(curr_time), time_object_to_string(total_end)])

    return available_slots

# Read input from a text file
with open('input.txt', 'r') as file:
    lines = file.readlines()

# Main Loop, parse all lines of the input, it should not count towards final time of the actual algorithm.
i = 0
with open('output.txt', 'w') as file2:
    while i < len(lines):

        if lines[i] == "\n":
            i += 1
            
        person1_busy_schedule = eval(re.sub(r"':'", "','", lines[i]))
        person1_work_hours = eval(lines[i+1])
        person2_busy_Schedule = eval(re.sub(r"':'", "','", lines[i+2]))
        person2_work_hours = eval(lines[i+3])
        duration_of_meeting = int(lines[i+4])
        i += 5

        # Call algorithm for the given input
        meeting_schedule = find_meeting_schedule(person1_busy_schedule, person1_work_hours, person2_busy_Schedule, person2_work_hours, duration_of_meeting)

        file2.write(f'Input:\n{person1_busy_schedule}\n{person1_work_hours}\n{person2_busy_Schedule}\n{person2_work_hours}\n{duration_of_meeting}\n\nOutput:\n{meeting_schedule}\n\n')
