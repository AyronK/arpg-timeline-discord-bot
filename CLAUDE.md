# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**aRPG Timeline Discord Bot** is a Discord bot that automatically tracks and notifies communities about upcoming Action RPG (aRPG) seasons using the aRPG Timeline API. It creates Discord scheduled events for upcoming seasons and manages server-specific game notification settings.

## Development Workflow

### Environment Setup

1. **Install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with:
   # - TOKEN: Discord bot token
   # - ARPG_API_BASE: aRPG Timeline API base URL (default: https://www.arpg-timeline.com/api)
   # - ARPG_TOKEN_URL: Token endpoint (default: https://www.arpg-timeline.com/api/v1/token)
   # - ARPG_CLIENT_ID & ARPG_CLIENT_SECRET: API credentials
   # - PREFIX: Optional command prefix
   # - INVITE_LINK: Optional bot invite link
   ```

### Running Locally

```bash
source .venv/bin/activate
python bot.py
```

The bot will:
- Initialize SQLite database from `database/schema.sql`
- Load all cogs from the `cogs/` directory
- Start a status task that rotates presence every minute
- Begin polling for active seasons every 5 minutes

### Docker Deployment

```bash
docker-compose up -d
```

This maps the database and logs to persistent volumes for data persistence.

### Slash Command Synchronization

After modifying commands, sync with Discord using the owner-only `/sync` command:
- `sync global` - Push changes application-wide (takes up to 1 hour to propagate)
- `sync guild` - Sync immediately to the current guild only

## Architecture

### Core Components

#### **bot.py** (Main Entry Point)
- **DiscordBot class**: Extends `commands.Bot` with:
  - Custom logging with color output to console and file (`logs/discord.log`)
  - Database initialization in `setup_hook()`
  - Status rotation task that updates presence every minute
  - Comprehensive error handling for both prefix and slash commands
  - Uptime tracking (UTC-aware)
  
- **Lifecycle**:
  1. Load environment variables
  2. Initialize intents (guilds, scheduled_events, message_content)
  3. On ready: Initialize database, load cogs, start status task
  4. Poll for new seasons every 5 minutes (via ARPGTimeline cog)
  5. Process seasons and create Discord events per guild settings

#### **database/__init__.py** (DatabaseManager)
Async SQLite wrapper providing guild configuration, season tracking, and API token caching:
- **Guild Settings**: Per-server master enable/disable flag
- **Guild Games**: Per-server per-game enable/disable toggles (default: OFF)
- **Season Cache**: Prevents duplicate notifications per guild/game/season
- **API Tokens**: Persistent storage for aRPG API tokens with expiry
- **API Cache**: Generic cache for games list and active seasons (TTL-based)

#### **services/arpg_api.py** (ARPGApiClient)
Manages all aRPG Timeline API communication:
- **Token Management**: Auto-refresh with fallback to cached tokens and exponential backoff on failures
- **Games Fetch**: `GET /games` with caching (30-min TTL)
- **Seasons Fetch**: `GET /games/seasons?scope=active` returning both current and upcoming seasons (5-min TTL)
- **Data Models**:
  - `Game`: slug, name, season_keyword, categories
  - `Season`: game_slug, game_name, season_key, title, starts_at, ends_at, url, patch_notes_url

Key patterns:
- Season keys are constructed identically for "current" and "next" blocks to prevent duplicates when a season transitions
- Token expires at least 60 seconds in the future before being considered valid
- Errors include detailed logging for debugging API issues

### Cogs (Command Modules)

#### **cogs/arpg_timeline.py** (Main Features)
Handles season polling, notifications, and user commands:

**Background Task:**
- `poll_seasons_task` (5-minute loop): Fetches active seasons and processes per guild
- For each guild with notifications enabled:
  - Check per-game toggles (default: OFF unless explicitly enabled)
  - Skip already-seen seasons
  - For upcoming seasons: Create a Discord scheduled event
  - For past seasons (>1 day old): Mark as seen silently (bootstrap)

**Commands (guild owner only):**
- `/arpg-enable <true/false>`: Master enable/disable for the server
- `/arpg-toggle-game`: Interactive dropdown to enable/disable specific games with pagination
- `/arpg-status`: Show current notification settings
- `/arpg-seasons`: List all currently active seasons
- `/arpg-check-permissions`: Verify bot has Manage Events + Create Events permissions

**Event Creation:**
- Creates external scheduled events with:
  - Name: `{GameName}: {SeasonTitle}`
  - Start: Season start time, End: Start time + 2 hours
  - Privacy: Guild-only
  - Location: "aRPG Timeline"
  - Description: Season URL or generic fallback

#### **cogs/general.py**
Community utilities:
- `/help`: Lists all slash commands grouped by cog with emoji labels
- Context menu: "Grab ID" to copy user IDs
- Context menu: "Remove spoilers" to strip `||` spoiler markers
- Feedback modal (unused but available)

#### **cogs/owner.py**
Admin-only utilities:
- `sync <global|guild>`: Synchronize slash commands with Discord
- `/stats`: Comprehensive dashboard showing:
  - Guild count, member count, user count
  - Uptime, command count, loaded cogs
  - CPU/memory usage (if psutil available)
  - Database row counts for all tables
  - Python and discord.py versions

### Database Schema

**guild_settings**: Master notifications toggle per guild
**guild_games**: Per-game toggle per guild (allows servers to pick which games to track)
**season_cache**: Deduplication cache (guild_id + game_slug + season_key)
**api_tokens**: Persistent token storage with ISO 8601 expiry times
**api_cache**: Generic cache for API responses (key, JSON value, expiry)

All tables use CURRENT_TIMESTAMP for audit fields.

## Key Design Decisions

1. **Event-Only Notifications**: Bot creates Discord scheduled events instead of sending messages. This allows Discord to handle reminders and provides a native UI.

2. **Season Key Deduplication**: When a "next" season transitions to "current", the key remains the same to prevent duplicate notifications.

3. **Per-Game Toggles Default OFF**: Servers must explicitly enable games they want to track. This prevents notification spam.

4. **Async-First**: All I/O operations (database, HTTP) are async to avoid blocking the event loop.

5. **Token Caching**: API tokens are persisted in the database so the bot can recover from restarts without re-authenticating.

6. **Permission Preflight Checks**: Before creating events, bot verifies it has both Manage Events and Create Events permissions to avoid silent failures.

## Common Development Tasks

### Adding a New Command
1. Create a method in a cog decorated with `@app_commands.command()`
2. Add permission checks (`_ensure_guild_owner()`, `await self.bot.is_owner()`)
3. Use embeds for responses with appropriate colors (0xBEBEFE for success, 0xE02B2B for errors)
4. Log actions via `self.bot.logger.info/warning/error()`
5. Sync commands: `sync guild` in dev, `sync global` before deploying

### Debugging API Issues
- Check `logs/discord.log` for detailed error messages from ARPGApiClient
- Verify `.env` has correct `ARPG_*` variables
- Test with `/arpg-seasons` to confirm API access
- Token failures trigger 10-minute backoff; wait or restart bot to reset

### Database Queries
- Use `DatabaseManager` methods for consistency
- All methods are async; await them
- Guild IDs are stored as strings (e.g., `str(guild.id)`)
- Season cache uses composite primary key (guild_id, game_slug, season_key)

### Testing Scheduled Events
- Use `/arpg-toggle-game` to enable a game in test guild
- Monitor logs for poll cycle: "action=create_event"
- Check guild's Events page to see created events
- Verify bot has Manage Events permission in guild role settings

## Dependencies

- **discord.py 2.6.3**: Discord API wrapper
- **aiohttp**: Async HTTP client for aRPG API
- **aiosqlite**: Async SQLite driver
- **python-dotenv**: Environment variable loading
- **psutil**: Optional, for resource monitoring in `/stats` command

