from openai import OpenAI, OpenAIError
import os
import sys

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
    import random

    style = load_style()

    MODES = [
        "do a \"fit check\" and mention every article of designer clothing you are wearing",
        "tell a short surreal anecdote from yesterday",
        "sound overly confident about something trivial",
        "deride the typical fashion choices in your vicinity",
        "make a fashion-forward observation",
        "blend tech language with cultural commentary",
        "say something wise that almost doesn’t make sense"
    ]

    mode = random.choice(MODES)

    prompt = f"""
You are a parody account.

VOICE AND STYLE:
{style}

TASK:
Write ONE original tweet (max 280 characters).

CREATIVE DIRECTION:
Today’s tweet should {mode}.

IMPORTANT:
Avoid repeating common phrases, themes, or structures from previous tweets.
If this sounds like something you’ve already written, do something different.

RULES:
- Do not quote real tweets
- No hashtags
- Cheeky, self-assured tone

Return ONLY the tweet text.
"""

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    for attempt in range(3):
        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

            tweet = response.output_text.strip()

            if is_safe(tweet):
                return tweet

        except OpenAIError as e:
            print("OpenAI API error, using fallback tweet.")
            print(e)
            break  # stop retrying if quota is exceeded

    # Always return something
    return "taking a mental health day"


from post_to_x import post_tweet

if __name__ == "__main__":
    try:
        tweet = generate_tweet()

        print("=== SAFE GENERATED TWEET ===")
        print(tweet)
        print("\nPosting tweet to X...")

        try:
            response = post_tweet(tweet)
            print("Tweet posted successfully")
            print(response)
        except Exception as e:
            print("Tweet failed to post, but workflow will continue.")
            print("Error details:")
            print(e)

    except Exception as e:
        print("Unexpected error occurred, but workflow will not fail.")
        print("Error details:")
        print(e)

    sys.exit(0)
