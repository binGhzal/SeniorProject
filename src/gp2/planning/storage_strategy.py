from dataclasses import dataclass


@dataclass
class StoragePolicy:
    on_device_retention_hours: int = 24
    app_storage_enabled: bool = True
    cloud_sync_enabled: bool = False
    encryption_required: bool = True


def needs_cloud_policy(policy: StoragePolicy) -> bool:
    return policy.cloud_sync_enabled
