# ARISE 2.1 — Financial Intelligence

ARISE 2.1 is an evolution of the original ARISE 1.2 project. The visual design, Liquid Glass styling, page structure, and interaction patterns are intentionally preserved.

## Added infrastructure
- Daily scheduled data refresh via GitHub Actions.
- Cached daily FX rates from Frankfurter (EUR base, listed currency set).
- Cached financial-news feed snapshot from GDELT.
- Client-side live fetch remains first choice; cached `data.json` is used as fallback when a provider is unavailable.
- Honest source date and fallback status; no fabricated quotes.

## Deploy
Commit all files at repository root, including `.github/workflows/deploy.yml` and `.github/workflows/data-refresh.yml`. Enable GitHub Pages with **GitHub Actions** as the source.

## Automated refresh
The refresh workflow runs daily at 04:20 UTC and can also be started manually from the Actions tab. It updates `data.json` and commits it only when data changes.

## Data sources
- FX reference rates: Frankfurter API (daily reference data, not live trading quotes).
- News: GDELT DOC API (news aggregation; feed availability varies).
- Gold, oil, and equities: not yet wired to a validated keyless source in this release; they remain marked unavailable rather than displaying invented values.

Educational information only; not investment advice.
