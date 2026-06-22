"""DLR Auto-Healer entry point — delegates to dlr_autohealer.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
exec(open(os.path.join(os.path.dirname(__file__), "dlr_autohealer.py")).read())
