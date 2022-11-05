import hashlib
import pathlib
import concurrent.futures
import shutil
from datetime import datetime

# DO NOT EDIT ABOVE THIS LINE



starting_path = r"" # Path to the folder you want to check
duplicates_folder = r"" # Path to the folder you want to move duplicates to.
logfile = r"" # Path to the log file
system_duplicate_log = r"./system_duplicate_log.log" # Path to the file where duplicate information is kept for recovery.
notification_on = True
logs_on = True


# DO NOT EDIT BELOW THIS LINE


system_duplicate_log = pahtlib.Path(system_duplicate_log)
log_file = pathlib.Path(logfile)
if log_file.exists():
    dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    notifiy("Log file exists, renaming it to {}.log".format(dt), True)
    shutil.move(log_file, log_file.parent / (log_file.stem + dt + log_file.suffix))


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
            f.write(message + "

")

def duplicate(f,hash):
    notify("{} is unique, adding hash to library.".format(f), False)
    with open(system_duplicate_log, "a") as lf:
        lf.write("{}:{}".format(file, hash) + "

")
    shutil.move(f, duplicates_folder)

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





if __name__ == "__main__":
    main()

