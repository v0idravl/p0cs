# p0cs

Proof-of-concept exploits and offensive **helpers**, each runnable the same way through one tiny
runner. CVE PoCs and plain utilities (key converters, decoders, protocol clients) live side by side;
the ones that fit the Metasploit module shape can be loaded as native `msf` modules.

> **Authorized use only.** Owned labs, CTF/graded boxes (HTB / PG / THM / pwn.college), and explicitly
> authorized assessments. Every entry takes its target as an option — none hardcode one. Read the
> source before you run anything against a host.

## Layout

```
run                     one uniform entrypoint for everything (see below)
pocs/<slug>/            exploits + auxiliary checks   — poc.py + metadata.yaml + README.md
tools/<slug>/           helpers (converters, decoders, clients) — same shape
modules/                Metasploit loadpath tree (Ruby modules); see modules/README.md
templates/              scaffolds: poc.py, metadata.yaml, module.rb, README.md
```

Each entry carries a `metadata.yaml` (`id`, `cve`, `type`, `lang`, `entrypoint`, `options`,
`required`, `argv_template`, `msf_module`) so the runner can drive heterogeneous scripts — positional
args, argparse flags, python/ruby/bash — through one interface.

## Use

```bash
./run --list                                   # every PoC and helper
./run --show cve-2025-32432                     # one entry's options + usage
./run cve-2025-32432 RHOST=target.example.com   # run it (options as KEY=VALUE)
./run ppk-to-openssh PPK=key.ppk > id_rsa       # a helper, same interface
./run --new my-poc                              # scaffold a new PoC (add `tool` for a helper)
./run --as-msf cve-2025-32432                   # load it as a Metasploit module
./run --install-modules                         # expose modules/ to msfrpcd + the Metasploit MCP
```

## Adding an entry

1. `./run --new <slug>` (append `tool` for a helper) — scaffolds the dir from `templates/`.
2. Write the PoC, fill `metadata.yaml` (set `required` + `argv_template` to match its CLI).
3. If it fits a Metasploit module, drop a Ruby module under `modules/` (from `templates/module.rb.tmpl`),
   point `msf_module:` at it, and `./run --install-modules`.
4. `./run --list` to confirm it registers.

## Current entries

| Slug | Type | CVE | What |
|---|---|---|---|
| cve-2025-32432 | exploit | CVE-2025-32432 | Craft CMS image-transform pre-auth RCE (check + RCE + msf module) |
| cve-2023-46604 | exploit | CVE-2023-46604 | Apache ActiveMQ OpenWire RCE |
| cve-2023-32784 | auxiliary | CVE-2023-32784 | KeePass 2.x master password from a memory dump (offline) |
| ppk-to-openssh | helper | — | PuTTY .ppk -> OpenSSH private key, no puttygen |
