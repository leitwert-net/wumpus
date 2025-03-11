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
import math
import socket
import struct

# Local imports
from wumpus.const import Input
from wumpus.const import TRACE_PREFIX_GAME
from wumpus.const import TRACE_PREFIX_MOVE
from wumpus.const import TRACE_PREFIX_SHOOT
from wumpus.const import TRACE_PREFIX_OUTPUT
from wumpus.const import TRACE_TARGET_IPV4

# Host constants
FIXED_HOST_BYTES = 6
FIXED_HOST_VALUE_BITS = 16
FIXED_HOST_VALUE_CHARS = 2
FIXED_HOST_VALUE_OFFSET = 2**((FIXED_HOST_VALUE_CHARS - 1) * 4)
FIXED_HOST_VALUES = 2**(FIXED_HOST_VALUE_CHARS * 4) - FIXED_HOST_VALUE_OFFSET


################
# INPUT/OUTPUT #
################

def game_ip(action, fwd=True):
    """ Convert game command to IPv6 address.
    """
    if fwd is not True:
        return int2rdns(int_to_host(action))
    return int2ip(cidr2int(TRACE_PREFIX_GAME)[0] + int_to_host(action))


def move_ip(room, fwd=True):
    """ Convert move command to IPv6 address.
    """
    if fwd is not True:
        return int2rdns(int_to_host(room))
    return int2ip(cidr2int(TRACE_PREFIX_MOVE)[0] + int_to_host(room))


def shoot_ip(shots, fwd=True):
    """ Convert shoot command to IPv6 address.
    """
    shots_int = 0
    for n_shot, shot in enumerate(shots):
        shots_int += shot * 21 ** n_shot
    if fwd is not True:
        return int2rdns(int_to_host(shots_int))
    return int2ip(cidr2int(TRACE_PREFIX_SHOOT)[0] + int_to_host(shots_int))


def output_ip(oid, fwd=True):
    """ Convert output text ID to IPv6 address (or reverse zone).
    """
    if oid is None or isinstance(oid, str) is True:
        return oid
    if fwd is not True:
        return int2rdns(int_to_host(240**3 - 240 + oid))
    return int2ip(cidr2int(TRACE_PREFIX_OUTPUT)[0] + int_to_host(240**3 - 240 + oid))


def input_ip(ip):
    """ Split IPv6 integer into net (command) and host (action) parts.
    """
    # Parse input IP address
    cmd, action = None, None
    try:
        # Support IPv4 in fallback mode
        if ip == TRACE_TARGET_IPV4:
            return Input.Game, Input.Game.IPV4

        # Ignore any other IPv4 address
        if ipv4(ip) is True:
            return None, None

        # Convert IPv6 address to integer
        ipint = ip2int(ip)

        # Split into network and fixed-size host integers
        cmd = (ipint >> (FIXED_HOST_BYTES * 8)) << (FIXED_HOST_BYTES * 8)
        cmd = {cidr2int(p)[0]: p for p in (TRACE_PREFIX_GAME, TRACE_PREFIX_MOVE, TRACE_PREFIX_SHOOT)}.get(cmd, None)
        if cmd is not None:
            action = host_to_int(ipint & (2**(FIXED_HOST_BYTES * 8) - 1))

        def int_to_shots(shots_int):
            """ Compute shot factors from fixed-base shot integer.
            """
            # Iterate shots
            shots = list()
            while True:
                shots_int, shot = divmod(shots_int, 21)
                shots.append(shot)
                if shots_int == 0:
                    break

            # Return tupelized shots
            return tuple(shots) if len(shots) > 0 else None

        # Parse command and action
        cmd, parse_action = {
            TRACE_PREFIX_GAME: (Input.Game, None),
            TRACE_PREFIX_MOVE: (Input.Move, None),
            TRACE_PREFIX_SHOOT: (Input.Shoot, int_to_shots),
        }.get(cmd, (None, None))
        if parse_action is not None:
            action = parse_action(action)

    # Ignore command/action errors
    except:  # pylint: disable=bare-except
        pass

    # Return parsed result
    return cmd, action


################
# HOST MAPPING #
################

def int_to_host(value):
    """ Convert integer value to fixed-length IPv6 host.
    """
    # Convert value to host part
    host, n_bytes = 0, 0
    while value > 0:
        value, byte = divmod(value, FIXED_HOST_VALUES)
        host += (byte + FIXED_HOST_VALUE_OFFSET) << (n_bytes * FIXED_HOST_VALUE_BITS)
        n_bytes += 1

    # Fill up to fixed length
    for n_bytes in range(n_bytes, math.ceil(FIXED_HOST_BYTES / FIXED_HOST_VALUE_CHARS)):
        host += FIXED_HOST_VALUE_OFFSET << (n_bytes * FIXED_HOST_VALUE_BITS)

    # Return host integer
    return host


def host_to_int(host):
    """ Convert fixed-length IPv6 host to integer value.
    """
    # Reconstruct original integer value
    value, n_bytes = 0, 1
    while host > 0:
        value += ((host & (2**FIXED_HOST_VALUE_BITS - 1)) - FIXED_HOST_VALUE_OFFSET) * FIXED_HOST_VALUES**(n_bytes - 1)
        host >>= FIXED_HOST_VALUE_BITS
        n_bytes += 1

    # Return original integer value
    return value


#################
# IP CONVERSION #
#################

def ipv4(ip):
    """ Check if input is an IPv4 address.
    """
    try:
        struct.unpack('!I', socket.inet_pton(socket.AF_INET, ip))
    except (ValueError, OSError):
        return False
    return True


def int2ip(addr):
    """ Convert an IPv6 address from 128 bit unsigned integer to dotted notation.
    """
    net, host = int(addr >> 64), int(0xffffffffffffffff & addr)
    try:
        return socket.inet_ntop(socket.AF_INET6, struct.pack("!QQ", int(net), int(host)))
    except (socket.error, struct.error) as error:
        raise ValueError("invalid ip address") from error


def ip2int(addr):
    """ Convert an IPv6 address from dotted notation to 128 bit unsinged integer.
    """
    try:
        hi, lo = struct.unpack("!QQ", socket.inet_pton(socket.AF_INET6, addr))
        return (int(hi) << 64) + int(lo)
    except (socket.error, struct.error) as error:
        raise ValueError("invalid ip address") from error


def int2rdns(addr):
    """ Convert an IPv6 address from integer to reversed dotted notation for arpa zones.
    """
    ip = list()
    for _ in range(0, 128 - cidr2int(TRACE_PREFIX_OUTPUT)[1], 4):
        ip.append(hex(addr & 0xf)[2:])
        addr >>= 4
    return '.'.join(ip)


def cidr2int(prefix):
    """ Convert CIDR IPv6 prefix string to IPv6 integer and mask.
    """
    # Split prefix and return integers
    ip, mask = prefix.split('/', 1)
    net, host = struct.unpack('!QQ', socket.inet_pton(socket.AF_INET6, ip))
    return (net << 64) + host, int(mask)
