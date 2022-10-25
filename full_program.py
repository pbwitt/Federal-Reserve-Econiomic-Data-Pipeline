
import numpy as np
import pandas as pd
import schedule

from sys import argv, exit
import datetime


import time

##FIle
def pull(frequency):
    print('')
    print('\nRunning DataPull from full program script....')

    import DataPull as dp
    import pandas as pd
    #pull data from DataPull Class

    pull_data=dp.DataPull()
    fetch_data=pull_data.data_pull()
    print('DataPull Sucessful. ')
    print('writing raw appended data to disc')
    print(fetch_data.count())
    fetch_data.to_csv('result_set_from_automation.csv')
    result_set=fetch_data

    import importlib
    import DataWrangle as DW


    print('cleaning data')
    DW.DataWrangle.clean_data(result_set)
    print('cleanding data complete')
    print(result_set.columns)

    to_file=DW.DataWrangle.DQ_H6Measure(result_set,frequency,'NSA')
    to_file.to_csv('tofile.csv')


    pd.set_option('display.float_format', lambda x: '%.3f' % x)

def main():

    frequency= argv[2]

    print(argv[2])
    print(argv[1])

    schedule.every().day.at(argv[1]).do(pull,frequency)




    while True:
        print_msg = "\rWaiting for the next scheduled time, " + str(schedule.next_run())
        schedule.run_pending()
        # Loading 'animation' to see if script is running
        print(print_msg + "    -", end="")
        time.sleep(1)
        print(print_msg + ".   /", end="")
        time.sleep(1)
        print(print_msg + "..  -", end="")
        time.sleep(1)
        print(print_msg + "... \\", end="")
        time.sleep(1)
        print(print_msg + "    -", end="")
main()
