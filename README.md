# gamma_entrainment_task

This code uses the raw JSON RC+S time-series outputs to adaptively update stimulation parameters in response to gamma entrainment.

## Getting started

This code uses Python 3.8.3. Here's how to replicate the exact environment: 
```
conda create --name entrain_env --file spec-file.txt
```

## Data
Four practice RC+S Session directories that correspond to four trials are uploaded in ./data/test_data. 

## Usage
```run_entrainment_task``` contains arguments of: <data_dir> <max_amp> <num_trials> <channel>
<br/>To run this function, navigate to the parent directory of this repository in Terminal, and enter in parameters for the function. For example,
```
python3 code/run_entrainment_task.py './data' 4 4 2
```

For each trial, the program will stall until a new data directory is added into <data_dir>. Here's one way to add data for a new trial when using the practice Session directories:
```
mv ./data/test_data/Session_trial1 ./data
```
Here's the output when using the practice datasets:
```
(py383) ➜  entrainment_task git:(main) ✗ python3 code/run_entrainment_task.py './data' 4 4 2
next trial (#0) stimulation frequency:  129.9
next trial (#0) stimulation amplitude:  2.7 

next trial (#1) stimulation frequency:  129.9
next trial (#1) stimulation amplitude:  2.4 

next trial (#2) stimulation frequency:  129.9
next trial (#2) stimulation amplitude:  2.1 

next trial (#3) stimulation frequency:  129.9
next trial (#3) stimulation amplitude:  1.8 

       stim_amp  stim_freq entrained
trial                               
0           3.0      129.9     False
1           2.7      129.9     False
2           2.4      129.9     False
3           2.1      129.9     False
```

## Algorithm
The task begins at the input stimulation frequency and amplitude. Updates to each trial's stimulation frequency and amplitude are optimized to determine the edges of the Arnold Tongue representations of the stimulation parameter field composed of each trial's gamma entrainment. 
