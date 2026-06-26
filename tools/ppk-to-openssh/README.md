# ppk-to-openssh

**Type:** helper (converter) · **No CVE** — a utility for when `puttygen` isn't on the box.

Converts an **unencrypted** PuTTY private key (`.ppk`, v2 or v3, RSA) into an OpenSSH private key,
without `puttygen`. Parses Public-Lines (e, n) and Private-Lines (d, p, q), derives the CRT params,
and serialises an OpenSSH key via `cryptography`. Encrypted PPKs are not handled.

## Usage
```bash
./run ppk-to-openssh PPK=key.ppk > id_rsa && chmod 600 id_rsa
```

## Safety
Read-only on input; writes the OpenSSH key to stdout. No network, no target interaction.

## References
- PuTTY .ppk format; OpenSSH private-key format.
