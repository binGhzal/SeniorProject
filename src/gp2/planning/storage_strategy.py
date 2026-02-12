"""Storage strategy models and local retention/replay helpers."""

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


@dataclass
class LocalStorageBuffer:
    """In-memory placeholder buffer for retention and replay logic."""

    policy: StoragePolicy
    events: list[StorageEvent] = field(default_factory=list)

    def add_event(self, event: StorageEvent):
        """Append event and enforce retention/queue bounds."""
        self.events.append(event)
        self.prune_retention()
        self.prune_capacity()

    def prune_retention(self, now: float | None = None):
        """Drop events older than retention window in hours."""
        effective_now = now if now is not None else time.time()
        cutoff = effective_now - (self.policy.on_device_retention_hours * 3600)
        self.events = [event for event in self.events if event.timestamp >= cutoff]

    def prune_capacity(self):
        """Bound stored events by configured maximum queue length."""
        max_items = max(1, self.policy.on_device_queue_max_items)
        if len(self.events) > max_items:
            self.events = self.events[-max_items:]

    def pending_replay_events(self):
        """Return unsynced events in insertion order for replay."""
        return [event for event in self.events if not event.synced]

    def mark_synced(self, indexes: list[int]):
        """Mark selected event indexes as synced after successful upload."""
        for index in indexes:
            if 0 <= index < len(self.events):
                self.events[index].synced = True


def needs_cloud_policy(policy: StoragePolicy) -> bool:
    """Return whether cloud sync policy configuration is required."""
    return policy.cloud_sync_enabled


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
