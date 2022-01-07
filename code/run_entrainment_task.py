#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Using the gamma entrainment protocol, this function computes 
the stimulation parameters of frequency and amplitude
for an entire gamma entrainment session

python3 run_entrainment_task.py <sr> <curr_stim_freq> <curr_stim_amp>  <max_amp> <num_trials> <channels>
python3 run_entrainment_task.py 250 130 4 5 40 2 

@author: mariaolaru
"""

import sys
import ast
import numpy as np
import pandas as pd
import signal_funcs as sgnl
import trial_funcs as trl

def get_stim_amp_labels(clin_stim_amp, max_amp, STIM_AMP_MIN_INTERVAL):
    min_amp = round(clin_stim_amp % STIM_AMP_MIN_INTERVAL, 5)

    lower_labels = np.arange(min_amp, clin_stim_amp, STIM_AMP_MIN_INTERVAL).round(1)
    upper_labels = np.arange(clin_stim_amp, max_amp + .001, STIM_AMP_MIN_INTERVAL).round(1)
    labels = np.concatenate((lower_labels, upper_labels))  

    return labels

def get_freq_amp_labels(MIN_STIM_FREQ, MAX_STIM_FREQ, STIM_FREQ_MIN_INTERVAL):
     labels = np.arange(MIN_STIM_FREQ, MAX_STIM_FREQ, STIM_FREQ_MIN_INTERVAL)
     return labels

def main():
    #Assumption: time domain data (tdd) is imported as csv filepath
    sr = int(sys.argv[1])
    clin_stim_freq = float(sys.argv[2])    
    clin_stim_amp = float(sys.argv[3])
    max_amp = float(sys.argv[4])
    num_trials = int(sys.argv[5])
    channels = ast.literal_eval(sys.argv[6])  

    """
    #inputs for debugging: 
    sr = 250 #sampling rate (Hz)
    clin_stim_freq = 130 #clinically therapeutic stimulation frequency (Hz)
    clin_stim_amp = 2.5 #clinically therapeutic stimulation amplitude (mA)
    native_stim_freq = 180 #clinically therapeutic stimulation frequency (Hz)
    native_stim_amp = 3 #clinically therapeutic stimulation amplitude (mA)
    max_amp = 5 #maximum amplitude that is reachable
    num_trials = 40 #number of trials in one session
    channels = [2,3] #the channels to analyze for entrainment
    """
    
    STIM_AMP_INTERVAL = 0.3 #need to program in a ramp rate of 0.1mA/s    
    STIM_FREQ_INTERVAL = 2

    STIM_AMP_MIN_INTERVAL = STIM_AMP_INTERVAL
    STIM_FREQ_MIN_INTERVAL = STIM_FREQ_INTERVAL

    MIN_STIM_FREQ = 100
    MAX_STIM_FREQ = 210

    #stim_amp_labels = get_stim_amp_labels(clin_stim_amp, max_amp, STIM_AMP_MIN_INTERVAL)
    #stim_freq_labels = get_freq_amp_labels(MIN_STIM_FREQ, MAX_STIM_FREQ, STIM_FREQ_MIN_INTERVAL)
    
#    df_trial_map = pd.DataFrame(np.NaN, stim_amp_labels, stim_freq_labels)
    df_trials = pd.DataFrame(np.NaN, np.arange(0, num_trials, 1), ['stim_amp', 'stim_freq', 'entrained'])    
    
    #Calculate each trial's stim parameters for the entire session
    for i in range(num_trials-1):
        if i == 0:
            df_trials['stim_amp'][i] = clin_stim_amp
            df_trials['stim_freq'][i] = clin_stim_freq

        tdd_fp = input("Enter full path of current data: ")
        #tdd_fp = '/Users/mariaolaru/Documents/temp/practice_tdd.csv' #debugging
        tdd_orig = np.loadtxt(open(tdd_fp, "rb"), delimiter = ",", skiprows = 1)
        tdd = tdd_orig[:, channels]
        
        entrained_arr = sgnl.compute_trial_entrainment(tdd, sr, df_trials['stim_freq'][i])
        trial_entrained = sgnl.compute_entrainment_decision(entrained_arr)
        df_trials.loc[i, 'entrained'] = trial_entrained
        
        entrain_trial_kernel = np.NaN
        [amp_next, freq_next, entrain_trial_kernel] = trl.get_next_trial_params(df_trials, max_amp, STIM_AMP_INTERVAL, STIM_FREQ_INTERVAL, clin_stim_freq, entrain_trial_kernel)

        df_trials.loc[i+1, 'stim_freq'] = freq_next
        df_trials.loc[i+1, 'stim_amp'] = amp_next

        print('trial' + str(i+1) + ' stimulation frequency: ', freq_next)
        print('trial' + str(i+1) + ' stimulation amplitude: ', amp_next)
                
if __name__ == '__main__':
    main()