import argparse

from c4_sign.screen import init_matrix, update_screen
from c4_sign.tasks import TaskManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulator", action="store_true")
    args = parser.parse_args()
    init_matrix(args.simulator)
    tm = TaskManager()

    print("Finishing up startup...")

    while True:
        tm.check_and_run_tasks()
        update_screen()


if __name__ == "__main__":
    main()
