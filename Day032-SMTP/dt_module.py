import datetime as dt

now = dt.datetime.now()

print(now)
print(type(now))
print(now.year)

days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
print(days[now.weekday()])

date_of_birth = dt.datetime(year=1998, month=11, day=7)
print(date_of_birth)
