"""
Lifeguard Settings
"""
import lifeguard_mongodb
import lifeguard_simple_dashboard

PLUGINS = [lifeguard_mongodb, lifeguard_simple_dashboard]


def setup(_lifeguard_context):
    print("in custom setup")
