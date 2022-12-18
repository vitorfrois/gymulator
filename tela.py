from tkinter import *
from gym import *

class Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.gym = Gym()
        self.n_machines = self.gym.n_machines
        
        self.initialize_vars()
        self.make_screen()

    def initialize_vars(self):
        self.money = StringVar(value="0 Kg")
        

        self.available_machines : dict[str, StringVar] = {}
        for k in self.n_machines.keys():
            self.available_machines[k] = StringVar(value=str(self.n_machines[k]))
            
    
    def increase_weight(self, value):
        curr = int(self.money.get()[:-3])
        curr += value
        self.money.set(f"{str(curr)} Kg")

    def check_exercise_finished(self, exec_set, exercise):
        self.available_machines[exercise].set(str(int(self.available_machines[exercise].get()) - 1))

        while exec_set.is_alive():
            pass
    
        if exercise == 'bench_press':
            self.increase_weight(10)
        elif exercise == 'leg_press':
            self.increase_weight(15)

        self.available_machines[exercise].set(str(int(self.available_machines[exercise].get()) + 1))

    def start_set(self, exercise):
        if int(self.available_machines[exercise].get()) > 0:
            exec_set = Thread(target=self.gym.use_machine , args=(exercise, f'Maromba{1}'))
            check_finished = Thread(target=self.check_exercise_finished, args=(exec_set, exercise))

            exec_set.start()
            check_finished.start()
    

    def make_screen(self):      
        self.lb_titulo = Label(self, text="GYMULATOR",fg='gray1',width=20,font=("bold", 20))
        self.lb_titulo.place(relx=0.5,rely=0.05, anchor=CENTER)

        self.lb_money = Label(self, textvariable=self.money, bg='green',fg='gray1',width=20,font=("bold", 20))
        self.lb_money.place(relx=0.8,y=40,width=150,height=40)

        self.bt_bench= Button(self, text="Bench Press", bg='green',fg='gray1', command=lambda: self.start_set('bench_press'))
        self.bt_bench.place(relx=0.13, rely=0.3,width=350,height=120)
        
        self.lb_available_bench= Label(self, textvariable=self.available_machines['bench_press'], bg='yellow',fg='gray1',width=20,font=("bold", 14))
        self.lb_available_bench.place(relx=0.42, rely=0.35,width=50,height=30)

        self.bt_bench= Button(self, text="Leg Press", bg='green',fg='gray1', command=lambda: self.start_set('leg_press'))
        self.bt_bench.place(relx=0.13, rely=0.5,width=350,height=120)

        self.lb_available_bench= Label(self, textvariable=self.available_machines['leg_press'], bg='yellow',fg='gray1',width=20,font=("bold", 14))
        self.lb_available_bench.place(relx=0.42, rely=0.55,width=50,height=30)