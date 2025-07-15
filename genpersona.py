import requests
import json

API_KEY = "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"
MODEL = "deepseek/deepseek-chat-v3-0324:free"
FILENAME = input("Enter scraped filename (e.g. username_numbered_scraped_with_links.txt): ").strip()

with open(FILENAME, "r", encoding="utf-8") as f:
    reddit_data = f.read()

# === Persona Prompt Template ===
system_prompt = """You are an expert persona analyst. Based on the given Reddit user's posts and comments, construct a complete user persona with supporting citations.

Generate the following traits:
- Age (guess)
- Occupation (guess)
- Status (e.g. single, student)
- Location (if possible)
- Archetype (e.g. The Explorer, The Creator)
- Motivations (convenience, speed, comfort, wellness, etc)
- Personality (Introvert–Extrovert, Thinking–Feeling, etc)
- Behaviour & Habits (e.g. frequency of posting, interests, writing tone)
- Frustrations (what they complain about or dislike)
- Goals & Needs (implicit or explicit desires)

IMPORTANT: For each trait or bullet, **cite a source link** from their posts or comments, using this format:
  - Loves gaming and memes. (source: https://reddit.com/r/xyz123)

Keep it professional and use bullet points where needed."""

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": reddit_data}
    ]
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",  # optional
    "X-Title": "PersonaGenerator",       # optional
}

print("🧠 Sending to DeepSeek API...")
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    data=json.dumps(payload)
)

if response.status_code == 200:
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    output_file = FILENAME.replace(".txt", "_persona.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ Persona saved to: {output_file}")
    print("\n--- Preview ---\n")
    print(content[:1000], "...\n[truncated]")
else:
    print(f"❌ Failed ({response.status_code}):")
    print(response.text)
