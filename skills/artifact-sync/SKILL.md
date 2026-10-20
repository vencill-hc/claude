---
name: artifact-sync
description: Export a published Claude artifact (page, published files, db collections, capabilities) into its workpod thread directory, and import such a directory back into the current Claude account as a fresh artifact with its db seeded. Use when asked to "save this artifact to the thread", "export the artifact", "republish this on my gdulabs/huntclub account", "import the artifact from the thread", "move this artifact to the other account", or when a thread's artifact/ directory holds a manifest.json and the user wants it live here. Not for building or editing artifact pages (artifact-design) or for reading comments.
---

# Artifact sync

Two Claude accounts share one workpod repo. An artifact's db and URL belong to the account that published it, so the
thread directory is the handoff: page source, published files, a per-collection dump of the db, and a manifest.
Local files are the source of truth (workpod CLAUDE.md); the artifact on claude.ai is a deployment of them.

Layout, one directory per artifact under the owning thread:

```
projects/<project>/threads/<slug>/artifact/<name>/
  manifest.json            page, capabilities, icon, files, collections, urls per account, updated_at
  <page>.html              the page as the Artifact tool publishes it
  <published files>        at their published paths (data.js, styles.css, …)
  seed/<collection>/<doc_id>.json   one document body per file
```

`scripts/artifact_sync.py` (stdlib) does the file work; the Artifact and ArtifactData tools do the network work.
Load ArtifactData with `ToolSearch select:ArtifactData` when it is not already in the tool list.

## Export: artifact on claude.ai → thread directory

1. Resolve the artifact URL (the user's link, `Artifact list`, or the thread's notes.md) and the thread directory
   (`bin/wp-active` resolves the active thread). Pick `<name>` from the page title, kebab-case.
2. Page: if the HTML already lives in the thread (it should, per CLAUDE.md), use it. Otherwise
   `Artifact read url=<url>` and save the returned HTML as `<name>/<page>.html`.
3. Published files: `Artifact list scope=files url=<url>`; for each path other than the page,
   `Artifact read url=<url> path=<p> out_dir=<name>/` so it lands at its published path.
4. Collections: `python3 -I scripts/artifact_sync.py collections <name>/<page>.html` lists what the page code reads.
   For each: `ArtifactData list url=<url> collection=<c> query.limit=1000 out_dir=<name>/seed`
   (page with `query.cursor` past 1000). Per-viewer data under `data/users/` is private and does not export; say so.
5. `python3 -I scripts/artifact_sync.py normalize <name>` strips the export wrapper (id, version, updatedAt) so each
   file is a plain document body.
6. Capabilities and icon come from the publish result or the conversation; when unknown, read them off the page
   (`claude.use("db")`, `claude.use("user")`, …) and say they were inferred.
   `python3 -I scripts/artifact_sync.py manifest <name> --page <page>.html --url <url> --account <huntclub|gdulabs> --capabilities '{"db":{},"user":{}}' --icon <icon> [--files data.js …]`
7. Commit scoped (`git add <name>` then commit `log: <slug> — artifact <name> exported from <account>`), and add one
   line to the thread's notes.md with the link and the data shape if it is not there yet.

## Import: thread directory → artifact on this account

1. Read `manifest.json`. If `urls` already has an entry for this account, the artifact exists here: publish to that
   `url` (read it first, as the Artifact tool requires) instead of creating a second one.
2. Publish: `Artifact publish file_path=<name>/<page>.html icon=<icon> capabilities=<manifest.capabilities>`
   with `files` mapping each manifest file to its path. Capabilities must be passed explicitly: a new artifact has
   none, and the page's db calls resolve `null` without them.
3. Seed: `python3 -I scripts/artifact_sync.py writes <name>` prints one JSON array per batch call (50 writes each).
   Pass each array as `writes` to `ArtifactData batch url=<new url>`. Documents are new, so no `if_version`.
   For a re-import into an existing artifact, `list` the collection first and pin each write with its `version`, or
   delete and reseed when the user wants the dump to win.
4. Verify once: `ArtifactData list url=<new url> collection=<c> query.limit=3`.
5. Record: `python3 -I scripts/artifact_sync.py manifest <name> --page <page>.html --url <new url> --account <this account>`,
   append the link to notes.md, commit scoped (`log: <slug> — artifact <name> published on <account>`).
6. Tell the user the new link, that it is private until shared from the page's Share menu, and which collections
   were seeded.

## Which account am I on

The session's config dir says: `~/.claude-huntclub` is huntclub, `~/.claude` (plain) is gdulabs. When unsure, ask
rather than guessing the `--account` label, since it keys the manifest's `urls`.

## Gotchas

- `out_dir` exports write `<out_dir>/<collection>/<id>.json` with a wrapper; always run `normalize` before `writes`,
  and again after any later re-export.
- `ArtifactData batch` entries with `file_path` send the file's top-level object as the document; a wrapped file
  would seed `{"id":…, "data":…}` as the body.
- A page whose state lives in the `artifact` (self-republish) capability has no db: export is the page alone.
- Never commit with `add -A` in the workpod; scope every add to the artifact directory and notes.md.
