#!/usr/bin/env python3
"""
Log pattern discovery module for automatically identifying log formats.
"""
import re
from collections import defaultdict, Counter
import json
import logging
from datetime import datetime
import ipaddress
from functools import partial

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('pattern_discovery')

class LogPatternDiscovery:
    """
    A class for automatically discovering patterns in log files.
    """
    def __init__(self, sample_size=10000, min_confidence=0.7):
        """
        Initialize the pattern discovery engine.
        
        Args:
            sample_size: Number of log lines to sample for pattern discovery
            min_confidence: Minimum confidence level for pattern detection (0.0-1.0)
        """
        self.sample_size = sample_size
        

    @staticmethod
    def text_mapper(line):
        LOG_PATTERN = r'(\S+) \S+ \S+ \[(.*?)\] "(.*?)" (\d+) (\S+) "(.*?)" "(.*?)"'

        match = re.match(LOG_PATTERN, line)
        if not match:
            return None
        
        ip, timestamp_str, request, status, size, referrer, user_agent = match.groups()
        
        # Parse the request to get method and path
        request_parts = request.split()
        method = path = http_version = ""
        if len(request_parts) >= 2:
            method = request_parts[0]
            path = request_parts[1]
            if len(request_parts) >= 3:
                http_version = request_parts[2]
        
        # Parse timestamp
        try:
            timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
            date = timestamp.strftime("%Y-%m-%d")
            hour = timestamp.strftime("%H")
        except ValueError:
            date = "unknown"
            hour = "unknown"
        
        # Convert size to int or 0 if '-'
        if size == '-':
            size = 0
        else:
            try:
                size = int(size)
            except ValueError:
                size = 0
        
        # Extract endpoint (remove query parameters)
        endpoint = path.split('?')[0]
        
        # Extract browser and device information from user-agent
        browser = "unknown"
        device = "unknown"
        
        if "Mozilla" in user_agent:
            if "iPhone" in user_agent or "iPad" in user_agent:
                device = "iOS"
            elif "Android" in user_agent:
                device = "Android"
            elif "Windows" in user_agent:
                device = "Windows"
            elif "Mac" in user_agent:
                device = "Mac"
            elif "Linux" in user_agent:
                device = "Linux"
            
            if "Chrome" in user_agent:
                browser = "Chrome"
            elif "Firefox" in user_agent:
                browser = "Firefox"
            elif "Safari" in user_agent and "Chrome" not in user_agent:
                browser = "Safari"
            elif "Edge" in user_agent:
                browser = "Edge"
            elif "MSIE" in user_agent or "Trident" in user_agent:
                browser = "Internet Explorer"
        
        return {
            "ip": ip,
            "date": date,
            "hour": hour,
            "method": method,
            "endpoint": endpoint,
            "status": int(status),
            "size": size,
            "referrer": referrer,
            "browser": browser,
            "device": device
        }

    def get_mapper_function(self):
        """
        Generate a mapper function based on detected patterns.
        
        Returns:
            A function that can be used as a mapper in the MapReduce framework
        """
        return self.text_mapper
        
    
    @staticmethod
    def merge_reducer(dict1, dict2):
        """
        Merge two dictionaries by summing their values.
        
        Args:
            dict1: First dictionary
            dict2: Second dictionary
        
        Returns:
            Merged dictionary
        """
         # Create a deep copy to avoid modifying the original dict
        merged = dict1.copy() if isinstance(dict1, dict) else dict1
        
        # Handle the case when dict1 might not be a dictionary
        if not isinstance(dict1, dict):
            print(f"Warning: dict1 is not a dictionary: {dict1}")
            return dict2
            
        # Handle the case when dict2 might not be a dictionary
        if not isinstance(dict2, dict):
            print(f"Warning: dict2 is not a dictionary: {dict2}")
            return merged
            
        for key, value in dict2.items():
            if key in merged:
                for k1, v1 in value.items():
                    if k1 in merged[key]:
                        merged[key][k1] += v1
                    else:
                        merged[key][k1] = v1
            else:
                merged[key] = value
        
        return merged
    
    def get_reducer_function(self):
        """
        Generate a reducer function based on detected patterns.
        
        Returns:
            A function that can be used as a reducer in the MapReduce framework
        """
        return self.merge_reducer

