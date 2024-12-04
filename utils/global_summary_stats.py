import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os
import pandas as pd

from pathlib import Path

def report_summary_stats(translated_filename):

    translated_filename

    project_root = Path.cwd()  # Set this to your project root manually if needed
    out_path = project_root / 'data' / 'generated' / 'index_table_output'
    extent_filename = out_path / translated_filename

    df = pd.read_csv(extent_filename)

    clim_value = translated_filename.split('_')[0]

    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))  # Create a date column (set to first day of month)
    df_annual = df.groupby('year')[clim_value].agg(
    mean='mean', 
    percentile_25=lambda x: x.quantile(0.25),  # 25th percentile
    percentile_90=lambda x: x.quantile(0.90)   # 90th percentile
    ).reset_index()

    # extreme highs -----------------------------------------------------------------------------
    # ----- MEAN -----
    top_3_annual_mean = df_annual.nlargest(5, 'mean')
    #top_3_annual_mean_years = top_3_annual_mean['year'].tolist()

    #give list of the desired attribute:
    # mean
    top_3_annual_mean_values = top_3_annual_mean['mean'].values  # Get the first 3 mean values or less
    # year
    top_3_annual_mean_years_list = top_3_annual_mean['year'].values

    # ----- 90th percentile -----

    top_3_max = df_annual.nlargest(5, 'percentile_90')
    #top_3_max_years = top_3_max['year'].tolist()

    #give list of the desired attribute:
    # 90th percentile
    top_3_max_values = top_3_max['mean'].values  # Get the first 3 mean values or less
    # year
    top_3_max_years_list = top_3_max['year'].values

    # ----- 25th percentile -----

    top_3_min = df_annual.nlargest(5, 'percentile_25')
    #top_3_min_years = top_3_min['year'].tolist()

    #give list of the desired attribute:
    # 25th percentile
    top_3_min_values = top_3_min['mean'].values  # Get the first 3 mean values or less
    # year
    top_3_min_years_list = top_3_min['year'].values

    # --------------------------
    # define how many index values should appear: -- This applies to both df1 and df2 (same length and the variable referenced does not matter, also same length)
    index_count = len(top_3_min_years_list)
    index_val = list(range(1, index_count + 1))  # Generate the index dynamically
    # --------------------------

    # --------------------------
    # Generate Extreme High Summary DF (1)
    # --------------------------

    df1 = pd.DataFrame({
        'year (25th)': top_3_min_years_list.tolist(),
        '25th': top_3_min_values.tolist(),
        'year (90th)': top_3_max_years_list.tolist(),
        '90th': top_3_max_values.tolist(),
        'year (mean)': top_3_annual_mean_years_list.tolist(),
        'mean': top_3_annual_mean_values.tolist()
    }, index=index_val)

    # -------------------------------------------------------------------------------------------
    # extreme lows -----------------------------------------------------------------------------

    # ----- MEAN -----

    bottom_3_annual_mean = df_annual.nsmallest(5, 'mean')
    #bottom_3_annual_mean_years = bottom_3_annual_mean['year'].tolist()

    #give list of the desired attribute:
    # mean
    bottom_3_annual_mean_values = bottom_3_annual_mean['mean'].values  # Get the first 3 mean values or less
    # year
    bottom_3_annual_mean_years_list = bottom_3_annual_mean['year'].values

    # ----- 90th percentile -----

    bottom_3_max = df_annual.nsmallest(5, 'percentile_90')
    bottom_3_max_years = bottom_3_max['year'].tolist()

    #give list of the desired attribute:
    # 90th percentile
    bottom_3_max_values = bottom_3_max['mean'].values  # Get the first 3 mean values or less
    # year
    bottom_3_max_years_list = bottom_3_max['year'].values

    # ----- 25th percentile -----

    bottom_3_min = df_annual.nsmallest(5, 'percentile_25')
    bottom_3_min_years = bottom_3_min['year'].tolist()

    #give list of the desired attribute:
    # 25th percentile
    bottom_3_min_values = bottom_3_min['mean'].values  # Get the first 3 mean values or less
    # year
    bottom_3_min_years_list = bottom_3_min['year'].values

    # --------------------------
    # Generate Extreme High Summary DF (1)
    # --------------------------

    df2 = pd.DataFrame({
        'year (25th)': bottom_3_min_years_list.tolist(),
        '25th': bottom_3_min_values.tolist(),
        'year (90th)': bottom_3_max_years_list.tolist(),
        '90th': bottom_3_max_values.tolist(),
        'year (mean)': bottom_3_annual_mean_years_list.tolist(),
        'mean': bottom_3_annual_mean_values.tolist()
    }, index=index_val)

    return(df_annual, df1, df2)



