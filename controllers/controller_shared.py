from datetime import date


def get_back_stringdate_into_date(date_variable):
    temp_parsed_date = date_variable.split('-')
    year = temp_parsed_date[0]
    if int(year) < 10 and len(year) < 2:
        year = f"000{year}"
    elif int(year) > 9 and int(year) < 100 and len(year) < 3:
        year = f"00{year}"
    elif int(year) > 99 and int(year) < 1000 and len(year) < 4:
        year = f"0{year}"
    month = temp_parsed_date[1]
    day = temp_parsed_date[2]
    parsed_date = date.fromisoformat(f"{year}-{month}-{day}")
    return parsed_date
