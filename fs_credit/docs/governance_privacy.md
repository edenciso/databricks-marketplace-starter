# Governance & Privacy — fs_credit

- **No PII**. Merchants are represented by salted hashes.
- **k-anonymity**: enforce k≥100 for region×MCC×day cells.
- **Differential privacy**: Laplace noise on rare cells; publish ε in listing.
- **Access**: Read-only via Delta Sharing; revocable at any time.
- **Lineage**: Publish data contracts and change logs with 30-day notice for breaking changes.
