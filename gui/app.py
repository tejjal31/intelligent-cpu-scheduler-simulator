# GUI Application for Intelligent CPU Scheduler Simulator
# Built using CustomTkinter for cross-platform compatibility

import customtkinter as ctk
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scheduler.fcfs import fcfs
from scheduler.sjf import sjf
from scheduler.round_robin import round_robin
from scheduler.priority import priority_scheduling

# Color palette for Gantt chart bars
COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']

process_entries = []

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def on_algorithm_change(choice):
    # Show Time Quantum only for Round Robin
    if choice == "Round Robin":
        tq_label.grid()
        tq_entry.grid()
    else:
        tq_label.grid_remove()
        tq_entry.grid_remove()
    refresh_process_table()

def refresh_process_table():
    # Clear existing table
    for widget in table_frame.winfo_children():
        widget.destroy()
    process_entries.clear()

    algo = algo_var.get()

    # Set headers based on algorithm
    headers = ["Process", "Arrival Time", "Burst Time"]
    if algo == "Priority Scheduling":
        headers.append("Priority")

    for j, h in enumerate(headers):
        ctk.CTkLabel(table_frame, text=h, font=("Arial", 12, "bold"),
                     width=130).grid(row=0, column=j, padx=5, pady=5)

    # Add 3 default process rows
    for i in range(3):
        add_process_row(i + 1)

def add_process_row(num=None):
    algo = algo_var.get()
    row = len(process_entries) + 1
    if num is None:
        num = row

    ctk.CTkLabel(table_frame, text=f"P{num}",
                 font=("Arial", 12, "bold"),
                 width=130).grid(row=row, column=0, padx=5, pady=4)

    arrival = ctk.CTkEntry(table_frame, width=130, font=("Arial", 12), justify='center')
    arrival.grid(row=row, column=1, padx=5, pady=4)

    burst = ctk.CTkEntry(table_frame, width=130, font=("Arial", 12), justify='center')
    burst.grid(row=row, column=2, padx=5, pady=4)

    priority = None
    if algo == "Priority Scheduling":
        priority = ctk.CTkEntry(table_frame, width=130, font=("Arial", 12), justify='center')
        priority.grid(row=row, column=3, padx=5, pady=4)

    process_entries.append((arrival, burst, priority))

def run_scheduler():
    processes = []
    algo = algo_var.get()

    if not algo or algo == "Select Algorithm":
        messagebox.showerror("Error", "Please select an algorithm first!")
        return

    try:
        for i, entry in enumerate(process_entries):
            arrival_val = entry[0].get().strip()
            burst_val = entry[1].get().strip()

            # Skip empty rows
            if not arrival_val and not burst_val:
                continue
            if not arrival_val or not burst_val:
                messagebox.showerror("Error", f"Please fill all fields for P{i+1}!")
                return

            arrival = int(arrival_val)
            burst = int(burst_val)
            name = f"P{i+1}"

            if algo == "Priority Scheduling":
                p_val = entry[2].get().strip()
                if not p_val:
                    messagebox.showerror("Error", f"Enter priority for P{i+1}!")
                    return
                processes.append([name, arrival, burst, int(p_val)])
            else:
                processes.append([name, arrival, burst])

        if not processes:
            messagebox.showerror("Error", "Enter at least one process!")
            return

        # Run selected algorithm
        if algo == "FCFS":
            results, gantt, avg_wt, avg_tat, avg_rt, cpu_util, throughput = fcfs(processes)
        elif algo == "SJF":
            results, gantt, avg_wt, avg_tat, avg_rt, cpu_util, throughput = sjf(processes)
        elif algo == "Round Robin":
            q = tq_entry.get().strip()
            if not q:
                messagebox.showerror("Error", "Enter Time Quantum!")
                return
            results, gantt, avg_wt, avg_tat, avg_rt, cpu_util, throughput = round_robin(processes, int(q))
        elif algo == "Priority Scheduling":
            results, gantt, avg_wt, avg_tat, avg_rt, cpu_util, throughput = priority_scheduling(processes)

        show_results(results, avg_wt, avg_tat, avg_rt, cpu_util, throughput)
        draw_gantt(gantt)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers only!")

