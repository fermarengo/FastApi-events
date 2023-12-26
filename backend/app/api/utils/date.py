from datetime import datetime


def get_day_of_week(datetime: datetime):
    day_off_week = datetime.weekday()
    days = {
        0: "Lun",
        1: "Mar",
        2: "Mié",
        3: "Jue",
        4: "Vie",
        5: "Sab",
        6: "Dom",
    }
    return days[day_off_week]
