from hashlib import sha256

import pytest

from somolier import B32KID, FixedMemoryStoragePort, Somolier, quarantine, wiff


def test_b32kid_requires_explicit_prefix():
    with pytest.raises(ValueError):
        B32KID("not-a-b32kid")


def test_wiff_supplies_b32kid_host_supplies_only_location():
    payload = b"wine"
    expected = wiff(payload, surface_type="text/plain")
    host = FixedMemoryStoragePort(
        location="memory://host-quarantine/wine",
    )

    receipt = quarantine(payload, host, surface_type="text/plain")

    assert receipt.b32kid == expected.b32kid
    assert receipt.location == "memory://host-quarantine/wine"
    assert receipt.source_digest == sha256(payload).hexdigest()
    assert host.read(receipt.allocation, "original.bin") == payload
    assert host.read(receipt.allocation, "sealed.bin") == payload


def test_storage_output_verb_is_stream():
    payload = b"stream-me"
    wr = wiff(payload)
    host = FixedMemoryStoragePort(location="memory://q/stream")
    allocation = host.allocate(
        b32kid=wr.b32kid,
        source_digest=sha256(payload).hexdigest(),
        metadata={},
    )

    location = host.stream(allocation, "artifact.bin", payload)

    assert location.endswith("/artifact.bin")
    assert host.read(allocation, "artifact.bin") == payload


def test_quarantine_b32kid_flows_into_b32k_packet():
    payload = b"wine"
    packet_id = wiff(payload).b32kid
    host = FixedMemoryStoragePort(
        location="memory://host-quarantine/wine-flow",
    )

    quarantine_receipt = quarantine(payload, host)
    taste_receipt = Somolier().taste_quarantine(quarantine_receipt, host)

    assert quarantine_receipt.b32kid == packet_id
    assert taste_receipt.packet.b32kid == packet_id
    assert taste_receipt.history["b32kid"] == str(packet_id)
    assert Somolier().render(taste_receipt) == payload


def test_same_bytes_get_same_wiff_b32kid_independent_of_host():
    payload = b"same bytes"
    left = FixedMemoryStoragePort(location="memory://q/left")
    right = FixedMemoryStoragePort(location="memory://q/right")

    left_receipt = quarantine(payload, left)
    right_receipt = quarantine(payload, right)

    assert left_receipt.source_digest == right_receipt.source_digest
    assert left_receipt.b32kid == right_receipt.b32kid
    assert left_receipt.location != right_receipt.location


def test_fixed_host_allocation_is_deterministic_for_same_identity():
    payload = b"deterministic"
    host = FixedMemoryStoragePort(
        location="memory://q/deterministic",
    )

    first = quarantine(payload, host)
    second = quarantine(payload, host)

    assert first == second
