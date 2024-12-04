# Nominal Resolution Consistency Across Indicators

## Context
In the Copernicus Data Store, climate extremes data is presented with a fixed resolution determined by the model, not the indicator. This raises the question of whether the nominal resolution is consistent across all indicators.

## Decision
The nominal resolution is consistent across all indicators for a given model. The decision to resample the data will depend on this fixed model resolution, and the resample factor should be informed by the model metadata.

## Considerations
- The resolution is defined by the model, not the indicator.
- A parameter is provided to change the resample factor, ensuring flexibility in resampling to a desired resolution.
- For details on the decision to use the HADGEM model, consult ADR (x).

## Consequences
- Resampling should be done carefully to avoid inconsistencies across indicators.
- Flexibility in adjusting the resolution is preserved.

