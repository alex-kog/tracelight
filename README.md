# TraceLight

This project is being developed for the "bitemBassy Hackathon 2018" https://www.hackbtc.org/

### Setup your LND Node
* https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md

### LND Documentation
* https://dev.lightning.community/
* https://api.lightning.community/


## What is TraceLight?

<MEDIUM POST LINK HERE>

## How to use Tracelight

### Preliminaries

In order to work with `tlcli`, the following dependencies are required:
  * Python 2.7+
  * Rscript
  
### Running TraceLight

To run Tracelight, a user should supply the pubkey of a destination node and amount he wish to test.

Tracelight has two modes: FULL and PRINT.
In FULL mode, TraceLight queries the current state of the LND network and ouputs the report.
In PRINT mode, TraceLight replays the log of a previous recoreded report.

#### FULL Mode
```
./tlcli -d 02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490 -a 400000 -t FULL
```

#### PRINT Mode
```
./tlcli -d 02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490 -a 400000 -t PRINT
```
