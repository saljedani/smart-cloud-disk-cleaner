import os
from file_manager import FileManager
from cloud_manager import CloudManager


def main():
    folder = input("Enter folder path: ")

    if not os.path.exists(folder):
        print("Folder not found.")
        return

    file_manager = FileManager(folder)
    cloud_manager = CloudManager()

    while True:
        print("\n--- Smart Disk Cleaner ---")
        print("1. Show largest files")
        print("2. Find duplicate files")
        print("3. Delete a file")
        print("4. Upload file to cloud and delete local copy")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            file_manager.show_largest_files()

        elif choice == "2":
            file_manager.find_duplicates()

        elif choice == "3":
            path = input("Enter full file path to delete: ")
            file_manager.delete_file(path)

        elif choice == "4":
            path = input("Enter full file path to upload: ")
            cloud_manager.upload_and_delete(path)

        elif choice == "5":
            print("Goodbye")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()