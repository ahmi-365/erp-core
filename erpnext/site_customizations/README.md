# ERPNext site customizations

This export contains the Station master and accounting dimension, Station fields and reports,
the Inward Gate Pass and Buying form scripts, and the Buying, Setup, and Inventory navigation.
It was exported from ERPNext 16.53.0 on Frappe 16.55.1.

Install ERPNext on the destination site and make this package available in its bench. Back up the
destination before importing. Run a dry run first to check for conflicting customizations.

```sh
bench --site <site> execute erpnext.site_customizations.install.apply
bench --site <site> execute erpnext.site_customizations.install.apply --kwargs '{"dry_run": false}'
```

The installer skips matching records and stops if an existing customization differs. The export
contains configuration only. To move Station records, transactions, users, or uploaded files,
migrate the original site with a database and files backup.
