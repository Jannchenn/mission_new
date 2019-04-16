#!/usr/bin/env bash

# roomba experiment
filename="indep_var.txt"
while read -r line
do
    para="$line"
    indep_var=(${para})
    echo ${indep_var[0]} ${indep_var[1]} ${indep_var[2]} ${indep_var[3]} ${indep_var[4]}>| boardinput.txt     # indep_var includes the current prob & dur_expo & arr_rate & arr_num & die_rate
    counter=1
    while [ ${counter} -le 1 ]
    do
        python Main.py
        ((counter++))
    done
    python WriteReport.py ${indep_var[0]} ${indep_var[1]} ${indep_var[2]} ${indep_var[3]} ${indep_var[4]} "dur" "0"
done < "$filename"
python Avgtime.py # 算时间的，这样之后random的时间和Roomba是一样的
python Edit.py

# random experiment
filename="indep_var.txt"
while read -r line
do
    para="$line"
    indep_var=(${para})
    echo ${indep_var[0]} ${indep_var[1]} ${indep_var[2]} ${indep_var[3]} ${indep_var[4]}>| boardinput.txt     # indep_var includes the current prob & dur_expo & arr_rate & arr_num & die_rate
    counter2=1
    while [ ${counter2} -le 1 ]
    do
        python Main.py
        ((counter2++))
    done
    python WriteReport.py ${indep_var[0]} ${indep_var[1]} ${indep_var[2]} ${indep_var[3]} ${indep_var[4]} "dur" "1"
done < "$filename"