import argparse
import asyncio
import os
import sys
import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DiscordMessageExporter(discord.Client):
    def __init__(self, channel_id: int, target_user_id: int, output_file: str, delay: float = 1.5):
        super().__init__()
        self.channel_id = channel_id
        self.target_user_id = target_user_id
        self.output_file = output_file
        self.delay = delay

    async def on_ready(self):
        print(f"[+] Authenticated as: {self.user}")
        
        channel = self.get_channel(self.channel_id)
        if not channel:
            print(f"[!] Error: Could not find channel with ID {self.channel_id}.")
            await self.close()
            return

        target_user = discord.Object(id=self.target_user_id)
        print(f"[+] Scraping #{channel.name} ({self.channel_id}) for messages by User ID {self.target_user_id}...")

        matched_count = 0

        try:
            with open(self.output_file, "w", encoding="utf-8") as file:
                file.write(f"--- Search Results for User ID {self.target_user_id} in #{channel.name} ---\n\n")

                async for msg in channel.search(authors=[target_user], limit=None):
                    timestamp = msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    file.write(f"[{timestamp}] {msg.author.name}: {msg.content}\n")
                    matched_count += 1

                    # Rate-limit safety pause after every 25 messages (1 API page)
                    if matched_count % 25 == 0:
                        print(f"    -> Extracted {matched_count} messages... (throttling {self.delay}s)")
                        await asyncio.sleep(self.delay)

            print(f"[✓] Success! Exported {matched_count} messages to '{self.output_file}'.")

        except Exception as err:
            print(f"[!] An error occurred during export: {err}")
        finally:
            await self.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract all messages sent by a specific user in a Discord channel."
    )
    parser.add_argument(
        "-c", "--channel", 
        type=int, 
        required=True, 
        help="Target Discord Channel ID"
    )
    parser.add_argument(
        "-u", "--user", 
        type=int, 
        required=True, 
        help="Target User ID"
    )
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default="exported_messages.txt", 
        help="Output text filename (default: exported_messages.txt)"
    )
    parser.add_argument(
        "-d", "--delay", 
        type=float, 
        default=1.5, 
        help="Throttling delay in seconds between page requests (default: 1.5)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("[!] Error: DISCORD_TOKEN not found. Make sure it is set in your .env file.")
        sys.exit(1)

    client = DiscordMessageExporter(
        channel_id=args.channel,
        target_user_id=args.user,
        output_file=args.output,
        delay=args.delay
    )

    try:
        client.run(token)
    except KeyboardInterrupt:
        print("\n[!] Script aborted by user.")


if __name__ == "__main__":
    main()