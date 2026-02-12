"""Storage strategy models and local retention/replay helpers."""

import json
import sqlite3
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StoragePolicy:
    """Storage and synchronization policy for runtime and app data."""

    on_device_retention_hours: int = 24
    on_device_queue_max_items: int = 500
    app_storage_enabled: bool = True
    cloud_sync_enabled: bool = False
    encryption_required: bool = True
    sync_conflict_policy: str = "last-write-wins"


@dataclass
class StorageEvent:
    """Serializable runtime event record for local buffering."""

    event_type: str
    payload: dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    synced: bool = False


@dataclass(frozen=True)
class TripSummary:
    """Application-side trip summary schema (v1)."""

    trip_id: str
    started_at: float
    ended_at: float
    distance_km: float
    event_count: int


@dataclass(frozen=True)
class DiagnosticRecord:
    """Application-side diagnostic snapshot schema (v1)."""

    recorded_at: float
    sensor_health: dict[str, Any]
    runtime_health: dict[str, Any]


@dataclass(frozen=True)
class EventClipMetadata:
    """Event-clip metadata schema for ±10-20 second buffering windows."""

    event_id: str
    trigger_ts: float
    pre_event_s: int = 10
    post_event_s: int = 20
    storage_uri: str = ""
    redacted: bool = False


class LocalStorageBuffer:
    """SQLite-backed local buffer for retention, replay, and sync bookkeeping."""

    def __init__(self, policy: StoragePolicy, db_path: str = ":memory:"):
        self.policy = policy
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                timestamp REAL NOT NULL,
                synced INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        self._conn.commit()

    @property
    def events(self) -> list[StorageEvent]:
        """Return all events in insertion order for compatibility with tests."""
        rows = self._conn.execute(
            "SELECT event_type, payload, timestamp, synced FROM events ORDER BY id ASC"
        ).fetchall()
        return [
            StorageEvent(
                event_type=str(row["event_type"]),
                payload=json.loads(str(row["payload"])),
                timestamp=float(row["timestamp"]),
                synced=bool(row["synced"]),
            )
            for row in rows
        ]

    def add_event(self, event: StorageEvent):
        """Append event and enforce retention/queue bounds."""
        self._conn.execute(
            "INSERT INTO events(event_type, payload, timestamp, synced) VALUES (?, ?, ?, ?)",
            (
                event.event_type,
                json.dumps(event.payload),
                float(event.timestamp),
                int(event.synced),
            ),
        )
        self._conn.commit()
        self.prune_retention()
        self.prune_capacity()

    def prune_retention(self, now: float | None = None):
        """Drop events older than retention window in hours."""
        effective_now = now if now is not None else time.time()
        cutoff = effective_now - (self.policy.on_device_retention_hours * 3600)
        self._conn.execute("DELETE FROM events WHERE timestamp < ?", (cutoff,))
        self._conn.commit()

    def prune_capacity(self):
        """Bound stored events by configured maximum queue length."""
        max_items = max(1, self.policy.on_device_queue_max_items)
        count_row = self._conn.execute("SELECT COUNT(*) AS total FROM events").fetchone()
        total = int(count_row["total"] if count_row else 0)
        overflow = total - max_items
        if overflow <= 0:
            return

        self._conn.execute(
            "DELETE FROM events WHERE id IN (SELECT id FROM events ORDER BY id ASC LIMIT ?)",
            (overflow,),
        )
        self._conn.commit()

    def pending_replay_events(self):
        """Return unsynced events in insertion order for replay."""
        rows = self._conn.execute(
            "SELECT event_type, payload, timestamp, synced "
            "FROM events WHERE synced = 0 ORDER BY id ASC"
        ).fetchall()
        return [
            StorageEvent(
                event_type=str(row["event_type"]),
                payload=json.loads(str(row["payload"])),
                timestamp=float(row["timestamp"]),
                synced=bool(row["synced"]),
            )
            for row in rows
        ]

    def mark_synced(self, indexes: list[int]):
        """Mark selected event indexes as synced after successful upload."""
        id_rows = self._conn.execute("SELECT id FROM events ORDER BY id ASC").fetchall()
        ordered_ids = [int(row["id"]) for row in id_rows]
        for index in indexes:
            if 0 <= index < len(ordered_ids):
                self._conn.execute(
                    "UPDATE events SET synced = 1 WHERE id = ?", (ordered_ids[index],)
                )
        self._conn.commit()


def needs_cloud_policy(policy: StoragePolicy) -> bool:
    """Return whether cloud sync policy configuration is required."""
    return policy.cloud_sync_enabled


def app_schema_v1() -> dict[str, str]:
    """Return app-side schema class mapping for storage integration boundaries."""

    return {
        "trip_summary": "TripSummary",
        "diagnostic_record": "DiagnosticRecord",
        "event_record": "StorageEvent",
        "event_clip_metadata": "EventClipMetadata",
    }


def dsar_supported_actions() -> list[str]:
    """Return supported DSAR workflow actions for user-requested data operations."""

    return [
        "access-export",
        "delete",
        "correction",
    ]


def resolve_sync_conflict(local_event: StorageEvent, remote_event: StorageEvent, policy: str):
    """Resolve sync conflicts with a deterministic policy strategy."""
    normalized = policy.strip().lower()
    if normalized == "local-wins":
        return local_event
    if normalized == "remote-wins":
        return remote_event
    if normalized == "last-write-wins":
        return local_event if local_event.timestamp >= remote_event.timestamp else remote_event
    raise ValueError(f"Unsupported sync conflict policy: {policy}")
