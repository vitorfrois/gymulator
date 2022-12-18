from threading import Semaphore, Thread
import time
from random import randint, choice
from bcolors import bcolors
from rich.progress import track, Progress
from rich.table import Table
from rich.live import Live


table = Table()

def create_track(reps):
    for step in track(range(reps*4)):
        time.sleep(0.5)

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
        self.live = Live()

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
        # with live:  # update 4 times a second to feel fluid
        self.live.update(create_track(reps))
            # do_step(step)
        # for _ in range(reps): 

        semaphore.release()

        print(f"{person_name} has finished using {display_name}", end='\t\t')
        print(f"{semaphore._value}/{n_machines} available.")

