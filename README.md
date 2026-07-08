# Jominy End-Quench Hardness & Core Quench Predictor

**Overview**

This computational materials science tool bridges the gap between theoretical physical metallurgy and real-world manufacturing. It processes datasets of steel alloy compositions to automatically predict their hardenability (Jominy End-Quench profiles) and autonomously evaluates whether they will meet specific engineering criteria when quenched as physical round bars.

<img width="1200" height="700" alt="Jominy_Hardness_Plot" src="https://github.com/user-attachments/assets/d392ae1c-378e-4622-b4ea-9a6aef09d133" />


**Key Features**

Batch Data Processing: Utilizes pandas to instantly ingest and process entire databases of steel compositions (Carbon, Manganese, Chromium, Molybdenum, Silicon, Nickel).

Robust Error Handling: Validates datasets upon loading, automatically drops incomplete rows, and safely catches missing files/columns without crashing.

Grossmann Quench Severity Modeling: Simulates real-world manufacturing by calculating the Equivalent Jominy Distance (EJD) for the core of a round bar based on physical diameter and quench medium (Water, Oil, Air).

Automated Material Selection: Interpolates curve data to determine the exact hardness at the core of the bar, automatically classifying alloys as "Passing" (solid lines) or "Failing" (dashed lines) based on user-defined minimum hardness criteria.

ETL Pipeline (Exporting Data): Automatically packages the generated exponential decay curves into a brand new DataFrame and exports it as jominy_results_export.csv for use in external reports.

**The Physics & Metallurgy**

The script utilizes standard empirical regressions to predict hardenability:

Maximum Hardness ($HRC_{max}$): Dictated by the Carbon content at the quenched tip.

Ideal Critical Diameter ($D_I$): Calculates the depth of hardenability using Grossmann multiplying factors for alloying elements ($Mn, Si, Cr, Ni, Mo$).

Equivalent Jominy Distance (EJD): Uses simplified Lamont chart correlations to map physical cooling rates of round bars to Jominy distances based on quench severity ($H$).

**Installation & Setup**

Clone this repository to your local machine.

Ensure you have the required Python libraries installed:

pip install pandas numpy matplotlib


Ensure your input data file steel_data.csv is in the same directory and follows this header format:
Alloy, C, Mn, Cr, Mo, Si, Ni

**Usage Guide**

Run the script via your terminal:

python jominy_predictor.py


The program will prompt you for your manufacturing parameters:

Bar Diameter: (e.g., 50 for a 50mm shaft)

Quench Medium: (Water, Oil, or Air)

Target Minimum Hardness: (e.g., 40 for 40 HRC)

**Output**

Terminal Report: Displays loaded data, calculated $HRC_{max}$ and $D_I$, and outputs a final "Manufacturing Prediction Report" listing the specific alloys that passed the core hardness test.

Data Export: Generates jominy_results_export.csv containing the raw array data for every calculated profile.

Visualization: Pops open a highly formatted matplotlib graph showing the decay curves, highlighted targets, and dynamic pass/fail stylings.

This project was developed to demonstrate the application of Python data engineering within the domain of Physical Metallurgy.
