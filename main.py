import hashlib
import pathlib
import concurrent.futures
import shutil

starting_path = r"" # Path to the folder you want to check
duplicates_folder = r"" # Path to the folder you want to move duplicates to.

p = pathlib.Path(starting_path)
duplicates_folder = pathlib.Path(duplicates_folder)
hashes = {}
if not duplicates_folder.is_dir():
    duplicates_folder.mkdir(parents=True, exist_ok=True)


def main():

    # Get a list of all files in the folder
    files = [x for x in p.glob("**/*") if x.is_file()]
    # Get a list of subfolders
    folders = [x for x in p.glob("**/*") if x.is_dir()]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(subfolder, folders)
    # Check for duplicates
    for f in files:
        print("Hashing file: ",str(f))
        hash = hashlib.sha256(f.read_bytes()).hexdigest()
        if hash in hashes:
            print("{} is a duplicate of {}".format(f, hashes[hash]))
            shutil.move(f, duplicates_folder)
        else:
            print("{} is unique, adding hash to library.".format(f))
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
            if hash in hashes:
                shutil.move(file, duplicates_folder)
            else:
                hashes[hash] = file





if __name__ == "__main__":
    main()

