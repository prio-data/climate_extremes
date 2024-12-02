## Statistical Context
- Add **descriptive statistics**:
    - Include basic summary stats for the requested indices.
- Allow users to view country-specific data:
    - Avoid packaging into larger datasets.

## Incorporating Accurate PRIOgrid Extent

    - Currently, the parameter for extent is the shapefile. Identify from Jim if 'global' will have a similar ingester 'filter' that exists for:
        1. Continents
        2. Regions
    - If this will be incorporated, then this parameter should be changed to match the ingester filter parameter.
    - However, this would still require the unit shape field, and it is not yet understood if this can be directly pulled from existing ingester code or whether a shapefile should be maintained in the repo directory for this reason.

## Approve Filename Structure 
1. Approve the filename structure of:
    - The output climate extreme CSV.
    - The Summary PDF.
    - Incorporate broad summary statistics into the PDF.
2. (Optional) Incorporate an activity log tracking meaningful attributes about which processes have recently been computed and the considered parameters to aid quick reference about which variables (and respective parameters) are prepared for a batch 'ingestion.'

3. This needs to be an ADR!

## Notes to add to the scipt:
1. add a print() line when building the scaffolders as this may take several minutes
