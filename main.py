from gym import *
from rich.console import Console
import names


def main():
    comand = " "
    while comand != "y" and comand != "n":
        comand = input("Simulate gym levels? (y) (n): ").lower()

    gym = Gym()
    console = Console()
    console.clear()
    if(comand == "y"):
        while playing:
            gym.uplevel()
            for i in range(5*gym.level):
                time.sleep(randint(2, 5))

                name = random.choice(names.names)        
                maromba = Thread(target=gym.start_training , args=(name,))
                maromba.start()
    else:
        for i in range(5):
            time.sleep(randint(2, 5))
            
            name = random.choice(names.names)        
            maromba = Thread(target=gym.start_training , args=(name,))
            maromba.start()

if __name__ == '__main__':
    main()
