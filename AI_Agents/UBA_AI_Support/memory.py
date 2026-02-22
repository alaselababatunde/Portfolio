from typing import List, Dict
import time

class SessionMemory:
    def __init__(self):
        # session_id -> list of messages
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        # session_id -> last update timestamp
        self.last_update: Dict[str, float] = {}

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        self.sessions[session_id].append({"role": role, "content": content})
        self.last_update[session_id] = time.time()
        
        # Limit history to last 10 messages to keep context size manageable
        if len(self.sessions[session_id]) > 10:
            self.sessions[session_id] = self.sessions[session_id][-10:]

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.last_update:
            del self.last_update[session_id]

# Singleton instance
memory_system = SessionMemory()
