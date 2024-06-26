#!/bin/bash
# Print setup message
echo "Setting up the test environment..."
# Clean up environment

# Print completion message
echo "Running Test."
python3 automated_test.py
if [ $? -ne 0 ]; then
    echo "Test Failed"
    exit 1
fi
echo "Test environment cleaned up."
#bash
