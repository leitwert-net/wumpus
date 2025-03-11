# -*- coding: utf-8 -*-
"""
TRACE_THE_WUMPUS
Copyright (C) 2014-2025 Leitwert GmbH

This software is distributed under the terms of the MIT license.
It can be found in the LICENSE file or at https://opensource.org/licenses/MIT.

Author Johann SCHLAMP <schlamp@leitwert.net>
Author Leonhard RABEL <rabel@leitwert.net>
"""

# Wumpus prefixes
FILTER_PREFIX_IPV6 = '2a06:2904::/30'
FILTER_PREFIX_IPV4 = '194.145.125.128/25'

# IPv6 target prefixes
TRACE_PREFIX_GAME   = '2a06:2904::/32'
TRACE_PREFIX_MOVE   = '2a06:2905::/32'
TRACE_PREFIX_SHOOT  = '2a06:2906::/32'
TRACE_PREFIX_OUTPUT = '2a06:2907::/32'

# IPv4 target address
TRACE_TARGET_IPV4 = '194.145.125.135'

# Packets per hop
TRACE_PPH = 3

# Expiry timeout
TRACE_TIMEOUT = 1
GAME_TIMEOUT = 300

# Highscore entries
MAX_HIGHSCORE = 10
CSV_HIGHSCORE = '/srv/wumpus/data/score.csv'

# Game board
ROOMS = {
    1:  (2, 5, 8),
    2:  (1, 3, 10),
    3:  (2, 4, 12),
    4:  (3, 5, 14),
    5:  (1, 4, 6),
    6:  (5, 7, 15),
    7:  (6, 8, 17),
    8:  (1, 7, 9),
    9:  (8, 10, 18),
    10: (2, 9, 11),
    11: (10, 12, 19),
    12: (3, 11, 13),
    13: (12, 14, 20),
    14: (4, 13, 15),
    15: (6, 14, 16),
    16: (15, 17, 20),
    17: (7, 16, 18),
    18: (9, 17, 19),
    19: (11, 18, 20),
    20: (13, 16, 19),
}


class Input:
    """ Game input commands.
    """
    class Game:
        """ Function commands.
        """
        # Available game functions
        START  = 0
        PLAY   = 1
        REPLAY = 2
        HELP   = 3
        MAP    = 4
        SCORE  = 5

        # IPv4 fallback
        IPV4 = -1

    class Move:
        """ Move commands.
        """

    class Shoot:
        """ Shoot commands.
        """


class Output:
    """ Game output text.
    """
    # Title/map/help lines
    INFO_TITLE = [*range(0, 20)]
    INFO_MAP   = [*range(30, 49)]
    INFO_HELP1 = [*range(60, 75)]
    INFO_HELP2 = [*range(75, 86)]
    INFO_HELP3 = [*range(86, 99)]
    INFO_HELP4 = [*range(99, 112)]

    # Position/tunnel lines
    STATE_POSITION = [*range(120, 140)]
    STATE_TUNNELS  = [*range(150, 170)]

    # Game lines
    GAME_HUNT   = 180
    GAME_WIN    = 181
    GAME_LOSS   = 182
    GAME_PLAY   = 183
    GAME_REPLAY = 184
    GAME_MOVE   = 185
    GAME_SHOOT  = 186
    GAME_EMPTY  = 187
    GAME_SCORE  = 188

    # Hazard lines
    HAZARD_WUMPUS = 200
    HAZARD_BAT    = 201
    HAZARD_PIT    = 202

    # Action lines
    ACTION_UNKNOWN       = 220
    ACTION_SHOOT_INVALID = 221
    ACTION_SHOOT_HIT     = 222
    ACTION_SHOOT_SELF    = 223
    ACTION_SHOOT_MISSED  = 224
    ACTION_MOVE_INVALID  = 225
    ACTION_MOVE_WUMPUS   = 226
    ACTION_MOVE_PIT      = 227
    ACTION_MOVE_BAT      = 228
    ACTION_WUMPUS_GOTCHA = 229
    ACTION_EXPIRED       = 230

    # High score
    SCORE_HEAD = [*range(240, 249)]

    # IPv4 fallback
    INFO_IPV4 = ['.'.join(TRACE_TARGET_IPV4.split('.')[:-1] + [str(int(TRACE_TARGET_IPV4.rsplit('.', 1)[-1]) + a)])
                 for a in reversed(range(1, 13))]
