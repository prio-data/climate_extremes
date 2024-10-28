def find_etccdi_timeindex(specified_year, specified_month, ds):
    """
    Finds the index of a specified month in a specified year in a NetCDF dataset.
    If the exact month is not found, it locates the index of the first month found in that year.

    Parameters:
        specified_year (str): The year to search for (e.g., '1990').
        specified_month (str): The month to search for (e.g., '01' for January).
        ds: The NetCDF dataset to search through.

    Returns:
        None
    """
    # Extract the time coordinate
    time_values = ds['time'].values  # Get the time coordinate values
    # Convert to string format to extract year and month
    time_strings = [str(t) for t in time_values]

    # Initialize variables to track indices and found months
    specified_month_index = None
    first_month_index = None

    # Search for any month in the specified year
    for idx, date in enumerate(time_strings):
        year, month, _ = date.split('-')  # Split to get year and month
        if year == specified_year:
            # Track the first month found
            if first_month_index is None:
                first_month_index = idx
            
            # Check for the specified month
            if month == specified_month:
                specified_month_index = idx  # Store the specified month index
                break  # Break immediately if specified month is found

    # Validate the results
    if specified_month_index is not None:
        # Confirm that the index corresponds to the specified month
        year_check, month_check, _ = time_strings[specified_month_index].split('-')
        print(f"Index of {specified_month} data for year {specified_year}: {specified_month_index}")
        print(f"Validation: Found data for Year: {year_check}, Month: {month_check} at index {specified_month_index}.")
        return(specified_month_index)
    else:
        # If the specified month data is not found, check if any month data exists
        if first_month_index is not None:
            print(f"No data found for {specified_month} of the year {specified_year} but located data for the first available month.")
            # Validate the first month found
            year_check, month_check, _ = time_strings[first_month_index].split('-')
            print(f"Validation: Found data for Year: {year_check}, Month: {month_check} at index {first_month_index}.")
            return(first_month_index)

        else:
            print(f"No data found for the year {specified_year}.")
            return(None)