# Accessing the Fly.io volume

The `data` volume (1 GB, `iad`) is mounted at `/data`. It can be attached to only one machine at a time, and `fly ssh` only works while a machine is running.

### While the bot is running
```sh
fly ssh console                          # interactive shell
fly ssh console -C "ls -lh /data/"       # one-off command
fly ssh console -C "cat /data/<file>"    # read a small file
```

### While the bot is stopped
Start a temporary machine that mounts the volume and idles:
```sh
fly scale count 0
fly machine run alpine --region iad --volume data:/data \
  --name volume-access --restart no --entrypoint "tail -f /dev/null"
fly ssh console --machine <id>
```
When you're done, destroy it to free the volume:
```sh
fly machine destroy <id> --force
fly scale count 1
```

### Transferring files
On WSL2, large transfers over `fly ssh` (`sftp`, piping through `console`) can stall because the WireGuard tunnel stops mid-transfer. Short commands still work. Enabling `fly wireguard websockets` may help.

- **Upload:** pass `--file-local /tmp/<file>=./<local-file>` to `fly machine run`, then copy it into `/data` from the entrypoint or a shell. The file travels over the HTTPS API, not the tunnel. See [database-upload.md](database-upload.md) for a full example.
- **Download:** `fly ssh sftp get /data/<file> ./<file>`. Check the result with `sha256sum` on both sides.

### Snapshots
Fly takes daily volume snapshots automatically. You can also take one yourself before risky changes:
```sh
fly volumes list                         # get the volume ID
fly volumes snapshots create <volume-id>
fly volumes snapshots list <volume-id>
```
