import pymysql
import csv
import random
from datetime import datetime
from google.cloud.sql.connector import Connector
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/user/msi/bdcc/proj1-files/appeng-svcacc-key.json"


# Environment Variables or Constants
IS_PROD = False




# Local Database Credentials
LOCAL_DB_HOST = "localhost"
LOCAL_DB_USER = "root"
LOCAL_DB_PASS = "root"
LOCAL_DB_NAME = "hospital_db"

# Cloud SQL Credentials
CLOUD_SQL_CONNECTION_NAME = "bdcc2025-451416:europe-west1:bdcc-proj1-mysql"
CLOUD_DB_USER = "root"
CLOUD_DB_PASS = "x%npoJsENm/5b8tz"
CLOUD_DB_NAME = "hospital_db"

# Function to connect to MySQL
def connect_to_db():
    if IS_PROD:
        print(f"🔹 Connecting to Cloud SQL: {CLOUD_SQL_CONNECTION_NAME}")
        connector = Connector()
        connection = connector.connect(
            CLOUD_SQL_CONNECTION_NAME,
            "pymysql",
            user=CLOUD_DB_USER,
            password=CLOUD_DB_PASS,
            db=CLOUD_DB_NAME,
        )
    else:
        print(f"🔹 Connecting to Local DB: {LOCAL_DB_HOST}")
        connection = pymysql.connect(
            host=LOCAL_DB_HOST,
            user=LOCAL_DB_USER,
            password=LOCAL_DB_PASS,
            database=LOCAL_DB_NAME,
            charset="utf8mb4",
        )
    
    return connection



NUM_BATCH = 5000


