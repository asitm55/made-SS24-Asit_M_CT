#!/bin/bash

export PYTHONPATH=$(pwd)/..

echo "Running unit tests..."
pytest ../tests/testpipeline.py
python test_datasets.py

