import asyncio
from scanner.target_analyzer import TargetAnalyzer

async def run():
    target = 'http://localhost/'
    cookies = {'PHPSESSID': 'squ5b28dn412sem5eaifggive3', 'security': 'low'}
    print(f"Testing crawler on: {target} with cookies: {cookies}")
    analyzer = TargetAnalyzer(
        timeout=15.0,
        max_depth=3,
        auth_cookies=cookies
    )
    
    # Let's inspect the initial page fetch
    resp = await analyzer._fetch_with_error_handling(target)
    if resp:
        print(f"Response status: {resp.status_code}")
        print(f"Final URL after redirects: {resp.url}")
        print(f"Is login page: {'login' in str(resp.url) or 'login' in resp.text.lower()}")
        print(f"Response content length: {len(resp.text)}")
        
        # Let's see what endpoints we discover
        analysis = await analyzer.analyze(target)
        print(f"Endpoints found: {len(analysis.endpoints)}")
        for ep in analysis.endpoints[:10]:
            print(f"  - {ep.method} {ep.url} (params: {ep.params}, source: {ep.source})")
    else:
        print("Failed to fetch initial response")
        
    await analyzer.close()

if __name__ == "__main__":
    asyncio.run(run())
