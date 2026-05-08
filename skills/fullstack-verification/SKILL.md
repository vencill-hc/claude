---
name: fullstack-verification
description: Verify a fullstack implementation (Python backend + React/TypeScript frontend) by checking file existence, type correctness, API endpoint health, and production build. Use when finishing a feature that spans both backend and frontend, when verifying a plan was implemented correctly, when doing pre-commit QA on a fullstack change, or when user says "verify", "check everything", "does it compile", or "test the endpoints".
---

# Fullstack Verification

Systematic verification of fullstack Python+React implementations. Runs four verification phases in order, halting at the first failure to fix before proceeding.

## Phase 1: File Existence Check

Verify all expected files exist. Use Glob to confirm each file path.

```
Expected files from implementation plan or git diff:
- Backend: src/**/*.py (models, routes, engine modules)
- Frontend: web/src/**/*.{ts,tsx} (components, hooks, lib, types, pages)
- Config: any new config files (.yaml, .env, etc.)
```

For each missing file, report it immediately. Do NOT proceed to Phase 2 until all files exist.

## Phase 2: Type Alignment

This is the most error-prone phase. Backend Python models and frontend TypeScript types MUST match.

### Check Python -> TypeScript field alignment

For each Pydantic model that has a corresponding TypeScript interface:

1. Read the Python model (field names, types, defaults)
2. Read the TypeScript interface (field names, types, optionality)
3. Compare field-by-field:
   - Field name must match exactly (Python `snake_case` = TypeScript `snake_case` for JSON serialization)
   - Field type must be compatible (`str` = `string`, `int` = `number`, `list[str]` = `string[]`, `dict` = `Record<string, unknown>`, `datetime` = `string` (ISO), `X | None` = `X | null`)
   - Optional fields in Python (`| None`, `= None`) must be optional in TypeScript (`?:` or `| null`)

### Common type mismatches to check

| Python | Correct TS | Common mistake |
|--------|-----------|----------------|
| `event_type: str` | `event_type: string` | Using `action: string` |
| `status: SomeEnum` | `status: 'val1' \| 'val2'` | Missing enum values or using wrong union |
| `list[TrainEvent]` | `TrainEvent[]` | Mismatched nested type fields |
| `created_at: datetime` | `created_at: string` | Using `Date` instead of `string` |

### Check mapper functions

If frontend has mapper functions (e.g., `mapTrainStatus`, `mapAgentStatus`), verify:
- Every backend enum value has a case in the mapper switch
- Default/fallback case is sensible
- Mapped values match frontend display type union

## Phase 3: API Endpoint Health

Start both servers if not already running:

```bash
# Backend (FastAPI)
cd /path/to/repo && .venv/bin/python -m uvicorn metroline.api.app:app --port 8420 &

# Frontend (Vite)
cd /path/to/repo/web && npm run dev -- --port 3001 &
```

Test every API endpoint by group:

```bash
# List endpoints pattern - test each resource
curl -s http://localhost:8420/api/{resource}/ | python3 -m json.tool | head -5

# Resources to test: lines, trains, agents, stations, dispatches
# System endpoints: /api/system/status, /api/system/config, /api/system/map
```

For each endpoint, verify:
- Returns 200 status
- Response is valid JSON
- Response shape matches TypeScript type

## Phase 4: Production Build

This catches type errors the dev server misses (Vite is lenient in dev mode).

```bash
cd /path/to/repo/web && npm run build 2>&1
```

If build fails:
1. Read the error message carefully
2. Most common: missing imports, unused imports, type errors
3. Fix the error
4. Re-run build
5. Repeat until clean

### Common production build failures

- **Missing type export**: A type is used in a file but not exported from its module
- **Unused import**: An import was added by a linter but the type is not used
- **Strict null checks**: A value might be `null` but is used without a guard
- **Enum exhaustiveness**: Switch statement does not cover all enum values

## Output

After all four phases pass, produce a summary:

```
Verification Complete
- Files: X/X present
- Type alignment: X models checked, Y fields verified
- API endpoints: X/X responding with correct shapes
- Production build: clean (0 errors, N warnings)
- Issues found and fixed: [list any]
```
