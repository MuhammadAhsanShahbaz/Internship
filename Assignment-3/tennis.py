import csv
import mysql.connector
from datetime import datetime


class Tennis:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.Connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.Connection.cursor()

    def update_csv(self, data, head):
        sorted_data = sorted(data, key=lambda x: x['Event'])

        event = {}
        for d in sorted_data:
            if d["Event"] not in event:
                event[d["Event"]] = []
            event[d["Event"]].append(d)

        for name, tennis in event.items():
            with open(f"{name}.csv", "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=head)
                writer.writeheader()
                for t in tennis:
                    writer.writerow(t)

        print("\ncsv files are updated.\n")

    def create_table(self, head):
        sql = """
        CREATE TABLE IF NOT EXISTS tennis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            DateCreated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            DateModified DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cursor.execute(sql)
        self.Connection.commit()

        for i in head:
            i = i.replace(" ", "")
            sql = f"""
            ALTER TABLE tennis 
            ADD {i.replace('%', 'p')} TEXT
            """
            self.cursor.execute(sql)

        self.Connection.commit()
        print("\nTable has been created.\n")

    def update_database(self, data, head):
        self.cursor.execute("SELECT * FROM tennis;")
        mids = self.cursor.fetchall()

        cmid = []
        for mid in mids:
            mid = mid[4]
            cmid.append(mid)
        if not mids:
            print("\nTable is empty\n")

        self.Connection.commit()

        hea = []
        for h in head:
            h = h.replace(" ", "")
            hea.append(h.replace("%", "p"))
        column_name = ",".join(hea)

        f = 0
        for i in data:
            i["Season URL"] = '"' + i["Season URL"]
            i["Player 2 Total Games Played"] = i["Player 2 Total Games Played"] + '"'
            column_values = '","'.join(list(i.values()))

            f += 1
            sql = f"""
                INSERT INTO tennis (id, {column_name})
                VALUES ({f}, {column_values})
                ON DUPLICATE KEY UPDATE DateModified = '{datetime.now()}';
            """
            self.cursor.execute(sql)
            print(f)

        if f == 0:
            print("\nNo entry is updated.\n")
        else:
            print(f"\n{f} entries updated.\n")

        self.Connection.commit()
        print('\ndatabase is updated.\n')



    def close_connection(self):
        self.cursor.close()
        self.Connection.close()


def main():
    database = Tennis(
        host="localhost",
        user="root",
        password="pokemon",
        database="tennis"
    )

    with open("Tennis Data.csv", "r") as file:
        data = list(csv.DictReader(file))
        head = list(data[0].keys())

    while True:
        print("1. Update data to csv. ")
        print("2. Create Table. ")
        print("3. Update database.")
        print("4. Exit")
        i = int(input("Enter the number of your operation : "))
        match i:
            case 1:
                database.update_csv(data, head)
            case 2:
                database.create_table(head)
            case 3:
                database.update_database(data, head)
            case 4:
                database.close_connection()
                break
            case _:
                print("\nInvalid input! Please enter a valid number.\n")

    print("\nProgram successfully exited.")


if __name__ == "__main__":
    main()