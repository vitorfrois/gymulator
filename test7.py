from threading import Semaphore, Thread
import time
from random import randint, choice
from bcolors import bcolors
from rich.progress import track, Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Console

table = Progress(
    "{task.description}"
    )

def using_machine(machine, qtt, total):
    for task in table.tasks:
        if machine in task.description:
            task.description = machine + " " + str(qtt) \
         + " / " + str(total)
    return table

progress_table.add_row(
    Panel.fit(table, width=30, title="Available Machines", border_style="red")
)

def init_live():
    with live:
        while playing:
            time.sleep(1)
            for job in job_progress.tasks:
                if not job.finished:
                    job_progress.advance(job.id, advance=0.5)
                else:
                    job_progress.remove_task(job.id)
                    #live.update(generate_table())

# table.update(using_machine(machine, semaphore._value, n_machines))


