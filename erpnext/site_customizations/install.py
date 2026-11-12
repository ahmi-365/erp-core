import json
from pathlib import Path

import frappe


def _matches(doc, expected):
	for key, value in expected.items():
		actual = doc.get(key)
		if isinstance(value, list):
			actual = actual or []
			if len(actual) != len(value) or any(
				not _matches(row, values) for row, values in zip(actual, value, strict=True)
			):
				return False
		elif actual != value:
			return False
	return True


def _find_existing(values):
	doctype = values["doctype"]
	if doctype == "Custom Sidebar":
		return frappe.db.get_value(
			doctype, {"module": values["module"], "user": values["user"]}, "name"
		)
	return frappe.db.exists(doctype, values["name"])


def apply(dry_run=True):
	"""Install the exported customizations without overwriting differing records."""
	path = Path(__file__).with_name("configuration.json")
	config = json.loads(path.read_text(encoding="utf-8"))
	pending = []
	conflicts = []
	for documents in config.values():
		for values in documents:
			doctype = values["doctype"]
			name = _find_existing(values)
			if not name:
				pending.append(values)
			elif not _matches(frappe.get_doc(doctype, name), values):
				conflicts.append(f"{doctype}: {values.get('name') or values['module']}")

	if conflicts:
		frappe.throw("Existing customizations differ from the export:\n" + "\n".join(conflicts))

	if not dry_run:
		for values in pending:
			frappe.get_doc(values).insert()
		frappe.db.commit()

	return {
		"already_present": sum(map(len, config.values())) - len(pending),
		"pending" if dry_run else "installed": len(pending),
	}
