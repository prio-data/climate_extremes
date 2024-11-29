## Decision Tree Development
- Create a **decision tree for defensible methods** based on different applications:
    - If performing at an admin or country scale, use method X.
    - Address the question: "At what scale does the utility of finer-grained PRIOgrid data diminish?"
    - Incorporate considerations of 'other' shapefile extents.

## API Considerations
- Investigate potential **API changes**:
    1. Ensure the `define_request.py` script is correctly referenced.
    2. Contact CDS to determine their API update schedule (e.g., every 6 months or yearly).
    3. Check the **CDS API forum** for transparency on updates.
    4. **Keep functionality of a .txt file to load an API Request copied directly from the CDS API.**

## Statistical Context
- Add **descriptive statistics**:
    - Include basic summary stats for the requested indices.
- Allow users to view country-specific data:
    - Avoid packaging into larger datasets.

## Additional Notes
- Add a **section in the documentation** clarifying how to migrate workflows toward ingestion smoothly.

## Incorporating Accurate PRIOgrid Extent
1. Incorporate accurate PG extent, informed by Jim's response:
    - Get this as a shapefile, or identify an ingestion-based method to apply shape geometries from the lat and long midpoints (once resolved by Jim) to avoid hosting a shapefile in the project.
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
