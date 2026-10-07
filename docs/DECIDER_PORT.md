# Decider Port

The Decider consumes a `TasteReceipt` and produces a disposition receipt.

```text
TasteReceipt + authority + gate results -> SPIT | SWALLOW
```

## Fail-closed law

```text
unregistered authority -> SPIT
missing gate           -> SPIT
failed gate            -> SPIT
all required gates     -> SWALLOW
```

Registration does not make a Decider permissive. It only supplies a lawful authority context in which `SWALLOW` can be earned.
