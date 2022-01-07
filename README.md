# gamma_entrainment_task

This code uses the RC+S time-series outputs as CSV files to adaptively update stimulation parameters in response to gamma entrainment.

## Getting started

This code uses Python 3.8.3

## Data
A practice RC+S time-series dataset that corresponds to a single trial is uploaded in /data. Each column in the dataset corresponds to an individual sensing channel.

## Usage
```run_entrainment_task``` contains arguments of: <sample_rate> <current_stim_freq> <current_stim_amp> <max_amp> <num_trials> <num_channel>
<br/>To run this function, navigate to the code folder of this repository in Terminal, and enter in parameters for the function. For example,
```
python3 code/run_entrainment_task.py 250 130 4 5 40 2
```

For each trial, you will be asked to enter the filepath of the corresponding time-series dataset:
```
Enter full path of current data:
```
A practice file is located in /data for test runs.

## Algorithm
The task begins at the input stimulation frequency and amplitude. Updates to each trial's stimulation frequency and amplitude are optimized to determine the edges of the Arnold Tongue representations of the stimulation parameter field composed of each trial's gamma entrainment. 
