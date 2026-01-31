# All HTML templates (Jinja2) as raw strings.\n# Notes:\n# - New creation forms show a “— Please select —” placeholder for required selects.\n# - Date inputs use <input type=\"date\">; a small JS polyfill loads flatpickr if the browser lacks support.\n\nTPL_BASE = r\"\"\"\n<!doctype html>\n<html>\n<head>\n  <meta charset=\"utf-8\">\n  <title>Store-This</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n  <style>\n    :root { --bg:#0e0f12; --fg:#e8e8ea; --muted:#a9acb3; --card:#171a1f; --pri:#4da3ff; --ok:#55d39e; --warn:#ffcc66; --bad:#ff6b6b; }\n    * { box-sizing: border-box; }\n    body { margin:0; font:16px/1.5 system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif; background: var(--bg); color: var(--fg); }\n    header.topnav { padding: 10px 16px; background: #111319; position: sticky; top:0; z-index:10; border-bottom:1px solid #222632; display:flex; align-items:center; gap:12px; }\n    .nav-left, .nav-right { display:flex; align-items:center; gap:12px; }\n    .nav-left a, .nav-right a { color: var(--fg); text-decoration:none; }\n    .nav-search { display:flex; align-items:center; gap:8px; flex:1 1 420px; max-width:560px; min-width:260px; margin: 0 8px; background:#0f1117; border:1px solid #2a2f3c; border-radius:999px; padding:6px 10px; }\n    .nav-search input[type=text] { background:transparent; border:none; outline:none; width:100%; color:var(--fg); padding:6px 4px; }\n    .nav-icon { width:18px; height:18px; display:inline-block; }\n    .pill { background:#0f1117; border:1px solid #2a2f3c; padding: 6px 10px; border-radius: 999px; }\n    main { max-width: 1100px; margin: 0 auto; padding: 20px; }\n    .card { background: var(--card); border:1px solid #232835; border-radius: 14px; padding: 16px; margin-bottom:16px; }\n    h1,h2,h3 { margin: 0 0 12px 0; }\n    form .row { display:flex; gap:12px; flex-wrap: wrap; }\n    label { display:block; font-size: 13px; color: var(--muted); margin-bottom:6px; }\n    input[type=text], input[type=date], input[type=password], select { background:#111319; color:var(--fg); border:1px solid #2a2f3c; border-radius:10px; padding:10px 12px; width: 100%; }\n    input[type=file] { color: var(--muted); }\n    textarea { background:#111319; color:var(--fg); border:1px solid #2a2f3c; border-radius:10px; padding:10px 12px; width:100%; min-height: 120px; }\n    .btn { display:inline-block; padding:10px 14px; border-radius: 10px; border:1px solid #2a2f3c; text-decoration:none; cursor:pointer; }\n    .btn.primary { background: var(--pri); color:#08111f; font-weight: 600; border-color: transparent; }\n    .btn.good { background: var(--ok); color:#062016; border-color: transparent; }\n    .btn.bad { background: var(--bad); color:#1f0808; border-color: transparent; }\n    .btn.warn { background: var(--warn); color:#1f1608; border-color: transparent; }\n    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px,1fr)); gap: 16px; }\n    .box { border:1px solid #2a2f3c; border-radius:12px; overflow:hidden; background:#0f1117; }\n    .box img { width:100%; height: 160px; object-fit: cover; background:#0b0d12;}\n    .muted { color: var(--muted); }\n    .flash { padding: 10px 12px; border-radius: 10px; margin-bottom: 12px; }\n    .flash.info { background:#142033; border:1px solid #24324a; }\n    .flash.success { background:#0f281f; border:1px solid #1d3d30; }\n    .flash.warning { background:#291f10; border:1px solid #3d2f1d; }\n    .flash.danger { background:#2b1616; border:1px solid #432121; }\n    table { width:100%; border-collapse: collapse; }\n    th, td { text-align:left; border-bottom:1px solid #232835; padding:8px 6px; vertical-align: top; }\n    .toolbar { display:flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px;}\n    .img-sm { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; background:#0b0d12; }\n    .footer-space { height: 20px; }\n  </style>\n\n  <!-- Date picker polyfill: loads only if input[type=date] unsupported -->\n  <script>\n  (function(){\n    var i=document.createElement('input'); i.setAttribute('type','date');\n    if(i.type!=='date'){\n      var l=document.createElement('link'); l.rel='stylesheet'; l.href='https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css';\n      var s=document.createElement('script'); s.src='https://cdn.jsdelivr.net/npm/flatpickr';\n      s.onload=function(){ if(window.flatpickr){ flatpickr('input[type=date]', {dateFormat:'Y-m-d'}); } };\n      document.head.appendChild(l); document.head.appendChild(s);\n    }\n  })();\n  </script>\n</head>\n<body>\n<header class=\"topnav\">\n  <div class=\"nav-left\">\n    <a href=\"{{ url_for('ui.home') }}\"><strong>Store-This</strong></a>\n    <a href=\"{{ url_for('ui.boxes_list') }}\">Boxes</a>\n  </div>\n  <form class=\"nav-search\" action=\"{{ url_for('ui.items_search') }}\" method=\"get\">\n    <span class=\"nav-icon\" aria-hidden=\"true\">🔍</span>\n    <input type=\"text\" name=\"q\" value=\"{{ request.args.get('q','') }}\" placeholder=\"Search items...\" aria-label=\"Search items\">\n  </form>\n  <div class=\"nav-right\">\n    {% if session.get('logged_in') %}\n      <span class=\"pill\">{{ session.get('user_name','Admin') }}</span>\n      <a class=\"pill\" href=\"{{ url_for('auth.logout') }}\">Logout</a>\n    {% else %}\n      <a class=\"pill\" href=\"{{ url_for('auth.login') }}\">Admin</a>\n    {% endif %}\n  </div>\n</header>\n<main>\n  {% with msgs = get_flashed_messages(with_categories=true) %}\n    {% if msgs %}\n      {% for cat,msg in msgs %}\n        <div class=\"flash {{ 'success' if cat=='success' else 'danger' if cat=='danger' else 'warning' if cat=='warning' else 'info' }}\">{{ msg }}</div>\n      {% endfor %}\n    {% endif %}\n  {% endwith %}\n  {{ content | safe }}\n  <div class=\"footer-space\"></div>\n</main>\n</body>\n</html>\n\"\"\"\n\nTPL_HOME = r\"\"\"\n<div class=\"card\">\n  <h2>Quick actions</h2>\n  <div class=\"toolbar\">\n    {% if session.get('logged_in') %}\n      <a class=\"btn primary\" href=\"{{ url_for('ui.item_new') }}\">+ New Item</a>\n      <a class=\"btn primary\" href=\"{{ url_for('ui.box_new') }}\">+ New Box</a>\n      <a class=\"btn\" href=\"{{ url_for('ui.move_items') }}\">Move Items</a>\n    {% else %}\n      <span class=\"muted\">Log in to add/edit/delete.</span>\n    {% endif %}\n  </div>\n</div>\n\"\"\"\n\nTPL_LOGIN = r\"\"\"\n<div class=\"card\">\n  <h2>Administrator Login</h2>\n  <form method=\"post\" class=\"row\" style=\"max-width:520px;\">\n    <div style=\"flex:1 1 50%; min-width:220px;\">\n      <label>Name (shown in top-nav)</label>\n      <input type=\"text\" name=\"user_name\" placeholder=\"e.g. Dylan\">\n    </div>\n    <div style=\"flex:1 1 50%; min-width:220px;\">\n      <label>Password</label>\n      <input type=\"password\" name=\"password\" placeholder=\"Enter admin password\" required>\n    </div>\n    <div><button class=\"btn primary\">Login</button></div>\n  </form>\n  <p class=\"muted\">Set the password via environment variable <code>STORE_THIS_ADMIN_PASSWORD</code>.</p>\n</div>\n\"\"\"\n\nTPL_BOXES = r\"\"\"\n<div class=\"card\" style=\"margin-top:-6px;\">\n  <form method=\"get\" action=\"{{ url_for('ui.boxes_list') }}\" class=\"row\" style=\"align-items:flex-end;\">\n    <div style=\"flex:1; min-width:180px;\">\n      <label>Owner</label>\n      <select name=\"owner_id\">\n        <option value=\"\">All Owners</option>\n        {% for r in owners %}\n          <option value=\"{{ r['owner_id'] }}\" {% if selected_owner_id and selected_owner_id==r['owner_id'] %}selected{% endif %}>{{ r['owner'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:220px;\">\n      <label>Location (multi)</label>\n      <select name=\"location_id\" multiple size=\"4\">\n        {% for r in locations %}\n          <option value=\"{{ r['location_id'] }}\" {% if r['location_id'] in selected_location_ids %}selected{% endif %}>{{ r['location'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:220px;\">\n      <label>Category (multi)</label>\n      <select name=\"category_id\" multiple size=\"4\">\n        {% for r in categories %}\n          <option value=\"{{ r['category_id'] }}\" {% if r['category_id'] in selected_category_ids %}selected{% endif %}>{{ r['category'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:180px;\">\n      <label>Status</label>\n      <select name=\"status_id\">\n        <option value=\"\">All Statuses</option>\n        {% for r in statuses %}\n          <option value=\"{{ r['status_id'] }}\" {% if selected_status_id and selected_status_id==r['status_id'] %}selected{% endif %}>{{ r['status'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:0 0 auto;\">\n      <button class=\"btn\">Apply</button>\n    </div>\n  </form>\n</div>\n\n<div class=\"grid\">\n  {% for b in rows %}\n    <div class=\"box\">\n      <a href=\"{{ url_for('ui.box_detail', box_id=b['box_id']) }}\">\n        <img src=\"{{ url_for('images.photo_box', box_id=b['box_id']) }}\" alt=\"Box photo\">\n      </a>\n      <div style=\"padding:12px;\">\n        <div><strong>{{ b['name'] or b['reference'] }}</strong></div>\n        <div class=\"muted\">Items: {{ b['item_count'] }}</div>\n        <div class=\"muted\">{{ b['owner'] }} • {{ b['location'] }} • {{ b['category'] }} • {{ b['status'] }}</div>\n        {% if session.get('logged_in') %}\n          <div style=\"margin-top:8px;\">\n            <a class=\"btn\" href=\"{{ url_for('ui.box_edit', box_id=b['box_id']) }}\">Edit</a>\n            <form method=\"post\" action=\"{{ url_for('ui.box_edit', box_id=b['box_id']) }}\" style=\"display:inline\" onsubmit=\"return confirm('Delete this box?');\">\n              <button class=\"btn bad\" name=\"_delete\" value=\"1\">Delete</button>\n            </form>\n          </div>\n        {% endif %}\n      </div>\n    </div>\n  {% endfor %}\n</div>\n\n<div class=\"card\">\n  <h3>Summary: Boxes by Owner × Category</h3>\n  <table>\n    <thead><tr><th>Owner</th><th>Category</th><th style=\"text-align:right\">Boxes</th></tr></thead>\n    <tbody>\n      {% for r in summary %}\n        <tr>\n          <td>{{ r['owner'] }}</td>\n          <td class=\"muted\">{{ r['category'] }}</td>\n          <td style=\"text-align:right;\">{{ r['cnt'] }}</td>\n        </tr>\n      {% endfor %}\n      {% if not summary %}\n        <tr><td colspan=\"3\" class=\"muted\">No boxes found for current filters.</td></tr>\n      {% endif %}\n    </tbody>\n  </table>\n</div>\n\"\"\"\n\nTPL_BOX_DETAIL = r\"\"\"\n<div class=\"card\">\n  <div class=\"row\" style=\"align-items:flex-start;\">\n    <div style=\"flex:0 0 280px;\">\n      <img src=\"{{ url_for('images.photo_box', box_id=box['box_id']) }}\" alt=\"Box photo\" style=\"width:100%; height:240px; object-fit:cover; border-radius:12px; border:1px solid #2a2f3c; background:#0b0d12;\">\n    </div>\n    <div style=\"flex:1;\">\n      <h2>{{ box['name'] or box['reference'] }}</h2>\n      <div class=\"muted\">{{ box['owner'] }} • {{ box['location'] }} • {{ box['category'] }} • {{ box['status'] }}</div>\n      <div class=\"muted\">Packed: {{ box['packed_on'] or '—' }} &nbsp; Stored: {{ box['stored_on'] or '—' }}</div>\n      {% if session.get('logged_in') %}\n        <div style=\"margin-top:8px;\">\n          <a class=\"btn\" href=\"{{ url_for('ui.box_edit', box_id=box['box_id']) }}\">Edit Box</a>\n          <a class=\"btn\" href=\"{{ url_for('ui.move_items') }}\">Move Items</a>\n        </div>\n      {% endif %}\n    </div>\n  </div>\n</div>\n\n<div class=\"card\">\n  <h3>Items in this box</h3>\n  <table>\n    <thead>\n      <tr><th>Photo</th><th>Item</th><th>Category</th><th>Status</th><th>Taken</th>{% if session.get('logged_in') %}<th>Actions</th>{% endif %}</tr>\n    </thead>\n    <tbody>\n      {% for i in items %}\n        <tr>\n          <td><img class=\"img-sm\" src=\"{{ url_for('images.photo_item', item_id=i['item_id']) }}\" alt=\"\"></td>\n          <td>{{ i['item'] }}</td>\n          <td class=\"muted\">{{ i['category'] }}</td>\n          <td class=\"muted\">{{ i['status'] }}</td>\n          <td class=\"muted\">{{ i['taken_on'] or '—' }}</td>\n          {% if session.get('logged_in') %}\n            <td>\n              <a class=\"btn\" href=\"{{ url_for('ui.item_edit', item_id=i['item_id']) }}\">Edit</a>\n              <form method=\"post\" action=\"{{ url_for('ui.item_delete', item_id=i['item_id']) }}\" style=\"display:inline\" onsubmit=\"return confirm('Delete this item?');\">\n                <button class=\"btn bad\">Delete</button>\n              </form>\n            </td>\n          {% endif %}\n        </tr>\n      {% endfor %}\n    </tbody>\n  </table>\n</div>\n\"\"\"\n\nTPL_BOX_FORM = r\"\"\"\n<div class=\"card\">\n  <h2>{{ 'Edit Box' if box else 'New Box' }}</h2>\n  <form method=\"post\" enctype=\"multipart/form-data\" class=\"row\">\n    <div style=\"flex:1; min-width:220px;\">\n      <label>Reference</label>\n      <input type=\"text\" name=\"reference\" value=\"{{ box['reference'] if box else '' }}\" placeholder=\"e.g. BX-001\" required>\n    </div>\n    <div style=\"flex:2; min-width:240px;\">\n      <label>Name (optional)</label>\n      <input type=\"text\" name=\"name\" value=\"{{ box['name'] if box else '' }}\" placeholder=\"e.g. Living Room Decorations\">\n    </div>\n    <div style=\"flex:1; min-width:200px;\">\n      <label>Owner</label>\n      <select name=\"owner_id\" required>\n        {% if not box %}<option value=\"\" selected disabled>— Please select —</option>{% endif %}\n        {% for r in owners %}\n          <option value=\"{{ r['owner_id'] }}\" {% if box and box['owner_id']==r['owner_id'] %}selected{% endif %}>{{ r['owner'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:200px;\">\n      <label>Location</label>\n      <select name=\"location_id\" required>\n        {% if not box %}<option value=\"\" selected disabled>— Please select —</option>{% endif %}\n        {% for r in locations %}\n          <option value=\"{{ r['location_id'] }}\" {% if box and box['location_id']==r['location_id'] %}selected{% endif %}>{{ r['location'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:200px;\">\n      <label>Category</label>\n      <select name=\"category_id\" required>\n        {% if not box %}<option value=\"\" selected disabled>— Please select —</option>{% endif %}\n        {% for r in categories %}\n          <option value=\"{{ r['category_id'] }}\" {% if box and box['category_id']==r['category_id'] %}selected{% endif %}>{{ r['category'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:200px;\">\n      <label>Status</label>\n      <select name=\"status_id\" required>\n        {% if not box %}<option value=\"\" selected disabled>— Please select —</option>{% endif %}\n        {% for r in statuses %}\n          <option value=\"{{ r['status_id'] }}\" {% if box and box['status_id']==r['status_id'] %}selected{% endif %}>{{ r['status'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:160px;\">\n      <label>Packed On</label>\n      <input type=\"date\" name=\"packed_on\" value=\"{{ box['packed_on'] if box else '' }}\" placeholder=\"YYYY-MM-DD\">\n    </div>\n    <div style=\"flex:1; min-width:160px;\">\n      <label>Stored On</label>\n      <input type=\"date\" name=\"stored_on\" value=\"{{ box['stored_on'] if box else '' }}\" placeholder=\"YYYY-MM-DD\">\n    </div>\n    <div style=\"flex:1 1 100%;\">\n      <label>Photo</label>\n      <input type=\"file\" name=\"photo\" accept=\"image/*\">\n    </div>\n\n    {% if not box %}\n      <div style=\"flex:1 1 100%;\">\n        <label>Assign Unassigned Items (optional)</label>\n        <div class=\"muted\">Select any items to immediately place into this box.</div>\n        <div style=\"max-height:180px; overflow:auto; border:1px solid #2a2f3c; border-radius:10px; padding:8px;\">\n          {% for i in unassigned %}\n            <label style=\"display:block;\"><input type=\"checkbox\" name=\"item_ids\" value=\"{{ i['item_id'] }}\"> {{ i['item'] }}</label>\n          {% endfor %}\n          {% if not unassigned %}<div class=\"muted\">No unassigned items.</div>{% endif %}\n        </div>\n      </div>\n    {% endif %}\n\n    <div style=\"flex:1 1 100%;\">\n      <button class=\"btn primary\">{{ 'Save Changes' if box else 'Create Box' }}</button>\n    </div>\n  </form>\n</div>\n\"\"\"\n\nTPL_ITEM_FORM = r\"\"\"\n<div class=\"card\">\n  <h2>{{ 'Edit Item' if item else 'New Item' }}</h2>\n  <form method=\"post\" enctype=\"multipart/form-data\" class=\"row\">\n    <div style=\"flex:2; min-width:260px;\">\n      <label>Item</label>\n      <input type=\"text\" name=\"item\" value=\"{{ item['item'] if item else '' }}\" placeholder=\"Describe the item\" required>\n    </div>\n    <div style=\"flex:1; min-width:200px;\">\n      <label>Category</label>\n      <select name=\"category_id\" required>\n        {% if not item %}<option value=\"\" selected disabled>— Please select —</option>{% endif %}\n        {% for r in categories %}\n          <option value=\"{{ r['category_id'] }}\" {% if item and item['category_id']==r['category_id'] %}selected{% endif %}>{{ r['category'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:200px;\">\n      <label>Status</label>\n      <select name=\"status_id\" required>\n        {% if not item %}<option value=\"\" selected disabled>— Please select —</option>{% endif %}\n        {% for r in statuses %}\n          <option value=\"{{ r['status_id'] }}\" {% if item and item['status_id']==r['status_id'] %}selected{% endif %}>{{ r['status'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:200px;\">\n      <label>Box</label>\n      <select name=\"box_id\">\n        {% if item %}\n          <option value=\"\">(Unassigned)</option>\n        {% else %}\n          <option value=\"\">— (Optional) Leave unassigned —</option>\n        {% endif %}\n        {% for r in boxes %}\n          <option value=\"{{ r['box_id'] }}\" {% if item and item['box_id']==r['box_id'] %}selected{% endif %}>{{ r['label'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1; min-width:160px;\">\n      <label>Taken On</label>\n      <input type=\"date\" name=\"taken_on\" value=\"{{ item['taken_on'] if item else '' }}\" placeholder=\"YYYY-MM-DD\">\n    </div>\n    <div style=\"flex:1 1 100%;\">\n      <label>Photo</label>\n      <input type=\"file\" name=\"photo\" accept=\"image/*\">\n    </div>\n    <div style=\"flex:1 1 100%;\">\n      <button class=\"btn primary\">{{ 'Save Changes' if item else 'Create Item' }}</button>\n    </div>\n  </form>\n</div>\n\"\"\"\n\nTPL_MOVE_ITEMS = r\"\"\"\n<div class=\"card\">\n  <h2>Move Items to a Different Box</h2>\n  <form method=\"post\" class=\"row\">\n    <div style=\"flex:1; min-width:260px;\">\n      <label>Target Box</label>\n      <select name=\"target_box_id\" required>\n        <option value=\"\" selected disabled>— Please select —</option>\n        {% for r in boxes %}\n          <option value=\"{{ r['box_id'] }}\">{{ r['label'] }}</option>\n        {% endfor %}\n      </select>\n    </div>\n    <div style=\"flex:1 1 100%;\"></div>\n    <div style=\"flex:1 1 100%;\">\n      <label>Select Items</label>\n      <div class=\"muted\">Tip: Use Ctrl/Cmd+F in the browser to search by item or current box label.</div>\n      <div style=\"max-height:320px; overflow:auto; border:1px solid #2a2f3c; border-radius:10px; padding:8px;\">\n        {% for i in items %}\n          <label style=\"display:block;\"><input type=\"checkbox\" name=\"item_ids\" value=\"{{ i['item_id'] }}\"> [{{ i['box_label'] }}] {{ i['item'] }}</label>\n        {% endfor %}\n      </div>\n    </div>\n    <div style=\"flex:1 1 100%;\">\n      <button class=\"btn primary\">Move Selected</button>\n    </div>\n  </form>\n</div>\n\"\"\"\n\nTPL_SEARCH = r\"\"\"\n<div class=\"card\">\n  <h2>Search Items</h2>\n  <form action=\"{{ url_for('ui.items_search') }}\" method=\"get\" class=\"row\" style=\"gap:8px; max-width:560px;\">\n    <input type=\"text\" name=\"q\" placeholder=\"e.g. kettle, HDMI cable, Christmas\" value=\"{{ q }}\" required>\n    <button class=\"btn\">Search</button>\n    {% if session.get('logged_in') %}\n      <a class=\"btn primary\" href=\"{{ url_for('ui.item_new') }}\">+ New Item</a>\n    {% endif %}\n  </form>\n</div>\n\n{% if q %}\n  <div class=\"grid\">\n    {% for r in rows %}\n      <div class=\"box\">\n        <img src=\"{{ url_for('images.photo_item', item_id=r['item_id']) }}\" alt=\"\">\n        <div style=\"padding:12px;\">\n          <div><strong>{{ r['item'] }}</strong></div>\n          <div class=\"muted\">Box: {% if r['box_id'] %}<a href=\"{{ url_for('ui.box_detail', box_id=r['box_id']) }}\">{{ r['box_label'] }}</a>{% else %}(Unassigned){% endif %}</div>\n          {% if session.get('logged_in') %}\n            <div style=\"margin-top:8px;\">\n              <a class=\"btn\" href=\"{{ url_for('ui.item_edit', item_id=r['item_id']) }}\">Edit</a>\n              <form method=\"post\" action=\"{{ url_for('ui.item_delete', item_id=r['item_id']) }}\" style=\"display:inline\" onsubmit=\"return confirm('Delete this item?');\">\n                <button class=\"btn bad\">Delete</button>\n              </form>\n            </div>\n          {% endif %}\n        </div>\n      </div>\n    {% endfor %}\n  </div>\n{% endif %}\n\"\"\"
# All HTML templates (Jinja2) as raw strings.
# Notes:
# - New creation forms show a “— Please select —” placeholder for required selects.
# - Date inputs use <input type="date">; a small JS polyfill loads flatpickr if the browser lacks support.

