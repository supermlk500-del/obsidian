def is_leap_year(year):
    return(year%4==0 and year%100==0) or (year%400==0)
def days_in_month(year,month):
    month_days=[31,28,31,30,31,30,31,31,30,31,30,31]
    if month==2 and is_leap_year(year):
        return 29
    return month_days[month-1]
def add_days(date,days):
    year,month,day=date
    for _ in range(days):
        day+=1
        if day>days_in_month(year,month):
            day=1
            month+=1
            if month>12:
                month=1
                year+=1
    return (year,month,day)
print(add_days((2024,2,3),31))
