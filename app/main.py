from infra.database import Connection
from sqlmodel import text

with Connection() as conn:
    conn.exec(text('select 1;'))