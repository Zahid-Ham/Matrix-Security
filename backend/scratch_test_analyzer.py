import asyncio
from scanner.target_analyzer import TargetAnalyzer

async def main():
    analyzer = TargetAnalyzer()
    try:
        analysis = await analyzer.analyze("http://zero.webappsecurity.com/")
        print("--- ANALYSIS COMPLETED ---")
        print(f"Status Code: {analysis.status_code}")
        print(f"Endpoints found: {len(analysis.endpoints)}")
        for ep in analysis.endpoints[:10]:
            print(f"  - {ep.method} {ep.url}")
        print(f"Technologies: {analysis.technology_stack}")
    finally:
        await analyzer.close()

if __name__ == "__main__":
    asyncio.run(main())
