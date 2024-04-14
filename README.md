# Pywikibot Additional Scripts

This repository contains some additional scripts, intend to expand the functionality of the official bundle.

## Prerequisites
* A normally functional pywikibot instance.

## How to use
1. Clone this repository: `git clone https://github.com/bilintsui/pywikibot-scripts.git`
2. Copy or link `.py` files in `scripts` directory to your pywikibot's `scripts` directory (you can also consider put it into `scripts/userscripts`).
3. Copy directory `script/i18n` to your pywikibot's `scripts` directory (if you choose `scripts/userscripts` in the step above, put it io `scripts/userscripts/i18n`, then link to `scripts/i18n`).
4. Execute scripts with `./pwb.py <script_name> ...` (you can use `./pwb.py <script_name> -help` to get script helps).

## Provided scripts
1. `create_redirect`: Create redirect page in page-target pair, single or in batch.
