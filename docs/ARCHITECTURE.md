# Somolier Architecture

```text
incoming object
    |
   WIFF      cheap wrapper sniff
    |
 quarantine
    |
  SWIRL      sealing boundary
    |
  TASTE      Somolier normalization / packetization
    |
 Decider     external authority and policy gates
   / \
SPIT SWALLOW
```

## Responsibility split

Somolier owns representation normalization and packet formation. It does not decide truth or admission.

The Decider is external. An unregistered Decider always returns `SPIT`. A registered Decider returns `SWALLOW` only when all required gates pass.

## Packet backend

Somolier uses a plugin interface for packet backends. B32K is bundled and configured by default in v0.1.

```text
surface is presentation
packet backend owns canonical packet representation
Decider owns admission
```
