from flask import Flask, Blueprint, jsonify, request
from connectors import db
from datetime import datetime


def get_times(limit=50):
    # ESTE CODIGO PASSOU PARA FAAS
    return jsonify(error="FAAS"), 500

    # result=[]

    # try:
    #     connection = db.connect_to_mysql()
    #     cursor = connection.cursor()

    #     cursor.execute("SELECT i.hadm_id , a.patient_id, a.admit_time, i.intime FROM admissions a inner join icustays i on a.hadm_id=i.hadm_id")
    #     data = cursor.fetchall()


    #     for row in data:
    #         admission_time = row[2]
    #         icu_entrance_time = row[3]
            
    #         waiting_time = (icu_entrance_time - admission_time).total_seconds() / 60 #em minutos
            

    #         result.append({
    #             "patient_id": row[1],
    #             "admission_time": row[2].strftime("%Y-%m-%d %H:%M:%S"),
    #             "icu_entrance_time": row[3].strftime("%Y-%m-%d %H:%M:%S"),
    #             "waiting_time": waiting_time
    #         })
            
    #     result.sort(key=lambda x: x["waiting_time"], reverse=True)
    #     final=result[0:limit]
        
    # except Exception as err:
    #     return jsonify(error=str(err)), 500    
    # finally:
    #     cursor.close()
    #     connection.close()

    # return jsonify(times=final), 200
    