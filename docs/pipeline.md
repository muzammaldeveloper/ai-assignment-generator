# Assignment Pipeline

## Stages

1. Research
2. Outline
3. Draft
4. Image Generation
5. Export (DOCX/PDF)

## Reliability

- Retries for external provider failures
- Clear status transitions for each stage
- Failure reason persistence for troubleshooting

## Improvements

- Idempotency keys to prevent duplicate jobs
- Provider fallback chain for resilience
- Queue routing by task type
