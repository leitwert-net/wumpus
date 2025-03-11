# TRACE_THE_WUMPUS
# Copyright (C) 2014-2025 Leitwert GmbH
#
# This software is distributed under the terms of the MIT license.
# It can be found in the LICENSE file or at https://opensource.org/licenses/MIT.
#
# Author Johann SCHLAMP <schlamp@leitwert.net>

# syntax=docker/dockerfile:1
FROM python:slim AS wumpus

# Copy runner script
COPY sh/runner.sh /srv/wumpus/sh/

# Setup container
RUN \
  # Install tools
  apt-get -y update && \
  apt-get -y install tcpdump inotify-tools && \
  # Install python modules
  pip install scapy && \
  # Cleanup
  pip cache purge && \
  apt-get clean
