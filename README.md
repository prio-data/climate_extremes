# Copernicus ETCCDI Data to Prio Grid Resolution


![Project Banner](https://pbs.twimg.com/profile_banners/1237000633896652800/1717069203/1500x500)


## Contact

**Project Owner:**  
Garrett Benz  
[garben@prio.org](mailto:garben@prio.org)

**Team:**  
VIEWS Research  
[Pvesco@prio.org](mailto:pvesco@prio.org)

## VIEWS

The **Violence & Impacts Early-Warning System (VIEWS)** is a state-of-the-art machine learning-based system that forecasts inter- and intrastate conflicts globally, focusing on scenarios involving government-affiliated actors and projecting up to three years into the future. Supported by an integrated consortium, VIEWS spearheads cutting-edge research on conflict forecasting and the analysis of its social impacts while actively engaging with key policymakers and stakeholders through dedicated outreach and knowledge transfer initiatives.

## Project Description: 

**Relevance of ETCCDI Copernicus Climate Data in Conflict Analysis**
The ETCCDI (Expert Team on Climate Change Detection and Indices) Copernicus climate data provides a structured approach to quantifying 27 key climate extremes, offering a critical dataset for analyzing climate impacts over time. These indices, encompassing metrics like temperature extremes, precipitation variability, and duration of climate anomalies, are particularly relevant for assessing the environmental conditions that may contribute to conflict dynamics. ETCCDI data brings rigor and comparability to climate-related studies by standardizing climate impact metrics, which are essential in understanding how shifts in climate extremes compound vulnerabilities across different regions. For conflict analysis, having access to this high-quality, standardized data forms a baseline for integrating climate data with socioeconomic and conflict indicators in a scientifically robust way.

**Impact of a Standardized Measurement Platform**
A platform that translates ETCCDI climate data to a standard unit of measure for conflict analysis has transformative potential. Such a platform would allow for the seamless integration of climate indices with other meaningful variables, including population density, agricultural yield, and existing conflict incidents, all within a unified resolution. This integration is key to isolating and mapping the compounded effects of climate and conflict on socioeconomic stability. By providing a standardized measurement framework, the platform enables researchers and policymakers to track, visualize, and compare the impact of climate extremes across diverse regions and contexts. This standardized approach is instrumental for building transparent, replicable methods, setting a benchmark for future climate-conflict research.

**Advancing Climate Security through Transparent Preprocessing**
This research project adds value by contributing a preprocessing layer that aligns climate and conflict data for use in predictive modeling. Although preprocessing ETCCDI data for conflict applications may not be analytically complex, it is a crucial step in ensuring data compatibility, transparency, and reproducibility. By harmonizing climate indices with high-resolution socioeconomic variables, the VIEWS research team can push the state of the art in climate security modeling. This approach enables a nuanced understanding of how climate extremes can exacerbate existing vulnerabilities in regions susceptible to conflict, facilitating proactive, data-driven policy responses. By featuring transparent methods and maintaining consistent standards across datasets, this project strengthens the reliability and applicability of climate-conflict research.

**Next Steps**

## Repository Structure

```
|-- ETCCDI_index/
    |-- README.md
    |-- LICENCE.md
    |-- .gitignore
    |-- requirements.txt
    |
    |-- docs
    |    |-- ADRs/
    |    |-- glossary.md
    |    |-- guide_to_git_in_vs_code.md
    |    |-- CONTRIBUTING.md
    |    |-- CODE_OF_CONDUCT.md
    |
    |-- configs/
    |
    |-- data/
    |    |-- raw_viewser/    % Store unprocessed VIEWSER data here
    |    |-- raw_external/
    |    |-- processed/
    |    |-- generated/
    |
    |-- notebooks/    % All your notebooks go here 
    |
    |-- reports/
    |   |-- plots/
    |
    |
    |-- src/
        |- dataloaders/    % Scripts for downloading viewser data
        |- architectures/
        |- utils/
        |- visualization/
        |- training/
        |- evaluation/
```

## Getting Started

### Prerequisites

To get started with this project, ensure that you have the following:

- **Git:** Installed to clone the repository.
- **Python Environment:** Use a virtual environment or Conda environment with the necessary packages.
- **CDS Login Credentials:**
- **CDS API Setup:** 

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/prio-data/climate_extremes.git
    ```

2. **Set Up the Environment**

    Ensure you have the necessary Python environment configured, specifically the latest `viewser` environment. If you don't have this set up, please contact us at [info@viewsforecasting.org](mailto:info@viewsforecasting.org) to inquire about getting access.

    ```bash
    conda activate viewser
    ```  

3. **Python Dependencies**
    The required Python packages can be installed using the provided `requirements.txt` file. To install them, run:
    
    ```bash
    pip install -r requirements.txt
    ```  

### Getting Started (Review before running `main.py`)
1. **Consult ETCCDI Index Options**
    Please reference the user guide provided by ECMWF:
    https://confluence.ecmwf.int/display/CKB/Climate+extreme+indices+and+heat+stress+indicators+derived+from+CMIP6+global+climate+projections%3A+Product+User+Guide


2. **Temporal Dimension**

The code will prompt you to define the temporal range for this process. If `yearly` is selected, a monthly value must still be provided because the raw netCDF format includes a month field. Typically, for annual indices, a value of `06` is used, which acts as a placeholder for completeness but does not relate to June.


3. **Analytic Decisions**

#### Consult the EDA documents for primary considerations two methodological parameter selections.

A TLDR is provided here: 

We recommend using `resample` as the default method for processing the primary data in VIEWSER. For future applications involving model comparisons or validations, the `raster_query` method, which preserves the original resolution, is preferred.

## Run Main.py

    ```bash
    python main.py
    ```  

## After Running the Script

Migrate workflow toward **VIEWSER Data Ingestion** using the existing github repo: https://github.com/UppsalaConflictDataProgram/ingester3_loaders.git 

The appropriate ingestion notebook for this process is located under the ETCCDI folder.

## Documentation

For more detailed information, refer to the following documents located in the `docs/` directory:

- **ADRs**: (Architectural Decision Records) that document the project's key decisions.
- **EDAs**: (Exploratory Data Analysis) refer to reports that uncover important findings during data preprocessing or identify key metadata attributes. These insights are valuable as they may influence Architectural Decision Reports (ADRs) by highlighting aspects of the data that need special consideration.
- **Glossary**: Definitions of key terms used throughout the project.

## Requirements

Before using this repository, ensure the following tools and dependencies are installed:

### Tools
The following tools may need to be installed separately to ensure full functionality:
- **CDS Tools**: Used for data processing and access through Copernicus. [Installation Guide](https://cds.climate.copernicus.eu/)
- **[Tool/Library Name]**: Brief description of its purpose.

### Python Dependencies
The required Python packages can be installed using the provided `requirements.txt` file. To install them, run:
```
bash
pip install -r requirements.txt
```  

## Maintenace Considerations

- Ensure the **reference table** adjusts to changes in the spatial extent of PRIOgrid. That is, when VIEWS migrates to global coverage, a new reference file should be constructed. This is redundant to what the ingester accomplishes, the added value of keeping this reference file updated is validating tables for analytic use that are not intended to be ingested.

## License

a) The ETCCDI and heat stress indicators (HSI) for CMIP6 historical and future scenarios are available free of charge from the Copernicus Climate Data Store.
b) These data are strictly for use in non-commercial research and education projects only. Scientific results based on these data must be submitted for publication in the open literature without delay.
c) Although care has been taken in preparing and testing the data products, we cannot guarantee that the data are correct in all circumstances; neither do we accept any liability whatsoever for any error or omission in the data products, their availability, or for any loss or damage arising from their use.

## API Considerations
- Maintain awareness of potential **API changes**:

While running the `main.py` code, you will be prompted to make a series of selections that will construct an API 'request'. This retrieval process is programmatic, but the primary considerations are built into the `.py` file `define_request.py`. 


Presently, the only hardcoded parameters are:
1. the model selection `hadgem3_gc31_ll`
    - (and corresponding ensemble member) `r1i1p1f3`
2. Version number `2_0`
3. Delivery format `netcdf`

```
request = {
        "variable": [variable],
        "product_type": [product_type],
        "model": ["hadgem3_gc31_ll"],
        "ensemble_member": ["r1i1p1f3"],
        "experiment": [experiment],
        "temporal_aggregation": [temporal_aggregation],
        "period": [period],
        "version": ["2_0"],
        "data_format": "netcdf"
    }
```

In the process of retrieving the desired dataset, the Copernicus Data Store generates an automated message: 

CDS API syntax is changed and some keys or parameter names may have also changed. To avoid requests failing, please use the "Show API request code" tool on the dataset Download Form to check you are using the correct syntax for your API request.

This is a caution that the request parameters may adapt, but is not an alert that some parameter is incompatible, which should result in a failed script and informative error message. Steps have been taken to mitigate the consequence of this potential hazard and keep future processing of these climate extremes data highly efficient. 

the first prompt of the main.py inquires whether you want to construct the API request using the terminal prompts [y/n]. A `n` response (no) indicates you will produce a valid request, saved to the `request.txt` file. This option allows the code to continue to function with minimal adjustment or added adversity. The user will navigate to the cds store and construct an API request from within the system. This ensures a valid API call is produced irrespective of the considerations.


If an issue is identified: 

first, reconstruct API request fromt he CDS with identical parameter selection and compare the elements to accepted parameters in the `allowed_values` dataframe (located within define_request.py file). Update this function and push changes if necessary.

second, investigate **CDS API forum** for transparency on updates. and     2. Contact CDS to determine their API update schedule (e.g., every 6 months or yearly).

temporarily proceed with the .txt file but document the issue. 

