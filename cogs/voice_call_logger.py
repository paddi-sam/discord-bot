# Cog for sending a message when a voice call starts

import os
from datetime import datetime

from discord.ext import commands


class VoiceCallLogger(commands.Cog):
    """Sends a message when a voice call starts in a server."""

    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(os.getenv("VOICE_LOG_CHANNEL_ID"))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Ignore leaving voice completely
        if after.channel is None:
            return

        # Ignore mute/deafen/stream changes while staying in the same voice channel
        if before.channel == after.channel:
            return

        voice_channel = after.channel

        # Only log when the voice channel has gone from empty to 1 person
        if len(voice_channel.members) != 1:
            return

        log_channel = self.bot.get_channel(self.log_channel_id)

        if log_channel is None:
            print("Could not find the log text channel.")
            return

        current_time = datetime.now().strftime("%H:%M")

        await log_channel.send(
            f"{member.display_name} joined {voice_channel.name} at {current_time}"
        )

        print(
            f"[CALL START] {member.display_name} joined "
            f"{voice_channel.name} at {current_time}"
        )


async def setup(bot):
    await bot.add_cog(VoiceCallLogger(bot))