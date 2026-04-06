# SJF Scheduling Algorithm
# Shortest Job First - process with smallest burst time executes first
# This is Non-Preemptive SJF

def sjf(processes):
    # processes = list of [name, arrival_time, burst_time]

    n = len(processes)
    completed = []
    results = []
    gantt = []
    current_time = 0
    visited = [False] * n

    # Keep running until all processes are completed
    while len(completed) < n:

        # Find all processes that have arrived by current time
        available = []
        for i in range(n):
            if processes[i][1] <= current_time and not visited[i]:
                available.append((processes[i][2], i))

        if available:
            # Pick process with shortest burst time
            available.sort()
            shortest = available[0][1]

            name = processes[shortest][0]
            arrival = processes[shortest][1]
            burst = processes[shortest][2]

            start_time = current_time
            finish_time = current_time + burst
            waiting_time = start_time - arrival
            turnaround_time = finish_time - arrival
            response_time = start_time - arrival

            gantt.append((name, start_time, finish_time))

            results.append({
                'name': name,
                'arrival': arrival,
                'burst': burst,
                'finish': finish_time,
                'waiting': waiting_time,
                'turnaround': turnaround_time,
                'response': response_time
            })

            visited[shortest] = True
            completed.append(shortest)
            current_time = finish_time

        else:
            # CPU idle, move time forward
            current_time += 1

    # Calculate averages
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