# -*- coding: utf-8 -*-
"""
TRACE_THE_WUMPUS
Copyright (C) 2014-2025 Leitwert GmbH

This software is distributed under the terms of the MIT license.
It can be found in the LICENSE file or at https://opensource.org/licenses/MIT.

Author Johann SCHLAMP <schlamp@leitwert.net>
Author Leonhard RABEL <rabel@leitwert.net>
"""

# System imports
import datetime
import os

# Local imports
from wumpus.const import Input
from wumpus.const import Output
from wumpus.iputil import input_ip
from wumpus.iputil import output_ip
from wumpus.session import Session
from wumpus.const import MAX_HIGHSCORE
from wumpus.const import CSV_HIGHSCORE


class Game:
    """ Game instance.
    """
    def __init__(self, logfile=None, verbose=False, debug=False):
        """ Initialize game.
        """
        # Prepare internals
        self.sessions = dict()
        self.highscore = dict()
        self.logfile = logfile
        self.verbose = verbose
        self.debug = debug
        self.error = False

        # Load highscore
        if os.path.isfile(CSV_HIGHSCORE) is True:
            with open(CSV_HIGHSCORE, 'r', encoding='utf-8') as fh:
                for line in fh:
                    _, player, duration = line.strip().split(',')
                    duration = float(duration)
                    if duration <= self.highscore.get(player, duration):
                        self.highscore[player] = duration

    def handle_input(self, client, target, proto=None, add_delays=False):
        """ Handle game input represented by <target> for player identified by <client>.
        """
        # Reset error
        self.error = False

        def handle():
            """ Generate output message(s) for given input command.
            """
            # Clear expired sessions
            for player in list(self.sessions):
                if self.sessions[player].expired() is True:
                    del self.sessions[player]

            # Access or initialize client session
            session = self.sessions.get(client, None)
            if session is None:
                session = Session(self.log_debug, client)
                self.sessions[client] = session

            # Renew timeout of client session
            self.sessions[client].update()

            # Parse target details
            cmd, action = input_ip(target)

            # Output debug message
            if self.debug is True:
                cmd_str = cmd.__name__.lower() if cmd is not None else '?'
                action_str = str(action) if action is not None else '?'
                proto_str = str(proto) if proto is not None else '?'
                self.log_debug(f'CMD [client={client}, target={target}, proto={proto_str}, cmd={cmd_str}, '
                               f'action={action_str}]')

            # Handle game commands
            if cmd == Input.Game:

                # Display IPv4 fallback
                if action == Input.Game.IPV4:
                    return session.output_ipv4()

                # Display help
                if action == Input.Game.HELP:
                    return session.output_help()
                session.last_help = -1

                # Display map
                if action == Input.Game.MAP:
                    return session.output_map()

                # Show high score
                if action == Input.Game.SCORE:
                    output = session.output_score()

                    # Add top players
                    last_duration = 0
                    for player, duration in sorted(self.highscore.items(), key=lambda item: item[1])[:MAX_HIGHSCORE]:
                        output.append((player, duration - last_duration))
                        last_duration = duration
                    if len(self.highscore) < MAX_HIGHSCORE:
                        output += [(None, None)] * (MAX_HIGHSCORE - len(self.highscore))

                    # Add footer and return output
                    output.append(Output.GAME_EMPTY)
                    output.append(Output.GAME_PLAY)
                    return output

                # Welcome new player
                if action == Input.Game.START:
                    session.clear()
                    return session.output_title()

                # Start new game
                if action == Input.Game.PLAY:
                    session.new()
                    return session.output_state(initial=True)

                # Disallow any actions (expired session)
                if session.live is False:
                    return session.output_expired()

                # Replay last game
                if action == Input.Game.REPLAY:
                    session.reset()
                    return session.output_state(initial=True)

                # Invalid command
                self.error = True
                return session.output_invalid()

            # Handle invalid command
            if cmd not in {Input.Move, Input.Shoot}:
                self.error = True
                return session.output_invalid()

            # Disallow any commands (expired session)
            if session.live is False:
                return session.output_expired()

            # Disallow any commands (already won)
            if session.won is True:
                return session.output_win()

            # Disallow any commands (already lost)
            if session.lost is True:
                return session.output_loss()

            # Handle move command
            if cmd == Input.Move:
                return session.move(action) + session.output_state()

            # Handle shoot command
            if cmd == Input.Shoot:
                output = session.shoot(action) + session.output_state()

                # Update highscore
                if session.won is True and session.scores is True:
                    self.log_debug(f'SCORE [client={client}, duration={session.duration:.3f}s]')
                    if session.duration <= self.highscore.get(client, session.duration):
                        self.highscore[client] = session.duration
                    with open(CSV_HIGHSCORE, 'a', encoding='utf-8') as fh:
                        fh.write(f'{int(self.utc(formatted=False))},{client},{session.duration:.3f}\n')

                # Return output
                return output

            # Handle invalid command
            self.error = True
            return session.output_invalid()

        # Handle input commands and prepare output messages (including optional sleep)
        output_ips = [(output_ip(oid), None) if isinstance(oid, tuple) is False else (output_ip(oid[0]), oid[1])
                      for oid in handle()]

        # Add target to output message
        if self.error is False:
            if target not in set(output_ips):
                output_ips.append((target, None))
        else:
            output_ips.append((output_ip(Output.GAME_EMPTY), None))

        # Return output messages
        if add_delays is False:
            return [oip[0] for oip in output_ips]
        return output_ips

    ###########
    # HELPERS #
    ###########

    def log_debug(self, message):
        """ Log debug message.
        """
        # Print colored console output
        msg = f'{self.utc()} {message}'
        if self.logfile is not None:
            with open(self.logfile, 'a', encoding='utf-8') as fh:
                fh.write(msg + '\n')
        if self.verbose is True and self.debug is True:
            print(f'\033[1;90m{msg}\033[0m\033[27m')

    def log_error(self, message):
        """ Log error message.
        """
        msg = f'{self.utc()} ERROR {message}'
        if self.logfile is not None:
            with open(self.logfile, 'a', encoding='utf-8') as fh:
                fh.write(msg + '\n')
        if self.verbose is True:
            print(f'\033[1;31m{msg}\033[0m\033[27m')

    @staticmethod
    def utc(formatted=True):
        """ Return current timestamp relative to UTC epoch.
        """
        ts = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
        if formatted is True:
            dt = datetime.datetime.utcfromtimestamp(ts)
            millis = f'{dt.microsecond / 1000.0:03.0f}'
            return f'{dt.strftime("%Y-%m-%d %H:%M:%S")}.{millis[0:3]}'
        return ts
