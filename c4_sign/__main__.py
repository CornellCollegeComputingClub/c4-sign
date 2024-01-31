
from c4_sign.screen import init_matrix, update_screen
from c4_sign.tasks import TaskManager

def main():
    init_matrix()
    tm = TaskManager()

    print('Finishing up...')
    
    while True:
        tm.check_and_run_tasks()
        update_screen()


if __name__ == "__main__":
    main()