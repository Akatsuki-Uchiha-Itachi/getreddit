from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# === Set path to your chromedriver if needed ===
# CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
# service = Service(executable_path=CHROMEDRIVER_PATH)

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment to run headless

driver = webdriver.Chrome(options=options)

username = input("Enter Reddit username (no /user/): ").strip()

# === Helper to extract full post/comment link from article ===
def extract_post_link(article):
    try:
        link_el = article.find_element(By.CSS_SELECTOR, 'a[href*="/comments/"]')
        href = link_el.get_attribute("href")
        if href and href.startswith("/"):
            return "https://www.reddit.com" + href
        return href
    except:
        return ""

# === Scrape posts ===
def scroll_and_collect_posts(url, min_words=5):
    print(f"🔹 Scraping posts from: {url}")
    driver.get(url)
    time.sleep(5)

    for _ in range(6):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)

    posts = []
    seen = set()
    articles = driver.find_elements(By.TAG_NAME, "article")
    print(f"🧩 Found {len(articles)} post <article> tags")

    for article in articles:
        try:
            content = article.get_attribute("aria-label")
            link = extract_post_link(article)

            if content and len(content.split()) >= min_words:
                key = content + link
                if key not in seen:
                    seen.add(key)
                    posts.append((content, link))
        except:
            continue

    return posts

# === Scrape comments (with post title and link) ===
def scroll_and_collect_comments_with_titles(url, min_words=5):
    print(f"🔹 Scraping comments from: {url}")
    driver.get(url)
    time.sleep(5)

    for _ in range(6):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)

    comments = []
    seen = set()
    articles = driver.find_elements(By.TAG_NAME, "article")
    print(f"🧩 Found {len(articles)} comment <article> tags")

    for article in articles:
        try:
            post_title = article.get_attribute("aria-label")
            link = extract_post_link(article)
            if not post_title or len(post_title.split()) < 2:
                continue

            ps = article.find_elements(By.TAG_NAME, "p")
            body = "\n".join([p.text.strip() for p in ps if len(p.text.strip()) >= min_words])
            key = post_title + body + link

            if not body or key in seen:
                continue

            seen.add(key)

            full_comment = f"POST: {post_title}\nLINK: {link}\n\nCOMMENT: {body}"
            comments.append(full_comment)

        except:
            continue

    return comments

# === Run the scrapers ===
posts_url = f"https://www.reddit.com/user/{username}/posts/"
comments_url = f"https://www.reddit.com/user/{username}/comments/"

posts = scroll_and_collect_posts(posts_url)
comments = scroll_and_collect_comments_with_titles(comments_url)

# === Done, close browser ===
driver.quit()

# === Save to file with numbering ===
output_file = f"{username}_numbered_scraped_with_links.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== POSTS ===\n\n")
    for i, (content, link) in enumerate(posts, 1):
        f.write(f"# {i}\n{content}\nLINK: {link}\n\n")

    f.write("\n=== COMMENTS ===\n\n")
    for i, c in enumerate(comments, 1):
        f.write(f"# COMMENT {i}\n{c}\n\n")

# === Summary ===
print(f"\n✅ Done scraping Reddit user: {username}")
print(f"📝 Posts captured: {len(posts)}")
print(f"💬 Comments captured: {len(comments)}")
print(f"📁 Output saved to: {output_file}")
