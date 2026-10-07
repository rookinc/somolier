# DECIDE Policy Port

DECIDE is the canonical Somolier admission verb and stage.

A configured decision policy consumes TASTE evidence plus explicit authority, gate, and dependency inputs and returns exactly one disposition:

    SPIT | SWALLOW

## Fail-closed law

    unregistered authority -> SPIT
    missing required port  -> SPIT
    DISCONNECTED port      -> SPIT
    FAILED port            -> SPIT
    missing gate           -> SPIT
    failed gate            -> SPIT
    all required evidence  -> SWALLOW

No missing value is interpreted as permission.

## B32K boundary

DECIDE does not redefine B32K validity. TASTE supplies B32K/profile validation evidence. DECIDE applies admission policy to that evidence.

SWALLOW authorizes the next stage to build/compute the admitted representation and request persistence. DECIDE itself does not STREAM.
