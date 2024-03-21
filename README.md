# C4 Sign
funny sign go brrrrrrrr

## Updates

Updates happen either:
- Every 24 hours (shortly after midnight)
- When the script is first launched (after like a reboot)

## Simulator

The simulator is a simple program that simulates the sign. It's not perfect, but it's good enough for testing.

```bash
python3 -m pip install -e '.[simulator]'
python3 -m c4_sign --simulator
```

## Real Sign

[To be written]

```bash
python3 -m pip install -e '.[physical]'
python3 -m c4_sign
```

## KRNL Sign Compatibility

Because of *unforeseen circumstances*, it is possible for code written for the C4 sign to be compatible with the KRNL sign. More information will be provided in the future.
