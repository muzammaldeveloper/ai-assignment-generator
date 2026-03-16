"""Fix existing assignment paths to use absolute paths."""
import sqlite3, os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(PROJECT_ROOT, 'instance', 'app.db')

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT id, docx_path, pdf_path FROM assignments WHERE status='completed'")
rows = c.fetchall()

for row in rows:
    aid, docx, pdf = row
    updates = {}
    if docx and not os.path.isabs(docx):
        abs_docx = os.path.abspath(os.path.join(PROJECT_ROOT, docx))
        updates['docx_path'] = abs_docx
    if pdf and not os.path.isabs(pdf):
        abs_pdf = os.path.abspath(os.path.join(PROJECT_ROOT, pdf))
        updates['pdf_path'] = abs_pdf
    if updates:
        sets = ', '.join(f"{k}=?" for k in updates)
        vals = list(updates.values()) + [aid]
        c.execute(f"UPDATE assignments SET {sets} WHERE id=?", vals)
        print(f"Fixed {aid}: {updates}")

conn.commit()
conn.close()
print("Done.")
