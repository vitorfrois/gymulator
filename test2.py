"""
Demonstrates the use of multiple Progress instances in a single Live display.    
"""

from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
import asyncio



async def printar():
    print("teste1")
    print("teste2")


async def chamar_barra():
    with Live(progress_table, refresh_per_second=10):
        while not overall_progress.finished:
            sleep(0.1)
            for job in job_progress.tasks:
                if not job.finished:
                    job_progress.advance(job.id)

            completed = sum(task.completed for task in job_progress.tasks)
            overall_progress.update(overall_task, completed=completed)

def create_track(reps, maromba):
    for step in track(range(reps*4)):
        time.sleep(0.5)

job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )

n = int(input(""))
jobs = []
for i in range(n):
    jobs.append(job_progress.add_task("[green]Maromba" + str(i)))

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))

progress_table = Table.grid()
progress_table.add_row(
    Panel.fit(
        overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)
    ),
    Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
)

async def main():
    await chamar_barra()
    await printar()

asyncio.run(main())