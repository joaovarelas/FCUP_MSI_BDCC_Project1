# Hospital Backend Project 1 - BDCC 24/25

This project is a backend system for hospital data management, deployed on Google Cloud Platform (GCP). It leverages the **MIMIC-III** database and provides a REST API for managing hospital data, patient admissions, medical progress, media files, and patient-related questions.

---

## Features

### Core Functionality
- **Hospital Data Management**: Handle patient data, admissions, medical progress, and media files.
- **Patient Intake**: Support for adding new patients.
- **Doctor Q&A**: Doctors responsible for a patient can answer one question per patient request (1 question = 1 response).
- **Deployment**: Hosted on Google Cloud Platform with autoscaling and high availability configured.

### Data Models
- **Patients**:
  - `id`: Unique identifier
  - `dob`: Date of birth
  - `dod`: Date of death (if applicable)
  - `gender`: Patient gender
- **Media**:
  - Documents, images, and videos associated with a patient.
- **Admissions**:
  - Hospital stays with patient ID, start/end dates, and status (active/discharged).
- **Progress**:
  - Medical interventions, lab results, medications, etc.
- **Questions**:
  - Questions and answers, including patient ID, user who asked, and question text.

---

## REST API



### Patients
- **Create**: Add a new patient.
- **Update**: Modify patient details.
- **Delete**: Remove a patient; associated admissions and progress will display "Deleted user".

### Media
- **Upload**: Upload files (documents, images, videos) for a patient (1 or 2 calls depending on operation).
- **Download**: Retrieve patient-associated files.

### Admissions
- **Create**: Record a new hospital admission.
- **Update**: Modify admission details.

### Progress
- **Create/Update**: Add medical interventions or lab results (sourced from `INPUTEVENTS_MV` and `LABEVENTS` in MIMIC-III).

### Questions
- **Create**: Submit a question for a patient by ID.
- **Respond**: Answer a question by patient ID.

---

## Additional Features
- **Longest Waiting Patients**: List patients with the longest wait times (possibly implemented as a Function-as-a-Service, FaaS).
- **Patient Progress**: Retrieve a patient's progress history by ID (possibly FaaS).

---

## Development & Testing
- **Database**: Uses the **MIMIC-III** dataset.
- **Auxiliary Scripts**: Includes helper/test scripts for development and validation.

### Load Testing
- **Tool**: [Artillery](https://www.artillery.io/)
- **Approach**:
  - Simulate a sequence of actions (e.g., create patient, admit patient, update progress).
  - Test with increasing `N` (number of requests) to evaluate system capacity, load, and timings.
- **Goals**:
  - Assess autoscaling and high availability on GCP.
  - Measure performance under stress.

---

## Deployment TODO
- **Platform**: Google Cloud Platform (GCP).
- **Configuration**:
  - Autoscaling enabled for handling variable loads.
  - High availability ensured for continuous operation.

---

## Setup Instructions TODO
*(To be completed based on your environment setup)*

1. Clone the repository.
2. Configure Google Cloud credentials.
3. Set up the MIMIC-III database.
4. Deploy using GCP tools (e.g., Cloud Run, App Engine, or Compute Engine).
5. Run load tests with Artillery.

---

## Future Improvements
- Expand FaaS usage for real-time analytics.
- Enhance media handling for larger file sizes.
- Add authentication and role-based access control.

---

## License
*(Add your preferred license here, e.g., MIT, Apache 2.0)*

---
*Last Updated: March 08, 2025*