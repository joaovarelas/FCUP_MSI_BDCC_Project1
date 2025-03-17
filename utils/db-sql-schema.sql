-- USE hospital_db;

-- Disable foreign key checks temporarily
SET foreign_key_checks = 0;

-- Drop all tables in the database
DROP DATABASE IF EXISTS hospital_db;
CREATE DATABASE hospital_db;

-- Use the newly created database
USE hospital_db;
SET foreign_key_checks = 1;



-- Create a table for users (doctors and staff)
-- caregivers.csv 

CREATE TABLE IF NOT EXISTS caregivers (
    caregiver_id INT AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(50),
    description VARCHAR(255)
);



CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    gender ENUM('M', 'F') NOT NULL,
    date_of_birth DATETIME NOT NULL,
    date_of_death DATETIME DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS admissions (
    hadm_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    patient_id INT NOT NULL,
    admit_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    discharge_time DATETIME DEFAULT NULL,
    death_time DATETIME DEFAULT NULL,
    admission_type VARCHAR(250),
    admission_location VARCHAR(250),
    discharge_location VARCHAR(250),
    insurance VARCHAR(250),
    language VARCHAR(100),
    religion VARCHAR(100),
    marital_status VARCHAR(100),
    ethnicity VARCHAR(100),
    ed_reg_time DATETIME DEFAULT NULL,
    ed_out_time DATETIME DEFAULT NULL,
    diagnosis TEXT,
    hospital_expire_flag INT DEFAULT 0,
    has_chartevents_data INT DEFAULT 0,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);



-- Create a table for medical progress (tests, interventions, etc.)
-- Table for Input Events (Medications, Fluids, etc.)
CREATE TABLE IF NOT EXISTS inputevents (
    inputevent_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    hadm_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NULL,
    caregiver_id INT NOT NULL,
    item_id INT NOT NULL,
    amount FLOAT NULL,
    amount_uom VARCHAR(50) NULL,
    rate FLOAT NULL,
    rate_uom VARCHAR(50) NULL,
    order_category VARCHAR(250) NULL,
    order_description VARCHAR(250) NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id) ON DELETE CASCADE,
    FOREIGN KEY (caregiver_id) REFERENCES caregivers(caregiver_id) ON DELETE CASCADE

);

-- Table for Lab Tests
CREATE TABLE IF NOT EXISTS labevents (
    labevent_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    hadm_id INT NULL, -- pode ser null pq ha quem faca analises sem estar internado
    item_id INT NOT NULL,
    test_time DATETIME NOT NULL,
    test_value VARCHAR(100) NULL,
    test_value_num FLOAT NULL,
    test_unit VARCHAR(50) NULL,
    test_flag VARCHAR(50) NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id) ON DELETE CASCADE
);


-- Create a table for media (images/videos related to a patient)
CREATE TABLE IF NOT EXISTS media (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    file_source VARCHAR(255) NOT NULL, -- storage reference, blob, path, url, etc
    file_description VARCHAR(250) NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    question TEXT NOT NULL,
    reply TEXT DEFAULT NULL,
    question_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    reply_date DATETIME DEFAULT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS icustays (
    icustay_id INT NOT NULL PRIMARY KEY,
    patient_id INT NOT NULL,
    hadm_id INT NOT NULL,
    intime DATETIME NOT NULL,
    outtime DATETIME DEFAULT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (hadm_id) REFERENCES admissions(hadm_id) ON DELETE CASCADE
);





/*
paciente doente entra no hospital
fica em fila de espera para ser atendido
e atendido por um medico (doctor que lhe fica atribuido), faz diagnostico
passa por N tratamentos (eventos) ...
e dada alta (discharge time) e sai do hospital
*/