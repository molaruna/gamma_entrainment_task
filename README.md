# gamma_entrainment_task

This code uses the raw JSON RC+S time-series outputs to adaptively update stimulation parameters in response to gamma entrainment.

## Getting started

This code uses Python 3.8.3 

## Data
Four practice RC+S time-series datasets that corresponds to four trials are uploaded in ./data/test_data. Each column in the dataset corresponds to an individual sensing channel.

## Usage
```run_entrainment_task``` contains arguments of: <data_dir> <max_amp> <num_trials> <channel>
<br/>To run this function, navigate to the parent directory of this repository in Terminal, and enter in parameters for the function. For example,
```
python3 code/run_entrainment_task.py './data' 4 4 2
```

For each trial, the program will stall until a new data directory is added into <data_dir>. For example,
```
mv ./data/test_data/Session_trial1 ./data
```

## Algorithm
The task begins at the input stimulation frequency and amplitude. Updates to each trial's stimulation frequency and amplitude are optimized to determine the edges of the Arnold Tongue representations of the stimulation parameter field composed of each trial's gamma entrainment. 
