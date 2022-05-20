#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Using the gamma entrainment protocol, this function computes 
the stimulation parameters of frequency and amplitude
for an entire gamma entrainment session

python3 run_entrainment_task.py <data_dir> <max_amp> <num_trials> <channel>
python3 run_entrainment_task.py  ./data 4 40 2 

@author: mariaolaru
"""

import sys
import ast
import os
import time
import json
import numpy as np
import pandas as pd
import signal_funcs as sgnl
import trial_funcs as trl

def get_current_sessions(main_dir):
    return os.listdir(main_dir)

def get_new_dir(main_dir, session_dir_list):
    new_list = os.listdir(main_dir)
    if new_list == session_dir_list:
        return ""
    else:
        file = set.pop(set(new_list) - set(session_dir_list))

    return os.path.join(main_dir, file)

def get_json_paths(session_dir):
    list_files = list()
    
    for (dirpath, dirnames, filenames) in os.walk(session_dir):
        list_files += [os.path.join(dirpath, file) for file in filenames]

    stim_fp = [string for string in list_files if 'StimLog.json' in string][0]
    td_fp = [string for string in list_files if 'RawDataTD.json' in string][0]
    
    return [stim_fp, td_fp]

#TO-DO: sanity-check sr of all packets 
def get_sr(td_data):
    sr_rcs = td_data[0]['SampleRate']

    dict_sr = {0: 250,
               1: 500,
               2: 1000}

    return dict_sr[sr_rcs]

#TO-DO: sanity-check this with Maria S.
def get_stim_params(stim_filepath):
    f = open(stim_filepath)
    data = json.load(f)
    
    data = data[1 :] #remove 1st index containing all therapy configurations
    
    df = pd.json_normalize(data)
    
    stim_freq_label = [string for string in df.columns if 'RateInHz' in string][0]
    stim_freq = df[stim_freq_label].values[0]
    
    stim_amp_label = [string for string in df.columns if 'AmplitudeInMilliamps' in string][0]
    stim_amp = df[stim_amp_label].values[0]

    return [stim_freq, stim_amp]

def get_ts(td_filepath, channel):
    f = open(td_filepath)
    data = json.load(f)

    td_data = data[0]['TimeDomainData']
    sr = get_sr(td_data)
    
    packets = pd.json_normalize(td_data, "ChannelSamples")
    packets = packets[packets['Key'] == channel]

    packet_vals = packets.Value.values
    
    timeseries = np.concatenate(packet_vals)

    return [timeseries, sr]

def main():
#def main(main_dir, max_amp, num_trials, channel):
    main_dir = sys.argv[1]
    max_amp = float(sys.argv[2])
    num_trials = int(sys.argv[3])
    channel = ast.literal_eval(sys.argv[4])      

    #these parameters may change on a pt-by-pt basis
    #debugging:
    
    #main_dir = './data'
    #max_amp = 4
    #num_trials = 4
    #channel = 2
    
    STIM_AMP_INTERVAL = 0.3 #need to program in a ramp rate of 0.1mA/s    
    STIM_FREQ_INTERVAL = 2


    df_trials = pd.DataFrame(np.NaN, np.arange(0, num_trials, 1), 
                             ['stim_amp', 'stim_freq', 'entrained'])   
    df_trials.index.name = 'trial'
    
    session_dir_list = get_current_sessions(main_dir)
    #Calculate each trial's stim parameters for the entire session
    for i in range(num_trials):
        
        #Wait to execute code until a new file is detected in the parent directory
        new_session_dir = get_new_dir(main_dir, session_dir_list)

        while not new_session_dir:
            time.sleep(1)
            new_session_dir = get_new_dir(main_dir, session_dir_list)
            
        [stim_filepath, td_filepath] = get_json_paths(new_session_dir)    

        [timeseries, sr] = get_ts(td_filepath, channel)        
        [stim_freq, stim_amp] = get_stim_params(stim_filepath)
        
        df_trials.loc[i, 'stim_amp'] = stim_amp
        df_trials.loc[i, 'stim_freq'] = stim_freq
         
        entrained_arr = sgnl.compute_trial_entrainment(timeseries, sr, df_trials['stim_freq'][i])
        trial_entrained = sgnl.compute_entrainment_decision(entrained_arr)
        df_trials.loc[i, 'entrained'] = trial_entrained
        
        entrain_trial_kernel = np.NaN
        [amp_next, freq_next, entrain_trial_kernel] = trl.get_next_trial_params(df_trials, max_amp, STIM_AMP_INTERVAL, STIM_FREQ_INTERVAL, stim_freq, entrain_trial_kernel)

        session_dir_list = get_current_sessions(main_dir)

        print('next trial (#' + str(i) + ') stimulation frequency: ', freq_next)
        print('next trial (#' + str(i) + ') stimulation amplitude: ', amp_next, '\n')
    
    print(df_trials)

if __name__ == '__main__':
    main()
    