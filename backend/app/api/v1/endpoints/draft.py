from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from app.models.draft import DraftSession, DraftAction, TeamComposition
from app.services.draft_service import DraftService
from app.services.websocket_service import WebSocketService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/session", response_model=DraftSession)
async def create_draft_session(
    blue_team: List[str] = [],
    red_team: List[str] = [],
    draft_service: DraftService = Depends()
):
    """Create new draft session"""
    try:
        session = await draft_service.create_session(blue_team, red_team)
        await WebSocketService.broadcast_session_created(session)
        return session
    except Exception as e:
        logger.error(f"Failed to create draft session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@router.get("/session/{session_id}", response_model=DraftSession)
async def get_draft_session(
    session_id: str,
    draft_service: DraftService = Depends()
):
    """Get draft session by ID"""
    session = await draft_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/session/{session_id}/action", response_model=DraftAction)
async def add_draft_action(
    session_id: str,
    champion_id: int,
    action_type: str,  # "pick" or "ban"
    team: str,  # "blue" or "red"
    draft_service: DraftService = Depends()
):
    """Add pick/ban action to draft"""
    try:
        action = await draft_service.add_action(
            session_id, champion_id, action_type, team
        )
        await WebSocketService.broadcast_action(session_id, action)
        return action
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to add draft action: {e}")
        raise HTTPException(status_code=500, detail="Failed to add action")

@router.get("/session/{session_id}/suggestions")
async def get_draft_suggestions(
    session_id: str,
    team: str,
    draft_service: DraftService = Depends()
):
    """Get AI suggestions for next pick/ban"""
    try:
        suggestions = await draft_service.get_suggestions(session_id, team)
        return suggestions
    except Exception as e:
        logger.error(f"Failed to get suggestions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get suggestions")

@router.get("/session/{session_id}/analysis", response_model=TeamComposition)
async def analyze_team_composition(
    session_id: str,
    team: str,
    draft_service: DraftService = Depends()
):
    """Analyze current team composition"""
    try:
        analysis = await draft_service.analyze_composition(session_id, team)
        return analysis
    except Exception as e:
        logger.error(f"Failed to analyze composition: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze composition")