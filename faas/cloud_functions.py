import functions_framework
from services import waitingtime_svc

@functions_framework.http
def get_all_times_http(request):
    try:
        return waitingtime_svc.get_times()
    except Exception as err:
        return {"error": str(err)}, 500