def show_results(results, avg_wt, avg_tat, avg_rt, cpu_util, throughput):
    # Clear previous results
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Results heading
    ctk.CTkLabel(result_frame, text="📊 Results",
                 font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=7, pady=8)

    # Table headers
    headers = ["Process", "Arrival Time", "Burst Time", "Completion Time", "Waiting Time", "Turnaround Time", "Response Time"]
    for j, h in enumerate(headers):
        ctk.CTkLabel(result_frame, text=h, font=("Arial", 10, "bold"),
                     width=110).grid(row=1, column=j, padx=2, pady=2)

    # Table rows
    for i, r in enumerate(results):
        values = [r['name'], r['arrival'], r['burst'],
                  r['finish'], r['waiting'], r['turnaround'], r['response']]
        for j, val in enumerate(values):
            ctk.CTkLabel(result_frame, text=str(val),
                        font=("Arial", 11), width=110).grid(row=i+2, column=j, padx=2, pady=2)

    # Performance metrics
    n = len(results)
    ctk.CTkLabel(result_frame,
                 text=f"Avg Waiting Time: {avg_wt:.2f}",
                 font=("Arial", 11, "bold"),
                 text_color="#FF6B6B").grid(row=n+2, column=0, columnspan=2, pady=8)

    ctk.CTkLabel(result_frame,
                 text=f"Avg Turnaround Time: {avg_tat:.2f}",
                 font=("Arial", 11, "bold"),
                 text_color="#4ECDC4").grid(row=n+2, column=2, columnspan=2, pady=8)

    ctk.CTkLabel(result_frame,
                 text=f"Avg Response Time: {avg_rt:.2f}",
                 font=("Arial", 11, "bold"),
                 text_color="#FFEAA7").grid(row=n+2, column=4, columnspan=2, pady=8)

    ctk.CTkLabel(result_frame,
                 text=f"CPU Utilization: {cpu_util:.2f}%",
                 font=("Arial", 11, "bold"),
                 text_color="#96CEB4").grid(row=n+3, column=0, columnspan=2, pady=4)

    ctk.CTkLabel(result_frame,
                 text=f"Throughput: {throughput:.2f} p/unit",
                 font=("Arial", 11, "bold"),
                 text_color="#DDA0DD").grid(row=n+3, column=2, columnspan=2, pady=4)

def draw_gantt(gantt):
    # Draw Gantt chart using matplotlib
    plt.close('all')
    fig, ax = plt.subplots(figsize=(12, 3))
    fig.patch.set_facecolor('#2C3E50')
    ax.set_facecolor('#34495E')

    for idx, (name, start, finish) in enumerate(gantt):
        color = COLORS[idx % len(COLORS)]
        ax.broken_barh([(start, finish - start)], (10, 8),
                       facecolors=color, edgecolors='white', linewidth=1.5)
        ax.text((start + finish) / 2, 14, name,
                ha='center', va='center', color='white',
                fontsize=10, fontweight='bold')
        ax.text(start, 9, str(start),
                ha='center', color='white', fontsize=8)

    if gantt:
        ax.text(gantt[-1][2], 9, str(gantt[-1][2]),
                ha='center', color='white', fontsize=8)

    ax.set_xlim(0, max(g[2] for g in gantt) + 1)
    ax.set_ylim(0, 25)
    ax.set_xlabel("Time", color='white')
    ax.set_title("Gantt Chart", color='white', fontsize=13, fontweight='bold')
    ax.tick_params(colors='white')
    ax.yaxis.set_visible(False)
    plt.tight_layout()
    plt.show()

# ── Main Window ─────────────────────────────────────────────────────
root = ctk.CTk()
root.title("Intelligent CPU Scheduler Simulator")
root.geometry("900x720")

# Title
ctk.CTkLabel(root, text="🖥️ Intelligent CPU Scheduler Simulator",
             font=("Arial", 20, "bold")).pack(pady=15)

# Algorithm Selection Row
top_frame = ctk.CTkFrame(root, fg_color="transparent")
top_frame.pack(pady=5)

ctk.CTkLabel(top_frame, text="Select Algorithm:",
             font=("Arial", 13)).grid(row=0, column=0, padx=10)

algo_var = ctk.StringVar()
algo_menu = ctk.CTkOptionMenu(top_frame, variable=algo_var,
                               values=["FCFS", "SJF", "Round Robin", "Priority Scheduling"],
                               command=on_algorithm_change,
                               font=("Arial", 12), width=220)
algo_menu.grid(row=0, column=1, padx=10)
algo_menu.set("Select Algorithm")

# Time Quantum — hidden by default
tq_label = ctk.CTkLabel(top_frame, text="Time Quantum:", font=("Arial", 13))
tq_label.grid(row=0, column=2, padx=10)
tq_label.grid_remove()

tq_entry = ctk.CTkEntry(top_frame, width=60, font=("Arial", 12))
tq_entry.insert(0, "2")
tq_entry.grid(row=0, column=3, padx=5)
tq_entry.grid_remove()

# Process Table
table_frame = ctk.CTkFrame(root, fg_color="transparent")
table_frame.pack(pady=10)

ctk.CTkLabel(table_frame, text="← Please select an algorithm first",
             font=("Arial", 13), text_color="gray").grid(row=0, column=0, pady=20)

# Buttons
btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(pady=8)

ctk.CTkButton(btn_frame, text="+ Add Process",
              command=lambda: add_process_row(),
              width=170, height=40,
              font=("Arial", 12)).grid(row=0, column=0, padx=15)

ctk.CTkButton(btn_frame, text="▶ Run Scheduler",
              command=run_scheduler,
              width=170, height=40,
              fg_color="#27AE60", hover_color="#1E8449",
              font=("Arial", 12)).grid(row=0, column=1, padx=15)

# Results Area
result_frame = ctk.CTkFrame(root, fg_color="transparent")
result_frame.pack(pady=10)

root.mainloop()
