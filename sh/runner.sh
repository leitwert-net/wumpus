#!/bin/bash
#
# TRACE_THE_WUMPUS
# Copyright (C) 2014-2025 Leitwert GmbH
# 
# This software is distributed under the terms of the MIT license.
# It can be found in the LICENSE file or at https://opensource.org/licenses/MIT.
# 
# Author Alexander MAENNEL <alexander.maennel@tu-dresden.de>
# Author Johann SCHLAMP <schlamp@leitwert.net>

# Define the Python script to monitor
PYTHON_SCRIPT="trace.py"
PYTHON_DIR="/srv/wumpus/src"

# Function to start the Python script
start_script() {
    python3 -u $PYTHON_DIR/$PYTHON_SCRIPT &
    SCRIPT_PID=$!
}

# Start the script initially
echo "Starting $PYTHON_SCRIPT."
start_script

# Restart the script in case of changes
while true ; do

    # Monitor the script file using inotifywait
    inotifywait -qq -e create -e delete -e modify --exclude "[^p].$|[^y]$" -r $PYTHON_DIR
    echo "Source directory has been modified, restarting $PYTHON_SCRIPT."

    # Kill current script process
    kill $SCRIPT_PID 2>/dev/null   

    # Wait for the script process to terminate
    wait $SCRIPT_PID

    # Start the script again
    start_script
done
