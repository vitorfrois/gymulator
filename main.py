from gym import *


def main():
    gym = Gym()
    for i in range(5):
        time.sleep(randint(2, 5))
        
        maromba = Thread(target=gym.start_training , args=(f'Maromba{i}',))
        maromba.start()

if __name__ == '__main__':
    main()
