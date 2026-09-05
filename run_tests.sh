#!/bin/bash

# Run tests

echo "Running JARVIS-Android Tests"
echo "=============================="

python3 -m pytest tests/ -v --tb=short

if [ $? -eq 0 ]; then
    echo ""
    echo "All tests passed! ✓"
else
    echo ""
    echo "Some tests failed. Please check the output above."
fi
