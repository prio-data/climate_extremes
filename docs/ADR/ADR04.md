# ADR 4: Resampled Resolution Factor

## Context
The climate extremes data from the Copernicus Data Store is provided at a specific resolution, determined by the model used (e.g., HADGEM). A decision is required on how to resample these rasters to a different resolution, if needed.

## Decision
The resample factor has been set based on the model's output resolution. This factor ensures that data consistency is maintained while allowing flexibility for different analysis needs.

## Considerations
- The model resolution is fixed, and resampling allows flexibility for downstream processing.
- The resampling factor should be chosen based on the specific application and granularity required.
- A parameter is introduced to allow users to change the resampled unit.

## Consequences
- By allowing resampling, we maintain model consistency while providing flexibility for different workflows.
- Potential loss of accuracy when downsampling.

