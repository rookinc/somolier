from hashlib import sha256

import pytest

from somolier import (
    B32KID,
    FixedMemoryStoragePort,
    Somolier,
    quarantine,
)


def test_b32kid_requires_explicit_prefix():
    with pytest.raises(ValueError):
        B32KID("not-a-b32kid")


def test_host_supplies_b32kid_and_quarantine_location():
    payload = b"wine"
    host = FixedMemoryStoragePort(
        b32kid=B32KID("b32kid:test-event-0001"),
        location="memory://host-quarantine/test-event-0001",
    )

    receipt = quarantine(payload, host, surface_type="text/plain")

    assert str(receipt.b32kid) == "b32kid:test-event-0001"
    assert receipt.location == "memory://host-quarantine/test-event-0001"
    assert receipt.source_digest == sha256(payload).hexdigest()
    assert host.read(receipt.allocation, "original.bin") == payload
    assert host.read(receipt.allocation, "sealed.bin") == payload


def test_quarantine_b32kid_flows_into_b32k_packet():
    payload = b"wine"
    packet_id = B32KID("b32kid:test-event-flow")
    host = FixedMemoryStoragePort(
        b32kid=packet_id,
        location="memory://host-quarantine/test-event-flow",
    )

    quarantine_receipt = quarantine(payload, host)
    taste_receipt = Somolier().taste_quarantine(quarantine_receipt, host)

    assert taste_receipt.packet.b32kid == packet_id
    assert taste_receipt.history["b32kid"] == str(packet_id)
    assert Somolier().render(taste_receipt) == payload


def test_same_bytes_can_have_distinct_host_event_ids():
    payload = b"same bytes"
    left = FixedMemoryStoragePort(
        b32kid=B32KID("b32kid:event-left"),
        location="memory://q/left",
    )
    right = FixedMemoryStoragePort(
        b32kid=B32KID("b32kid:event-right"),
        location="memory://q/right",
    )

    left_receipt = quarantine(payload, left)
    right_receipt = quarantine(payload, right)

    assert left_receipt.source_digest == right_receipt.source_digest
    assert left_receipt.b32kid != right_receipt.b32kid


def test_fixed_host_allocation_is_deterministic_for_same_event():
    payload = b"deterministic"
    host = FixedMemoryStoragePort(
        b32kid=B32KID("b32kid:deterministic-1"),
        location="memory://q/deterministic-1",
    )

    first = quarantine(payload, host)
    second = quarantine(payload, host)

    assert first == second
