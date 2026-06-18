# Cog for logging voice channel activity

import os
from datetime import datetime

from discord.ext import commands


class VoiceCallLogger(commands.Cog):
    """Logs when a voice call starts and when users leave voice channels."""

    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(os.getenv("VOICE_LOG_CHANNEL_ID"))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Ignore mute/deafen/stream changes while staying in the same voice channel
        if before.channel == after.channel:
            return

        log_channel = self.bot.get_channel(self.log_channel_id)

        if log_channel is None:
            print("Could not find the log text channel.")
            return

        current_time = datetime.now().strftime("%H:%M")

        # User joined a voice channel from not being in voice
        if before.channel is None and after.channel is not None:
            voice_channel = after.channel

            # Only log "call start" when the channel went from empty to 1 person
            if len(voice_channel.members) == 1:
                await log_channel.send(
                    f"Call started in **{voice_channel.name}** by {member.display_name} at {current_time}"
                )

                print(
                    f"[CALL START] {member.display_name} started "
                    f"{voice_channel.name} at {current_time}"
                )

            return

        # User left voice completely
        if before.channel is not None and after.channel is None:
            await log_channel.send(
                f"{member.display_name} left **{before.channel.name}** at {current_time}"
            )

            print(
                f"[VOICE LEAVE] {member.display_name} left "
                f"{before.channel.name} at {current_time}"
            )

            return

        # User moved between voice channels
        if before.channel is not None and after.channel is not None:
            old_channel = before.channel
            new_channel = after.channel

            # Log that they left the old channel
            await log_channel.send(
                f"{member.display_name} left **{old_channel.name}** and moved to **{new_channel.name}** at {current_time}"
            )

            print(
                f"[VOICE MOVE] {member.display_name} moved from "
                f"{old_channel.name} to {new_channel.name} at {current_time}"
            )

            # If the new channel now has 1 member, that means this move started a new call there
            if len(new_channel.members) == 1:
                await log_channel.send(
                    f"Call started in **{new_channel.name}** by {member.display_name} at {current_time}"
                )

                print(
                    f"[CALL START] {member.display_name} started "
                    f"{new_channel.name} at {current_time}"
                )


async def setup(bot):
    await bot.add_cog(VoiceCallLogger(bot))