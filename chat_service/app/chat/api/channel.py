import asyncio
from fastapi import APIRouter

from app.db.scylla import get_cluster

cluster = get_cluster()
session = cluster.connect("chat")
router = APIRouter()

def query_messages():
    query = """
        SELECT message_id, content, created_at, sender_uid
        FROM messages
        WHERE channel_uid= %s 
        LIMIT 500000
    """
    result_set = session.execute(query, ("channel_1",))
    return [
        {
            "message_id": str(row.message_id),
            "content": row.content,
            "sender_uid": row.sender_uid,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
        for row in result_set
    ]

@router.get("/")
async def messages():
    loop = asyncio.get_running_loop()
    results = await loop.run_in_executor(None, query_messages)
    return {"results": results}
