import os
import shutil
import general
import datetime

# DIRECTORIES = ["new","new/baby","new/english","new/hebrew","delete","skip"]
# SONG_DIR="C:/Users/SmadarENB3/Desktop/songs"
# COPY_TO_NEW_FOLDER=True

DIRECTORIES = ["skip","baby","english","hebrew","delete"]
SONG_DIR="C:/Users/SmadarENB3/Desktop/songs/new"
COPY_TO_NEW_FOLDER=False

DATE=True
def oreder_songs(directory_path):
    # Ensure the given path is a directory
    if not os.path.isdir(directory_path):
        print(f"{directory_path} is not a valid directory.")
        return

    # List all files in the directory
    files = os.listdir(directory_path)

    print_list=""
    for index, directory in enumerate(DIRECTORIES):
                print_list+=f"{index}. {directory}\n"
                print(f"{index}. {directory}")
    # Iterate through each file
    for file_name in files:
        # Construct the full path to the file
        file_path = os.path.join(directory_path, file_name)

        # Check if it is a file (not a directory)
        if os.path.isfile(file_path):
            # Extract the title (filename without extension)
            title, _ = os.path.splitext(file_name)
            title = general.hebrew_fix(title)

            # Get the creation time of the file
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            # Format the creation time to display only day and month
            creation_time_formatted = creation_time.strftime("%d-%b")

            # Print the title and date
            print(f"Title: {title}")
            if DATE:
                print(f"Creation Time: {creation_time_formatted}")
            # Get the user's decision
            decision = input("index or name if need the list enter list \n")
            if decision=="list":
                print(print_list)
                decision = input("index or name if need the list enter list \n")
            if decision.isdigit():
                target_directory=DIRECTORIES[int(decision)]
            else:
                 target_directory=decision.lower()
            if target_directory in DIRECTORIES:
                if target_directory  == 'delete':
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    print("=" * 30)
                    continue
                elif target_directory  == 'skip':
                    print("Skipped the file.")
                    print("=" * 30)
                    continue
                else:
                     # Construct the full path to the target directory
                    target_directory_path = os.path.join(directory_path, target_directory)

                    # Create the target directory if it doesn't exist
                    os.makedirs(target_directory_path, exist_ok=True)

                    # Move the file to the target directory
                    target_file_path = os.path.join(target_directory_path, file_name)
                    #copy to new folder
                    if target_directory !="new" and COPY_TO_NEW_FOLDER:
                        shutil.copy2(file_path, SONG_DIR+"/new")
                    shutil.move(file_path, target_file_path)
                    
                    print(f"Moved to: {target_file_path}")
                    print("=" * 30)        
            else:
                print("Invalid decision. Skipping the file.")
                print("=" * 30)
                continue

            

if __name__ == '__main__':
    oreder_songs(SONG_DIR)