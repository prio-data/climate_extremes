# ADR: Resampling Method for Raster Data

## Context
In the context of resampling raster data to a finer resolution, we need to upscale the resolution by a factor of 10. This results in a grid that has 10 times the number of rows and columns compared to the original raster data, corresponding to a higher resolution 'below' the PRIOgrid resolution. The goal is to maintain as much spatial coherence as possible when increasing the resolution of the raster data.

The resampling process involves adjusting the spatial resolution of the data to match a new grid size, which can impact the quality and accuracy of the output. There are multiple methods to achieve this, each with its strengths and weaknesses.

## Decision
We have chosen **bilinear resampling** for this task. The resampling operation is performed using the `rasterio` library, where we scale the resolution of the raster data by a factor of 10. The following code line implements bilinear resampling to achieve this:

```python
# Resample the raster data to the new resolution
resampled_raster = raster_data.rio.reproject(
    raster_data.rio.crs,
    shape=(
        int(raster_data.shape[1] * 10),  # Increase number of rows by a factor of 10
        int(raster_data.shape[2] * 10)   # Increase number of columns by a factor of 10
    ),
    resampling=Resampling.bilinear  # Use the correct resampling method
)
``` 

## Alternatives Considered

### 1. Nearest Neighbor Resampling
- **Description**: The nearest neighbor method assigns the value of the nearest pixel from the original raster to each pixel in the resampled raster. It is computationally fast and preserves the original values of the raster.
- **Downsides**: While fast, this method can result in a blocky, stair-step effect that is not suitable for most cases where smooth transitions between pixel values are required, especially in continuous data (e.g., temperature, elevation).
- **Conclusion**: Not ideal for this use case, as it would likely produce undesirable artifacts in the resampled raster.

### 2. Cubic Convolution Resampling
- **Description**: Cubic convolution is a more advanced interpolation method that takes a larger neighborhood of pixels into account, resulting in smoother transitions.
- **Downsides**: While it can produce smoother results, cubic convolution is computationally more expensive and may introduce smoothing artifacts, which could be undesirable for raster data representing phenomena with sharp transitions (e.g., temperature gradients).
- **Conclusion**: While smoother, cubic convolution may be unnecessarily computationally expensive and potentially distort the data more than needed.

### 3. Lanczos Resampling
- **Description**: Lanczos is a high-quality resampling method that works by convolving the image with a sinc function, producing very sharp results.
- **Downsides**: Lanczos can create ringing artifacts (overshoot effects around edges), which can be problematic for certain types of data.
- **Conclusion**: Lanczos might be overkill for our needs and could introduce unwanted artifacts.

