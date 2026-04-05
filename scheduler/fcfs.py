# FCFS Scheduling Algorithm
# First Come First Serve - processes are executed in order of arrival

def fcfs(processes):
    # processes = list of [name, arrival_time, burst_time]

    # Sort processes by arrival time
    processes.sort(key=lambda x: x[1])

    # Initialize variables
    current_time = 0      # Tracks current CPU time
    results = []          # Stores result for each process
    gantt = []            # Stores data for Gantt chart

    # Process each task one by one
    for process in processes:
        name = process[0]          # Process name (P1, P2...)
        arrival = process[1]       # Arrival time
        burst = process[2]         # Burst time (execution time needed)

        # If CPU is idle, jump to process arrival time
        if current_time < arrival:
            current_time = arrival

        start_time = current_time            # Process start time
        finish_time = current_time + burst   # Process finish time

        waiting_time = start_time - arrival           # Time spent waiting
        turnaround_time = finish_time - arrival       # Total time from arrival to finish
        response_time = start_time - arrival          # First time process got CPU

        # Record for Gantt chart
        gantt.append((name, start_time, finish_time))

        # Store all results for this process
        results.append({
            'name': name,
            'arrival': arrival,
            'burst': burst,
            'finish': finish_time,
            'waiting': waiting_time,
            'turnaround': turnaround_time,
            'response': response_time
        })

        # Move current time forward
        current_time = finish_time

    # Calculate average metrics
    avg_waiting = sum(r['waiting'] for r in results) / len(results)
    avg_turnaround = sum(r['turnaround'] for r in results) / len(results)
    avg_response = sum(r['response'] for r in results) / len(results)

    # Calculate CPU Utilization
    total_time = results[-1]['finish'] - results[0]['arrival']
    busy_time = sum(r['burst'] for r in results)
    cpu_utilization = (busy_time / total_time) * 100 if total_time > 0 else 100

    # Calculate Throughput
    throughput = len(results) / total_time if total_time > 0 else 0

    return results, gantt, avg_waiting, avg_turnaround, avg_response, cpu_utilization, throughput