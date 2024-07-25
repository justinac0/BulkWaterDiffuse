import csv

def write_csv(file_path: str, headers: list[str]):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['aa'])
        writer.writerow(['sss'])