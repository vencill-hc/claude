---
name: metroline-dev
description: Development skill for the Metroline project - a git-backed pipeline orchestration system using transit metaphors (Lines=pipelines, Stations=steps, Trains=runs, Agents=workers, Dispatches=alerts). Use when implementing features, fixing bugs, or extending the Metroline codebase. Covers Python backend (FastAPI + Typer CLI + Pydantic models + git-backed YAML state), React frontend (Vite + TypeScript + Tailwind + Solarized tokens), and the engine subsystem (scheduler, executor, handlers, event bus, failure engineer). Also use when designing new Metroline pipelines or self-hosting Metroline's own development workflows.
---

# Metroline Development

Build and extend the Metroline pipeline orchestration system.

## Architecture Overview

```
metroline/
  src/metroline/
    models/          Pydantic domain models (MetroModel base, Line, Station, Train, Agent, Dispatch)
    state/           GitStateEngine - YAML files in state/ with atomic git commits
    api/             FastAPI on port 8420 - /api/{lines,trains,agents,stations,dispatches,system}/
    api/routes/      Route modules per resource
    api/websocket.py WebSocket for real-time events
    cli/             Typer CLI (`metro` command) with subcommands per entity
    engine/          Core runtime: daemon, scheduler, runner, executor, handlers, event bus
  web/
    src/types/       api.ts (backend-aligned), index.ts (frontend display), mappers.ts (bridge)
    src/hooks/       React Query hooks (queries.ts, mutations.ts, queryKeys.ts, useWebSocket.ts)
    src/lib/         api.ts (fetch client), ws.ts (WebSocket client)
    src/pages/       MetroMap, WorkQueue, AgentDashboard, HistoryTimeline
    src/components/  transit/ (domain components), layout/ (NavBar, etc.)
```

## Domain Model

| Transit Metaphor | Code Entity | Purpose |
|-----------------|-------------|---------|
| Line | `Line` | Pipeline definition with ordered station IDs, color, merge strategy |
| Station | `Station` | Pipeline step with handler (shell or skill), retry policy, order |
| Train | `Train` | Pipeline run with status lifecycle, history events, cargo dict |
| Agent | `Agent` | Worker process with worktree, capabilities, heartbeat |
| Dispatch | `Dispatch` | Human-attention alert (failure, queue, gate) with available actions |

### Status Lifecycles

**Train:** queued -> boarding -> in_transit -> at_station -> completed/failed/held/derailed
**Agent:** idle -> assigned -> running -> idle (or error/stopped)
**Dispatch:** pending -> acknowledged -> resolved/expired
**Line:** active/paused/stopped/archived

### Key Relationships

- Line.stations: list[str] (Station IDs in order)
- Station.line_id -> Line
- Train.line_id -> Line
- Train.current_station_id -> Station
- Agent.current_train_id -> Train
- Dispatch.train_id -> Train, Dispatch.line_id -> Line, Dispatch.station_id -> Station

## Engine Execution Flow

1. **MetroDaemon** starts Scheduler + FailureEngineer + AgentRunner
2. **Scheduler** polls for queued trains, matches to idle agents by line_ids/capabilities
3. **AgentRunner** creates git worktrees, assigns trains, manages agent lifecycle
4. **PipelineExecutor** walks ordered stations: arrive -> handle -> commit -> depart
5. **StationHandler** (shell) or **SkillHandler** (claude --print) executes station work
6. **EventBus** emits events to subscribers (dispatcher, WebSocket, etc.)
7. **DispatcherMonitor** creates Dispatch records for failures, gates, queue issues
8. **FailureEngineer** auto-creates triage trains for failed trains

## Adding a New Feature

### New API Resource

1. Create Pydantic model in `src/metroline/models/`
2. Export from `models/__init__.py`
3. Register entity type in `state/engine.py` (TYPE_DIRS dict)
4. Create route module in `api/routes/`
5. Register router in `api/app.py`
6. Add CLI commands in `cli/commands/`
7. Register CLI app in `cli/app.py`
8. Add TypeScript types in `web/src/types/api.ts`
9. Add mapper functions in `web/src/types/mappers.ts` if needed
10. Add React Query hooks in `web/src/hooks/`
11. Update pages to consume new data

### New Station Handler Type

1. Create handler class in `engine/` extending StationHandler interface
2. Add HandlerType enum value to `models/station.py`
3. Register in `handler.py` create_handler() factory
4. Handler must return HandlerResult(success, exit_code, stdout, stderr, duration_seconds)

### New Event Channel

1. Define events in emitting code using `bus.emit(channel, event_type, data)`
2. Subscribe in consuming code with `bus.subscribe(channel, callback)`
3. Add WebSocket forwarding in `api/websocket.py`
4. Add frontend handling in `web/src/hooks/useWebSocket.ts`

## Type Alignment Rules

Python Pydantic models serialize to JSON with snake_case keys. TypeScript interfaces MUST mirror this exactly:

- Python `field_name: str` = TypeScript `field_name: string`
- Python `field: X | None = None` = TypeScript `field: X | null` or `field?: X | null`
- Python `datetime` = TypeScript `string` (ISO format from JSON serialization)
- Python `list[X]` = TypeScript `X[]`
- Python `dict` = TypeScript `Record<string, unknown>`
- Python `StrEnum` values = TypeScript string literal union

Always verify with `web/npm run build` -- Vite dev mode is lenient but production build catches strict type errors.

## Self-Referential Development

Metroline can orchestrate its own development. A session's workflow maps to:

- **Line**: The overall task (e.g., "frontend-implementation-verification")
- **Stations**: Steps in order (file-check, type-alignment, endpoint-test, prod-build, commit)
- **Train**: One execution of that workflow
- **Agent**: Claude Code session or subagent doing the work
- **Dispatch**: Bugs or blockers found that need human/AI attention

When designing new Metroline features, consider: "Could this feature's own development be a Line in Metroline?"
