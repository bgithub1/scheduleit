#!/usr/bin/env bash
#example usage
# run daily at 10 am, avoid weekends and holidays (default
#  bash schedule_daily_example.sh regular 
# run by hour
#  bash schedule_daily_example.sh on_holidays avoid weekends only
# run regular, but avoid tuesday's and thursdays
#  bash schedule_daily_example.sh not_tues_thurs


run_type=$1
if [[ -z ${run_type} ]]
then
   run_type=regular
fi

if [[ ${run_type} = 'regular' ]]
then
   for i in {1..1000};do python schedule_daily.py --hour_to_wait_for 10;echo daily run regular;sleep 3600;done
elif [[ ${run_type} = 'on_holidays' ]]
then
   for i in {1..1000};do python schedule_daily.py --hour_to_wait_for 10 --avoid_holidays False;echo daily run on holidays;sleep 3600;done
elif [[ ${run_type} = 'not_tues_thurs' ]]
then
   for i in {1..1000};do python schedule_daily.py --hour_to_wait_for 10 --weekdays_to_avoid '1,3';echo daily run avoid tues and thurs;sleep 3600;done
fi
