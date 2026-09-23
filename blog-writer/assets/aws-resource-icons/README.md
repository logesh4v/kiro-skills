# AWS resource icons

All 513 SVGs are imported unmodified from the `Resource-Icons_07312026`
folder in AWS's official Q3 2026 Architecture Icons package:
https://aws.amazon.com/architecture/icons/

`MANIFEST.json` records file, resource name, category, and whether the source
asset is light-theme, dark-theme, or category-coloured. Use these only when
the diagram needs resource-level precision — for example public/private
subnets, an EC2 instance, an IAM role, an S3 bucket, or a Lambda function.
Use `assets/aws-icons/` for service-level nodes.

Update both corpora from the same official ZIP:

```bash
python3 scripts/import_aws_icons.py /path/to/Icon-package_MMDDYYYY.zip
python3 scripts/import_aws_resource_icons.py /path/to/Icon-package_MMDDYYYY.zip
```

AWS's terms govern these files. Do not redraw or recolour them.
