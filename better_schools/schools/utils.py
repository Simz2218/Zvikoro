import datetime
import pandas as pd
from django.http import HttpResponse
import os
def safe_int(val):
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None

def get_current_year_term():
    now = datetime.date.today()
    month = now.month
    if month <= 4:
        term = 1
    elif month <= 8:
        term = 2
    else:
        term = 3
    return now.year, term

def parse_date_paid(date_str):
    dt = datetime.datetime.strptime(date_str[:10], "%Y-%m-%d")
    return int(dt.strftime("%Y%m%d"))

def validate_excel_file_extension(value):
    allowed = [".xls", ".xlsx"]
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed:
        raise serializer.ValidationError(
            f"Invalid file type {ext}. Only {', '.join(allowed)} allowed."
        )

def dataframe_to_excel_response(df, filename):
    resp = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    df.to_excel(resp, index=False)
    return resp
