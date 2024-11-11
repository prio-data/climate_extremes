# Define a function to generate the request

def generate_and_validate_request(variable, product_type, experiment, temporal_aggregation):
    # Define the allowed values (could be moved to a global variable or constant for reuse)
    allowed_values = {
        "product_type": {
            "base_period_1961_1990": [
                "cold_days", "cold_nights", "warm_days", "warm_nights"
            ],
            "base_independent": {
                "options": [
                    "consecutive_dry_days",
                    "consecutive_wet_days",
                    "diurnal_temperature_range",
                    "frost_days",
                    "growing_season_length",
                    "heavy_precipitation_days",
                    "ice_days",
                    "maximum_1_day_precipitation",
                    "maximum_5_day_precipitation",
                    "maximum_value_of_daily_maximum_temperature",
                    "minimum_value_of_daily_maximum_temperature",
                    "maximum_value_of_daily_minimum_temperature",
                    "minimum_value_of_daily_minimum_temperature",
                    "number_of_wet_days",
                    "simple_daily_intensity_index",
                    "summer_days",
                    "total_wet_day_precipitation",
                    "tropical_nights",
                    "very_heavy_precipitation_days"
                ],
                "yearly_only": ['summer_days',
                                'frost_days',
                                'consecutive_dry_days',
                                'very_heavy_precipitation_days',
                                'simple_daily_intensity_index',
                                'ice_days',
                                'tropical_nights',
                                'number_of_wet_days',
                                'heavy_precipitation_days',
                                'total_wet_day_precipitation',
                                'growing_season_length',
                                'consecutive_wet_days'
                                ]  # variables that can only be yearly
            }
        },
        "experiment": ["Historical", "ssp1_2_6", "SSP2_4_5", "SSP5_8_5"],
        "temporal_aggregation": {
            "monthly": {
                "Historical": ["185001-201412"],
                "ssp1_2_6": ["201501_210012"],
                "SSP2_4_5": ["201501_210012"],
                "SSP5_8_5": ["201501_210012"]
            },
            "yearly": {
                "Historical": ["1850-2014"],
                "ssp1_2_6": ["2015-2100"],
                "SSP2_4_5": ["2015-2100"],
                "SSP5_8_5": ["2015-2100"]
            }
        },
        "data_format": "netcdf"
    }

    # Generate the request dictionary
    request = {
        "variable": [variable],
        "product_type": [product_type],
        "model": ["hadgem3_gc31_ll"],
        "ensemble_member": ["r1i1p1f3"],
        "experiment": [experiment],
        "temporal_aggregation": [temporal_aggregation],
        "period": ["201501_210012"] if temporal_aggregation == "monthly" else ["1850-2014"],  # Update period based on temporal_aggregation
        "version": ["2_0"],
        "data_format": "netcdf"
    }

    # Validate the request
    product_type = request["product_type"][0]
    variable = request["variable"][0]
    
    # Check if the product_type is valid
    if product_type not in allowed_values["product_type"]:
        raise ValueError("Invalid product_type. Must be 'base_period_1961_1990' or 'base_independent'.")
    
    # Validate variable based on product_type
    if product_type == "base_period_1961_1990":
        if variable not in allowed_values["product_type"]["base_period_1961_1990"]:
            raise ValueError("Invalid variable for product_type 'base_period_1961_1990'. Must be one of ['cold_days', 'cold_nights', 'warm_days', 'warm_nights'].")
    elif product_type == "base_independent":
        if variable not in allowed_values["product_type"]["base_independent"]["options"]:
            raise ValueError("Invalid variable for product_type 'base_independent'. Must be one of "
            "'summer_days', 'frost_days', 'consecutive_dry_days', "
            "'very_heavy_precipitation_days', 'simple_daily_intensity_index', "
            "'ice_days', 'tropical_nights', 'number_of_wet_days', "
            "'heavy_precipitation_days', 'total_wet_day_precipitation', "
            "'growing_season_length', 'consecutive_wet_days'.")
        
        # Check if 'ww' or 'yy' are being used with 'monthly'
        if variable in allowed_values["product_type"]["base_independent"]["yearly_only"]:
            if request["temporal_aggregation"][0] == "monthly":
                raise ValueError(f"Variable '{variable}' cannot be computed with monthly temporal aggregation.")
    
    # Check experiment is valid
    if request["experiment"][0] not in allowed_values["experiment"]:
        raise ValueError("Invalid experiment. Must be one of 'Historical', 'ssp1_2_6', 'SSP2_4_5', or 'SSP5_8_5'.")

    # Check temporal_aggregation
    temporal_agg = request["temporal_aggregation"][0]
    if temporal_agg not in allowed_values["temporal_aggregation"]:
        raise ValueError("Invalid temporal_aggregation. Must be 'monthly' or 'yearly'.")

    # Set valid periods based on experiment and temporal aggregation
    experiment = request["experiment"][0]
    valid_periods = allowed_values["temporal_aggregation"][temporal_agg].get(experiment)
    
    if valid_periods is None:
        raise ValueError(f"No valid periods for {temporal_agg} aggregation and experiment '{experiment}'.")
    
    if request["period"][0] not in valid_periods:
        raise ValueError(f"Invalid period for {temporal_agg} aggregation with experiment '{experiment}'. Must be one of {valid_periods}.")

    print("Request is valid.")
    return request