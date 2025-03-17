# ADR 8: Raster Query Process and Granularity

## Context
The raster data returned by the query process appears grainy compared to the original GeoTIFF resolution. This requires an understanding of the product's resolution and why it appears different.

## Decision
The grainy appearance of the raster is a result of the query process applied to the data. This granularity can be due to downsampling during the query or limitations in the underlying data resolution.

## Considerations
- The granularity of the raster is dependent on the query parameters and the data resolution.
- This issue can be mitigated by refining the query process or adjusting the resolution at the resampling step.

## Consequences
- Users will be aware that the "graininess" is an expected result of querying data at lower resolution.
- To improve clarity, the process for querying and its effects on resolution should be documented.
