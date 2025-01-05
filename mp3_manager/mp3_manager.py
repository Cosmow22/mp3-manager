import asyncio
import eyed3
import csv
from pathlib import Path
from os.path import getctime
from datetime import date
from pydub import AudioSegment
from pydub.utils import make_chunks
from .terminal import HiddenPrints, print_to


def table_content_is_modified(table_content, metavar):
    if metavar is not None:
        if metavar != table_content:
            return True
        else:
            return False
    elif table_content != "":
        return True
    else:
        return False

    
def scan(args):
    mp3 = Path.cwd() / args.path
    with open(Path.cwd() / args.csv, "w", newline="", encoding="utf-8") as fp:
        musics_writer = csv.writer(fp)
        musics_writer.writerow(["Title", "New Title", "Artist(s)", "Album","Genre", "Date added", "N°"])

        for music in mp3.rglob("*.mp3"): 
            with HiddenPrints(): audiofile = eyed3.load(music)
            song_name = music.name[:-4]
            if audiofile is not None:
                with HiddenPrints(): genre = audiofile.tag.genre.name if audiofile.tag.genre else None
                musics_writer.writerow([
                        song_name, 
                        None,  # New Title
                        audiofile.tag.artist, 
                        audiofile.tag.album, 
                        genre, 
                        date.fromtimestamp(getctime(music)),
                        audiofile.tag.track_num.count
                        ])


def edit(args):
    mp3 = Path.cwd() / args.path
    csv_file = Path.cwd()/ args.csv
    csv_is_modified = False
    with open(csv_file, encoding="utf-8") as fp:
        musics_reader = csv.reader(fp)
        rows = list(musics_reader)[1:]
        for index, row in enumerate(rows):
            filename = row[0] + ".mp3"
            with HiddenPrints(): 
                try:
                    audiofile = eyed3.load(mp3/filename)
                except OSError:
                    print("Failed to load", mp3/filename)
                    continue
                genre = audiofile.tag.genre.name if audiofile.tag.genre else None
                                
            if audiofile is not None:
                if table_content_is_modified(row[2], audiofile.tag.artist):
                    print(filename, f"artist: {audiofile.tag.artist} → '{row[2]}'")
                    audiofile.tag.artist = row[2]
                    audiofile.tag.save()
                if table_content_is_modified(row[3], audiofile.tag.album):
                    print(filename, f"album: {audiofile.tag.album} → '{row[3]}'")
                    audiofile.tag.album = row[3]
                    audiofile.tag.save()
                
                if table_content_is_modified(row[4], genre):
                    print(filename, f"genre: {genre} → '{row[4]}'")
                    audiofile.tag.genre = row[4]
                    audiofile.tag.save()

            if row[1] != "" and row[1] != row[0]:
                print(f"filename: {row[0]} → {row[1]}")
                (mp3/Path(filename)).rename(mp3/(row[1]+".mp3"))
                updated_row = row
                updated_row[0] = row[1]
                updated_row[1] =  None
                rows[index] = updated_row
                csv_is_modified = True
                
    if csv_is_modified:
        with open(csv_file, "w", newline="", encoding="utf-8") as fp:
            musics_writer = csv.writer(fp)
            musics_writer.writerow(["Title", "New Title", "Artist(s)", "Album","Genre", "Date added", "N°"])
            musics_writer.writerows(rows)
            

def process_audio(music: Path, target_dBFS: int):
    sound = AudioSegment.from_file(music)
    loudness = max(chunk.dBFS for chunk in make_chunks(sound, 60_000))
    gain = target_dBFS - loudness
    if abs(gain) < 1: return
    equalized_sound = sound.apply_gain(gain)  # set dBFS to target_dBFS
    
    with HiddenPrints(): 
        audiofile = eyed3.load(music)
        genre = audiofile.tag.genre.name if audiofile.tag.genre else ""
    equalized_sound.export(
        music, 
        format="mp3", 
        tags={
            "album": "" if audiofile.tag.album is None else audiofile.tag.album,
            "artist": "" if audiofile.tag.artist is None else audiofile.tag.artist,
            "genre": genre,
            }
        )


async def run_equalize_coroutine(music: Path, target_dBFS: int, semaphore: asyncio.Semaphore, thread_id: int):
    async with semaphore: 
        await asyncio.to_thread(process_audio, music, target_dBFS)
        print_to(thread_id, music.name)
                
async def equalize(args):
    mp3 = Path.cwd() / args.path
    print("Thread 0: ...")
    print("Thread 1: ...")
    print("Thread 2: ...")
    print("Thread 3: ...")
    print("Thread 4: ...")
    print('\033[?25l', end="")  # Hide cursor
    thread_id = 0
    semaphore = asyncio.Semaphore(5)
    coroutines = []
    for music in mp3.rglob("*.mp3"):
        if thread_id == 4: thread_id = 0
        else: thread_id += 1
        coroutines.append(run_equalize_coroutine(music, args.dBFS, semaphore, thread_id))
    await asyncio.gather(*coroutines)
    
    print('\033[?25h', end="")  # Show cursor
    print("\nDone !")

def run_equalize(args):
    asyncio.run(equalize(args))