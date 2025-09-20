from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from app.models.champion import Champion, ChampionStats
from app.services.champion_service import ChampionService
from app.services.riot_service import RiotService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[Champion])
async def get_champions(
    role: Optional[str] = Query(None, description="Filter by role"),
    search: Optional[str] = Query(None, description="Search by name"),
    champion_service: ChampionService = Depends()
):
    """Get all champions with optional filtering"""
    try:
        champions = await champion_service.get_champions(role=role, search=search)
        return champions
    except Exception as e:
        logger.error(f"Failed to get champions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get champions")

@router.get("/{champion_id}", response_model=Champion)
async def get_champion(
    champion_id: int,
    champion_service: ChampionService = Depends()
):
    """Get champion by ID"""
    champion = await champion_service.get_champion(champion_id)
    if not champion:
        raise HTTPException(status_code=404, detail="Champion not found")
    return champion

@router.get("/{champion_id}/stats", response_model=ChampionStats)
async def get_champion_stats(
    champion_id: int,
    patch: Optional[str] = Query(None, description="Game patch version"),
    rank: Optional[str] = Query("PLATINUM", description="Rank tier"),
    champion_service: ChampionService = Depends()
):
    """Get champion statistics"""
    try:
        stats = await champion_service.get_champion_stats(
            champion_id, patch=patch, rank=rank
        )
        return stats
    except Exception as e:
        logger.error(f"Failed to get champion stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get stats")

@router.get("/{champion_id}/counters")
async def get_champion_counters(
    champion_id: int,
    role: Optional[str] = Query(None, description="Role context"),
    champion_service: ChampionService = Depends()
):
    """Get champion counters and synergies"""
    try:
        counters = await champion_service.get_counters(champion_id, role=role)
        return counters
    except Exception as e:
        logger.error(f"Failed to get counters: {e}")
        raise HTTPException(status_code=500, detail="Failed to get counters")

@router.post("/update-data")
async def update_champion_data(
    riot_service: RiotService = Depends()
):
    """Update champion data from Riot API (admin endpoint)"""
    try:
        await riot_service.update_champion_data()
        return {"message": "Champion data updated successfully"}
    except Exception as e:
        logger.error(f"Failed to update champion data: {e}")
        raise HTTPException(status_code=500, detail="Failed to update data")