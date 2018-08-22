import csv


def read_csv_to_list_of_dicts(file_path):
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        list_of_dicts = [dict(line) for line in reader]
    return list_of_dicts


def append_line_to_csv(file_path, data_header, line_to_append):
    with open(file_path, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_header)
        writer.writerow(line_to_append)


def update_csv(file_path, data_header, updated_data):
    with open(file_path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_header)
        writer.writeheader()
        writer.writerows(updated_data)
