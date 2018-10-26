#!/usr/bin/env bash
#example usage
# run daily
#  bash schedule_daily_example.sh each_day
# run by hour
#  bash schedule_it_example.sh each_hour
# run by minute (default)
#  bash schedule_it_example.sh each_minute


run_type=$1
if [[ -z ${run_type} ]]
then
   run_type=each_minute
fi

if [[ ${run_type} = 'each_minute' ]]
then
   for i in {1..1000};do python schedule_it.py second 57;echo saying hello on second 57 of each minute;sleep 12;done
elif [[ ${run_type} = 'each_hour' ]]
then
   for i in {1..1000};do python schedule_it.py minute 57;echo saying hello on minute 57 of each hour;sleep 120;done
elif [[ ${run_type} = 'each_day' ]]
then
   for i in {1..1000};do python schedule_it.py hour 23;echo saying hello on hour 23;sleep 3700;done
fi