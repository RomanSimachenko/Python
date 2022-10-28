import psycopg2
from auth_data import host, port, user, password, db_name

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
    )
    print(f"Connected to database - {db_name}\n")

    # # Create table
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("CREATE TABLE STUDENT (ADMISSION INT PRIMARY KEY NOT NULL, "
    #                        "NAME TEXT NOT NULL, "
    #                        "AGE INT NOT NULL, "
    #                        "COURSE CHAR(50), "
    #                        "DEPARTMENT CHAR(50));")
    #         connection.commit()
    # except Exception as error:
    #     print(error)
    # finally:
    #     print("Table created successfully...\n")

    # # Insert data
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) "
    #                        "VALUES (3420, 'John', 18, 'Computer Science', 'ICT')")
    #         cursor.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) "
    #                        "VALUES (3419, 'Abel', 17, 'Computer Science', 'ICT')")
    #         cursor.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) "
    #                        "VALUES (3421, 'Joel', 17, 'Computer Science', 'ICT')")
    #         cursor.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) "
    #                        "VALUES (3422, 'Antony', 19, 'Electrical Engineering', 'Engineering')")
    #         cursor.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) "
    #                        "VALUES (3423, 'Alice', 18, 'Information Technology', 'ICT')")
    #         connection.commit()
    # except Exception as error:
    #     print(error)
    # finally:
    #     print("Data wrote successfully...\n")

    # # Select all data from table
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT admission, name, age, course, department from STUDENT")
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print("ADMISSION =", row[0])
    #             print("NAME =", row[1])
    #             print("AGE =", row[2])
    #             print("COURSE =", row[3])
    #             print("DEPARTMENT =", row[4], "\n")
    # except Exception as error:
    #     print(error)
    # finally:
    #     print("All data got successfully...\n")

    # # Update data
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("UPDATE STUDENT set AGE = 20 where ADMISSION = 3420")
    #         connection.commit()
    #         print(f"Total updated rows: {cursor.rowcount}\n")
    #         cursor.execute("SELECT admission, age, name, course, department from STUDENT")
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print("ADMISSION =", row[0])
    #             print("NAME =", row[1])
    #             print("AGE =", row[2])
    #             print("COURSE =", row[2])
    #             print("DEPARTMENT =", row[3], "\n")
    # except Exception as error:
    #     print(error)
    # finally:
    #     print("Data updated successfully...\n")

    # # Delete data
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("DELETE from STUDENT where ADMISSION=3420;")
    #         connection.commit()
    #         print(f"Total deleted rows: {cursor.rowcount}\n")
    #         cursor.execute("SELECT admission, name, age, course, department from STUDENT")
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print("ADMISSION =", row[0])
    #             print("NAME =", row[1])
    #             print("AGE =", row[2])
    #             print("COURSE =", row[3])
    #             print("DEPARTMENT =", row[4], "\n")
    # except Exception as error:
    #     print(error)
    # finally:
    #     print("Data deleted successfully...\n")

except Exception as error:
    print(error)

finally:
    connection.close()