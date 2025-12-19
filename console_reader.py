"""
Screeps Console Log Fetcher
Fetches console logs from a Screeps private server for autonomous agent analysis
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class ScreepsConsoleReader:
    def __init__(self, server_url: str, username: str, password: str):
        """
        Initialize the Screeps console reader.
        
        Args:
            server_url: Base URL of the Screeps server (e.g., 'http://192.168.1.160:21025')
            username: Your Screeps username
            password: Your Screeps password
        """
        self.server_url = server_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """
        Authenticate with the Screeps server.
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            response = self.session.post(
                f"{self.server_url}/api/auth/signin",
                json={
                    "email": self.username,
                    "password": self.password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                # Set token in session headers
                self.session.headers.update({
                    'X-Token': self.token,
                    'X-Username': self.token
                })
                print(f"✓ Authenticated as {self.username}")
                return True
            else:
                print(f"✗ Authentication failed: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return False
    
    def get_console_logs(self) -> Optional[List[str]]:
        """
        Fetch console logs from the server.
        
        Returns:
            List of console log messages, or None if request fails
        """
        try:
            response = self.session.get(
                f"{self.server_url}/api/user/console"
            )
            
            if response.status_code == 200:
                data = response.json()
                # Console logs are in data['log'] as a list of strings
                logs = data.get('log', [])
                return logs
            else:
                print(f"✗ Failed to fetch console: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Error fetching console: {e}")
            return None
    
    def get_memory(self) -> Optional[Dict]:
        """
        Fetch game memory from the server.
        
        Returns:
            Memory object as dict, or None if request fails
        """
        try:
            response = self.session.get(
                f"{self.server_url}/api/user/memory"
            )
            
            if response.status_code == 200:
                data = response.json()
                # Memory is stored as a JSON string in data['data']
                memory_str = data.get('data', '{}')
                return json.loads(memory_str)
            else:
                print(f"✗ Failed to fetch memory: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Error fetching memory: {e}")
            return None
    
    def parse_console_logs(self, logs: List[str]) -> Dict:
        """
        Parse console logs into structured format for agent analysis.
        
        Args:
            logs: Raw console log strings
            
        Returns:
            Structured log data with errors, warnings, and info messages
        """
        parsed = {
            'errors': [],
            'warnings': [],
            'info': [],
            'raw': logs
        }
        
        for log in logs:
            log_lower = log.lower()
            
            # Categorize by content
            if 'error' in log_lower or 'exception' in log_lower or 'fail' in log_lower:
                parsed['errors'].append(log)
            elif 'warn' in log_lower or 'warning' in log_lower:
                parsed['warnings'].append(log)
            else:
                parsed['info'].append(log)
        
        return parsed


def main():
    """Example usage"""
    # Configuration
    SERVER_URL = "http://192.168.1.160:21025"
    USERNAME = "your_username"  # Replace with your Screeps username
    PASSWORD = "your_password"  # Replace with your Screeps password
    
    # Initialize reader
    reader = ScreepsConsoleReader(SERVER_URL, USERNAME, PASSWORD)
    
    # Authenticate
    if not reader.authenticate():
        print("Failed to authenticate. Exiting.")
        return
    
    # Fetch console logs
    print("\nFetching console logs...")
    logs = reader.get_console_logs()
    
    if logs is not None:
        print(f"\n=== Console Logs ({len(logs)} entries) ===")
        for log in logs:
            print(log)
        
        # Parse logs for structured analysis
        parsed = reader.parse_console_logs(logs)
        print(f"\n=== Parsed Analysis ===")
        print(f"Errors: {len(parsed['errors'])}")
        print(f"Warnings: {len(parsed['warnings'])}")
        print(f"Info: {len(parsed['info'])}")
        
        if parsed['errors']:
            print("\n=== Errors ===")
            for error in parsed['errors']:
                print(f"  • {error}")
    
    # Optionally fetch memory
    print("\nFetching memory...")
    memory = reader.get_memory()
    if memory:
        print(f"Memory keys: {list(memory.keys())}")


if __name__ == "__main__":
    main()
