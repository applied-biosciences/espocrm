# NuriVoyage development rules

- Stage 1–2 work belongs on `codex/nurivoyage-stage-1-2`; never modify master directly.
- Do not edit EspoCRM core unless unavoidable; explain the reason and upgrade impact first.
- Use supported `custom/Espo/Custom` and `client/custom` resources and extensions.
- Never commit credentials, runtime config, database exports or `.env`.
- Use only synthetic development data, never production customer/passport data.
- Run `scripts/local smoke` before committing and include its actual result.
- Do not silently upgrade EspoCRM (10.0.10), MariaDB (11.4.5), or other pinned services.
- Preserve and document schema migrations in `docs/nurivoyage/migrations.md`.
- Document custom entities, fields and permissions in `docs/nurivoyage/stage-1-design.md`.
- Keep future AWS infrastructure in `infrastructure/terraform`; no AWS deployment in Stage 1–2.
- Use Espo's storage interface for documents: MinIO locally, S3-compatible configuration later.
- Human UAT is pending until a human records completion. Automated browser checks do not replace it.
