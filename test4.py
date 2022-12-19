from random import randint, choice
available_machines = {
        "leg_press": 1,
        "bench_press": 2,
        "supino": 3
        }

for elem in available_machines:
    print(available_machines[elem])


print(choice(list(available_machines)))