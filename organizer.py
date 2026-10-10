import os
from datetime import datetime

categories = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"
    ],

    "Documents": [
        ".pdf", ".doc", ".docx", ".txt",
        ".xls", ".xlsx",
        ".ppt", ".pptx",
        ".csv"
    ],

    "Audio": [
        ".mp3", ".wav", ".flac", ".aac", ".m4a"
    ],

    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov", ".webm"
    ],

    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ]
}

def view_activity_log():

    if not os.path.exists("organizer_log.txt"):
        print()
        print("No activity log found.")
        return

    print()
    print("========== ACTIVITY LOG ==========")

    with open("organizer_log.txt", "r", encoding="utf-8") as log_file:

        log_data = log_file.read()

        if log_data.strip() == "":
            print("No activities recorded yet.")
        else:
            print(log_data, end="")

    print("==================================")



def view_files_overview():

    folder = input("Enter folder path: ").strip()

    if not folder:
        print("Please enter a folder path.")
        return

    if not os.path.isdir(folder):
        print("Folder not found.")
        return

    categories_to_count = [
        "Images",
        "Documents",
        "Audio",
        "Videos",
        "Archives",
        "Others"
    ]

    print()
    print("========== FILES OVERVIEW ==========")

    for category in categories_to_count:

        category_folder = os.path.join(folder, category)
        count = 0

        if os.path.isdir(category_folder):
            for file in os.listdir(category_folder):
                file_path = os.path.join(category_folder, file)

                if os.path.isfile(file_path):
                    count += 1

        print(f"{category:<10}: {count}")

    print("====================================")


def preview_organization(folder):

    if not folder.strip():
        print("Please enter a folder path.")
        return

    if not os.path.isdir(folder):
        print("Folder not found.")
        return

    files = os.listdir(folder)
    preview_count = 0

    print()
    print("========== DRY RUN PREVIEW ==========")

    for file in files:

        file_path = os.path.join(folder, file)

        if not os.path.isfile(file_path):
            continue

        name, extension = os.path.splitext(file)
        category = "Others"

        for category_name, extensions in categories.items():

            if extension.lower() in extensions:
                category = category_name
                break

        
        category_folder = os.path.join(folder, category)
        destination = os.path.join(category_folder, file)

        if os.path.exists(destination):

            counter = 1

            while os.path.exists(destination):
                new_name = f"{name}_{counter}{extension}"
                destination = os.path.join(category_folder, new_name)
                counter += 1

            print(f"{file} -> {category}/{new_name}")

        else:
            print(f"{file} -> {category}/{file}")

        preview_count += 1


    print("-------------------------------------")
    print("Files to organize:", preview_count)
    print("Preview only. No files were moved.")
    print("=====================================")


def organize_files(folder):

    if not folder.strip():
        print("Please enter a folder path.")
        return

    if not os.path.isdir(folder):
        print("Folder not found.")
        return

    files = os.listdir(folder)

    scanned_count = 0
    moved_count = 0
    failed_count = 0
    folders_skipped_count = 0

    category_counts = {
        "Images": 0,
        "Documents": 0,
        "Audio": 0,
        "Videos": 0,
        "Archives": 0,
        "Others": 0
    }

    for file in files:

        file_path = os.path.join(folder, file)

        # Skip folders
        if not os.path.isfile(file_path):
            folders_skipped_count += 1
            continue

        scanned_count += 1

        name, extension = os.path.splitext(file)

        category = "Others"

        for category_name, extensions in categories.items():

            if extension.lower() in extensions:
                category = category_name
                break

        category_folder = os.path.join(folder, category)

        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        destination = os.path.join(category_folder, file)

        # Handle duplicate file names
        if os.path.exists(destination):

            counter = 1

            while os.path.exists(destination):
                new_name = f"{name}_{counter}{extension}"
                destination = os.path.join(category_folder, new_name)
                counter += 1
        
        try:

            os.rename(file_path, destination)

            print(file, "→", category)

            with open("organizer_log.txt", "a", encoding="utf-8") as log_file:

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                log_file.write(
                    f"[{current_time}] {file} -> {category}\n"
           )

            moved_count += 1
            category_counts[category] += 1

        except Exception as e:

            print("Could not move:", file)
            print("Reason:", e)

            failed_count += 1

    print()
    print("========== ORGANIZATION COMPLETE ==========")
    print("Files scanned    :", scanned_count)
    print("Organized        :", moved_count)
    print("Folders skipped  :", folders_skipped_count)
    print("Failed           :", failed_count)
    
    if os.path.exists("organizer_log.txt"):
        print("Activity Log     : Available")
    else:
        print("Activity Log     : Not Found")

    print()
    print("Category Breakdown:")
    print("Images           :", category_counts["Images"])
    print("Documents        :", category_counts["Documents"])
    print("Audio            :", category_counts["Audio"])
    print("Videos           :", category_counts["Videos"])
    print("Archives         :", category_counts["Archives"])
    print("Others           :", category_counts["Others"])
    print("===========================================")

while True:

    print()
    print("================================")
    print("        FILE ORGANIZER")
    print("================================")
    
    print("1. Organize Files")
    print("2. View Supported File Types")
    print("3. View Activity Log")
    print("4. Exit")
    print("5. View Files Overview")
    print("6. Preview File Organization (Dry Run)")

    print("================================")

    choice = input("Enter your choice: ").strip()

    if choice == "1":

        folder = input("Enter folder path: ").strip()

        organize_files(folder)

    elif choice == "2":

        print()
        print("========== SUPPORTED FILE TYPES ==========")

        print("Images     : JPG, JPEG, PNG, GIF, WEBP, SVG")
        print("Documents  : PDF, DOC, DOCX, TXT, XLS, XLSX, PPT, PPTX, CSV")
        print("Audio      : MP3, WAV, FLAC, AAC, M4A")
        print("Videos     : MP4, MKV, AVI, MOV, WEBM")
        print("Archives   : ZIP, RAR, 7Z, TAR, GZ")
        print("Others     : Any unsupported file type")

        print("===========================================")

    elif choice == "3":

        view_activity_log()


    
    elif choice == "5":

        view_files_overview()
    

    elif choice == "6":

        folder = input("Enter folder path: ").strip()
        preview_organization(folder)

    elif choice == "4":

        print("Exiting File Organizer...")
        break


    else:
        print("Invalid choice! Please enter a number from 1 to 6.")
