import pymysql
import csv
import random
from datetime import datetime

# Function to connect to the database
def connect_to_db():
    return pymysql.connect(
        host='localhost',
        user='root',        # Your DB user
        password='root',  # Your DB password
        database='hospital_db',   # Your DB name
        charset='utf8mb4'
    )

# Function to insert doctors into the database
def insert_doctors():
    print("Loading DOCTORS data...")
    try:
        # Connect to the database
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to insert doctors into the doctors table
        insert_query = """
        INSERT INTO doctors (doctor_name)
        VALUES (%s)
        """

        # Insert 10 doctors with names like 'Doctor #01', 'Doctor #02', etc.
        for i in range(1, 11):
            doctor_name = f"Doctor #{i:02d}"
            cursor.execute(insert_query, (doctor_name,))

        # Commit the transaction
        connection.commit()

        print("Successfully inserted 10 doctors into the 'doctors' table.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()




# Function to load CSV data into MySQL database
def load_patients_data(csv_file_path):
    print("Loading PATIENTS data...")

    # Establish database connection
    connection = connect_to_db()
    cursor = connection.cursor()

    # SQL query to insert patient data
    insert_query = """
        INSERT INTO patients (patient_id, gender, date_of_birth, date_of_death)
        VALUES (%s, %s, %s, %s)
    """

    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                patient_id = row['SUBJECT_ID']
                gender = row['GENDER']
                dob = row['DOB']
                dod = row['DOD'] if row['DOD'] else None  # If no DOD, set to None

                # Convert DOB and DOD to datetime format
                try:
                    dob = datetime.strptime(dob, '%Y-%m-%d %H:%M:%S')
                    dod = datetime.strptime(dod, '%Y-%m-%d %H:%M:%S') if dod else None
                except ValueError as e:
                    print(f"Skipping invalid date format: {e} for row: {row}")
                    continue

                # Insert the patient data into the database
                cursor.execute(insert_query, (patient_id, gender, dob, dod))

        # Commit the transaction to the database
        connection.commit()

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()

    print("PATIENTS data has been loaded successfully!")




def load_admissions_to_db(csv_file):
    print("Loading ADMISSIONS data...")


    # Establish connection to the MySQL database
    connection = connect_to_db()    
    cursor = connection.cursor()

    # Read the CSV file using pandas
    # Prepare the SQL insert statement
    insert_query = '''
    INSERT INTO admissions (patient_id, doctor_id, admit_time, discharge_time, admission_type, diagnosis)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''

    # Open and read the CSV file using csv.reader
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # Iterate through each row in the CSV
        for index, row in enumerate(csv_reader):
            patient_id = row['SUBJECT_ID']
            doctor_id = random.randint(1, 10)  # Randomly select a doctor_id between 1 and 10
            admit_time = row['ADMITTIME']
            discharge_time = row['DISCHTIME'] if row['DISCHTIME'] else None
            admission_type = row['ADMISSION_TYPE']
            diagnosis = row['DIAGNOSIS']

            # Convert admit_time and discharge_time to datetime format if necessary
            admit_time = datetime.strptime(admit_time, '%Y-%m-%d %H:%M:%S')
            discharge_time = datetime.strptime(discharge_time, '%Y-%m-%d %H:%M:%S') if discharge_time else None

            # Execute the insert query
            cursor.execute(insert_query, (patient_id, doctor_id, admit_time, discharge_time, admission_type, diagnosis))
            
            # Commit the transaction every 1000 rows
            if index % 1000 == 0:
                connection.commit()

    # Commit any remaining rows
    connection.commit()

    # Close the cursor and the connection
    cursor.close()
    connection.close()

    print("ADMISSIONS data has been loaded successfully!")





def MAIN():
    # Call the function to insert doctors
    insert_doctors()
    load_patients_data('./csv/PATIENTS.csv')
    load_admissions_to_db('./csv/ADMISSIONS.csv')



if __name__ == "__main__":
    MAIN()


