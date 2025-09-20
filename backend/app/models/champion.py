from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    TOP = "top"
    JUNGLE = "jungle"
    MID = "mid"
    ADC = "adc"
    SUPPORT = "support"

class DamageType(str, Enum):
    PHYSICAL = "physical"
    MAGICAL = "magical"
    TRUE = "true"
    MIXED = "mixed"

class Champion(BaseModel):
    """Champion base data"""
    id: int = Field(..., description="Champion ID")
    key: str = Field(..., description="Champion key")
    name: str = Field(..., description="Champion name")
    title: str = Field(..., description="Champion title")
    
    # Basic info
    roles: List[Role] = Field(..., description="Primary roles")
    difficulty: int = Field(..., description="Difficulty 1-10")
    
    # Combat stats
    damage_type: DamageType = Field(..., description="Primary damage type")
    attack_range: int = Field(..., description="Attack range")
    
    # Tags for categorization
    tags: List[str] = Field(default=[], description="Champion tags")
    
    # Assets
    icon_url: str = Field(..., description="Champion icon URL")
    splash_url: str = Field(..., description="Champion splash URL")
    
    # Meta
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True

class ChampionAbility(BaseModel):
    """Champion ability data"""
    key: str = Field(..., description="Ability key (Q/W/E/R/P)")
    name: str = Field(..., description="Ability name")
    description: str = Field(..., description="Ability description")
    cooldown: List[float] = Field(default=[], description="Cooldown per rank")
    cost: List[int] = Field(default=[], description="Resource cost per rank")
    range: List[int] = Field(default=[], description="Range per rank")

class ChampionStats(BaseModel):
    """Champion performance statistics"""
    champion_id: int = Field(..., description="Champion ID")
    patch: str = Field(..., description="Game patch version")
    rank_tier: str = Field(..., description="Rank tier for stats")
    role: Optional[Role] = Field(None, description="Specific role stats")
    
    # Performance metrics
    pick_rate: float = Field(..., description="Pick rate percentage")
    ban_rate: float = Field(..., description="Ban rate percentage")
    win_rate: float = Field(..., description="Win rate percentage")
    
    # Detailed stats
    average_kda: Dict[str, float] = Field(default={}, description="Average K/D/A")
    average_cs: float = Field(0.0, description="Average CS per minute")
    average_damage: float = Field(0.0, description="Average damage per game")
    average_gold: float = Field(0.0, description="Average gold per minute")
    
    # Game phases
    early_game_wr: float = Field(0.0, description="Win rate at 15 minutes")
    mid_game_wr: float = Field(0.0, description="Win rate at 25 minutes")
    late_game_wr: float = Field(0.0, description="Win rate at 35+ minutes")
    
    # Build data
    popular_items: List[int] = Field(default=[], description="Most popular item IDs")
    popular_runes: Dict[str, Any] = Field(default={}, description="Most popular runes")
    popular_skills: List[str] = Field(default=[], description="Skill order")
    
    # Sample size
    games_analyzed: int = Field(..., description="Number of games in sample")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True

class ChampionMatchup(BaseModel):
    """Champion vs champion matchup data"""
    champion_id: int = Field(..., description="Main champion ID")
    opponent_id: int = Field(..., description="Opponent champion ID")
    role: Role = Field(..., description="Lane/role context")
    
    # Matchup stats
    win_rate: float = Field(..., description="Win rate in this matchup")
    kill_rate: float = Field(0.0, description="Kill rate advantage")
    cs_diff: float = Field(0.0, description="CS difference at 15min")
    gold_diff: float = Field(0.0, description="Gold difference at 15min")
    
    # Difficulty
    difficulty_score: float = Field(..., description="Matchup difficulty 0-100")
    
    # Recommendations
    counter_strength: float = Field(..., description="How strong a counter 0-100")
    play_style_tips: List[str] = Field(default=[], description="Matchup advice")
    
    # Meta
    games_analyzed: int = Field(..., description="Sample size")
    patch: str = Field(..., description="Patch version")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True

class ChampionSynergy(BaseModel):
    """Champion team synergy data"""
    champion_id: int = Field(..., description="Main champion ID")
    synergy_champion_id: int = Field(..., description="Synergy partner ID")
    
    # Synergy metrics
    synergy_score: float = Field(..., description="Synergy strength 0-100")
    win_rate_together: float = Field(..., description="Win rate when picked together")
    pick_rate_together: float = Field(..., description="How often picked together")
    
    # Context
    synergy_type: str = Field(..., description="Type of synergy (engage, poke, etc)")
    synergy_reasons: List[str] = Field(default=[], description="Why they synergize")
    
    # Requirements
    requires_coordination: bool = Field(False, description="Needs team coordination")
    skill_floor: int = Field(1, description="Minimum skill required 1-10")
    
    # Meta
    games_analyzed: int = Field(..., description="Sample size")
    patch: str = Field(..., description="Patch version")
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class ChampionTierList(BaseModel):
    """Champion tier ranking"""
    patch: str = Field(..., description="Patch version")
    rank_tier: str = Field(..., description="Rank context")
    role: Role = Field(..., description="Role context")
    
    # Tier data
    s_tier: List[int] = Field(default=[], description="S tier champion IDs")
    a_tier: List[int] = Field(default=[], description="A tier champion IDs")
    b_tier: List[int] = Field(default=[], description="B tier champion IDs")
    c_tier: List[int] = Field(default=[], description="C tier champion IDs")
    d_tier: List[int] = Field(default=[], description="D tier champion IDs")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    algorithm_version: str = Field(..., description="Tier calculation version")
    
    class Config:
        use_enum_values = True