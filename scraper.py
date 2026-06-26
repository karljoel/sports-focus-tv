import requests
from bs4 import BeautifulSoup
import re
import base64
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Your GitHub settings
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "sports-focus-tv"
FILE_PATH = "app.py"
GITHUB_API_URL = f"https://api.github.com/repos/karljoel/{REPO_NAME}/contents/{FILE_PATH}"

# ---- SOURCE SITES ----
SOURCE_SITES = [
    {
        "name": "Hes-Goals",
        "search_url": "https://hes-goals.com/search?q={query}",
        "find_link": lambda soup: soup.find('iframe', {'id': 'player'})
    },
    {
        "name": "VIPLeague",
        "search_url": "https://www.vipleague.si/search/{query}",
        "find_link": lambda soup: soup.find('a', href=re.compile(r'/embed/'))
    },
    {
        "name": "SoccerStreams",
        "search_url": "https://soccerstreams100.io/search?q={query}",
        "find_link": lambda soup: soup.find('iframe', src=re.compile(r'player|stream'))
    },
    {
        "name": "BuffStreams",
        "search_url": "https://buffstreams.io/search/{query}",
        "find_link": lambda soup: soup.find('iframe', src=re.compile(r'player|stream'))
    }
]

def get_current_matches():
    """Fetches the current match list from your app.py on GitHub"""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(GITHUB_API_URL, headers=headers)
    
    print(f"📡 GitHub API Status: {response.status_code}")
    
    if response.status_code == 404:
        print("❌ app.py not found on GitHub!")
        return [], "", ""
    
    if response.status_code == 401:
        print("❌ Invalid token! Please check your .env file.")
        return [], "", ""
    
    data = response.json()
    
    if 'content' not in data:
        print(f"❌ Unexpected response: {data}")
        return [], "", ""
    
    content = base64.b64decode(data['content']).decode('utf-8')
    sha = data['sha']
    
    matches = []
    match_blocks = re.findall(r'\{[^}]*"home"[^}]*"away"[^}]*"stream_link"[^}]*\}', content, re.DOTALL)
    
    for block in match_blocks:
        home_match = re.search(r'"home":\s*"([^"]+)"', block)
        away_match = re.search(r'"away":\s*"([^"]+)"', block)
        link_match = re.search(r'"stream_link":\s*([^,}]+)', block)
        
        if home_match and away_match:
            home = home_match.group(1)
            away = away_match.group(1)
            link = link_match.group(1).strip() if link_match else "None"
            if link == "None" or link == '""' or link is None:
                matches.append((home, away))
    
    return matches, content, sha

def find_stream_on_sites(home, away):
    """Searches ALL source sites for a stream link"""
    search_terms = [
        f"{home} vs {away}",
        f"{home} {away}",
        f"{away} vs {home}"
    ]
    
    for site in SOURCE_SITES:
        print(f"  🔍 Searching {site['name']}...")
        for term in search_terms:
            query = term.replace(' ', '+')
            search_url = site['search_url'].format(query=query)
            
            try:
                response = requests.get(search_url, timeout=15, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Use the site-specific find_link function
                element = site['find_link'](soup)
                if element:
                    src = element.get('src') or element.get('href')
                    if src and src.startswith('http'):
                        return src
                        
            except Exception as e:
                print(f"    ⚠️ Error on {site['name']}: {e}")
                continue
    return None

def update_multiple_streams(matches_to_update, content, sha):
    """Updates all matches in one commit"""
    if not matches_to_update:
        print("📭 No matches need stream updates")
        return False
    
    print(f"\n📝 Updating {len(matches_to_update)} matches...")
    
    for home, away, link in matches_to_update:
        match_pattern = rf'(\{{[^}}]*"home":\s*"{home}"[^}}]*"away":\s*"{away}"[^}}]*"stream_link":\s*)[^,}}]+'
        replacement = rf'\1"{link}"'
        content = re.sub(match_pattern, replacement, content, flags=re.DOTALL)
        print(f"  ✅ {home} vs {away} → {link[:50]}...")
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    commit_data = {
        "message": f"🤖 Bot: Added streams for {len(matches_to_update)} matches",
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "sha": sha
    }
    
    response = requests.put(GITHUB_API_URL, headers=headers, json=commit_data)
    if response.status_code == 200:
        print(f"\n✅ Bot successfully updated {len(matches_to_update)} streams!")
        return True
    else:
        print(f"\n❌ Bot failed: {response.text}")
        return False

def main():
    print("\n" + "="*50)
    print("⚽ SPORTS FOCUS TV — AUTO STREAM BOT (4 SOURCES)")
    print("="*50 + "\n")
    
    print("📡 Fetching matches from GitHub...")
    matches, content, sha = get_current_matches()
    
    if not matches and content == "":
        print("⚠️ No matches found. Please check your app.py on GitHub.")
        return
    
    if not matches:
        print("🎉 All matches already have streams! Nothing to do.")
        return
    
    print(f"🔍 Found {len(matches)} matches needing streams:")
    for home, away in matches:
        print(f"  - {home} vs {away}")
    
    print("\n" + "="*50)
    print("🔎 SEARCHING FOR STREAMS ON 4 SITES...")
    print("="*50 + "\n")
    
    matches_with_links = []
    for idx, (home, away) in enumerate(matches, 1):
        print(f"[{idx}/{len(matches)}] {home} vs {away}")
        link = find_stream_on_sites(home, away)
        
        if link:
            matches_with_links.append((home, away, link))
            print(f"  ✅ Found: {link[:60]}...")
        else:
            print(f"  ❌ No stream found on any site")
        print()
        time.sleep(2)
    
    if matches_with_links:
        print("\n" + "="*50)
        print("📤 UPLOADING TO GITHUB...")
        print("="*50 + "\n")
        update_multiple_streams(matches_with_links, content, sha)
    else:
        print("\n⚠️ No streams found for any match. Try again later.")

if __name__ == "__main__":
    main()