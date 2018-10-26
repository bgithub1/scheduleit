'''
Created on Aug 10, 2018
Schedule daily task, but ignore certain days or holidays

Usage:
        1. run normally (avoid holidays and Saturday and Sunday)
            python schedule_daily.py --hour_to_wait_for 11
        2. Don't avoid holidays, but avoid Saturday and Sunday)
            python schedule_daily.py --hour_to_wait_for 11 --avoid_holidays False
        3. Avoid Tuesday and Thursday and holidays, but don't avoid Saturday and Sunday)
            python schedule_daily.py --hour_to_wait_for 11 --weekdays_to_avoid '1,3' 
  

@author: bperlman1
'''

import argparse as ap


        
if __name__=='__main__':
    import os,sys
    sys.path.append(os.getcwd()+"/../")
    sys.path.append(os.getcwd())
    from scheduleit import  schedule_it as sch
    parser = ap.ArgumentParser()
    parser.add_argument('--hour_to_wait_for',type=int,help='a military hour to wait for (like 23 for 11 pm')
    parser.add_argument('--avoid_holidays', type=str, 
                        help="True if you avoid US bank holidays (default)",
                        nargs="?")
    parser.add_argument('--weekdays_to_avoid',type=str,
                        help='comma separate list of day numbers to avoid, where 0 is Monday and 6 is Sunday',
                        nargs="?")
    parser.add_argument('--logfile_path', type=str, help="path to a logfile", nargs="?")
    parser.add_argument('--logging_level', type=str, help="log level for logger", nargs="?")

    args = parser.parse_args()
    hour_to_wait_for = args.hour_to_wait_for
    avoid_holidays = args.avoid_holidays
    weekdays_to_avoid = args.weekdays_to_avoid
    logfile_path = args.logfile_path
    logging_level = args.logging_level
    sd  = sch.ScheduleDaily(hour_to_wait_for,
                        avoid_holidays=avoid_holidays,
                        weekdays_to_avoid=weekdays_to_avoid,
                        logfile_path=logfile_path,
                        logging_level=logging_level)
    sd.process()
         
            
            
    