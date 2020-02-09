from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Appointment

class Calendar(HTMLCalendar):
    def __init__(self ,year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar ,self).__init__()
     #bu takvim oluşturuyo ve superle inherit ediyo

    def formatday(self, day,weekday, appointments):
        events_per_day = appointments.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
    def formatmonth(self, theyear, themonth, withyear=True):
        events = Appointment.objects.filter(start_time__year=theyear, start_time__month=themonth)
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="calendar">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)