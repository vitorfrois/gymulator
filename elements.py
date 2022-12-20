from bcolors import bcolors
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

REP_INTERVAL = 2 # seconds
playing = True

job_progress = Progress(
    "{task.description}",
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)

table = Progress(
    "{task.description}"
    )

level_table = Progress(
    "{task.description}"
)


console = Table().grid()
consoleExc = Table().grid()
consoleFim = Table().grid()

progress_table = Table(expand=False).grid()
progress_table.add_row(
    Panel.fit("G Y M U L A T O R"),
    Panel.fit(level_table, width=50, title="[b]Level", border_style="green")
)

progress_table.add_row(
    Panel.fit(job_progress, width=50, title="[b]Training", border_style="red"),
    Panel.fit(table, width=50, title="[b]Available Machines", border_style="red"),
)
progress_table.add_row(
    Panel.fit(console, width=50, title="[b]Start Log", border_style="yellow"),
    Panel.fit(consoleExc, width=50, title="[b]Finish Log", border_style="yellow")
)

def generate_bar(person='Pessoa', reps=5, machine='MachineName') -> Progress:
    # job_progress.add_task("[green]Cooking")
    job_progress.add_task(f"{person} using {machine} ", total=reps, visible=True)
    return job_progress

def recreate_table(available_machines, n_machines, semaphores):
    for task in table.tasks:
        table.remove_task(task.id)
    for elem in available_machines:
        table.add_task(elem.replace("_", " ") + " " + str(semaphores[elem]._value) + " / " + str(n_machines[elem]))
    return table 

def update_level_table(level):
    for task in level_table.tasks:
        level_table.remove_task(task.id)
    level_table.add_task(f" {level} ", total=level)
    return level_table

def init_live():
    startTask = False
    live = Live(progress_table, refresh_per_second=10)
    with live:
        while playing and (len(job_progress.tasks) > 0 or not startTask):
            time.sleep(REP_INTERVAL)
            for job in job_progress.tasks:
                startTask = True
                if not job.finished:
                    job_progress.advance(job.id, advance=1)
                else:
                    job_progress.remove_task(job.id)
