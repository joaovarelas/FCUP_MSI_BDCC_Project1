from flask import Flask, Blueprint, jsonify, request
from connectors import db
from datetime import datetime


def get_times(limit=50):
    result=[]

    try:
        connection = db.connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute("SELECT i.hadm_id , a.patient_id, a.admit_time, i.intime FROM ADMISSIONS a inner join ICUSTAYS i on a.hadm_id=i.hadm_id LIMIT %s", (limit,))
        data = cursor.fetchall()


        for row in data:
            admission_time = row[2]
            icu_entrance_time = row[3]
            
            waiting_time = (icu_entrance_time - admission_time).total_seconds() / 60 #em minutos
            

            result.append({
                "patient_id": row[1],
                "admission_time": row[2].strftime("%Y-%m-%d %H:%M:%S"),
                "icu_entrence_time": row[3].strftime("%Y-%m-%d %H:%M:%S"),
                "waiting_time": waiting_time
            })
        
    except Exception as err:
        return jsonify(error=str(err)), 500    
    finally:
        cursor.close()
        connection.close()

    return jsonify(times=result), 200
    