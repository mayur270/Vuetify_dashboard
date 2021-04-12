from rest_framework.exceptions import APIException


class EndDateException(APIException):
    status_code = 400
    default_detail = "End Date is incorrect, add a later date"
    default_code = "End_Date is not correct"
