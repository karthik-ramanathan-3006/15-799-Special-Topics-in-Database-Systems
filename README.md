## Adding new Benchbase workloads
- Clone Andy's copy of Benchbase to `noispage-pilot/build/benchbase`:
```
cd ~/noisepage-pilot/build/benchbase
git remote add pavlo git@github.com:apavlo/benchbase.git
git fetch pavlo
git checkout -b project1
git branch -u pavlo/main project1
git pull
```
- Ensure that it always points to latest main for the purpose of this project
- Run the following commands to trigger a run:
```
# Load the benchmark schema
doit benchbase_run --benchmark="indexjungle" --config="./artifacts/project/indexjungle_config.xml" --args="--create=true --load=true"
doit project1_enable_logging
doit benchbase_run --benchmark="indexjungle" --config="./artifacts/project/indexjungle_config.xml" --args="--execute=true"
doit project1_disable_logging
```

## Getting workload data
