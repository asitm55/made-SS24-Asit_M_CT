#!/bin/bash
# Print setup message
echo "Setting up the test environment..."
# Clean up environment
echo "Cleaning up test environment..."
rm -f ../data/database.sqlite
# Print test running message
echo "Running pipeline..."
# Run pytest for your test script
bash pipeline.sh
if [ $? -ne 0 ]; then
    echo "Pipeline Failed"
    exit 1
fi
# Print completion message
echo "Running Test."
python3 automated_test.py
if [ $? -ne 0 ]; then
    echo "Test Failed"
    exit 1
fi
echo "Test environment cleaned up."
#bash
