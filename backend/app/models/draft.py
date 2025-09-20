from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ActionType(str, Enum):
    PICK = "pick"
    BAN = "ban"

class Team(str, Enum):
    BLUE = "blue"
    RED = "red"

class DraftPhase(str, Enum):
    BANS_1 = "bans_1"
    PICKS_1 = "picks_1" 
    BANS_2 = "bans_2"
    PICKS_2 = "picks_2"
    BANS_3 = "bans_3"
    PICKS_3 = "picks_3"
    COMPLETED = "completed"

class DraftAction(BaseModel):
    """Single draft action (pick/ban)"""
    id: str = Field(..., description="Unique action ID")
    session_id: str = Field(..., description="Draft session ID")
    champion_id: int = Field(..., description="Champion ID")
    champion_name: str = Field(..., description="Champion name")
    action_type: ActionType = Field(..., description="Pick or ban")
    team: Team = Field(..., description="Team making the action")
    order: int = Field(..., description="Action order in draft")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True

class TeamComposition(BaseModel):
    """Team composition analysis"""
    team: Team
    champions: List[int] = Field(default=[], description="Champion IDs")
    roles_filled: Dict[str, int] = Field(default={}, description="Role assignments")
    
    # Composition metrics
    damage_distribution: Dict[str, float] = Field(default={}, description="AD/AP/True damage %")
    crowd_control_score: float = Field(0.0, description="CC capability 0-100")
    teamfight_score: float = Field(0.0, description="Teamfight strength 0-100")
    early_game_score: float = Field(0.0, description="Early game power 0-100")
    late_game_score: float = Field(0.0, description="Late game scaling 0-100")
    
    # Synergy analysis
    synergy_score: float = Field(0.0, description="Team synergy 0-100")
    synergy_reasons: List[str] = Field(default=[], description="Synergy explanations")
    
    # Weaknesses
    vulnerabilities: List[str] = Field(default=[], description="Team weaknesses")
    missing_roles: List[str] = Field(default=[], description="Unfilled roles")
    
    class Config:
        use_enum_values = True

class WinPrediction(BaseModel):
    """Win probability prediction"""
    blue_team_win_rate: float = Field(..., description="Blue team win probability 0-1")
    red_team_win_rate: float = Field(..., description="Red team win probability 0-1")
    confidence: float = Field(..., description="Prediction confidence 0-1")
    
    # Factors
    key_factors: List[str] = Field(default=[], description="Main prediction factors")
    matchup_advantages: Dict[str, float] = Field(default={}, description="Role matchup scores")
    
    model_version: str = Field(..., description="ML model version used")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DraftSession(BaseModel):
    """Complete draft session"""
    id: str = Field(..., description="Unique session ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Draft state
    current_phase: DraftPhase = Field(default=DraftPhase.BANS_1)
    current_team: Team = Field(default=Team.BLUE)
    current_action_order: int = Field(default=1)
    
    # Teams
    blue_team_players: List[str] = Field(default=[], description="Player summoner names")
    red_team_players: List[str] = Field(default=[], description="Player summoner names")
    
    # Actions history
    actions: List[DraftAction] = Field(default=[], description="All draft actions")
    
    # Current state
    blue_picks: List[int] = Field(default=[], description="Blue team champion IDs")
    red_picks: List[int] = Field(default=[], description="Red team champion IDs")
    blue_bans: List[int] = Field(default=[], description="Blue team banned champions")
    red_bans: List[int] = Field(default=[], description="Red team banned champions")
    
    # Analysis
    blue_composition: Optional[TeamComposition] = None
    red_composition: Optional[TeamComposition] = None
    win_prediction: Optional[WinPrediction] = None
    
    # Settings
    is_tournament_draft: bool = Field(default=False, description="Tournament mode (10 bans)")
    patch_version: str = Field(default="14.19", description="Game patch")
    
    class Config:
        use_enum_values = True

class DraftSuggestion(BaseModel):
    """AI suggestion for draft action"""
    champion_id: int = Field(..., description="Suggested champion ID")
    champion_name: str = Field(..., description="Champion name")
    action_type: ActionType = Field(..., description="Suggested action type")
    
    priority_score: float = Field(..., description="Priority score 0-100")
    reasoning: List[str] = Field(..., description="Reasons for suggestion")
    
    # Context
    counters: List[int] = Field(default=[], description="Champions this counters")
    synergizes_with: List[int] = Field(default=[], description="Team synergies")
    role_fit: str = Field(..., description="Recommended role")
    
    # Metrics
    win_rate_impact: float = Field(..., description="Expected win rate change")
    pick_rate: float = Field(..., description="Current pick rate in meta")
    ban_rate: float = Field(..., description="Current ban rate in meta")
    
    class Config:
        use_enum_values = True