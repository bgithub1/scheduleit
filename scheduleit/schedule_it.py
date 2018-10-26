'''
Created on Aug 10, 2018

Usage: python schedule_it.py hour 23
  

@author: bperlman1
'''
import pytz
from calendar import monthrange
import logging
import sys
import datetime as dt
import time
from pandas.tseries.holiday import USFederalHolidayCalendar


def init_root_logger(logfile,logging_level=None):
    level = logging_level
    if level is None:
        level = logging.DEBUG
    # get root level logger
    logger = logging.getLogger()
    if len(logger.handlers)>0:
        return logger
    logger.setLevel(logging.getLevelName(level))

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)   
    return logger

class ScheduleNext():
    """
    Sleep until the next occurence of second, minute,hour,day or month X.
    Example: Sleep until the next occurrence of second 14, for 10 successive minutes:
    for _ in range(10):
        sit = ScheduleNext('second',14) # set up scheduler
        sit.wait() # wait until the second hand is at 14
        time.sleep(3) # wait a couple of seconds and then do it again
    
    """
    def __init__(self,time_type,wait_until_value,timezone=None,logger=None):
        self.logger = logger if logger is not None else init_root_logger('ScheduleIt.log', 'INFO')
        self.time_type = time_type
        self.wait_until_value=wait_until_value
        self.timezone = pytz.timezone('America/New_York') if timezone is None else timezone
        
    def wait(self):
        this_time  = dt.datetime.now(self.timezone)
        next_time = self.next_execute_time(this_time)
        secs_to_wait = (next_time-this_time).total_seconds()
        self.logger.info("Sleeping at time %s for %f hours" %(str(this_time),secs_to_wait/3600.0))
        time.sleep(secs_to_wait)
        self.logger.info("Waking at time: %s" %(str(next_time)))
    
    def next_execute_time(self,last_execute_time):
        next_time = None
        n = dt.datetime.now(self.timezone)
        if self.time_type.lower()=='second':
            next_time = last_execute_time + dt.timedelta(seconds=self.wait_until_value - n.second + (60 if self.wait_until_value < n.second else 0))
        if self.time_type.lower()=='minute':
            next_time = last_execute_time + dt.timedelta(minutes=self.wait_until_value - n.minute + (60 if self.wait_until_value < n.minute else 0))
            next_time = next_time.replace(second=0)
        if self.time_type.lower()=='hour':
            next_time = last_execute_time + dt.timedelta(hours=self.wait_until_value - n.hour + (24 if self.wait_until_value < n.hour else 0))
            next_time = next_time.replace(minute=0,second=0)
        if self.time_type.lower()=='day':
            days_in_month = monthrange(last_execute_time.year,last_execute_time.month)[1]
            next_time = last_execute_time + dt.timedelta(days=self.wait_until_value - n.day + (days_in_month if self.wait_until_value < n.day else 0))
            next_time = next_time.replace(hour=0,minute=0,second=0)
        if self.time_type.lower()=='month':
            next_time = last_execute_time + dt.timedelta(months=self.wait_until_value - n.month + (12 if self.wait_until_value < n.month else 0))
            next_time = next_time.replace(day=0,hour=0,minute=0,second=0)
        return next_time

    def minimum_seconds_to_delay(self):
        if self.time_type.lower()=='second':
            return 3
        if self.time_type.lower()=='minute':
            return 63
        if self.time_type.lower()=='hour':
            return 60*60 + 3
        if self.time_type.lower()=='day':
            return 24*60*60 + 3
        if self.time_type.lower()=='month':
            return 12*24*60*60 + 3



class ScheduleDaily():
    def __init__(self,hour_to_wait_for,avoid_holidays=None,weekdays_to_avoid=None,logfile_path=None,logging_level=None):
        pass
        self.logger = init_root_logger(
                                               'logfile.log' if logfile_path is None else logfile_path,
                                               'INFO' if logging_level is None else logging_level)
        
        self.hour_to_wait_for = hour_to_wait_for
        wta = '5,6' if weekdays_to_avoid is None else weekdays_to_avoid
        self.days_to_go_back_to_sleep = [int(s) for s in wta.split(',')]
        self.avoid_holidays = True if avoid_holidays is None else avoid_holidays.lower()=='true'
        
        # get all of the holdidays in the current year
        cal = USFederalHolidayCalendar()
        y1 = dt.datetime.now().year                                                    
        y2= y1+1
        self.holidays = cal.holidays(start=str(y1)+'-01-01', end=str(y2)+'-01-01').to_pydatetime()
    
    def process(self):
        time_type = 'hour'
        wait_until_value = self.hour_to_wait_for
        sit = ScheduleNext(time_type=time_type,wait_until_value=wait_until_value)
        
        # calculate the total number of days that you might have to go back to sleep, b/c you don't want to wake up on one of those days
        #   those days could be like Saturday and Sunday, or any Holiday.
        #   The value total_days_to_go_back_to_sleep will equal the number of days in weekdays_to_avoid, plus 1 for the possibility of 
        #     waking up on a Holiday that you want to avoid waking up on.
        total_days_to_go_back_to_sleep = len(self.days_to_go_back_to_sleep) + 1
        for _ in range(total_days_to_go_back_to_sleep):
            try:
                # run wait in a try block so that if you are starting the routine on the hour that you are waiting, it will except, but's that's ok
                sit.wait()
            except:
                pass
            
            
            # get today's day number
            n = dt.datetime.now()
            todays_weekday = n.weekday()        
            # see of the day that we are waking up is a day to go back to sleep
            go_back_to_sleep = False
            if todays_weekday in self.days_to_go_back_to_sleep:
                go_back_to_sleep = True
            if n in self.holidays:
                go_back_to_sleep = True
            if go_back_to_sleep:
                # sleep 61 minutes
                time.sleep(60*61)
                # go back to sleep
                continue
            # if you get here, you will break and return to the caller
            break    
        
if __name__=='__main__':
    ''' 
    sys.argv[1]: a time type (second, minute, hour, day, month)
    sys.argv[2]: the time value (like 23 for 11 pm)
    Usage:
    python schedule_it.py hour 23
    
    '''
    time_type = sys.argv[1]
    wait_until_value = int(sys.argv[2])
    sit = ScheduleNext(time_type=time_type,wait_until_value=wait_until_value)
    sit.wait()
    if len(sys.argv)>3:            
        number_of_loops = int(sys.argv[3]) - 1
        for _ in range(number_of_loops):
            time.sleep(sit.minimum_seconds_to_delay())
            sit = ScheduleNext(time_type=time_type,wait_until_value=wait_until_value)
            sit.wait()
            
            
            
    