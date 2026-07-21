# Security and ingestion policy

All external content is untrusted input.

- Do not execute, source, import, install, or activate discovered code.
- Do not expose repository, organization, runner, or user secrets to ingestion jobs.
- Fetch only allowlisted first-party endpoints.
- Store provenance: canonical URL, retrieval timestamp, upstream revision, and SHA-256 digest.
- Flag binaries, obfuscated content, install hooks, network side effects, credential access, and persistence behavior.
- Require human review before expanding the allowlist or changing automation permissions.
