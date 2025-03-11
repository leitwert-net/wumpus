#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRACE_THE_WUMPUS
Copyright (C) 2014-2025 Leitwert GmbH

This software is distributed under the terms of the MIT license.
It can be found in the LICENSE file or at https://opensource.org/licenses/MIT.

Author Johann SCHLAMP <schlamp@leitwert.net>
"""

# Local imports
from wumpus.game import Game
from wumpus.const import FILTER_PREFIX_IPV6
from wumpus.const import FILTER_PREFIX_IPV4

# Constants
INTERFACE = "eth0"

# Global game engine
game = Game(verbose=True, debug=True)

# Sample game input
src, dst, proto = "2001::1", "2a06:2904::10:10:10", "udp"

# Sample game output
hops = game.handle_input(src, dst, proto)
print(f"Sample traceroute from {src} to {dst}:" + "\n -> ".join(hops))

# TODO WWWWWWWWWWWWWW
# TODO W YOUR TASKS W
# TODO WWWWWWWWWWWWWW
# TODO
# TODO • Capture and print packets for given INTERFACE
# TODO
# TODO • Implement ICMP ping for incoming echo requests
# TODO   —> test with "ping wumpus.quest"
# TODO
# TODO • Implement ICMP traceroute for incoming TCP/UDP requests
# TODO   —> generate response IP addresses with game.handle_input()
# TODO   —> test with "traceroute wumpus.quest"
# TODO
# TODO • Rewrite both routines to support ICMPv6
# TODO   —> test with "ping6 wumpus.quest"
# TODO   —> test with "traceroute6 wumpus.quest"
# TODO
# TODO • Play the wumpus.quest and have fun :)
