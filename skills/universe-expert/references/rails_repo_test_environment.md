# Running tests in data-universe-rails (agent-replicable steps)

The Rails repo (`~/Documents/git/data-universe-rails`) needs its full docker stack up before **any** `bin/rails test` run — `rails/test_help`'s `maintain_test_schema` touches both Postgres *and* RisingWave, so a missing service blocks even pure-Postgres model tests. These steps were verified working on 2026-08-20.

## Every shell command needs two PATH fixes

```sh
export PATH="$HOME/.asdf/shims:/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

- `$HOME/.asdf/shims` — non-login shells otherwise pick up macOS system Ruby 2.6 and `bin/rails` dies with `Could not find 'bundler'`.
- Docker's `Resources/bin` — `docker` is not on PATH, and `docker compose` also needs `docker-credential-desktop` from that same dir (without it: `error getting credentials`).

## Bring-up sequence (each step's failure mode listed)

1. **Docker daemon**: `docker info --format ok` — if it fails, `open -a Docker` and poll `docker info` until ok (~20s).
2. **Loopback alias**: `ifconfig lo0 | grep 127.0.0.2` — the alias is manual and does NOT survive reboot. If missing, the *user* must run `sudo ifconfig lo0 alias 127.0.0.2 up` (needs password; agents can't sudo). Compose fails with `bind: can't assign requested address` on any 127.0.0.2 port without it.
3. **Services** (from the repo root): `docker compose up -d risingwave-standalone redis pubsub`
   - This is the minimal set: `risingwave-standalone` pulls in `postgres`, `opensearch`, `postgres-0` (RW meta), and `minio-0` via `depends_on`. Deliberately skips grafana/prometheus/opensearch-dashboards/message_queue — dev niceties that eat disk (per-user request: keep docker storage lean; don't `docker compose up -d` the whole stack).
   - Wait for health: `docker inspect -f '{{.State.Health.Status}}' data-universe-rails-risingwave-standalone` until `healthy` (~10s after start).
4. **Port-theft check** (only if postgres starts but Rails still can't connect): the data-universe-pipelines repo's compose postgres binds wildcard `5432:5432` and steals `127.0.0.2:5432`. `lsof -nP -iTCP:5432 -sTCP:LISTEN` should show `com.docke` (docker proxy), not a bare native `postgres` only. Fix: stop the pipelines postgres container, force-recreate this repo's.
5. **Test DBs** (first run on a fresh volume): `RAILS_ENV=test bin/rails db:prepare` — creates `data_universe_test` + `risingwave_test` and loads both schemas, including RisingWave streaming jobs. Symptom when needed: `ActiveRecord::NoDatabaseError: Database not found: data_universe_test`.
   - If RisingWave errors with license `ExpiredSignature`: `ALTER SYSTEM SET license_key = '<RW_LICENSE_KEY from .env>'` via `psql "postgres://root@127.0.0.2:4566/dev?sslmode=disable"` (sslmode=disable is required or the connection dies during SSL negotiation).

## Then run tests / lint normally

```sh
bin/rails test packs/<pack>/test/path/to/file_test.rb   # specific file (`:42` suffix for one test)
bin/rubocop packs/<pack>
bin/packwerk check
```

## Cleanup (user cares about docker disk usage)

When done for the session: `docker compose stop` (keeps volumes/DBs for next time, frees RAM — RisingWave reserves 28G). Do **not** `docker compose down -v` unless asked: it deletes the postgres/opensearch volumes and forces a full `db:prepare` + fixture rebuild next time. If disk pressure is the complaint, `docker system df` then `docker image prune` — never prune volumes unprompted.
