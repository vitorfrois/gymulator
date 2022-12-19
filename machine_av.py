class AvMachine:
    def __init__(self):
        self.available_machines = [
            "leg_press", 
            "bench_press",
            "pulley",
            "squat",
            "leg_extension",
            "scott_machine",
            "pulldown",
            "treadmill",
            "bike",
        ]

        self.n_machines: dict[str, int] = {}

        # Initial machines
        self.n_machines['leg_press'] = 1
        self.n_machines['bench_press'] = 2
        self.n_machines['pulley'] = 2
        self.n_machines['squat'] = 2
        self.n_machines['leg_extension'] = 1
        self.n_machines['scott_machine'] = 1
        self.n_machines['pulldown'] = 2
        self.n_machines['treadmill'] = 4
        self.n_machines['bike'] = 4