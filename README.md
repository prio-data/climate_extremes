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

## Project Description: VIEWS FOA_Index

**Anticipating Future Developments to Mitigate Human Suffering**

In a world increasingly characterized by complex, interlinked crises, the ability to forecast and respond to emerging violent conflicts is critical. The **Violence & Impacts Early-Warning System (VIEWS)** is designed to provide reliable and actionable conflict forecasts. By doing so, VIEWS aims to empower organizations to mobilize resources and implement timely interventions that mitigate human suffering and protect human dignity.

**Leveraging Advanced Analytics for Conflict and Food Crisis Forecasting**

Recent global crises, such as the COVID-19 pandemic and the war in Ukraine, have underscored the fragile balance of food security and the potential for conflict to exacerbate humanitarian emergencies. The VIEWS FOA_Index project addresses this challenge by focusing on the intersection of conflict forecasting and disaster risk financing, particularly in preventing food crises.

**The Conflict and Food Crisis Nexus**

The FAO's role in this project is to develop a robust analytical framework that monitors violent conflicts and anticipates their potential to trigger food crises. The goal is to create an index that identifies spikes in conflict, which can then be used as a trigger for parametric insurance mechanisms designed to prevent food crises from escalating into full-blown famines.

**Strategic Importance**

The VIEWS FOA_Index project contributes to the broader objective of developing a disaster risk financing structure. This structure is intended to provide rapid, preemptive financing in response to early signs of food crises, ensuring that resources are available when they are most needed, and before the situation deteriorates into famine.

**Next Steps and Vision**

As the project advances, efforts will focus on refining analytical methods, validating trigger mechanisms with stakeholders, and scaling the approach to additional countries. The ultimate goal is to develop a scalable, adaptable system that integrates conflict forecasting with humanitarian financing, thereby enhancing global preparedness and response to food crises.


## Repository Structure

```

|-- FAO_index/
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
    |   |-- timelapse/
    |   |-- papers/
    |   |-- presentations/
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
    git clone https://github.com/your-repo-url/FAO_index.git
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

## License

This project is licensed under the MIT License. See the [LICENSE.md](./LICENSE.md) file for more details.

## Google Cloud Storage data links (currently for internal development)

----
### Main files
- **df_monthly_country_return_periods.csv**: [Download CSV](https://storage.googleapis.com/views-fao_bucket_01/data/generated/df_monthly_country_return_periods.csv)
- **df_monthly_country_return_periods.pkl**: [Download PKL](https://storage.googleapis.com/views-fao_bucket_01/data/generated/df_monthly_country_return_periods.pkl)
- **df_yearly_country_return_periods.csv**: [Download CSV](https://storage.googleapis.com/views-fao_bucket_01/data/generated/df_yearly_country_return_periods.csv)
- **df_yearly_country_return_periods.pkl**: [Download PKL](https://storage.googleapis.com/views-fao_bucket_01/data/generated/df_yearly_country_return_periods.pkl)
