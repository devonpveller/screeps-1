# Screeps Console Reader

Python script to fetch console logs from your Screeps private server remotely.

## Installation

```bash
pip install requests
```

## Usage

### Basic Usage

Edit `console_reader.py` and set your credentials:
```python
SERVER_URL = "http://192.168.1.160:21025"
USERNAME = "your_username"
PASSWORD = "your_password"
```

Then run:
```bash
python console_reader.py
```

### Integration with Your Agent

```python
from console_reader import ScreepsConsoleReader

# Initialize
reader = ScreepsConsoleReader(
    "http://192.168.1.160:21025",
    "your_username",
    "your_password"
)

# Authenticate
reader.authenticate()

# Get logs
logs = reader.get_console_logs()

# Parse for errors
parsed = reader.parse_console_logs(logs)
errors = parsed['errors']  # List of error messages

# Use errors to inform your AI agent's next iteration
```

## API Methods

- `authenticate()` - Login to the server
- `get_console_logs()` - Fetch console output
- `get_memory()` - Fetch game memory state
- `parse_console_logs(logs)` - Structure logs into errors/warnings/info

## Output Format

Parsed logs return:
```python
{
    'errors': [...],      # Error messages
    'warnings': [...],    # Warning messages
    'info': [...],        # Info messages
    'raw': [...]          # All raw log lines
}
```

## Continuous Monitoring

For continuous polling, wrap in a loop:
```python
import time

while True:
    logs = reader.get_console_logs()
    parsed = reader.parse_console_logs(logs)
    
    if parsed['errors']:
        # Trigger your agent to analyze and fix
        pass
    
    time.sleep(60)  # Poll every 60 seconds
```
