# Round Robin Scheduling Algorithm
# Each process gets a fixed time slice (quantum) in cyclic order

def round_robin(processes, quantum):
    # processes = list of [name, arrival_time, burst_time]
    # quantum = fixed time slice for each process

    # Sort by arrival time
    processes.sort(key=lambda x: x[1])

    n = len(processes)
    remaining = [p[2] for p in processes]   # Remaining burst time
    current_time = 0
    results = []
    gantt = []

    finish_times = [0] * n
    response_times = [-1] * n   # First time each process got CPU
    visited = [False] * n
    completed = 0
    queue = []

    # Add first process to queue
    queue.append(0)
    visited[0] = True

    while completed < n:
        if queue:
            idx = queue.pop(0)

            # Record response time - first time process got CPU
            if response_times[idx] == -1:
                response_times[idx] = current_time - processes[idx][1]

            # Execute for quantum or remaining time
            exec_time = min(quantum, remaining[idx])
            gantt.append((processes[idx][0], current_time, current_time + exec_time))
            current_time += exec_time
            remaining[idx] -= exec_time

            # Add newly arrived processes to queue
            for j in range(n):
                if processes[j][1] <= current_time and not visited[j]:
                    queue.append(j)
                    visited[j] = True

            if remaining[idx] == 0:
                finish_times[idx] = current_time
                completed += 1
            else:
                queue.append(idx)

        else:
            current_time += 1
            for j in range(n):
                if processes[j][1] <= current_time and not visited[j]:
                    queue.append(j)
                    visited[j] = True

    # Calculate results
    for idx in range(n):
        arrival = processes[idx][1]
        burst = processes[idx][2]
        finish = finish_times[idx]
        turnaround = finish - arrival
        waiting = turnaround - burst

        results.append({
            'name': processes[idx][0],
            'arrival': arrival,
            'burst': burst,
            'finish': finish,
            'waiting': waiting,
            'turnaround': turnaround,
            'response': response_times[idx]
        })

    # Calculate averages
    avg_waiting = sum(r['waiting'] for r in results) / len(results)
    avg_turnaround = sum(r['turnaround'] for r in results) / len(results)
    avg_response = sum(r['response'] for r in results) / len(results)

    # Calculate CPU Utilization
    total_time = max(finish_times) - processes[0][1]
    busy_time = sum(r['burst'] for r in results)
    cpu_utilization = (busy_time / total_time) * 100 if total_time > 0 else 100

    # Calculate Throughput
    throughput = len(results) / total_time if total_time > 0 else 0

    return results, gantt, avg_waiting, avg_turnaround, avg_response, cpu_utilization, throughput