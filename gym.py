from threading import Semaphore, Thread
import time
from random import randint, choice
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

level = Progress(
    "Level: ",
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)


console = Table().grid()
consoleExc = Table().grid()
consoleFim = Table().grid()

progress_table = Table(expand=False).grid()
progress_table.add_row(
    Panel.fit("G Y M U L A T O R"),
    # Panel.fit(level, width=50, title="[b]Level", border_style="red")
)

progress_table.add_row(
    Panel.fit(job_progress, width=50, title="[b]Jobs", border_style="red"),
    Panel.fit(table, width=50, title="Available Machines", border_style="red"),
)
progress_table.add_row(
    Panel.fit(console, width=50, title="[b]People Started", border_style="yellow"),
    Panel.fit(consoleExc, width=50, title="[b]Console Exercise", border_style="yellow")
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

class Gym:
    def __init__(self):
        self.available_machines = [
            "Leg_press", 
            "Bench_press",
            "Pulley",
            "Squat",
            "Leg_extension",
            "Scott_machine",
            "Pulldown",
            "Treadmill",
            "Bike",
        ]

        self.n_machines: dict[str, int] = {}

        self.semaphores: dict[str, Semaphore] = {}

        # Initial machines
        self.n_machines['Leg_press'] = 1
        self.n_machines['Bench_press'] = 2
        self.n_machines['Pulley'] = 2
        self.n_machines['Squat'] = 2
        self.n_machines['Leg_extension'] = 1
        self.n_machines['Scott_machine'] = 1
        self.n_machines['Pulldown'] = 2
        self.n_machines['Treadmill'] = 4
        self.n_machines['Bike'] = 4

        for machine in self.available_machines:
            self.semaphores[machine] = Semaphore(self.n_machines[machine])

        try:
            table.update(recreate_table(self.available_machines, self.n_machines, self.semaphores))
        except:
            pass

        thread = Thread(target=init_live)
        thread.start()

        self.level = 1

    def uplevel(self):
        self.level += 1
        for machine in self.n_machines:
            machine += random.randint(1)

    def start_training(self, person_name: str):
        # This will be the target for maromba's thread. It should execute various
        # exercises during the existence of that maromba.
        n_exercices = randint(1, int(len(self.available_machines)/3))
        console.add_row(f"{person_name} has just started and will be doing {n_exercices} exercises.")

        for _ in range(n_exercices):
            machine = choice(self.available_machines)
            console.add_row(f"{person_name} wants to use {machine}!")
            
            exercise = Thread(target=self.use_machine , args=(machine, person_name,))
            exercise.start()
            exercise.join()

    def use_machine(self, machine: str, person_name: str):
        if machine not in self.n_machines:
            raise KeyError("Unknown machine!")

        n_machines = self.n_machines[machine]
        semaphore = self.semaphores[machine]

        display_name = machine.replace("_", " ").title()

        semaphore.acquire() # Lock machine, someone is using it

        reps = randint(2, 4)
        
        # consoleExc.add_row(f"{person_name} will be doing {reps} reps of {display_name}")
        
        try:
            table.update(recreate_table(self.available_machines, self.n_machines, self.semaphores))
        except:
            pass

        try:
            job_progress.update(generate_bar(person_name, reps, display_name))
        except:
            pass

        for _ in range(reps):
            time.sleep(REP_INTERVAL)

        semaphore.release()

        try:
            table.update(recreate_table(self.available_machines, self.n_machines, self.semaphores))
        except:
            pass

        consoleExc.add_row(f"{person_name} finished using {display_name}")
