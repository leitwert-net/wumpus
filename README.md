# TRACE-THE-WUMPUS

> *»An exciting simulated hunt in a hidden maze of caverns and twisting tunnels!  
> Seek out the lair of the Wumpus, while avoiding perils along the way!«*

`~$ traceroute6 -f 8 -q 1 wumpus.quest`
```
traceroute to wumpus.quest (2a06:2904::10:10:10), 30 hops max, 80 byte packets
 8 W-------------------------------------------------------------W (2a06:2907::ff:ff:10)  32.379 ms
 9 W---WWWWWWW--WWWWWWW---WWWWW---WWWWWWW--WWWWWWW---------------W (2a06:2907::ff:ff:11)  56.951 ms
10 W---W--W--W---W----W---W---W----W----W---W----W---------------W (2a06:2907::ff:ff:12)  69.030 ms
11 W------W------WWWWWW---WWWWW----W--------WWWW-----------------W (2a06:2907::ff:ff:13)  59.887 ms
12 W------W------W--WW----W---W----W----W---W----W---------------W (2a06:2907::ff:ff:14)  41.416 ms
13 W-----WWW----WW---WW--WW---WW--WWWWWWW--WWWWWWW---------------W (2a06:2907::ff:ff:15)  44.857 ms
14 W-------------------------------------------------------------W (2a06:2907::ff:ff:16)  62.604 ms
15 W--------WWWWWWW--WW---WW--WWWWWWW----------------------------W (2a06:2907::ff:ff:17)  51.063 ms
16 W--------W--W--W---W---W----W----W----------------------------W (2a06:2907::ff:ff:18)  53.221 ms
17 W-----------W------WWWWW----WWWW------------------------------W (2a06:2907::ff:ff:19)  47.669 ms
18 W-----------W------W---W----W----W----------------------------W (2a06:2907::ff:ff:1a)  38.514 ms
19 W----------WWW----WW---WW--WWWWWWW----------------------------W (2a06:2907::ff:ff:1b)  74.751 ms
20 W-------------------------------------------------------------W (2a06:2907::ff:ff:1c)  71.737 ms
21 W---WW-------WW--WW---WW--WW---WW--WWWWWWW--WW---WW--WWWWWW---W (2a06:2907::ff:ff:1d)  35.490 ms
22 W----W---W---W----W---W----WW-WW----W----W---W---W---W--------W (2a06:2907::ff:ff:1e)  26.461 ms
23 W-----W-W-W-W-----W---W----W-W-W----WWWWWW---W---W---WWWWWW---W (2a06:2907::ff:ff:1f)  65.190 ms
24 W------W---W------W---W----W---W----W--------W---W--------W---W (2a06:2907::ff:ff:20)  55.469 ms
25 W-----WW---WW------WWW----WW---WW--WW---------WWW----WWWWWW---W (2a06:2907::ff:ff:21)  17.370 ms
26 W-------------------------------------------------------------W (2a06:2907::ff:ff:22)  44.477 ms
27 W--NEW.GAME--play.wumpus.quest-------HELP--help.wumpus.quest--W (2a06:2907::ff:ff:23)  18.802 ms
28 W-------------------------------------------------------------W (2a06:2904::10:10:10)  33.176 ms
```

## Overview

**`TRACE-THE-WUMPUS`** is a traceroute-based computer game ported from *Hunt
the Wumpus (1973)* by Gregory Yob. It was first published in [The Best of
Creative Computing](https://www.atariarchives.org/bcc1/showpage.php?page=247)
in 1976.

This repository contains a *programming task* for network students and
engineers. It provides a ready to use Docker setup and teaches IPv6 network
programming on layers 2-7 using Python.

## The task

You need to implement a Python component that emulates a network on layers 2-7.
Incoming traceroute packets towards that network must trigger replies
corresponding to the output of the **`TRACE-THE-WUMPUS`** text adventure. A
game engine provided with this code package determines response IP addresses
based on given source and target IP addresses of incoming packets:

```python
# Local imports
from wumpus.game import Game

# Constants
INTERFACE = "eth0"

# Global game engine
game = Game(verbose=True, debug=True)

# Sample game input
src = "2001::1"
dst = "2a06:2904::10:10:10"
proto = "udp"

# Sample game output
hops = game.handle_input(src, dst, proto)
```

Your task is to capture packets for the given `INTERFACE` and craft
TTL-exceeded packets according to the `hops` information provided by the game
engine. You may test your implementation using standard traceroute on Windows,
macOS or Linux.

Refer to [`src/trace.py`](src/trace.py) for a full list of TODOs and first
steps.

NOTE: The docker container provided with this repository sets up routing on
your local machine such that all packets towards `wumpus.quest` are forwarded
to the docker container. Updates to [`src/trace.py`](src/trace.py) outside the
container trigger a restart of the Python component within the container
(suitable for rapid prototyping).

#### Background

For an introduction to the Wumpus game and the features of the traceroute port,
refer to the slides presented at [RIPE89](https://ripe89.ripe.net/presentations/61-LEITWERT_2024-10-29_RIPE89_Trace-the-Wumpus.pdf).

#### Solution

There is a running instance of **`TRACE-THE-WUMPUS`** that can be played online
via `traceroute6 wumpus.quest`. If you are the teacher/advisor of a programming
course, you may contact us and we'll happily provide you with the reference
implementation.

## Compatibility

This package is compatible with `python3.6` and `pypy3.6-v7.0.0` or greater.

## Installation

Install `docker.io` and `docker-compose-v2` and run

```
~$ docker compose build
~$ docker compose up
```

to start the Wumpus docker container.

## Author

Johann SCHLAMP <[schlamp@leitwert.net](mailto:schlamp@leitwert.net)>

## License

Copyright (C) 2014-2025 Leitwert GmbH

This software is distributed under the terms of the MIT license.  
It can be found in the LICENSE file or at [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

<sub>OOPS - BUMPED A WUMPUS.</sub>
