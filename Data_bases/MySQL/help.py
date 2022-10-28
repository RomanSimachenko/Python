import pymysql
from auth_data import host, port, user, password, db_name

try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor,
        )
    print(f"Connected to database - {db_name}\n")

    # # Create table
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("CREATE TABLE test (ID int AUTO_INCREMENT, "
    #                        "IP varchar(15), "
    #                        "Best int(11), "
    #                        "PRIMARY KEY(ID));")
    # except Exception as error:
    #     print(error)
    # finally:
    #     print('Table created successfully...\n')

    # # Insert data
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("INSERT INTO test (IP, Best) "
    #                        "VALUES ('192.168.0.0.1', 10346)")
    #         cursor.execute("INSERT INTO test (IP, Best) "
    #                        "VALUES ('192.168.0.103', 65)")
    #         cursor.execute("INSERT INTO test (IP, Best) "
    #                        "VALUES ('192.168.0.102', 0)")
    #         cursor.execute("INSERT INTO test (IP, Best) "
    #                        "VALUES ('192.168.0', 201)")
    #         connection.commit()
    # except Exception as error:
    #     print(error)
    # finally:
    #     print('Data wrote successfully...\n')

    # # Select all data from table
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT IP, Best from test")
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print(row)
    # except Exception as error:
    #     print(error)
    # finally:
    #     print("All data got successfully...\n")

    # # Update data
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("UPDATE test SET Best=777 WHERE ID=3;")
    #         connection.commit()
    #         print(f"Total updated rows: {cursor.rowcount}\n")
    #         cursor.execute("SELECT Ip, Best from test")
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print(row)
    # except Exception as error:
    #     print(error)
    # finally:
    #     print("Data updated successfully...\n")

    # # Delete data
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("DELETE from test where ID=2;")
    #         connection.commit()
    #         print(f"Total deleted rows: {cursor.rowcount}\n")
    #         cursor.execute("SELECT IP, Best from test")
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print(row)
    # except Exception as error:
    #     print(error)
    # finally:
    #     print("Data deleted successfully...\n")

except Exception as error:
    print(error)

finally:
    connection.close()