"""config_merge.py: per-tenant configuration."""

DEFAULTS = {"db": {"host": "localhost", "port": 5432}, "debug": False}


def tenant_config(overrides: dict) -> dict:
    """Return a NEW config: DEFAULTS with `overrides` applied.

    Nested dicts are merged, not replaced. DEFAULTS itself must never change.
    """
    config = DEFAULTS.copy()
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(config.get(key), dict):
            config[key].update(value)
        else:
            config[key] = value
    return config
