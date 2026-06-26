# Metasploit modules

A loadpath tree of Ruby Metasploit modules for the PoCs that fit the module shape. The path under
`modules/` becomes the module fullname, e.g.:

```
modules/exploits/multi/http/craftcms_transform_rce.rb  ->  exploit/multi/http/craftcms_transform_rce
```

## Use them two ways

**A) Interactive msfconsole** — load this tree directly:
```bash
msfconsole -q -x 'loadpath ~/projects/p0cs/modules; use exploit/multi/http/craftcms_transform_rce; options'
```

**B) Via msfrpcd + the Metasploit MCP** — msfrpcd only auto-loads modules under `~/.msf4/modules`,
so symlink them in once:
```bash
./run --install-modules        # symlinks modules/**/*.rb into ~/.msf4/modules (mirrors the tree)
# restart msfrpcd, then from Claude:  mcp__metasploit__run_exploit("exploit/multi/http/craftcms_transform_rce", {...})
```

`./run --as-msf <slug>` prints the exact recipe for any PoC whose `metadata.yaml` sets `msf_module`.

New module? Copy `templates/module.rb.tmpl`, drop it at the right path under `modules/`, set
`msf_module:` in the PoC's `metadata.yaml`, and re-run `./run --install-modules`.
