import csv


def main():
    # Getting data from main employees file
    with open("employees.csv", 'r') as file:
        data = list(csv.DictReader(file))
        file_headers = list(data[0].keys())
        print('Reading data from main employees file', end='\n\n')

    # Applying sorting on the base of salary
    sorted_data = sorted(data, key=lambda x: int(x.get('SALARY').replace(',', '')))
    print('Sorting data on the bases of there salary', end='\n\n')

    # Separating data on the bases of job id
    job_data = {}
    for row in sorted_data:
        row_job_id = row.get("JOB_ID", '')

        if row_job_id not in job_data:
            job_data[row_job_id] = []

        job_data[row_job_id].append(row)

    # Writing data in different files according to our job ids
    for job_id, employees in job_data.items():
        with open(f"{job_id}.csv", "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=file_headers)

            writer.writeheader()

            for employee in employees:
                writer.writerow(employee)

    print('Writing data in different files', end='\n\n')


if __name__ == "__main__":
    main()