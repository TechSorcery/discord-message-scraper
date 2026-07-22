# Discord Message Scraper

A lightweight Python command-line utility built on `discord.py-self` to extract all messages sent by a specific user within a Discord channel and save them to a formatted text file.

It includes built-in rate-limit handling and throttling to prevent API trigger limits (429 responses) while scraping large chat histories.

---

## Features

- **Targeted Scraping:** Pulls messages from a specific user in a chosen channel.
- **Rate-Limit Safe:** Throttles request batches every 25 messages to avoid Discord rate limits.
- **CLI Interface:** Easily pass channel IDs, target user IDs, output filenames, and delay intervals via command-line arguments.
- **Environment Security:** Uses `.env` files to keep your Discord authorization token safe and out of version control.

---

## Prerequisites

- **Python 3.10+** installed on your system.
- Your personal Discord Authorization Token (User Token).

---

## Setup & Installation

1. **Clone or download the repository:**
   git clone [https://github.com/YourUsername/discord-message-scraper.git](https://github.com/YourUsername/discord-message-scraper.git)
   
   cd discord-message-scraper
