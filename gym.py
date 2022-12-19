from threading import Semaphore, Thread
import time
from random import randint, choice
from bcolors import bcolors
from rich.progress import track, Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Console

playing = True

job_progress = Progress(
    "{task.description}",
    # SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)

table = Progress(
    "{task.description}"
    )

def generate_bar(person='Pessoa', reps=5) -> Progress:
    # job_progress.add_task("[green]Cooking")
    job_progress.add_task(f"{person} treinando... ", total=reps, visible=True)
    return job_progress

def recreate_table(available_machines, n_machines) -> Progress:
    for task in table.tasks:
        table.remove_task(task)
    for elem in available_machines:
        table.add_task(elem + " " + 
            str(n_machines[elem]) + "/" + 
            str(available_machines[elem]))
    return table

console = Table().grid()

progress_table = Table(expand=False).grid()
progress_table.add_row(
    Panel.fit("GYMULATOR"),
    Panel.fit(table, width=30, title="Available Machines", border_style="red")
)
progress_table.add_row(
    Panel.fit(job_progress, width=50, title="[b]Jobs", border_style="red"),
    # Panel.fit(console, width=80, title="[b]Log", border_style="red")
)

live = Live(progress_table, refresh_per_second=10)


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
class Gym:
    def __init__(self):
        self.available_machines = [
            "leg_press", 
            "bench_press"
        ]

        self.n_machines: dict[str, int] = {}

        self.semaphores: dict[str, Semaphore] = {}

        # Initial machines
        self.n_machines['leg_press'] = 1
        self.n_machines['bench_press'] = 2

        self.semaphores['leg_press'] = Semaphore(self.n_machines['leg_press'])
        self.semaphores['bench_press'] = Semaphore(self.n_machines['bench_press'])

        thread = Thread(target=init_live)
        thread.start()

    def start_training(self, person_name: str):
        # This will be the target for maromba's thread. It should execute various
        # exercises during the existence of that maromba.
        n_exercices = randint(1, len(self.available_machines))
        # print(bcolors.WARNING + f"{person_name} has just started and will be doing {n_exercices} exercises." + bcolors.ENDC)
        console.add_row(f"{person_name} has just started and will be doing {n_exercices} exercises.")

        for _ in range(n_exercices):
            machine = choice(self.available_machines)
            # print(bcolors.OKBLUE + f"{person_name} wants to use {machine}!" + bcolors.ENDC)
            console.add_row(f"{person_name} wants to use {machine}!")
            
            exercise = Thread(target=self.use_machine , args=(machine, person_name,))
            exercise.start()
        # console = Table()


    def use_machine(self, machine: str, person_name: str):
        if machine not in self.n_machines:
            raise KeyError("Unknown machine!")

        n_machines = self.n_machines[machine]
        semaphore = self.semaphores[machine]

        display_name = machine.replace("_", " ").title()

        semaphore.acquire() # Lock machine, someone is using it

        reps = randint(2, 4)
        
        # print(f"{person_name} will be doing {reps} reps of {display_name}", end='\t')
        # print(f"{semaphore._value}/{n_machines} available.")
        console.add_row(f"{person_name} will be doing {reps} reps of {display_name}")
        console.add_row(f"{semaphore._value}/{n_machines} available.")
        
        
        try:
            job_progress.update(generate_bar(person_name, reps))
            table.update(recreate_table(self.available_machines, self.n_machines))
        except:
            pass

        for _ in range(reps):
            time.sleep(0.2)

        semaphore.release()

        try:
            table.update(recreate_table(self.available_machines, self.n_machines))
        except:
            pass

        # print(f"{person_name} has finished using {display_name}", end='\t\t')
        # print(f"{semaphore._value}/{n_machines} available.")
        console.add_row(f"{person_name} has finished using {display_name}")
        console.add_row(f"{semaphore._value}/{n_machines} available.")

