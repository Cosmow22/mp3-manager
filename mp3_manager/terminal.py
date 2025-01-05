import os, sys


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, *args):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        
        
def print_to(line, music_name):
    print(f"\033[{5-line}A", end="")  # move cursor up
    print("\033[2K", end="")  # clear line
    print(f"Thread {line}: {music_name}", end="\r")
    print(f"\033[{5-line}B", end="")  # move cursor back
    