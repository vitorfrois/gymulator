from threading import Semaphore, Thread
import time
from random import randint, choice
from bcolors import bcolors
from rich.progress import track, Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
import asyncio


table = Table()
progress = Progress()
live = Live()

playing = True

def create_track(reps):
    for step in track(range(reps*4)):
        time.sleep(0.5)

async def init_live(progress_table, job_progress):
    with Live(progress_table, refresh_per_second=10):
        while playing:
            time.sleep(0.1)
            for job in job_progress.tasks:
                if not job.finished:
                    job_progress.advance(job.id)

            completed = sum(task.completed for task in job_progress.tasks)
            # overall_progress.update(overall_task, completed=completed)

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
        
        job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )

        total = sum(task.total for task in job_progress.tasks)
        overall_progress = Progress()
        overall_task = overall_progress.add_task("All Jobs", total=int(total))

        self.progress_table = Table.grid()
        self.progress_table.add_row(
            Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
        )
        asyncio.run(init_live(self.progress_table, job_progress))


    def start_training(self, person_name: str):
        # This will be the target for maromba's thread. It should execute various
        # exercises during the existence of that maromba.
        n_exercices = randint(1, len(self.available_machines))
        print(bcolors.WARNING + f"{person_name} has just started and will be doing {n_exercices} exercises." + bcolors.ENDC)

        for _ in range(n_exercices):
            machine = choice(self.available_machines)
            print(bcolors.OKBLUE + f"{person_name} wants to use {machine}!" + bcolors.ENDC)
            exercise = Thread(target=self.use_machine , args=(machine, person_name,))
            exercise.start()


    def use_machine(self, machine: str, person_name: str):
        if machine not in self.n_machines:
            raise KeyError("Unknown machine!")

        n_machines = self.n_machines[machine]
        semaphore = self.semaphores[machine]

        display_name = machine.replace("_", " ").title()

        semaphore.acquire() # Lock machine, someone is using it

        reps = randint(2, 4)
        
        print(f"{person_name} will be doing {reps} reps of {display_name}", end='\t')
        print(f"{semaphore._value}/{n_machines} available.")

        # Execute repetitions
        # with self.live:  # update 4 times a second to feel fluid
        #     self.live.update(create_track(reps))

        # with live:
        #     with Progress() as progress:
        #         task_id = progress.add_task("Maromba trein... ", total=reps, visible=True)
        #         while not progress.finished:
        #             progress.update(task_id, advance=0.5)
        #             time.sleep(0.5)
        # for _ in track(range(reps)): 
        #     progress.update(task_id, advance=0.1)
        #     time.sleep(0.5)
        job1 = job_progress.add_task("[green]Maromba 1", total=reps)
        semaphore.release()


        print(f"{person_name} has finished using {display_name}", end='\t\t')
        print(f"{semaphore._value}/{n_machines} available.")

