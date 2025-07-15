# Reddit User Persona Generator

This tool scrapes a Reddit user's posts and comments using **Selenium**, then analyzes the data using **LLMs (like DeepSeek)** to generate a full **user persona** — including traits like behavior, frustrations, motivations, and personality, with proper citation links.

---

##  Features

- ✅ Scrapes Reddit posts and comments with links
- ✅ Cleans and deduplicates raw text
- ✅ Cites source links for every trait (e.g. POST / COMMENT)
- ✅ Generates a persona using DeepSeek LLM via [OpenRouter.ai](https://openrouter.ai/)
- ✅ Output is saved as a clean `.txt` file for easy reading

---

## Requirements

- Python 3.9+
- Google Chrome installed
- ChromeDriver matching your Chrome version

---

## 📦 Setup

### 1. Clone this repo

```bash
git clone https://github.com/yourusername/reddit-persona-generator.git
cd reddit-persona-generator
````

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 ChromeDriver Setup

You have 2 options:

### Option 1: Manual (if using fixed driver path)

1. Find your Chrome version:

   * Run `google-chrome --version` or visit `chrome://settings/help`
2. Download the matching [ChromeDriver](https://chromedriver.chromium.org/downloads)
3. Place it at a known path like:

   * Linux: `/usr/local/bin/chromedriver`
   * Windows: `C:\chromedriver\chromedriver.exe`
4. Update your Python script to:

```python
from selenium.webdriver.chrome.service import Service
service = Service(executable_path="/your/path/to/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
```

### Option 2: Recommended — Use `webdriver-manager`

Just install:

```bash
pip install webdriver-manager
```

And your script can automatically install the right driver!

---

## 🧪 Usage

### 🔹 Step 1: Scrape a Reddit user

```bash
python scraper.py
# You'll be prompted to enter a Reddit username (no /user/)
```

This saves:

```
<username>_numbered_scraped_with_links.txt
```

### 🔸 Step 2: Generate persona from text

```bash
python generate_persona.py
# Enter the filename from step 1
```

This saves:

```
<username>_persona.txt
```

---

## 🧠 Persona Output Example

```
Age: ~23-27 (source: https://reddit.com/r/xyz)
Frustrations:
- Hates slow delivery times (source: ...)
- Complains about bugs in apps (source: ...)

Personality:
- Introvert, likes gaming (source: ...)
```

---

## 📌 Notes

* Your OpenRouter API key is required in `generate_persona.py`
* Supports `deepseek/deepseek-chat-v3-0324:free` or any OpenRouter LLM

---

## 🛡️ License

MIT License

---

## 🙌 Credits

Created with ❤️ by [RavinderKumar](https://github.com/akatsuki-uchiha-itachi)
Powered by Selenium, OpenRouter, DeepSeek
