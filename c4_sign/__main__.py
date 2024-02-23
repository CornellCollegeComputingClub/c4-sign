import argparse
from c4_sign.screen import init_matrix, update_screen
from c4_sign.tasks import TaskManager

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulator', action='store_true')
    args = parser.parse_args()
    init_matrix(args.simulator)
    tm = TaskManager()

    frame_count = 0
    to_profile = 10

    # print('Finishing up...')
    
    while True:
        tm.check_and_run_tasks()
        update_screen()
        frame_count += 1
        if frame_count >= to_profile:
            break
        print(frame_count)

if __name__ == "__main__":
    from pyinstrument import Profiler
    from pyinstrument.renderers import SpeedscopeRenderer

    with Profiler() as profiler:
        try:
            main()
        except KeyboardInterrupt:
            pass
    print('Writing profile...')
    with open('profile.speedscope.json', 'w') as f:
        f.write(profiler.output(renderer=SpeedscopeRenderer(show_all=True)))
