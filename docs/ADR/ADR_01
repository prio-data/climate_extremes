# ADR 001: Storage and File Structure for Multi-Year Geotiff Processing

## Status  
Accepted

---

## Context  
When processing multi-year `.tif` files, each temporal period generates two types of raster outputs:  
1. **Original Raster**: The initial raster file, with `-9999` assigned to any null values.  
2. **Upsampled Raster**: A processed raster with finer-grain resolution.

These outputs need to be stored in a way that facilitates easy access for validation, further analysis, or deletion if they are no longer needed. 

---

## Decision  
- **Original Raster TIFFs**: Save in a designated folder, ensuring null values are replaced with `-9999`.  
- **Upsampled Raster TIFFs**: Save in a separate folder to distinguish processed files.  
- Each temporal period (e.g., year or month) will generate uniquely named output files to avoid overwriting and to maintain clear version control.  

---

## Rationale  
- **Referencing**: Keeping original and processed files separate allows for immediate reference during validation or additional analysis.  
- **Cleanup**: Segregated storage simplifies the deletion of either type of file if they are no longer needed, conserving disk space.  
- **Traceability**: Unique naming conventions for temporal outputs ensure traceability of generated files across the years.  

---

## Consequences  
### Positive  
1. Files are organized and easy to locate for debugging or reuse.  
2. Validation workflows are streamlined with distinct folders for original and processed outputs.  
3. Unnecessary files can be deleted without affecting other outputs.  

### Negative  
1. Increased disk space usage due to storing both original and upsampled versions.  
2. Potential for higher organizational overhead if naming conventions are not followed consistently.  

---

## Implementation Notes  
- Folder structure:
