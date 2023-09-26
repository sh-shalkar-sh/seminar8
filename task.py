import os
import json
import csv
import pickle


def save_directory_info(directory_path, output_path):
    directory_info = {}

    def explore_directory(current_path):
        current_dir = os.path.basename(current_path)
        dir_size = 0
        objects = []

        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                subdirectory_size, subdirectory_objects = explore_directory(item_path)
                dir_size += subdirectory_size
                objects.append({"name": item, "type": "directory", "size": subdirectory_size})
                objects.extend(subdirectory_objects)
            else:
                file_size = os.path.getsize(item_path)
                dir_size += file_size
                objects.append({"name": item, "type": "file", "size": file_size})

        return dir_size, objects

    total_size, result_objects = explore_directory(directory_path)

    with open(output_path + ".json", "w") as json_file:
        json.dump({"total_size": total_size, "objects": result_objects}, json_file, indent=4)

    with open(output_path + ".csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["name", "type", "size"])
        for obj in result_objects:
            csv_writer.writerow([obj["name"], obj["type"], obj["size"]])

    with open(output_path + ".pkl", "wb") as pickle_file:
        pickle.dump({"total_size": total_size, "objects": result_objects}, pickle_file)


directory_to_scan = "C:/Users/shake/PycharmProjects/seminar8"
output_file_path = "результаты_обхода"

save_directory_info(directory_to_scan, output_file_path)
