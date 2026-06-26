import asyncio
from sqlalchemy import select, desc
from core.database import get_db_context
from models.scan import Scan
from models.forensic import ForensicRecord, ForensicTimeline
from models.vulnerability import Vulnerability

async def main():
    async with get_db_context() as db:
        s = (await db.execute(select(Scan).order_by(desc(Scan.id)).limit(1))).scalar_one_or_none()
        if s:
            print(f"=== Scan Details ===")
            print(f"Scan ID: {s.id}")
            print(f"URL: {s.target_url}")
            print(f"Status: {s.status}")
            print(f"Endpoints discovered: {s.endpoints_discovered}")
            print(f"Forms discovered: {s.forms_discovered}")
            print(f"Technology Stack: {s.technology_stack}")
            
            print(f"\n=== Vulnerabilities Found ===")
            vulns = (await db.execute(select(Vulnerability).where(Vulnerability.scan_id == s.id))).scalars().all()
            print(f"Count: {len(vulns)}")
            for v in vulns:
                print(f"  - [{v.severity.upper()}] {v.title} on {v.url} (Type: {v.vulnerability_type}, Agent: {v.detected_by})")
                
            print(f"\n=== Timeline Events ===")
            record = (await db.execute(select(ForensicRecord).where(ForensicRecord.scan_id == s.id))).scalar_one_or_none()
            if record:
                events = (await db.execute(
                    select(ForensicTimeline)
                    .where(ForensicTimeline.forensic_record_id == record.id)
                    .order_by(ForensicTimeline.timestamp)
                )).scalars().all()
                for e in events:
                    print(f"  [{e.timestamp.strftime('%H:%M:%S')}] {e.source_module} - {e.event_type}: {e.description}")
            else:
                print("No forensic record found for this scan.")

if __name__ == "__main__":
    asyncio.run(main())
