# routes_ui.py
from __future__ import annotations
from flask import Blueprint, request, render_template_string, redirect, url_for, flash
from db import q_all, q_one, exec_sql
from lookups import choices
from routes_auth import login_required
from templates import (
    TPL_BASE, TPL_HOME, TPL_BOXES, TPL_BOX_DETAIL, TPL_BOX_FORM,
    TPL_ITEM_FORM, TPL_MOVE_ITEMS, TPL_SEARCH
)

ui_bp = Blueprint("ui", __name__)

@ui_bp.route("/")
def home():
    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_HOME, **ch), **ch)

@ui_bp.route("/boxes")
def boxes_list():
    owner_id = request.args.get("owner_id")
    location_id = request.args.get("location_id")
    category_id = request.args.get("category_id")
    status_id = request.args.get("status_id")

    filters = []
    params = []
    if owner_id and owner_id.isdigit():
        filters.append("b.owner_id = ?"); params.append(int(owner_id))
    if location_id and location_id.isdigit():
        filters.append("b.location_id = ?"); params.append(int(location_id))
    if category_id and category_id.isdigit():
        filters.append("b.category_id = ?"); params.append(int(category_id))
    if status_id and status_id.isdigit():
        filters.append("b.status_id = ?"); params.append(int(status_id))

    where = ("WHERE " + " AND ".join(filters)) if filters else ""

    rows = q_all(f"""
        SELECT b.*,
               o.owner, l.location, c.category, s.status,
               (SELECT COUNT(1) FROM items i WHERE i.box_id = b.box_id) AS item_count
          FROM boxes b
          JOIN owners o     ON o.owner_id = b.owner_id
          JOIN locations l  ON l.location_id = b.location_id
          JOIN categories c ON c.category_id = b.category_id
          JOIN statuses s   ON s.status_id = b.status_id
          {where}
         ORDER BY COALESCE(b.name, b.reference)
    """, tuple(params))

    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_BOXES, rows=rows, **ch), **ch)

@ui_bp.route("/box/<int:box_id>")
def box_detail(box_id:int):
    box = q_one("""
        SELECT b.*,
               o.owner, l.location, c.category, s.status
          FROM boxes b
          JOIN owners o     ON o.owner_id = b.owner_id
          JOIN locations l  ON l.location_id = b.location_id
          JOIN categories c ON c.category_id = b.category_id
          JOIN statuses s   ON s.status_id = b.status_id
         WHERE b.box_id = ?
    """, (box_id,))
    if not box:
        return ("Not found", 404)
    items = q_all("""
        SELECT i.*, c.category, s.status
          FROM items i
          JOIN categories c ON c.category_id = i.category_id
          JOIN statuses s   ON s.status_id = i.status_id
         WHERE i.box_id = ?
         ORDER BY i.item
    """, (box_id,))
    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_BOX_DETAIL, box=box, items=items, **ch), **ch)

@ui_bp.route("/box/new", methods=["GET","POST"])
@login_required
def box_new():
    if request.method == "POST":
        try:
            reference = (request.form.get("reference") or "").strip()
            name = (request.form.get("name") or "").strip()
            owner_id = int(request.form.get("owner_id"))
            location_id = int(request.form.get("location_id"))
            category_id = int(request.form.get("category_id"))
            status_id = int(request.form.get("status_id"))
        except (TypeError, ValueError):
            flash("Please select Owner, Location, Category and Status.", "danger")
            return redirect(url_for("ui.box_new"))

        packed_on = request.form.get("packed_on") or None
        stored_on = request.form.get("stored_on") or None
        photo = request.files.get("photo")
        photo_blob = photo.read() if (photo and photo.filename) else None

        box_id = exec_sql("""
            INSERT INTO boxes (reference, name, location_id, category_id, owner_id, status_id, photo, packed_on, stored_on)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (reference, name, location_id, category_id, owner_id, status_id, photo_blob, packed_on, stored_on))

        # Optionally assign items
        item_ids = request.form.getlist("item_ids")
        for iid in item_ids:
            if iid.isdigit():
                exec_sql("UPDATE items SET box_id = ? WHERE item_id = ?", (box_id, int(iid)))

        flash("Box created.", "success")
        return redirect(url_for("ui.box_detail", box_id=box_id))

    unassigned = q_all("SELECT item_id, item FROM items WHERE box_id IS NULL ORDER BY item")
    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_BOX_FORM, unassigned=unassigned, box=None, **ch), **ch)

@ui_bp.route("/box/<int:box_id>/edit", methods=["GET","POST"])
@login_required
def box_edit(box_id:int):
    box = q_one("SELECT * FROM boxes WHERE box_id = ?", (box_id,))
    if not box:
        return ("Not found", 404)
    if request.method == "POST":
        # Deletion path (from Boxes list form)
        if request.form.get("_delete") == "1":
            exec_sql("UPDATE items SET box_id = NULL WHERE box_id = ?", (box_id,))
            exec_sql("DELETE FROM boxes WHERE box_id = ?", (box_id,))
            flash("Box deleted.", "info")
            return redirect(url_for("ui.boxes_list"))

        reference = (request.form.get("reference") or "").strip()
        name = (request.form.get("name") or "").strip()
        owner_id = int(request.form.get("owner_id"))
        location_id = int(request.form.get("location_id"))
        category_id = int(request.form.get("category_id"))
        status_id = int(request.form.get("status_id"))
        packed_on = request.form.get("packed_on") or None
        stored_on = request.form.get("stored_on") or None
        photo = request.files.get("photo")
        photo_blob = photo.read() if (photo and photo.filename) else None

        exec_sql("""
            UPDATE boxes
               SET reference=?, name=?, location_id=?, category_id=?, owner_id=?, status_id=?, packed_on=?, stored_on=?
             WHERE box_id=?
        """, (reference, name, location_id, category_id, owner_id, status_id, packed_on, stored_on, box_id))
        if photo_blob is not None:
            exec_sql("UPDATE boxes SET photo=? WHERE box_id=?", (photo_blob, box_id))

        flash("Box updated.", "success")
        return redirect(url_for("ui.box_detail", box_id=box_id))

    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_BOX_FORM, unassigned=[], box=box, **ch), **ch)

# ---- Items ----
@ui_bp.route("/items/new", methods=["GET","POST"])
@login_required
def item_new():
    if request.method == "POST":
        item_text = (request.form.get("item") or "").strip()
        try:
            category_id = int(request.form.get("category_id"))
            status_id = int(request.form.get("status_id"))
        except (TypeError, ValueError):
            flash("Please select Category and Status.", "danger")
            return redirect(url_for("ui.item_new"))

        box_id_val = request.form.get("box_id")
        box_id = int(box_id_val) if box_id_val and box_id_val.isdigit() else None
        taken_on = request.form.get("taken_on") or None
        photo = request.files.get("photo")
        photo_blob = photo.read() if (photo and photo.filename) else None

        exec_sql("""
            INSERT INTO items (box_id, item, category_id, status_id, photo, taken_on)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (box_id, item_text, category_id, status_id, photo_blob, taken_on))

        flash("Item created.", "success")
        return redirect(url_for("ui.box_detail", box_id=box_id) if box_id else url_for("ui.home"))

    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_ITEM_FORM, item=None, **ch), **ch)

