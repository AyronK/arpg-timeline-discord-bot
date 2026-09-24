# aRPG Timeline Discord Bot

[![Discord](https://img.shields.io/discord/1258784665771311126?color=7289da&logo=discord&logoColor=white)](https://discord.gg/MA4eGN9Hbu)
[![License](https://img.shields.io/github/license/svn-josh/aRPG-Timeline-Discord-Bot)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A Discord bot that tracks upcoming **Action RPG (aRPG) seasons** using the [aRPG Timeline API](https://arpg-timeline.com) and adds them to your server as Discord scheduled events. Never miss a new season launch again!

## 🎮 Features

- **📅 Discord Events**: Creates a scheduled Discord event for each upcoming season, so members can mark themselves as interested and get Discord's own event reminders
- **🔄 Kept Up to Date**: Updates events when season details change and deletes them if a season is cancelled or postponed
- **⚙️ Configurable**: Choose which games get events in your server
- **🎯 Multiple Games**: Supports Diablo, Path of Exile, Torchlight, and more
- **📊 Season Tracking**: View active seasons with start/end dates
- **🛡️ Permission Checks**: Validates bot permissions before enabling features

## 🚀 Quick Start

### Use the Official Bot (Recommended)

The easiest way to get started is by inviting the official bot to your Discord server:

**[🤖 Invite Official Bot](https://discord.com/oauth2/authorize?client_id=1420355725426688010&scope=bot&permissions=17602923482112)**

*The official bot is hosted and maintained by the aRPG Timeline team.*

### Self-Hosting with Docker

If you prefer to host your own instance:

1. **Clone the repository**
   ```bash
   git clone https://github.com/svn-josh/aRPG-Timeline-Discord-Bot.git
   cd aRPG-Timeline-Discord-Bot
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and API credentials
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

## 🔧 Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/arpg-enable <true/false>` | Enable/disable all season notifications | Server Owner |
| `/arpg-toggle-game` | Interactive menu to enable/disable specific games | Server Owner |
| `/arpg-status` | Show current notification settings | Anyone |
| `/arpg-seasons` | List all currently active seasons | Anyone |
| `/arpg-check-permissions` | Check if bot has required permissions | Anyone |

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

*Game support depends on data availability from [aRPG Timeline](https://arpg-timeline.com)*

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
| `PREFIX` | Command prefix (for legacy commands) | ❌ |
| `INVITE_LINK` | Bot invite link | ❌ |
| `FEEDBACK_USER_IDS` | Comma-separated user IDs that receive `/feedback` DMs (defaults to the app/team owner). Each must share a server with the bot and allow DMs | ❌ |
| `ARPG_API_BASE` | aRPG Timeline API base URL | ❌ |
| `ARPG_CLIENT_ID` | API client ID | ❌ |
| `ARPG_CLIENT_SECRET` | API client secret | ❌ |
| `TOPGG_TOKEN` | top.gg API token; if set, the server count is posted to top.gg every 30 minutes | ❌ |

### Server Setup

1. **Invite the bot** with the permissions above
2. **Run** `/arpg-check-permissions` to verify setup
3. **Enable notifications** with `/arpg-enable true`
4. **Configure games** using `/arpg-toggle-game`

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
- **API tokens** - Cached authentication tokens

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