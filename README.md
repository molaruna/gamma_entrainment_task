# gamma_entrainment_task

This code uses the RC+S time-series outputs as CSV files to adaptively update stimulation parameters in response to gamma entrainment.

## Getting started

This code uses Python 3.8.3

## Data
A practice RC+S time-series dataset that corresponds to a single trial is uploaded in /data. Each column in the dataset corresponds to an individual sensing channel.

## Usage
In terminal, navigate to the code folder of this repository, and run code.run_entrainment_task():
```
python3 run_entrainment_task.py 250 130 4 5 40 2
