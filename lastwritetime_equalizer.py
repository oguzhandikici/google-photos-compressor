import os


def change_last_write_time(src_folder, dest_folder):
    for src_filename in os.listdir(src_folder):
        src_filepath = os.path.join(src_folder, src_filename)
        for dest_filename in os.listdir(dest_folder):
            dest_filepath = os.path.join(dest_folder, dest_filename)

            if dest_filename.split('.')[0] in src_filename:
                src_last_write_time = os.path.getmtime(src_filepath)
                dest_last_write_time = os.path.getmtime(dest_filepath)

                # Change the LastWriteTime of the source file to match the destination file
                os.utime(src_filepath, (src_last_write_time, dest_last_write_time))
                print(f"LastWriteTime of '{src_filename}' updated.")


# Example Usage
compressed_folder = r'C:\Users\oguzh\Desktop\yeni fotolar\foto_compressed'
original_folder = r'C:\Users\oguzh\Desktop\yeni fotolar\foto'

change_last_write_time(compressed_folder, original_folder)