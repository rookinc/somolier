# Decider Port

The Decider consumes a TasteReceipt plus explicit configuration inputs and
produces exactly one disposition receipt.

    TasteReceipt + authority + gate results + port results -> SPIT | SWALLOW

## Fail-closed law

    unregistered authority -> SPIT
    missing required port  -> SPIT
    disconnected port      -> SPIT
    failed port            -> SPIT
    missing gate           -> SPIT
    failed gate            -> SPIT
    all ports READY
      + all gates PASS      -> SWALLOW

Registration does not make a Decider permissive. It only supplies a lawful
authority context in which SWALLOW can be earned.

## Connectivity state

Required dependencies are explicit configuration. Each required port is in one
of three states:

    READY
    DISCONNECTED
    FAILED

Anything except READY is fail-closed. Missing required port status is treated
as DISCONNECTED.

This is dependency-state awareness, not inference: the caller reports the
state of configured ports and Somolier deterministically receipts it.
