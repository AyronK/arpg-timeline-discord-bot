# aRPG Timeline Discord Bot

[![Discord](https://img.shields.io/discord/1258784665771311126?color=7289da&logo=discord&logoColor=white)](https://discord.gg/MA4eGN9Hbu)
[![License](https://img.shields.io/github/license/AyronK/arpg-timeline-discord-bot)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A Discord bot that tracks upcoming **Action RPG (aRPG) seasons** using the [aRPG Timeline API](https://arpg-timeline.com) and adds them to your server as Discord scheduled events. Never miss a new season launch again!

## 🎮 Features

- **📅 Discord Events**: Creates a scheduled Discord event for each upcoming season, so members can mark themselves as interested and get Discord's own event reminders
- **🔄 Kept Up to Date**: Checks for season changes every 15 minutes, updates events when details change and deletes them if a season is cancelled or postponed
- **⚙️ Configurable**: Choose which games get events in your server
- **🎯 Multiple Games**: Supports Diablo, Path of Exile, Torchlight, and more
- **📊 Season Tracking**: View active seasons with start/end dates
- **🛡️ Permission Checks**: Validates bot permissions before enabling features
- **🔒 Privacy-Friendly**: No privileged intents; stores only server settings and event IDs, and deletes them when the bot leaves a server

## 🚀 Quick Start

### Use the Official Bot (Recommended)

The easiest way to get started is by inviting the official bot to your Discord server:

**[🤖 Invite Official Bot](https://discord.com/oauth2/authorize?client_id=1420355725426688010&scope=bot&permissions=17602923482112)**

*The official bot is hosted and maintained by the aRPG Timeline team.*

### Self-Hosting with Docker

If you prefer to host your own instance:

1. **Clone the repository**
   ```bash
   git clone https://github.com/AyronK/arpg-timeline-discord-bot.git
   cd arpg-timeline-discord-bot
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and aRPG Timeline API credentials
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

To run without Docker (Python 3.12):
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python bot.py
```

The official bot runs on Fly.io; see [docs/fly/deployment.md](docs/fly/deployment.md).

## 🔧 Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/arpg-enable <true/false>` | Enable/disable season events for the server (on by default) | Server Owner |
| `/arpg-toggle-game` | Interactive menu to choose which games get events (all off by default) | Server Owner |
| `/arpg-status` | Show current season event settings | Anyone |
| `/arpg-seasons` | List all currently active seasons | Anyone |
| `/arpg-check-permissions` | Check if bot has required permissions | Anyone |
| `/help` | List all slash commands | Anyone |
| `/ping` | Check bot latency | Anyone |
| `/invite` | Get the bot invite link | Anyone |
| `/support` | Get the support server link | Anyone |
| `/feedback` | Send feedback privately to the maintainers | Anyone |

Bot owners also have `/stats`, `/load`, `/unload`, `/reload`, `/shutdown`, `/say`, `/embed`, and the prefix commands `sync` / `unsync` (use them in a DM with the bot, or by @mentioning it in a channel it can see).

## 🎯 Supported Games

The bot tracks seasons for popular aRPG titles including:

- **Diablo II: Resurrected**
- **Diablo IV**
- **Path of Exile** 
- **Path of Exile 2**
- **Torchlight: Infinite**
- **Last Epoch**
- **Titan Quest 2**
- And more!

*The game list comes live from [aRPG Timeline](https://arpg-timeline.com), so new games appear automatically.*

## 📋 Required Permissions

| Permission | Why |
|---|---|
| **View Channels** | See the channels commands are used in |
| **Send Messages** | Reply in channels (owner utility commands) |
| **Embed Links** | Rich embed formatting |
| **Use Application Commands** | Slash commands |
| **Manage Events** | Update events when season details change and delete them when a season is cancelled or postponed |
| **Create Events** | Create a scheduled event for each upcoming season |

The invite links above request exactly these (`permissions=17602923482112`). Use the same value when self-hosting.

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TOKEN` | Discord bot token | ✅ |
| `ARPG_API_BASE` | aRPG Timeline API base URL (`https://www.arpg-timeline.com/api`) | ✅ |
| `ARPG_TOKEN_URL` | Token endpoint (defaults to `{ARPG_API_BASE}/token`) | ❌ |
| `ARPG_CLIENT_ID` | aRPG Timeline API client ID | ✅ |
| `ARPG_CLIENT_SECRET` | aRPG Timeline API client secret | ✅ |
| `PREFIX` | Prefix for the owner `sync` / `unsync` commands | ❌ |
| `INVITE_LINK` | Link shown by `/invite` | ❌ |
| `FEEDBACK_USER_IDS` | Comma-separated user IDs that receive `/feedback` DMs (defaults to the app/team owner). Each must share a server with the bot and allow DMs | ❌ |
| `TOPGG_TOKEN` | top.gg API token; if set, the server count is posted to top.gg every 30 minutes | ❌ |
| `DB_PATH` | SQLite database path (defaults to `database/database.db`) | ❌ |

### Server Setup

1. **Invite the bot** with the permissions above
2. **Run** `/arpg-check-permissions` to verify setup
3. **Choose games** using `/arpg-toggle-game` (all games start disabled)
4. Season events are on by default; use `/arpg-enable false` to pause them

## 🐳 Docker Deployment

The bot includes a complete Docker setup for easy deployment:

```yaml
# docker-compose.yml
services:
  discord-bot:
    build: .
    env_file:
      - .env
    volumes:
      - ./database:/bot/database
      - ./logs:/bot/logs
    restart: always
```

## 📊 Database

Uses SQLite for data persistence:
- **Guild settings** - Server-specific configuration
- **Game toggles** - Per-server game enable/disable state
- **Season cache** - Which seasons already have an event, and that event's ID (prevents duplicates)
- **API tokens / API cache** - Cached aRPG Timeline API token and responses

Server data is deleted when the bot leaves a server, including servers it left while offline. Logs rotate at 1 MB with 3 backups.

## 🔗 Related Links

- **[aRPG Timeline Website](https://arpg-timeline.com)** - Source of season data
- **[Bot Page](https://www.arpg-timeline.com/discord-bot)** - About the bot
- **[Terms of Service](https://www.arpg-timeline.com/terms)** - Terms for using the bot (section 9)
- **[Privacy Policy](https://www.arpg-timeline.com/privacy#discord-bot)** - What data the bot stores and for how long
- **[Official Bot Invite](https://discord.com/oauth2/authorize?client_id=1420355725426688010&scope=bot&permissions=17602923482112)** - Add to your server
- **[Support Server](https://discord.gg/MA4eGN9Hbu)** - Get help and support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper
- [aRPG Timeline](https://arpg-timeline.com) - Season data provider
- All the aRPG communities for feedback and support

---

**Made with ❤️ for the aRPG community**

*Keep track of all your favorite aRPG seasons in one place!*