from gym import *
import names
import random


def main():
    gym = Gym()
    for i in range(5):
        time.sleep(randint(2, 5))

        name = random.choice(names.names)        
        maromba = Thread(target=gym.start_training , args=(name,))
        maromba.start()

if __name__ == '__main__':
    main()
