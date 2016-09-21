# Send Icecast listeners to Graphite

Grabs the current listener count for a given Icecast mountpoint and shoves it into Graphite. No fuss.


## Installation

There isn't really much to do besides

```sh
pip install -r requirements.txt
```

You know the drill about virtual envs and all that already.


## Usage


```sh
icecast_listeners_to_carbon.py  --host streamer.host.tld --port 8000 --user admin --password hackme --mountpoint /live.mp3 --metric listeners-live
```

The full set of options is:

```sh
$ ./icecast_listeners_to_carbon.py
usage: icecast_listeners_to_carbon.py [-h] --host HOST --port PORT --user USER
                                      --password PASSWORD --mountpoint
                                      MOUNTPOINT [--metric METRIC]
                                      [--graphite-server GRAPHITE_SERVER]
                                      [--graphite-port GRAPHITE_PORT]
                                      [--dry-run]
```

If not given the metric will be 'mountpoint-listeners'.
You probably want to run this periodically from cron or something like that. (and change the default password too...)
