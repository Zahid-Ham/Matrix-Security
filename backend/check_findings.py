import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def run():
    engine = create_async_engine('sqlite+aiosqlite:///./matrix.db')
    async with engine.connect() as conn:
        print("--- SCANS ---")
        scans = (await conn.execute(text('SELECT id, target_url, endpoints_discovered, forms_discovered, status FROM scans ORDER BY id DESC LIMIT 5'))).fetchall()
        for s in scans:
            print(s)
            
        print("\n--- VULNERABILITIES FOR LATEST SCAN ---")
        vulns = (await conn.execute(text('SELECT id, title, url, severity, detected_by FROM vulnerabilities ORDER BY id DESC LIMIT 10'))).fetchall()
        for v in vulns:
            print(v)

if __name__ == "__main__":
    asyncio.run(run())
