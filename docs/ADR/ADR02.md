# ADR 002: Deployment of Two Methods for Translating ETCCDI Copernicus Data Store Climate Indices

## Status  
Accepted

---

## Context  
The ETCCDI Copernicus Data Store climate indices are provided as rasters with a coarse native resolution. Translating these data to align with the PRIOgrid framework requires a decision on how to handle their spatial resolution. Two methods have been chosen for deployment:  
1. **Resampled Raster**: Produces a significantly finer-grained resolution (~20x finer) using bilinear resampling.  
2. **Original Resolution Raster**: Preserves the original resolution, assigning the nearest PRIOgrid cell center to the closest raster cell center value.

Each method serves different analytical purposes, catering to users with varying needs for spatial granularity and data preservation.

---

## Decision  
- **Option 1: Resampling**  
  - Bilinear resampling is applied to disaggregate the original raster resolution into a significantly finer resolution.  
  - The resampled raster provides a more detailed view, although it is not informed by deeper learning models or assumptions about finer-scale spatial relationships.

- **Option 2: Original Resolution**  
  - The raster is maintained at its native resolution.  
  - Values are directly assigned to the nearest PRIOgrid cell center, preserving the original spatial integrity of the data.  

Both methods will be generated and stored to allow for flexibility in downstream use.

---

## Rationale  
### Method 1: Resampling  
- **Granularity**: Provides a more detailed spatial dataset, offering a "best guess" for finer-scale values without completely uninformed assumptions.  
- **Informed Resampling**: The bilinear approach uses adjacent values to create a smooth, coherent result, though it does not guarantee rigorously accurate finer-scale spatial relationships.  
- **Utility**: Useful for analyses requiring finer-grained spatial inputs when the original resolution is too coarse for meaningful interpretation.  

### Method 2: Original Resolution  
- **Preservation**: Maintains the original data's resolution and spatial extent, ensuring compatibility with the PRIOgrid vector format.  
- **Spatial Gaps**: Retains the spatial distribution of `NaN` values, which are closely aligned with PRIOgrid's gaps.  
- **Non-Interpolation**: Appeals to users who prefer to work only with the original data values, avoiding any interpolation.

---

## Consequences  
### Positive  
1. **Flexibility**: Two outputs cater to different analytical needs, allowing users to choose the most appropriate resolution.  
2. **Preservation**: Original resolution ensures fidelity to the native data, particularly for users concerned with minimizing assumptions.  
3. **Granularity**: Resampled data offers a more detailed spatial perspective for exploratory analysis.

### Negative  
1. **Inconsistency**: Spatial gaps may differ between the original and resampled data due to resolution mismatches, potentially complicating comparisons.  
2. **Accuracy Tradeoff**: Resampled data might imply finer-scale accuracy that is not inherently supported by the original dataset.  
3. **Storage Overhead**: Generating and storing two versions of the data increases computational and storage demands.

---

## Implementation Notes  
- **Folder Structure**: 
