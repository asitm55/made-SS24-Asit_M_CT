%%bash

# Print setup message
echo "Setting up the test environment..."

# Install pytest
pip install pytest

# Print test running message
echo "Running tests..."

# Run pytest for your test script
pytest test_pipeline.py

# Print completion message
echo "Tests completed."

# Clean up environment
echo "Cleaning up test environment..."
rm -f your_database.db

echo "Test environment cleaned up."
