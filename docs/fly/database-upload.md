# Uploading a database to Fly.io

The bot's SQLite database lives on the `data` volume at `/data/database.db`. To replace it with a local file:

### 1. Stop the bot
```sh
fly scale count 0
```
This destroys the machine, but the volume and its contents persist.

### 2. Upload via a temporary machine
`fly ssh sftp` hangs on WSL2 (the WireGuard tunnel stalls on large transfers), so send the file with the machine config instead. `--file-local` goes over the HTTPS API. On start, the machine backs up any existing database to `database.db.bak-<timestamp>`, copies the new file onto the volume, then idles:
```sh
fly machine run alpine --region iad --volume data:/data \
  --name db-upload --restart no \
  --file-local /tmp/database.db=./database/database.db \
  --entrypoint "sh -c '[ -f /data/database.db ] && mv /data/database.db /data/database.db.bak-$(date +%Y%m%d-%H%M%S); cp /tmp/database.db /data/database.db && tail -f /dev/null'"
```
The file is staged in `/tmp` because the volume is mounted over `/data` after config files are written.

### 3. Verify (hashes must match)
```sh
sha256sum ./database/database.db
fly ssh console --machine <id> -C "sha256sum /data/database.db"
```

### 4. Clean up and restart the bot
```sh
fly machine destroy <id> --force
fly scale count 1
fly logs
```
