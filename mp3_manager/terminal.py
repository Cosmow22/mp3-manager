import os, sys


class HiddenPrints:
    """Hide errors from terminal."""
    def __enter__(self):        
        self._original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, *args):
        sys.stderr.close()
        sys.stderr = self._original_stderr
        
        
        
def print_to(line, music_name):
    print(f"\033[{5-line}A", end="")  # move cursor up
    print("\033[2K", end="")  # clear line
    print(f"Thread {line}: {music_name}", end="\r")
    print(f"\033[{5-line}B", end="")  # move cursor back
    