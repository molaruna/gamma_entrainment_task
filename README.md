# gamma_entrainment_task

This code uses the RC+S time-series outputs as CSV files to adaptively update stimulation parameters in response to gamma entrainment.

## Getting started

This code uses Python 3.8.3

## Data
A practice RC+S time-series dataset that corresponds to a single trial is uploaded in /data. Each column in the dataset corresponds to an individual sensing channel.

## Usage
```run_entrainment_task``` contains arguments of <sample_rate> <current_stim_freq> <max_amp> <num_trials> <channels>
In terminal, navigate to the code folder of this repository, and run the task:
```
python3 code/run_entrainment_task.py 250 130 4 5 40 2
```

For each trial, you will be asked to enter in the time-series file:
```
Enter full path of current data:
```
A practice file is located in /data for test runs.
