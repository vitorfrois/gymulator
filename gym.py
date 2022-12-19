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
    # SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)

table = Progress(
    "{task.description}"
    )

def generate_bar(person='Pessoa', reps=5, machine='MachineName') -> Progress:
    # job_progress.add_task("[green]Cooking")
    job_progress.add_task(f"{person} using {machine} ", total=reps, visible=True)
    return job_progress

console = Table()

progress_table = Table(expand=False).grid()
progress_table.add_row(
    Panel.fit("GYMULATOR")
)

progress_table.add_row(
    Panel.fit(job_progress, width=50, title="[b]Jobs", border_style="red"),
    Panel.fit(table, width=30, title="Available Machines", border_style="red"),
)
progress_table.add_row(
    Panel.fit(console, width=80, title="[b]Log", border_style="red")
)


def recreate_table(available_machines, n_machines, semaphores):
    print(available_machines)
    print(n_machines)
    print(semaphores, "\n\n")
    for task in table.tasks:
        table.remove_task(task)
    for elem in available_machines:
        table.add_task(elem + " " + str(semaphores[elem]._value) + " / " + str(n_machines[elem]))
    return table
               

def init_live():
    live = Live(progress_table, refresh_per_second=10)
    with live:
        while playing:
            time.sleep(REP_INTERVAL)
            for job in job_progress.tasks:
                if not job.finished:
                    job_progress.advance(job.id, advance=1)
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

        try:
            table.update(recreate_table(self.available_machines, self.n_machines, self.semaphores))
        except:
            pass

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
            exercise.join()
        # console = Table()


    def use_machine(self, machine: str, person_name: str):
        if machine not in self.n_machines:
            raise KeyError("Unknown machine!")

        n_machines = self.n_machines[machine]
        semaphore = self.semaphores[machine]

        display_name = machine.replace("_", " ").title()

        semaphore.acquire() # Lock machine, someone is using it

        reps = randint(2, 4)
        
        console.add_row(f"{person_name} will be doing {reps} reps of {display_name}")
        # console.add_row(f"{semaphore._value}/{n_machines} available.")
        
        try:
            job_progress.update(generate_bar(person_name, reps))
            table.update(recreate_table(self.available_machines, self.n_machines, self.semaphores))
        except:
            pass


        for _ in range(reps):
            time.sleep(REP_INTERVAL)

        semaphore.release()
        # table.update(recreate_table(self.available_machines, self.n_machines, self.semaphores))

        try:
            # a = 10
            table.update(recreate_table(self.available_machines, self.n_machines, self.semaphores))
        except:
            pass
        console.add_row(f"{person_name} finished using {display_name}")
        # console.add_row(f"{semaphore._value}/{n_machines} available.")

