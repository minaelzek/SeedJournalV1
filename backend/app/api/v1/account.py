import json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_deps import get_current_user_id
from app.core.deps import get_db
from app.identity.account import delete_user_account, export_user_data

router = APIRouter()


@router.get("/export")
async def export_account(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
) -> Response:
    payload = await export_user_data(session, user_id)
    if not payload:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    body = json.dumps(payload, indent=2).encode("utf-8")
    return Response(
        content=body,
        media_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="seedjournal-export.json"'},
    )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
) -> Response:
    ok = await delete_user_account(session, user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)