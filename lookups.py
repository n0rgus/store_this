# lookups.py
from __future__ import annotations
from flask import current_app, flash
from db import q_all, q_one

def choices():
    """Return lookup lists for dropdowns with explicit mapping + debug output."""
    M = {
        'owners': ('owners', 'owner_id', 'owner'),
        'locations': ('locations', 'location_id', 'location'),
        'categories': ('categories', 'category_id', 'category'),
        'statuses': ('statuses', 'status_id', 'status'),
    }

    def table_exists(name:str) -> bool:
        row = q_one("SELECT name FROM sqlite_master WHERE type='table' AND lower(name)=lower(?)", (name,))
        return bool(row)

    def list_tables(limit:int=50):
        rows = q_all("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [r['name'] for r in rows][:limit]

    def list_columns(table:str):
        info = q_all(f"PRAGMA table_info({table})")
        return [r['name'] for r in info]

    def fetch(key: str, id_alias: str, label_alias: str):
        app = current_app
        table, id_col, label_col = M[key]
        if not table_exists(table):
            existing = list_tables()
            msg = f"Lookup '{key}': table '{table}' not found. Existing tables: {', '.join(existing) or '(none)'}"
            flash(msg, 'warning'); app.logger.warning(msg)
            return []
        cols = list_columns(table)
        missing = [c for c in (id_col, label_col) if c not in cols]
        if missing:
            msg = f"Lookup '{key}': missing column(s) {missing} on table '{table}'. Available: {', '.join(cols) or '(none)'}"
            flash(msg, 'warning'); app.logger.warning(msg)
            return []
        cnt_row = q_one(f"SELECT COUNT(*) AS c FROM {table}")
        cnt = cnt_row['c'] if cnt_row else None
        app.logger.warning("Lookup '%s': %s rows in %s", key, cnt, table)
        rows = q_all(f"SELECT {id_col} AS {id_alias}, {label_col} AS {label_alias} FROM {table} ORDER BY {label_col}")
        if rows:
            try:
                app.logger.warning("Lookup '%s': first row example -> %s", key, dict(rows[0]))
            except Exception:
                pass
        else:
            flash(f"Lookup '{key}': query returned 0 rows from {table}.", 'warning')
        return rows

    owners = fetch('owners', 'owner_id', 'owner')
    locations = fetch('locations', 'location_id', 'location')
    categories = fetch('categories', 'category_id', 'category')
    statuses = fetch('statuses', 'status_id', 'status')

    try:
        boxes = q_all("SELECT box_id, COALESCE(name, reference) AS label FROM boxes ORDER BY label")
        if not boxes:
            current_app.logger.warning("[choices] Boxes query returned 0 rows.")
    except Exception as e:
        current_app.logger.exception("[choices] Boxes SELECT failed: %s", e)
        flash(f"Boxes lookup failed: {e}", 'danger')
        boxes = []

    return {
        'owners': owners,
        'locations': locations,
        'categories': categories,
        'statuses': statuses,
        'boxes': boxes,
    }
