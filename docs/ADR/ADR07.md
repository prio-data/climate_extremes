# ADR 7: Processing Extent

## Context
The Ingester has access to the full set of global Priogrid ID values and maintains the coordinate center points for each grid cell. Referencing these latitude and longitude values, both methods (`resample` and `raster_query`) construct a global shapefile grid that defines both the spatial extent referenced to translate climate extreme indices. This data, when ingested into the VIEWSER system, is then trimmed to the spatial extent defined by the database. 

## Decision
Programatically process at a global spatial extent, but consider only land cells to conserve space and processing time.


## Considerations
Producing independent global climate extreme indices at the standard Priogrid resolution enhances the functionality and utility of this procedure. While the novelty of the approach is modest, maximizing the processing extent increases its impact.  A global extent supports Peace Science Infrastructure (PSI) PRIOGrid research efforts and offers flexibility for other researchers considering a scope beyond Africa and Middle East regions.

## Consequences
Marginally increased processing time as this is done programmatically (not is mapping software).

