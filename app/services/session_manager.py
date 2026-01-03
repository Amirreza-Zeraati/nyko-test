"""Session management service for tracking user state across requests."""

import json
from typing import Optional
from datetime import datetime, timedelta
import asyncio

from app.models.user_models import SessionData

class SessionManager:
    """
    Manages user sessions with in-memory storage.
    
    In production, this should be replaced with Redis or similar
    distributed cache for scalability and persistence.
    """
    
    def __init__(self, timeout_seconds: int = 3600):
        self._sessions = {}
        self._timeout = timeout_seconds
        self._lock = asyncio.Lock()
    
    async def initialize(self):
        """Initialize session manager."""
        # Start cleanup task
        asyncio.create_task(self._cleanup_expired_sessions())
    
    async def cleanup(self):
        """Cleanup on shutdown."""
        self._sessions.clear()
    
    async def save_session(self, session_id: str, session_data: SessionData):
        """Save session data."""
        async with self._lock:
            session_data.last_activity = datetime.utcnow()
            self._sessions[session_id] = session_data
    
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """Retrieve session data."""
        async with self._lock:
            session = self._sessions.get(session_id)
            
            if session:
                # Check if expired
                age = datetime.utcnow() - session.last_activity
                if age.total_seconds() > self._timeout:
                    del self._sessions[session_id]
                    return None
                
                # Update last activity
                session.last_activity = datetime.utcnow()
            
            return session
    
    async def delete_session(self, session_id: str):
        """Delete a session."""
        async with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
    
    async def _cleanup_expired_sessions(self):
        """Periodically clean up expired sessions."""
        while True:
            await asyncio.sleep(300)  # Run every 5 minutes
            
            async with self._lock:
                now = datetime.utcnow()
                expired = [
                    sid for sid, session in self._sessions.items()
                    if (now - session.last_activity).total_seconds() > self._timeout
                ]
                
                for sid in expired:
                    del self._sessions[sid]
