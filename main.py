import hashlib
import pathlib
import concurrent.futures
import shutil
from datetime import datetime

# DO NOT EDIT ABOVE THIS LINE



starting_path = r"." # Path to the folder you want to check
duplicates_folder = r"./duplicates" # Path to the folder you want to move duplicates to.
logfile = r"" # Path to the log file
system_duplicate_log = r"./system_duplicate_log.log" # Path to the file where duplicate information is kept for recovery.
notifications_on = True
logs_on = True


# DO NOT EDIT BELOW THIS LINE


system_duplicate_log = pathlib.Path(system_duplicate_log)
log_file = pathlib.Path(logfile)



p = pathlib.Path(starting_path)
duplicates_folder = pathlib.Path(duplicates_folder)
hashes = {}
if not duplicates_folder.is_dir():
    duplicates_folder.mkdir(parents=True, exist_ok=True)

def notify(message, log=False):
    if notifications_on:
        print(message)
    if logs_on:
        with open(log_file, "a") as f:
            f.write(message + """

""")

def duplicate(f,hash):
    if f == system_duplicate_log or f == log_file:
        return
    notify("{} is duplicate, moving it to duplicates folder".format(f), False)

    try:
        shutil.move(f, duplicates_folder)
        with open(system_duplicate_log, "a") as f:
            f.write("{}:{}".format(hash,f)
    except Exception as e:
        notify("Error moving file: " + str(e), True)
        notify("Trying to rename file and move it to duplicates folder.", True)
        try:
            dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            shutil.move(f, duplicates_folder / (f.name + " - " + dt))
            notify("File renamed to {} and moved to duplicates folder.".format(f.name + " - " + dt), True)
            with open(system_duplicate_log, "a") as f:
                f.write("{}:{}".format(hash, f)
        except Exception as e:
            notify("Error moving file: " + str(e) + """"
                                                    
                                                    Move failed!""", True)


def main():

    # Get a list of all files in the folder
    files = [x for x in p.glob("**/*") if x.is_file()]
    # Get a list of subfolders
    folders = [x for x in p.glob("**/*") if x.is_dir()]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(subfolder, folders)
    # Check for duplicates
    for f in files:
        notify("Hashing file: " + str(f), False)
        hash = hashlib.sha256(f.read_bytes()).hexdigest()
        notify("Checking to see if {} is in the library.".format(f), False)
        if hash in hashes:
            duplicate(f, hash)
        else:
            hashes[hash] = f
    notify("Done!", False)


def subfolder(folder):
    if folder == duplicates_folder:
        return
    # Get a list of all files in the folder
    files = [x for x in folder.glob("**/*") if x.is_file()]
    # Check for duplicates
    for file in files:
        with file.read_bytes():
            hash = hashlib.sha256().hexdigest()
            notify("Checking to see if {} is in the library.".format(file), False)
            if hash in hashes:
                duplicate(file, hash)
            else:
                notify("{} is unique, adding hash to library.".format(file), False)
                hashes[hash] = file

# DO NOT PLACE FUNCTIONS BELOW THIS LINE

if log_file.exists():
    dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    notify("Log file exists, renaming it to {}.log".format(dt), True)
    shutil.move(log_file, log_file.parent / (log_file.stem + dt + log_file.suffix))
else:
    log_file.touch()

if __name__ == "__main__":
    main()

