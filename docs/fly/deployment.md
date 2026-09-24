# Deploying to Fly.io

### Deploy
```sh
fly deploy
fly logs
```
Check that the bot connects and loads its cogs.

### Database
The SQLite database is stored on the `data` volume at `/data/database.db` (`DB_PATH`), so it survives deploys. The bot creates it from `database/schema.sql` on first start. Local `database/*.db` files are excluded from the image by `.dockerignore`. To upload an existing database, see [database-upload.md](database-upload.md).

### Useful commands
```sh
fly status              # machine state
fly scale count 0|1     # stop / start the bot
fly ssh console         # shell into the running machine
```