TPL_BASE = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Store-This</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root { --bg:#0e0f12; --fg:#e8e8ea; --muted:#a9acb3; --card:#171a1f; --pri:#4da3ff; --ok:#55d39e; --warn:#ffcc66; --bad:#ff6b6b; }
    * { box-sizing: border-box; }
    body { margin:0; font:16px/1.5 system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif; background: var(--bg); color: var(--fg); }
    header { padding: 16px 20px; background: #111319; position: sticky; top:0; z-index:10; border-bottom:1px solid #222632; }
    header a { color: var(--fg); text-decoration:none; margin-right:16px; }
    header .right { float:right; }
    main { max-width: 1100px; margin: 0 auto; padding: 20px; }
    .card { background: var(--card); border:1px solid #232835; border-radius: 14px; padding: 16px; margin-bottom:16px; }
    h1,h2,h3 { margin: 0 0 12px 0; }
    form .row { display:flex; gap:12px; flex-wrap: wrap; }
    label { display:block; font-size: 13px; color: var(--muted); margin-bottom:6px; }
    input[type=text], input[type=date], input[type=password], select { background:#111319; color:var(--fg); border:1px solid #2a2f3c; border-radius:10px; padding:10px 12px; width: 100%; }
    input[type=file] { color: var(--muted); }
    textarea { background:#111319; color:var(--fg); border:1px solid #2a2f3c; border-radius:10px; padding:10px 12px; width:100%; min-height: 120px; }
    .btn { display:inline-block; padding:10px 14px; border-radius: 10px; border:1px solid #2a2f3c; text-decoration:none; cursor:pointer; }
    .btn.primary { background: var(--pri); color:#08111f; font-weight: 600; border-color: transparent; }
    .btn.good { background: var(--ok); color:#062016; border-color: transparent; }
    .btn.bad { background: var(--bad); color:#1f0808; border-color: transparent; }
    .btn.warn { background: var(--warn); color:#1f1608; border-color: transparent; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px,1fr)); gap: 16px; }
    .box { border:1px solid #2a2f3c; border-radius:12px; overflow:hidden; background:#0f1117; }
    .box img { width:100%; height: 160px; object-fit: cover; background:#0b0d12;}
    .muted { color: var(--muted); }
    .flash { padding: 10px 12px; border-radius: 10px; margin-bottom: 12px; }
    .flash.info { background:#142033; border:1px solid #24324a; }
    .flash.success { background:#0f281f; border:1px solid #1d3d30; }
    .flash.warning { background:#291f10; border:1px solid #3d2f1d; }
    .flash.danger { background:#2b1616; border:1px solid #432121; }
    table { width:100%; border-collapse: collapse; }
    th, td { text-align:left; border-bottom:1px solid #232835; padding:8px 6px; vertical-align: top; }
    .toolbar { display:flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px;}
    .pill { background:#0f1117; border:1px solid #2a2f3c; padding: 8px 10px; border-radius: 999px; }
    .img-sm { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; background:#0b0d12; }
    .right { float:right; }
    .footer-space { height: 20px; }
  </style>

  <!-- Date picker polyfill: loads only if input[type=date] unsupported -->
  <script>
  (function(){
    var i=document.createElement('input'); i.setAttribute('type','date');
    if(i.type!=='date'){
      var l=document.createElement('link'); l.rel='stylesheet'; l.href='https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css';
      var s=document.createElement('script'); s.src='https://cdn.jsdelivr.net/npm/flatpickr';
      s.onload=function(){ if(window.flatpickr){ flatpickr('input[type=date]', {dateFormat:'Y-m-d'}); } };
      document.head.appendChild(l); document.head.appendChild(s);
    }
  })();
  </script>
</head>
<body>
<header>
  <a href="{{ url_for('ui.home') }}"><strong>Store-This</strong></a>
  <a href="{{ url_for('ui.boxes_list') }}">Boxes</a>
  <a href="{{ url_for('ui.items_search') }}">Search Items</a>
  {% if session.get('logged_in') %}
    <span class="right"><a class="pill" href="{{ url_for('auth.logout') }}">Logout</a></span>
  {% else %}
    <span class="right"><a class="pill" href="{{ url_for('auth.login') }}">Admin</a></span>
  {% endif %}
</header>
<main>
  {% with msgs = get_flashed_messages(with_categories=true) %}
    {% if msgs %}
      {% for cat,msg in msgs %}
        <div class="flash {{ 'success' if cat=='success' else 'danger' if cat=='danger' else 'warning' if cat=='warning' else 'info' }}">{{ msg }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}
  {{ content | safe }}
  <div class="footer-space"></div>
</main>
</body>
</html>
"""

TPL_HOME = r"""
<div class="card">
  <h2>Quick actions</h2>
  <div class="toolbar">
    <form action="{{ url_for('ui.items_search') }}" method="get" class="row" style="gap:8px;">
      <input type="text" name="q" placeholder="Search items..." required>
      <button class="btn">Search</button>
    </form>
    {% if session.get('logged_in') %}
      <a class="btn primary" href="{{ url_for('ui.item_new') }}">+ New Item</a>
      <a class="btn primary" href="{{ url_for('ui.box_new') }}">+ New Box</a>
      <a class="btn" href="{{ url_for('ui.move_items') }}">Move Items</a>
    {% else %}
      <span class="muted">Log in to add/edit/delete.</span>
    {% endif %}
  </div>
</div>

<div class="card">
  <h2>Filter Boxes</h2>
  <form method="get" action="{{ url_for('ui.boxes_list') }}" class="row">
    <div style="flex:1; min-width:160px;">
      <label>Owner</label>
      <select name="owner_id">
        <option value="">All Owners</option>
        {% for r in owners %}
          <option value="{{ r['owner_id'] }}">{{ r['owner'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:160px;">
      <label>Location</label>
      <select name="location_id">
        <option value="">All Locations</option>
        {% for r in locations %}
          <option value="{{ r['location_id'] }}">{{ r['location'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:160px;">
      <label>Category</label>
      <select name="category_id">
        <option value="">All Categories</option>
        {% for r in categories %}
          <option value="{{ r['category_id'] }}">{{ r['category'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:160px;">
      <label>Status</label>
      <select name="status_id">
        <option value="">All Statuses</option>
        {% for r in statuses %}
          <option value="{{ r['status_id'] }}">{{ r['status'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="align-self:flex-end;">
      <button class="btn">Show Boxes</button>
    </div>
  </form>
</div>
"""

TPL_LOGIN = r"""
<div class="card">
  <h2>Administrator Login</h2>
  <form method="post" class="row" style="max-width:420px;">
    <div style="flex:1 1 100%;">
      <label>Password</label>
      <input type="password" name="password" placeholder="Enter admin password" required>
    </div>
    <div><button class="btn primary">Login</button></div>
  </form>
  <p class="muted">Set the password via environment variable <code>STORE_THIS_ADMIN_PASSWORD</code>.</p>
</div>
"""

TPL_BOXES = r"""
<div class="grid">
  {% for b in rows %}
    <div class="box">
      <a href="{{ url_for('ui.box_detail', box_id=b['box_id']) }}">
        <img src="{{ url_for('images.photo_box', box_id=b['box_id']) }}" alt="Box photo">
      </a>
      <div style="padding:12px;">
        <div><strong>{{ b['name'] or b['reference'] }}</strong></div>
        <div class="muted">Items: {{ b['item_count'] }}</div>
        <div class="muted">{{ b['owner'] }} • {{ b['location'] }} • {{ b['category'] }} • {{ b['status'] }}</div>
        {% if session.get('logged_in') %}
          <div style="margin-top:8px;">
            <a class="btn" href="{{ url_for('ui.box_edit', box_id=b['box_id']) }}">Edit</a>
            <form method="post" action="{{ url_for('ui.box_edit', box_id=b['box_id']) }}" style="display:inline" onsubmit="return confirm('Delete this box?');">
              <button class="btn bad" name="_delete" value="1">Delete</button>
            </form>
          </div>
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>
"""

TPL_BOX_DETAIL = r"""
<div class="card">
  <div class="row" style="align-items:flex-start;">
    <div style="flex:0 0 280px;">
      <img src="{{ url_for('images.photo_box', box_id=box['box_id']) }}" alt="Box photo" style="width:100%; height:240px; object-fit:cover; border-radius:12px; border:1px solid #2a2f3c; background:#0b0d12;">
    </div>
    <div style="flex:1;">
      <h2>{{ box['name'] or box['reference'] }}</h2>
      <div class="muted">{{ box['owner'] }} • {{ box['location'] }} • {{ box['category'] }} • {{ box['status'] }}</div>
      <div class="muted">Packed: {{ box['packed_on'] or '—' }} &nbsp; Stored: {{ box['stored_on'] or '—' }}</div>
      {% if session.get('logged_in') %}
        <div style="margin-top:8px;">
          <a class="btn" href="{{ url_for('ui.box_edit', box_id=box['box_id']) }}">Edit Box</a>
          <a class="btn" href="{{ url_for('ui.move_items') }}">Move Items</a>
        </div>
      {% endif %}
    </div>
  </div>
</div>

<div class="card">
  <h3>Items in this box</h3>
  <table>
    <thead>
      <tr><th>Photo</th><th>Item</th><th>Category</th><th>Status</th><th>Taken</th>{% if session.get('logged_in') %}<th>Actions</th>{% endif %}</tr>
    </thead>
    <tbody>
      {% for i in items %}
        <tr>
          <td><img class="img-sm" src="{{ url_for('images.photo_item', item_id=i['item_id']) }}" alt=""></td>
          <td>{{ i['item'] }}</td>
          <td class="muted">{{ i['category'] }}</td>
          <td class="muted">{{ i['status'] }}</td>
          <td class="muted">{{ i['taken_on'] or '—' }}</td>
          {% if session.get('logged_in') %}
            <td>
              <a class="btn" href="{{ url_for('ui.item_edit', item_id=i['item_id']) }}">Edit</a>
              <form method="post" action="{{ url_for('ui.item_delete', item_id=i['item_id']) }}" style="display:inline" onsubmit="return confirm('Delete this item?');">
                <button class="btn bad">Delete</button>
              </form>
            </td>
          {% endif %}
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
"""

TPL_BOX_FORM = r"""
<div class="card">
  <h2>{{ 'Edit Box' if box else 'New Box' }}</h2>
  <form method="post" enctype="multipart/form-data" class="row">
    <div style="flex:1; min-width:220px;">
      <label>Reference</label>
      <input type="text" name="reference" value="{{ box['reference'] if box else '' }}" placeholder="e.g. BX-001" required>
    </div>
    <div style="flex:2; min-width:240px;">
      <label>Name (optional)</label>
      <input type="text" name="name" value="{{ box['name'] if box else '' }}" placeholder="e.g. Living Room Decorations">
    </div>
    <div style="flex:1; min-width:200px;">
      <label>Owner</label>
      <select name="owner_id" required>
        {% if not box %}<option value="" selected disabled>— Please select —</option>{% endif %}
        {% for r in owners %}
          <option value="{{ r['owner_id'] }}" {% if box and box['owner_id']==r['owner_id'] %}selected{% endif %}>{{ r['owner'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:200px;">
      <label>Location</label>
      <select name="location_id" required>
        {% if not box %}<option value="" selected disabled>— Please select —</option>{% endif %}
        {% for r in locations %}
          <option value="{{ r['location_id'] }}" {% if box and box['location_id']==r['location_id'] %}selected{% endif %}>{{ r['location'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:200px;">
      <label>Category</label>
      <select name="category_id" required>
        {% if not box %}<option value="" selected disabled>— Please select —</option>{% endif %}
        {% for r in categories %}
          <option value="{{ r['category_id'] }}" {% if box and box['category_id']==r['category_id'] %}selected{% endif %}>{{ r['category'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:200px;">
      <label>Status</label>
      <select name="status_id" required>
        {% if not box %}<option value="" selected disabled>— Please select —</option>{% endif %}
        {% for r in statuses %}
          <option value="{{ r['status_id'] }}" {% if box and box['status_id']==r['status_id'] %}selected{% endif %}>{{ r['status'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:160px;">
      <label>Packed On</label>
      <input type="date" name="packed_on" value="{{ box['packed_on'] if box else '' }}" placeholder="YYYY-MM-DD">
    </div>
    <div style="flex:1; min-width:160px;">
      <label>Stored On</label>
      <input type="date" name="stored_on" value="{{ box['stored_on'] if box else '' }}" placeholder="YYYY-MM-DD">
    </div>
    <div style="flex:1 1 100%;">
      <label>Photo</label>
      <input type="file" name="photo" accept="image/*">
    </div>

    {% if not box %}
      <div style="flex:1 1 100%;">
        <label>Assign Unassigned Items (optional)</label>
        <div class="muted">Select any items to immediately place into this box.</div>
        <div style="max-height:180px; overflow:auto; border:1px solid #2a2f3c; border-radius:10px; padding:8px;">
          {% for i in unassigned %}
            <label style="display:block;"><input type="checkbox" name="item_ids" value="{{ i['item_id'] }}"> {{ i['item'] }}</label>
          {% endfor %}
          {% if not unassigned %}<div class="muted">No unassigned items.</div>{% endif %}
        </div>
      </div>
    {% endif %}

    <div style="flex:1 1 100%;">
      <button class="btn primary">{{ 'Save Changes' if box else 'Create Box' }}</button>
    </div>
  </form>
</div>
"""

TPL_ITEM_FORM = r"""
<div class="card">
  <h2>{{ 'Edit Item' if item else 'New Item' }}</h2>
  <form method="post" enctype="multipart/form-data" class="row">
    <div style="flex:2; min-width:260px;">
      <label>Item</label>
      <input type="text" name="item" value="{{ item['item'] if item else '' }}" placeholder="Describe the item" required>
    </div>
    <div style="flex:1; min-width:200px;">
      <label>Category</label>
      <select name="category_id" required>
        {% if not item %}<option value="" selected disabled>— Please select —</option>{% endif %}
        {% for r in categories %}
          <option value="{{ r['category_id'] }}" {% if item and item['category_id']==r['category_id'] %}selected{% endif %}>{{ r['category'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:200px;">
      <label>Status</label>
      <select name="status_id" required>
        {% if not item %}<option value="" selected disabled>— Please select —</option>{% endif %}
        {% for r in statuses %}
          <option value="{{ r['status_id'] }}" {% if item and item['status_id']==r['status_id'] %}selected{% endif %}>{{ r['status'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:200px;">
      <label>Box</label>
      <select name="box_id">
        {% if item %}
          <option value="">(Unassigned)</option>
        {% else %}
          <option value="">— (Optional) Leave unassigned —</option>
        {% endif %}
        {% for r in boxes %}
          <option value="{{ r['box_id'] }}" {% if item and item['box_id']==r['box_id'] %}selected{% endif %}>{{ r['label'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1; min-width:160px;">
      <label>Taken On</label>
      <input type="date" name="taken_on" value="{{ item['taken_on'] if item else '' }}" placeholder="YYYY-MM-DD">
    </div>
    <div style="flex:1 1 100%;">
      <label>Photo</label>
      <input type="file" name="photo" accept="image/*">
    </div>
    <div style="flex:1 1 100%;">
      <button class="btn primary">{{ 'Save Changes' if item else 'Create Item' }}</button>
    </div>
  </form>
</div>
"""

TPL_MOVE_ITEMS = r"""
<div class="card">
  <h2>Move Items to a Different Box</h2>
  <form method="post" class="row">
    <div style="flex:1; min-width:260px;">
      <label>Target Box</label>
      <select name="target_box_id" required>
        <option value="" selected disabled>— Please select —</option>
        {% for r in boxes %}
          <option value="{{ r['box_id'] }}">{{ r['label'] }}</option>
        {% endfor %}
      </select>
    </div>
    <div style="flex:1 1 100%;"></div>
    <div style="flex:1 1 100%;">
      <label>Select Items</label>
      <div class="muted">Tip: Use Ctrl/Cmd+F in the browser to search by item or current box label.</div>
      <div style="max-height:320px; overflow:auto; border:1px solid #2a2f3c; border-radius:10px; padding:8px;">
        {% for i in items %}
          <label style="display:block;"><input type="checkbox" name="item_ids" value="{{ i['item_id'] }}"> [{{ i['box_label'] }}] {{ i['item'] }}</label>
        {% endfor %}
      </div>
    </div>
    <div style="flex:1 1 100%;">
      <button class="btn primary">Move Selected</button>
    </div>
  </form>
</div>
"""

TPL_SEARCH = r"""
<div class="card">
  <h2>Search Items</h2>
  <form action="{{ url_for('ui.items_search') }}" method="get" class="row" style="gap:8px; max-width:560px;">
    <input type="text" name="q" placeholder="e.g. kettle, HDMI cable, Christmas" value="{{ q }}" required>
    <button class="btn">Search</button>
    {% if session.get('logged_in') %}
      <a class="btn primary" href="{{ url_for('ui.item_new') }}">+ New Item</a>
    {% endif %}
  </form>
</div>

{% if q %}
  <div class="grid">
    {% for r in rows %}
      <div class="box">
        <img src="{{ url_for('images.photo_item', item_id=r['item_id']) }}" alt="">
        <div style="padding:12px;">
          <div><strong>{{ r['item'] }}</strong></div>
          <div class="muted">Box: {% if r['box_id'] %}<a href="{{ url_for('ui.box_detail', box_id=r['box_id']) }}">{{ r['box_label'] }}</a>{% else %}(Unassigned){% endif %}</div>
          {% if session.get('logged_in') %}
            <div style="margin-top:8px;">
              <a class="btn" href="{{ url_for('ui.item_edit', item_id=r['item_id']) }}">Edit</a>
              <form method="post" action="{{ url_for('ui.item_delete', item_id=r['item_id']) }}" style="display:inline" onsubmit="return confirm('Delete this item?');">
                <button class="btn bad">Delete</button>
              </form>
            </div>
          {% endif %}
        </div>
      </div>
    {% endfor %}
  </div>
{% endif %}
"""