def plot_statistics(variable, df_annual, df1, df2):

    project_root = Path.cwd()  # Set this to your project root manually if needed
    output_folder = project_root / 'docs' / 'Graphics' / 'Standard_review'

    file_name = os.path.join(output_folder, f'{variable}_Summary_plots.pdf')

    print_title = f'Annual Data Report of Climate Extreme Variable: {variable} '

    # Sample data for the tables (5 rows, 3 columns)
    # Convert the first column to integers (no decimals)
    df1[df1.columns[0]] = df1[df1.columns[0]].astype(int)

    # Round all other columns to 2 decimal places
    df1.iloc[:, 1:] = df1.iloc[:, 1:].round(2)

    # Convert the first column to integers (no decimals)
    df2[df2.columns[0]] = df2[df2.columns[0]].astype(int)

    # Round all other columns to 2 decimal places
    df2.iloc[:, 1:] = df2.iloc[:, 1:].round(2)


    # Create a figure
    fig = plt.figure(figsize=(15, 10))  # Adjust the figure size to fit 5 columns and 3 rows

    # Create a GridSpec with 3 rows and 5 columns (equal sizes for all subplots)
    gs = GridSpec(3, 5)  # 3 rows, 5 columns

    # Create subplots in the grid
    ax2 = fig.add_subplot(gs[0, 1:4])  # Top-center-left subplot

    ax6 = fig.add_subplot(gs[1, 0:2])  # Middle-left subplot
    ax8 = fig.add_subplot(gs[1:, 2:])  # Middle-center-right subplot

    ax11 = fig.add_subplot(gs[2, 0:2]) # Bottom-left subplot


    # Set titles for each subplot
    ax2.axis('off')
    ax2.text(0.5, 0.5, print_title, ha='center', va='center', fontsize=26, color='black', weight='bold')

    ax6.set_title("Report of maximum values",fontsize=16)  # Adjust the pad to control the distance between title and table
    table6 = ax6.table(cellText=df1.values, colLabels=df1.columns, loc='center', cellLoc='center', colLoc='center')
    ax6.axis('tight')
    ax6.axis('off')
    # Get the actual size of ax6 in inches (not normalized)
    bbox = ax6.get_window_extent().transformed(fig.dpi_scale_trans.inverted())  # Get axis bounding box in inches
    ax_width, ax_height = bbox.width, bbox.height  # Get the width and height of the axes in inches

    # Number of rows and columns
    num_columns = len(df1.columns)
    num_rows = len(df1)

    # Calculate the column width and row height to fit the axes' size
    column_width = ax_width / num_columns  # Divide the axis width by the number of columns
    column_width = 1.6  # Divide the axis width by the number of columns

    row_height = 1.6  # Divide the axis height by the number of rows, adding some space for margins

    # Apply the scaling to the table
    table6.scale(column_width, row_height)  # Scale both width and height proportionally


    # Adjust layout to make sure everything fits well
    plt.tight_layout()

    ax8.plot(df_annual['year'], df_annual['mean'], marker='o', color='b', label='Annual Mean')
    ax8.set_title(f'Annual average of {variable} over time')
    ax8.set_xlabel('Year')
    ax8.set_ylabel(f'{variable} Mean')
    ax8.legend()
    ax8.grid(True)


    ax11.set_title("Report of minimum values",fontsize=16)
    # Add table in ax6
    table11 = ax11.table(cellText=df2.values, colLabels=df1.columns, loc='center', cellLoc='center', colLoc='center')
    ax11.axis('tight')
    ax11.axis('off')
    # Get the actual size of ax6 in inches (not normalized)
    bbox = ax11.get_window_extent().transformed(fig.dpi_scale_trans.inverted())  # Get axis bounding box in inches
    ax_width, ax_height = bbox.width, bbox.height  # Get the width and height of the axes in inches

    # Number of rows and columns
    num_columns = len(df2.columns)
    num_rows = len(df2)

    # Calculate the column width and row height to fit the axes' size
    column_width = 1.6  # Divide the axis width by the number of columns
    row_height = 2.0  # Divide the axis height by the number of rows, adding some space for margins

    # Apply the scaling to the table
    table11.scale(column_width, row_height)  # Scale both width and height proportionally


    # Adjust layout to prevent overlap
    plt.tight_layout()

    plt.savefig(file_name, format="pdf")

    # Show the plots
    #plt.show()
