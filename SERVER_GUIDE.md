# Screeps Server Guide

## Server Connection Details

- **IP Address (Local):** `localhost` or `127.0.0.1`
- **IP Address (Network):** `192.168.1.160`
- **Game Port:** `21025`
- **CLI Port:** `21026`

### Connecting from Steam Client

1. Launch Screeps
2. Click "Change server"
3. Enter:
   - Host: `192.168.1.160` (or `localhost` from host machine)
   - Port: `21025`
   - Password: (leave blank)

## Docker Commands

### Start Server
```bash
docker-compose up -d
```

### Stop Server
```bash
docker-compose down
```

### Restart Server
```bash
docker-compose restart
```

### View Server Logs
```bash
docker-compose logs -f
```

### Stop Logs (Ctrl+C)
Press `Ctrl+C` to exit log view

## Server CLI Access

### Connect to CLI
```bash
docker exec -it screeps-server screeps cli
```

### Exit CLI
Type `exit` or press `Ctrl+C`

### Common CLI Commands
Once connected to the CLI, you can run:

- `help` - Show available commands
- `system.resetAllData()` - Reset all server data
- `storage.db.users.find()` - List all users
- `storage.db.rooms.find()` - List all rooms

## Accessing Console Logs

### Web Interface (Recommended)
Open in your browser:
- **Local:** `http://localhost:21025`
- **Network:** `http://192.168.1.160:21025`

Log in with your account and view the console panel for all `console.log()` output from your scripts.

### Via CLI
```bash
docker exec -it screeps-server screeps cli
```
Then run:
```javascript
storage.db['users.console'].find({user: 'YOUR_USER_ID'})
```

### In Steam Client
When connected to the server via Steam client, the console panel will display your script output in real-time.

## Configuration

The server configuration is stored in `.screepsrc` file with:
- Steam Web API Key
- Port settings
- Server password (currently blank)

Any changes to `.screepsrc` require a server restart:
```bash
docker-compose restart
```

## Troubleshooting

### Server won't start
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f
```

### Check if server is running
```bash
docker ps -f name=screeps-server
```

### Remove and recreate server
```bash
docker-compose down
docker-compose up -d
```
