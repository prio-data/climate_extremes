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


3. **Download Raw Data**

    Use the provided scripts under `src/dataloaders/` to download the raw data required for analysis.

## Documentation

For more detailed information, refer to the following documents located in the `docs/` directory:

- **ADRs**: Architectural Decision Records that document the project's key decisions.
- **Glossary**: Definitions of key terms used throughout the project.
- **Guide to Git in VS Code**: Step-by-step guide for working with Git in Visual Studio Code.
- **Contributing Guide**: Instructions on how to contribute to the project.
- **Code of Conduct**: Expected behavior guidelines for contributors.

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



## License

This project is licensed under the MIT License. See the [LICENSE.md](./LICENSE.md) file for more details.

## Google Cloud Storage data links (currently for internal development)

----
### Main files
- **Priogrid Shapefile**: [Download shp](https:// ....)
