from openai import OpenAI
import os
import re

BANNED_WORDS = [
    "kill", "die", "hate", "nazi", "terrorist"
]

def load_style():
    with open("style.md", "r", encoding="utf-8") as f:
        return f.read()

def is_safe(tweet):
    if len(tweet) > 280:
        return False

    if "@" in tweet:
        return False

    if "http://" in tweet or "https://" in tweet:
        return False

    lower = tweet.lower()
    for word in BANNED_WORDS:
        if word in lower:
            return False

    return True

def generate_tweet():
    style = load_style()

    prompt = f"""
You are a parody account.

VOICE AND STYLE:
{style}

TASK:
Write ONE original tweet (max 280 characters).
- Do not quote real tweets
- Do not mention real people
- No hashtags
- Cheeky, self-assured tone

Return ONLY the tweet text.
"""

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    for attempt in range(3):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        tweet = response.output_text.strip()

        if is_safe(tweet):
            return tweet

    return "Most problems persist because fixing them would upset someone who benefits from the status quo."

from post_to_x import post_tweet

if __name__ == "__main__":
    tweet = generate_tweet()

    print("=== SAFE GENERATED TWEET ===")
    print(tweet)
    print("\nPosting tweet to X...")

    response = post_tweet(tweet)

    print("Tweet posted successfully")
    print(response)