@ui_bp.route("/item/<int:item_id>/edit", methods=["GET","POST"])
@login_required
def item_edit(item_id:int):
    item = q_one("SELECT * FROM items WHERE item_id=?", (item_id,))
    if not item:
        return ("Not found", 404)
    if request.method == "POST":
        item_text = (request.form.get("item") or "").strip()
        category_id = int(request.form.get("category_id"))
        status_id = int(request.form.get("status_id"))
        box_id_val = request.form.get("box_id")
        box_id = int(box_id_val) if box_id_val and box_id_val.isdigit() else None
        taken_on = request.form.get("taken_on") or None
        photo = request.files.get("photo")
        photo_blob = photo.read() if (photo and photo.filename) else None

        exec_sql("""
            UPDATE items
               SET box_id=?, item=?, category_id=?, status_id=?, taken_on=?
             WHERE item_id=?
        """, (box_id, item_text, category_id, status_id, taken_on, item_id))
        if photo_blob is not None:
            exec_sql("UPDATE items SET photo=? WHERE item_id=?", (photo_blob, item_id))

        flash("Item updated.", "success")
        return redirect(url_for("ui.box_detail", box_id=box_id) if box_id else url_for("ui.home"))

    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_ITEM_FORM, item=item, **ch), **ch)

@ui_bp.route("/item/<int:item_id>/delete", methods=["POST"])
@login_required
def item_delete(item_id:int):
    exec_sql("DELETE FROM items WHERE item_id=?", (item_id,))
    flash("Item deleted.", "info")
    return redirect(url_for("ui.home"))

# ---- Move items ----
@ui_bp.route("/move-items", methods=["GET","POST"])
@login_required
def move_items():
    if request.method == "POST":
        target_box_id = int(request.form.get("target_box_id"))
        item_ids = [int(x) for x in request.form.getlist("item_ids")]
        if not item_ids:
            flash("Select at least one item.", "warning")
            return redirect(url_for("ui.move_items"))
        placeholders = ",".join("?" for _ in item_ids)
        params = [target_box_id, *item_ids]
        exec_sql(f"UPDATE items SET box_id=? WHERE item_id IN ({placeholders})", tuple(params))
        flash(f"Moved {len(item_ids)} item(s).", "success")
        return redirect(url_for("ui.box_detail", box_id=target_box_id))

    items = q_all("""
        SELECT i.item_id, i.item,
               i.box_id,
               COALESCE(b.name, b.reference, '(No box)') AS box_label
          FROM items i
          LEFT JOIN boxes b ON b.box_id = i.box_id
         ORDER BY box_label, i.item
    """)
    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_MOVE_ITEMS, items=items, **ch), **ch)

# ---- Search ----
@ui_bp.route("/items/search")
def items_search():
    q = (request.args.get("q") or "").strip()
    rows = []
    if q:
        like = f"%{q}%"
        rows = q_all("""
            SELECT i.*, COALESCE(b.name, b.reference) AS box_label, b.box_id
              FROM items i
              LEFT JOIN boxes b ON b.box_id = i.box_id
             WHERE i.item LIKE ?
             ORDER BY i.item
        """, (like,))
    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_SEARCH, q=q, rows=rows, **ch), **ch)
