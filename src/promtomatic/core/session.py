"""
Module for managing optimization sessions and their state.
"""

from datetime import datetime
from typing import List, Dict, Optional
from .feedback import Feedback
from ..utils.logging import SessionLogger
from ..core.config import Config

class OptimizationSession:
    """
    Manages the state and lifecycle of a prompt optimization session.
    
    Attributes:
        session_id (str): Unique identifier for the session
        initial_human_input (str): Original prompt from user
        updated_human_input (str): Current version of the prompt
        latest_optimized_prompt (str): Most recent optimized prompt
        config (Config): Session configuration
        created_at (datetime): Session creation timestamp
        logger (SessionLogger): Session-specific logger
    """
    
    def __init__(self, session_id: str, initial_human_input: str, config: Config):
        """
        Initialize a new optimization session.
        
        Args:
            session_id (str): Unique identifier for the session
            initial_human_input (str): Original prompt from user
            config (Config): Configuration for the session
        """
        self.session_id = session_id
        self.initial_human_input = initial_human_input
        self.updated_human_input = initial_human_input
        self.latest_optimized_prompt = None
        self.latest_human_feedback: List[Feedback] = []
        self.config = config
        self.created_at = datetime.now()
        self.logger = SessionLogger(session_id)
        
        # Log session creation
        self.logger.add_entry("SESSION_START", {
            "action": "Session Created",
            "input": initial_human_input,
            "config": {
                "model": config.model_name,
                "task_type": config.task_type
            }
        })
    
    def add_feedback(self, feedback: Feedback) -> None:
        """Add a new feedback to the session."""
        self.latest_human_feedback.append(feedback)
        self.logger.add_entry("COMMENT_ADDED", {
            "feedback_id": feedback.id,
            "text": feedback.text,
            "feedback": feedback.feedback
        })
    
    def update_optimized_prompt(self, new_prompt: str) -> None:
        """Update the latest optimized prompt."""
        self.latest_optimized_prompt = new_prompt
        self.logger.add_entry("PROMPT_UPDATE", {
            "action": "Optimized Prompt Updated",
            "new_prompt": new_prompt
        })
    
    def update_human_input(self, new_input: str) -> None:
        """Update the human input prompt."""
        self.updated_human_input = new_input
        self.logger.add_entry("INPUT_UPDATE", {
            "action": "Human Input Updated",
            "new_input": new_input
        })
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary format."""
        return {
            'session_id': self.session_id,
            'initial_human_input': self.initial_human_input,
            'updated_human_input': self.updated_human_input,
            'latest_optimized_prompt': self.latest_optimized_prompt,
            'latest_human_feedback': [{
                'id': c.id,
                'text': c.text,
                'start_offset': c.start_offset,
                'end_offset': c.end_offset,
                'feedback': c.feedback,
                'created_at': c.created_at.isoformat()
            } for c in self.latest_human_feedback],
            'created_at': self.created_at.isoformat()
        }

class SessionManager:
    """
    Manages multiple optimization sessions.
    """
    
    def __init__(self):
        self.sessions: Dict[str, OptimizationSession] = {}
    
    def create_session(self, session_id: str, initial_input: str, config: Config) -> OptimizationSession:
        """Create and store a new optimization session."""
        session = OptimizationSession(session_id, initial_input, config)
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[OptimizationSession]:
        """Retrieve a session by ID."""
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[Dict]:
        """List all active sessions."""
        return [session.to_dict() for session in self.sessions.values()] 