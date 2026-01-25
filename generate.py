from openai import OpenAI

def load_style():
    with open("style.md", "r", encoding="utf-8") as f:
        return f.read()

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

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )

    tweet = response.choices[0].message.content.strip()
    return tweet


if __name__ == "__main__":
    print(generate_tweet())
