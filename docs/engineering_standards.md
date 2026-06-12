# Engineering Standards

These standards define the baseline rules for future FH6 Farm Tool work.

## Naming Conventions

- Use `snake_case` for file names, function names, and variable names.
- Use `PascalCase` for class names.
- Prefer explicit names over vague names.
- Names should describe the responsibility of the code they identify.

## Architecture Rules

- Keep files small and focused. Do not create monolithic files.
- Keep `main.py` minimal. Do not put automation logic in `main.py`.
- Do not put UI logic in core systems.
- Shared runtime systems belong in `core/`.
- Automation modules belong in `automation/`.
- Configuration files belong in `config/`.
- Configuration loading belongs in dedicated configuration-loading modules.
- Logging remains centralized in the project logging module.
- Keep responsibilities separated by module.

## Code Quality Rules

- Prefer readability over cleverness.
- Use small, focused functions.
- Do not hardcode behavior that should come from configuration.
- Do not add speculative architecture.
- Add only the structure needed for the current milestone.
- Keep future behavior easy to review before it is implemented.

## Current Boundaries

- No automation behavior exists yet.
- No UI behavior exists yet.
- No shared runtime systems are implemented yet.
- No profile management is implemented yet.
