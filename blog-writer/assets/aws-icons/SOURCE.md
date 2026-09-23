# AWS icon source and update record

The `Arch_*_64.svg` files in this directory come from the official AWS
Architecture Icons package — not a community mirror.

- **Release:** Q3 2026, published 31 July 2026
- **Package:** `Icon-package_07312026.zip`
- **Official page:** https://aws.amazon.com/architecture/icons/
- **Official CDN:** `d1.awsstatic.com/onedam/marketing-channels/website/public/shared/architecture-icon-release/`
- **Imported:** 24 September 2026
- **Coverage:** all 303 uniquely named 64px Architecture Service SVGs in the
  package, plus the separately sourced Strands Agents mark

The AWS ZIP contains 305 service-icon entries but two duplicate filenames:

- `Arch_AWS-Compute-Optimizer_64.svg` appears under Compute and Management
  Tools; this bundle keeps the Management Tools export.
- `Arch_Amazon-Kinesis-Video-Streams_64.svg` appears under Analytics and Media
  Services; this bundle keeps the Analytics export.

The duplicates differ in category colour, not service identity. Keeping one
canonical file avoids ambiguous manifest keys without losing a service.

## Quarterly update

AWS says icon packages ship at the end of January, April and July. Download the
new **Icon package** from the official page, then run from `blog-writer/`:

```bash
python3 scripts/import_aws_icons.py /path/to/Icon-package_MMDDYYYY.zip
python3 ../tests/validate_skill.py
```

The importer replaces only `Arch_*.svg`; it preserves the Strands mark. Review
removed and renamed files in the Git diff, update this record, render every
layout template, and open each PNG before merging.

AWS's terms govern these icon files. Do not recolour, redraw or use them to
imply AWS endorsement.
