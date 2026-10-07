# Somolier Architecture

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
     Decider     external configured gates and dependency states
       / \
    SPIT SWALLOW

## Deterministic service law

Somolier is a one-in / one-out deterministic transducer.

For fixed input bytes, fixed configuration, and fixed reported dependency
states, the output is fixed:

    same input + same config + same dependency state = same output

The algorithm does not adapt itself to ambient context. Variability belongs in
explicit configuration data and explicit port-state inputs.

## Responsibility split

Somolier owns representation normalization and packet formation. It does not
decide truth or embed downstream business policy.

The Decider is an external port. An unregistered Decider always returns SPIT.
A registered Decider returns SWALLOW only when all required ports are READY
and all required gates pass.

## Fail-closed connectivity

Configured dependencies report READY, DISCONNECTED, or FAILED. Missing status
for a required dependency is treated as DISCONNECTED. Every non-READY state
produces SPIT.

## Packet backend

Somolier uses a plugin interface for packet backends. B32K is bundled and
configured by default in v0.1.

    surface is presentation
    packet backend owns canonical packet representation
    Decider owns admission
