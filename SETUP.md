# Setup

Bootstrap this Claude Code config on a new machine.

## Prerequisites

- macOS (paths assume `~/Documents/git/`; adjust for Linux/Windows)
- [Claude Code](https://docs.claude.com/en/docs/claude-code) installed (creates `~/.claude/`)
- Node.js (for `activate-profile.js`)
- `git`, `make`
- A separate `vencill-hc/dotfiles` clone if you want the same statusline, prompt, hooks, etc. — see that repo for its own setup

## One-shot bootstrap

```bash
mkdir -p ~/Documents/git && cd ~/Documents/git
git clone https://github.com/vencill-hc/claude.git
cd claude
make install
```

This will:

1. Create `~/.claude/{skills,agents,commands}/` if missing
2. Clone [`garrytan/gstack`](https://github.com/garrytan/gstack) to `~/Documents/git/gstack` (sibling repo — needed for the `gstack` profile)
3. Activate the default profile (`core`)

To use the `claude-profile` alias, add this to your shell rc (or rely on the dotfiles repo to set it):

```bash
alias claude-profile="node ~/Documents/git/claude/activate-profile.js"
```

## How it works

Skills, agents, and commands live in this repo as the source of truth. `activate-profile.js` clears `~/.claude/{skills,agents,commands}/` of symlinks, then symlinks back only the entries listed in the profile(s) you select. Multiple profiles can be active at once and merge.

`profiles/<name>/skills/<skill>` is a symlink pointing back into `skills/<skill>` (or, for the `gstack` profile, into the sibling `~/Documents/git/gstack/gstack/<skill>` repo). To add a skill to a profile:

```bash
cd profiles/pipelines/skills
ln -s ../../../skills/<skill-name> .
```

To create a new profile:

```bash
mkdir -p profiles/<name>/{skills,agents,commands}
# add symlinks as above
```

## Daily commands

```bash
make list                                 # see available profiles
make show                                 # see currently active
make activate PROFILES="core pipelines"   # activate
claude-profile core gstack                # same thing, via alias
```

The active profile list is written to `~/.claude/.active-profiles` and read by the statusline (configured in the dotfiles repo) to render `[core|pipelines]`.

## Caveats

- `~/.claude/skills/`, `~/.claude/agents/`, `~/.claude/commands/` are **managed**. Anything dropped there ad-hoc gets wiped on the next `make activate`. Add new skills to `skills/` in this repo and symlink into a profile instead.
- Plugin-managed skills (anything from `~/.claude/plugins/`, e.g. `superpowers`, `code-simplifier`) and slash commands in `commands/` are NOT profile-managed — they stay always-on regardless of active profile.
- `gstack` is a separate repo (cloned to `~/Documents/git/gstack`). The `gstack` profile symlinks point at `~/Documents/git/gstack/gstack/<skill>/`. If gstack moves or its internal layout changes, those symlinks break.

## Reset

```bash
make clean        # remove all profile-managed symlinks and clear active-profiles state
```
