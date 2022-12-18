from gym import *
from tkinter import *

from tela import Screen


# def main():
#     gym = Gym()
#     for i in range(5):
#         time.sleep(randint(2, 5))
        
#         maromba = Thread(target=gym.start_training , args=(f'Maromba{i}',))
#         maromba.start()

# if __name__ == '__main__':
#     main()

class MainApplication(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.initialize_root()
        

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
    def initialize_root(self):
        self.resizable(False, False)
        self.geometry("1280x720")
        self.title("Gymulator 2022")     

        container = Frame(self, bg="#fff")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Screen,):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Screen")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()