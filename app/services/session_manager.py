"""Session management service for tracking user state across requests."""

import json
from typing import Optional, Dict
from datetime import datetime, timedelta
import logging

from app.models.user_models import SessionData

logger = logging.getLogger(__name__)

class SessionManager:
    """Singleton session manager to ensure sessions are shared across all routes."""
    
    _instance = None
    _sessions: Dict[str, SessionData] = {}
    _timeout = 3600  # 1 hour timeout
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            logger.info("SessionManager instance created")
        return cls._instance
    
    def save_session(self, session_id: str, session_data: SessionData):
        """Save session data."""
        session_data.last_activity = datetime.utcnow()
        self._sessions[session_id] = session_data
        logger.info(f"Session saved: {session_id}. Total sessions: {len(self._sessions)}")
    
    def get_session(self, session_id: str) -> Optional[SessionData]:
        """Retrieve session data."""
        logger.info(f"Looking for session: {session_id}. Available sessions: {list(self._sessions.keys())}")
        session = self._sessions.get(session_id)
        
        if session:
            # Check if expired
            if session.last_activity:
                age = datetime.utcnow() - session.last_activity
                if age.total_seconds() > self._timeout:
                    logger.warning(f"Session {session_id} expired")
                    del self._sessions[session_id]
                    return None
            
            # Update last activity
            session.last_activity = datetime.utcnow()
            logger.info(f"Session {session_id} found and updated")
        else:
            logger.warning(f"Session {session_id} not found")
        
        return session
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Session {session_id} deleted")
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions. Can be called manually or via a scheduled task."""
        now = datetime.utcnow()
        expired = [
            sid for sid, session in self._sessions.items()
            if session.last_activity and (now - session.last_activity).total_seconds() > self._timeout
        ]
        
        for sid in expired:
            del self._sessions[sid]
            logger.info(f"Expired session removed: {sid}")
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")
        
        return len(expired)

# Create singleton instance
session_manager = SessionManager()
