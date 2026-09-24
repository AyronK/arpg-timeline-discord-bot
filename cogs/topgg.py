import os
from typing import Optional

import aiohttp
from discord.ext import commands, tasks

TOPGG_STATS_URL = "https://top.gg/api/bots/{bot_id}/stats"


class TopGG(commands.Cog, name="topgg"):
    """Posts the bot's server count to top.gg. Disabled unless TOPGG_TOKEN is set."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.token = os.getenv("TOPGG_TOKEN")
        self.session: Optional[aiohttp.ClientSession] = None
        if self.token:
            self.post_stats_task.start()

    async def cog_unload(self) -> None:
        self.post_stats_task.cancel()
        if self.session and not self.session.closed:
            await self.session.close()

    # top.gg allows 60 requests/minute; every 30 minutes is well within limits
    @tasks.loop(minutes=30.0)
    async def post_stats_task(self) -> None:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))

        server_count = len(self.bot.guilds)
        try:
            async with self.session.post(
                TOPGG_STATS_URL.format(bot_id=self.bot.user.id),
                json={"server_count": server_count},
                headers={"Authorization": self.token},
            ) as resp:
                if resp.status == 429:
                    self.bot.logger.warning(
                        f"top.gg rate limited stats post; retry-after={resp.headers.get('Retry-After')}"
                    )
                elif resp.status >= 400:
                    self.bot.logger.warning(f"top.gg stats post failed: status={resp.status}")
                else:
                    self.bot.logger.info(f"Posted server count to top.gg: {server_count}")
        except Exception as e:
            self.bot.logger.warning(f"top.gg stats post failed: {type(e).__name__}")

    @post_stats_task.before_loop
    async def before_post_stats_task(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TopGG(bot))
