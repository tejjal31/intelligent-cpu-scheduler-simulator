# Main entry point for Intelligent CPU Scheduler Simulator
# Run this file to launch the application

import sys
import os

# Add project root to path so all modules load correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import *