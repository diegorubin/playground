"""
Lifeguard Settings
"""
import lifeguard_tinydb
import lifeguard_simple_dashboard

PLUGINS = [lifeguard_tinydb, lifeguard_simple_dashboard]


def setup(_lifeguard_context):
    print("in custom setup")
