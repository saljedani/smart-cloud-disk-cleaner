import os
import hashlib


class FileManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_all_files(self):
        file_paths = []

        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                file_paths.append(full_path)

        return file_paths

    def show_largest_files(self):
        files = self.get_all_files()
        files_with_size = []

        for file in files:
            try:
                size = os.path.getsize(file)
                files_with_size.append((file, size))
            except:
                pass

        files_with_size.sort(key=lambda x: x[1], reverse=True)

        print("\nTop 10 Largest Files:\n")
        for file, size in files_with_size[:10]:
            size_mb = size / (1024 * 1024)
            print(f"{file} - {size_mb:.2f} MB")

    def get_file_hash(self, file_path):
        hasher = hashlib.md5()

        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return None

    def find_duplicates(self):
        files = self.get_all_files()
        hashes = {}
        duplicates = []

        for file in files:
            file_hash = self.get_file_hash(file)

            if not file_hash:
                continue

            if file_hash in hashes:
                duplicates.append(file)
            else:
                hashes[file_hash] = file

        print("\nDuplicate Files:\n")
        if duplicates:
            for file in duplicates:
                print(file)
        else:
            print("No duplicate files found.")

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print("File deleted successfully.")
        else:
            print("File not found.")