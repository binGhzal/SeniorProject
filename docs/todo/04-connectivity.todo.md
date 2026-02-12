# TODO 04: Connectivity

- [x] Add validated runtime connectivity configuration model
- [x] Add bounded offline queue + reconnect backoff placeholders
- [x] Enforce distinct QoS policy for STATUS vs ALERT messages
- [x] Complete Phase 4 software deliverables

- [ ] Select primary transport path (Wi-Fi/BLE/USB)
- [ ] Define topic schema and payload contracts
- [ ] Set telemetry cadence and alert latency targets
- [ ] Implement reconnection and offline replay behavior
- [ ] Add transport security and credential rotation policy

## Implementation plan

- Week 2: select primary transport profile and freeze topic/payload contracts.
- Week 2: implement and test offline replay flush behavior in telemetry client.
- Week 2: add TLS/auth settings + credential rotation procedure in deployment docs.
