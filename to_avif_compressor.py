import multiprocessing
import os
import shutil

import numpy as np
import pillow_heif
from PIL import Image

threads = 8
images = []
compressed_images = []
others = []


def get_source():
    while True:
        # source_path = input("Enter the path where images are located: ")
        source_path = r"C:\Users\oguzh\Desktop\yeni fotolar\foto"
        if os.path.exists(source_path):
            return source_path
        else:
            print("Invalid path")


def get_target():
    while True:
        # target_path = input("Enter the path where images to save: ")
        target_path = r"C:\Users\oguzh\Desktop\yeni fotolar\foto_compressed"
        if os.path.exists(target_path):
            if os.access(target_path, os.W_OK):
                return target_path
            else:
                print("You dont have write permission for this path")
        else:
            try:
                os.makedirs(target_path)
                return target_path
            except:
                print("You dont have right permission for this path")


def fetch_images(source_path, target_path):
    target_files = os.listdir(target_path)
    for file in os.listdir(source_path):
        extention = str.lower(os.path.basename(file).split(".")[-1])
        if extention.lower() in ["jpg", "jpeg", "png", "heic", "webp"]:
            already_converted = False
            for converted_file in target_files:
                if converted_file.split('.avif')[0] in file:
                    already_converted = True
                    break
            if not already_converted:
                images.append(file)
        elif extention in ["avif"]:
            compressed_images.append(file)
        else:
            others.append(file)


def convert(source_path, target_path, images, thread_id=1):
    pillow_heif.register_avif_opener()
    pillow_heif.register_heif_opener()
    total_count = (len(images))
    count = 1
    for image in images:
        # temp_image = Image.open(os.path.join(source_path, image))
        with Image.open(os.path.join(source_path, image)) as temp_image:
            print("{}. Thread: Converting {} out of {}  {}".format(thread_id, count, total_count, image))
            temp_image.save(os.path.join(target_path, image.strip(image.split(".")[-1]) + "avif"), "avif")
        count += 1


def copy_files(source_path, target_path, compressed_images, others):
    compressed_images_path = os.path.join(target_path, "compressed_images")
    other_files_path = os.path.join(target_path, "other_files")
    os.makedirs(compressed_images_path, exist_ok=True)
    os.makedirs(other_files_path, exist_ok=True)
    for image in compressed_images:
        source_file = os.path.join(source_path, image)
        target_file = os.path.join(compressed_images_path, image)
        print("Copying {}".format(image))
        shutil.copyfile(source_file, target_file)
    for file in others:
        source_file = os.path.join(source_path, file)
        target_file = os.path.join(other_files_path, file)
        print("Copying {}".format(file))
        shutil.copyfile(source_file, target_file)


def main():
    source_path = get_source()
    target_path = get_target()
    fetch_images(source_path, target_path)
    # convert(source_path, target_path, images)
    splitted_array = np.array_split(images, threads)
    pool = multiprocessing.Pool(processes=threads)
    for idx, array in enumerate(splitted_array):
        pool.apply_async(convert, args=(source_path, target_path, array, idx))
    pool.close()
    pool.join()
    print("Conversion completed successfully")
    print('already compressed: ', compressed_images)
    print('others: ', others)
    # copy_files(source_path, target_path, compressed_images, others)
    print("finished 🎉")


if __name__ == "__main__":
    main()