def load_caregivers_data(csv_file_path):
    print("Loading CAREGIVERS data...")

    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO caregivers (caregiver_id, label, description)
        VALUES (%s, %s, %s )
    """

    insert_data = []

    try:
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)

            for index, row in enumerate(csv_reader):
                #row_id = int(row['ROW_ID'])
                cgid = int(row['CGID'])
                label = row['LABEL'] if row['LABEL'] else None
                description = row['DESCRIPTION'] if row['DESCRIPTION'] else None

                insert_data.append((cgid, label, description))

                if index % NUM_BATCH == 0 and insert_data:
                    cursor.executemany(insert_query, insert_data)
                    connection.commit()
                    print(f"-> Loaded {index} rows...")
                    insert_data = []  

            if insert_data:
                cursor.executemany(insert_query, insert_data)
                connection.commit()

        print("CAREIGIVERS data loaded successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
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

    insert_data = []
    
    try:
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)

            for index, row in enumerate(csv_reader):
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


                insert_data.append((patient_id, gender, dob, dod))

                # Insert the patient data into the database
                #cursor.execute(insert_query, (patient_id, gender, dob, dod))

                if index % NUM_BATCH == 0 and insert_data:
                    cursor.executemany(insert_query, insert_data)
                    connection.commit()
                    print(f"-> Loaded {index} rows...")
                    insert_data = []  # Clear the batch list

            # Insert remaining rows
            if insert_data:
                cursor.executemany(insert_query, insert_data)
                connection.commit()

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

    # SQL insert statement
    insert_query = '''
    INSERT INTO admissions (
        hadm_id, patient_id, admit_time, discharge_time, death_time, 
        admission_type, admission_location, discharge_location, insurance, 
        language, religion, marital_status, ethnicity, ed_reg_time, ed_out_time, 
        diagnosis, hospital_expire_flag, has_chartevents_data
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    insert_data = []

    # Open and read the CSV file
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        # Iterate through each row in the CSV
        for index, row in enumerate(csv_reader):
            hadm_id = int(row['HADM_ID'])
            patient_id = int(row['SUBJECT_ID'])
            admit_time = datetime.strptime(row['ADMITTIME'], '%Y-%m-%d %H:%M:%S')
            discharge_time = datetime.strptime(row['DISCHTIME'], '%Y-%m-%d %H:%M:%S') if row['DISCHTIME'] else None
            death_time = datetime.strptime(row['DEATHTIME'], '%Y-%m-%d %H:%M:%S') if row['DEATHTIME'] else None
            admission_type = row['ADMISSION_TYPE']
            admission_location = row['ADMISSION_LOCATION']
            discharge_location = row['DISCHARGE_LOCATION']
            insurance = row['INSURANCE']
            language = row['LANGUAGE'] if row['LANGUAGE'] else None
            religion = row['RELIGION'] if row['RELIGION'] else None
            marital_status = row['MARITAL_STATUS'] if row['MARITAL_STATUS'] else None
            ethnicity = row['ETHNICITY']
            edreg_time = datetime.strptime(row['EDREGTIME'], '%Y-%m-%d %H:%M:%S') if row['EDREGTIME'] else None
            edout_time = datetime.strptime(row['EDOUTTIME'], '%Y-%m-%d %H:%M:%S') if row['EDOUTTIME'] else None
            diagnosis = row['DIAGNOSIS']
            hospital_expire_flag = int(row['HOSPITAL_EXPIRE_FLAG'])
            has_chartevents_data = int(row['HAS_CHARTEVENTS_DATA'])

            # Append row data to batch insert list
            insert_data.append((
                hadm_id, patient_id, admit_time, discharge_time, death_time,
                admission_type, admission_location, discharge_location, insurance,
                language, religion, marital_status, ethnicity, edreg_time, edout_time,
                diagnosis, hospital_expire_flag, has_chartevents_data
            ))

            # Execute batch insert every NUM_BATCH rows
            if index % NUM_BATCH == 0 and insert_data:
                cursor.executemany(insert_query, insert_data)
                connection.commit()
                print(f"-> Loaded {index} rows...")
                insert_data = []  # Clear batch list

        # Insert any remaining rows
        if insert_data:
            cursor.executemany(insert_query, insert_data)
            connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    print("ADMISSIONS data has been loaded successfully!")


def load_inputevents_data(csv_file_path):
    print("Loading INPUTEVENTS_MV data...")

    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO inputevents (patient_id, hadm_id, start_time, end_time, caregiver_id, item_id, amount, amount_uom, rate, rate_uom, order_category, order_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    insert_data = []

    try:
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)

            for index, row in enumerate(csv_reader):
                patient_id = int(row['SUBJECT_ID'])
                hadm_id = int(row['HADM_ID'])
                caregiver_id = int(row['CGID']) if row['CGID'] else None
                item_id = int(row['ITEMID'])
                amount = float(row['AMOUNT']) if row['AMOUNT'] else None
                amount_uom = row['AMOUNTUOM'] if row['AMOUNTUOM'] else None
                rate = float(row['RATE']) if row['RATE'] else None
                rate_uom = row['RATEUOM'] if row['RATEUOM'] else None
                order_category = row['ORDERCATEGORYNAME'] if row['ORDERCATEGORYNAME'] else None
                order_description = row['ORDERCATEGORYDESCRIPTION'] if row['ORDERCATEGORYDESCRIPTION'] else None

                # Convert date formats
                try:
                    start_time = datetime.strptime(row['STARTTIME'], '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.strptime(row['ENDTIME'], '%Y-%m-%d %H:%M:%S') if row['ENDTIME'] else None
                except ValueError as e:
                    print(f"Skipping invalid date format: {e} for row: {row}")
                    continue

                insert_data.append((patient_id, hadm_id, start_time, end_time, caregiver_id, item_id, amount, amount_uom, rate, rate_uom, order_category, order_description))

                # Commit after every 1000 rows
                if index % NUM_BATCH == 0 and insert_data:
                    cursor.executemany(insert_query, insert_data)
                    connection.commit()
                    print(f"-> Loaded {index} rows...")
                    insert_data = []  # Clear the batch list

            # Insert remaining rows
            if insert_data:
                cursor.executemany(insert_query, insert_data)
                connection.commit()

        print("INPUTEVENTS_MV data loaded successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

# Function to load LABEVENTS.csv into labevents table
def load_labevents_data(csv_file_path):
    print("Loading LABEVENTS data...")

    connection = connect_to_db()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO labevents (patient_id, hadm_id, item_id, test_time, test_value, test_value_num, test_unit, test_flag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    insert_data= []

    try:
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)

            for index, row in enumerate(csv_reader):
                patient_id = row['SUBJECT_ID']
                hadm_id = row['HADM_ID'] if row['HADM_ID'] else None
                item_id = row['ITEMID']  if row['ITEMID'] else None
                test_time = row['CHARTTIME']  if row['CHARTTIME'] else None
                test_value = row['VALUE'] if row['VALUE'] else None
                test_value_num = float(row['VALUENUM']) if row['VALUENUM'] else None
                test_unit = row['VALUEUOM'] if row['VALUEUOM'] else None
                test_flag = row['FLAG'] if row['FLAG'] else None

                # Convert date format
                try:
                    test_time = datetime.strptime(test_time, '%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    print(f"Skipping invalid date format: {e} for row: {row}")
                    continue

                #cursor.execute(insert_query, (patient_id, hadm_id, item_id, test_time, test_value, test_value_num, test_unit, test_flag))
                insert_data.append((patient_id, hadm_id, item_id, test_time, test_value, test_value_num, test_unit, test_flag))
                 # Commit after every 1000 rows
                if index % NUM_BATCH == 0 and insert_data:
                    cursor.executemany(insert_query, insert_data)
                    connection.commit()
                    print(f"-> Loaded {index} rows...")
                    insert_data = []  # Clear the batch list

            # Insert remaining rows
            if insert_data:
                cursor.executemany(insert_query, insert_data)
                connection.commit()

        connection.commit()
        print("LABEVENTS data loaded successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()


# Function to load ICUSTAYS.csv into icustays table
def load_icustays_data(csv_file_path):
    print("Loading ICUSTAYS data...")
    
    connection = connect_to_db()
    cursor = connection.cursor()
    
    insert_query = """
        INSERT INTO icustays (patient_id, hadm_id, icustay_id, intime, outtime)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    insert_data = []
    
    try:
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            
            for index, row in enumerate(csv_reader):
                patient_id = row['SUBJECT_ID']
                hadm_id = row['HADM_ID'] if row['HADM_ID'] else None
                icustay_id = row['ICUSTAY_ID']
                intime = row['INTIME'] if row['INTIME'] else None
                outtime = row['OUTTIME'] if row['OUTTIME'] else None
                
                # Convert datetime format
                try:
                    intime = datetime.strptime(intime, '%Y-%m-%d %H:%M:%S') if intime else None
                    outtime = datetime.strptime(outtime, '%Y-%m-%d %H:%M:%S') if outtime else None
                except ValueError as e:
                    print(f"Skipping invalid date format: {e} for row: {row}")
                    continue
                
                insert_data.append((patient_id, hadm_id, icustay_id, intime, outtime))
                
                # Commit after every NUM_BATCH rows
                if index % NUM_BATCH == 0 and insert_data:
                    cursor.executemany(insert_query, insert_data)
                    connection.commit()
                    print(f"-> Loaded {index} rows...")
                    insert_data = []  # Clear the batch list
            
            # Insert remaining rows
            if insert_data:
                cursor.executemany(insert_query, insert_data)
                connection.commit()
        
        print("ICUSTAYS data loaded successfully!")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

#######


def MAIN():
    # Call the function to insert doctors
    load_caregivers_data('./csv/CAREGIVERS.csv')
    load_patients_data('./csv/PATIENTS.csv')
    load_admissions_to_db('./csv/ADMISSIONS.csv')
    load_inputevents_data("./csv/INPUTEVENTS_MV.csv")
    load_labevents_data("./csv/LABEVENTS.csv")
    load_icustays_data("./csv/ICUSTAYS.csv")



if __name__ == "__main__":
    MAIN()


