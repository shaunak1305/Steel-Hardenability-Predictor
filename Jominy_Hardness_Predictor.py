import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# --- ENGINEERING FUNCTION: Grossmann Quench Severity ---
def get_equivalent_jominy_distance(diameter_mm, medium):
    """
    Simplified Lamont chart correlations for the CENTER of a round bar.
    Maps physical cooling rates to equivalent Jominy distances (mm).
    """
    medium = medium.upper()
    if medium == 'WATER':
        # Fast quench (H = 1.0)
        return diameter_mm * 0.15
    elif medium == 'OIL':
        # Moderate quench (H = 0.5)
        return diameter_mm * 0.25
    elif medium == 'AIR':
        # Slow cooling (H = 0.02)
        return diameter_mm * 1.20
    else:
        print("Unknown medium. Defaulting to Oil.")
        return diameter_mm * 0.25

# Load the CSV file into a DataFrame with Error Handling
print("-----Loading Steel Dataset-----")
try:
    df = pd.read_csv('steel_data.csv')
except FileNotFoundError:
    print("File Not Found, Please Check your Folders")
    sys.exit()

required_columns = ['Alloy', 'C', 'Mn', 'Cr', 'Mo', 'Si', 'Ni']

for col in required_columns:
    if col not in df.columns:
        print(f"Column {col} Missing in the CSV File, Please Check Headers")
        sys.exit()

# Data Cleaning by Skipping Missing Data
original_count = len(df)
df = df.dropna(subset = required_columns)
if len(df) < original_count:
    print(f"(Skipped {original_count - len(df)} because of missing data)")
else:
    print("File is in perfect order")


# HRc Calculation
df['HRc_max'] = 60 * np.sqrt(df['C']) + 20

# Initial Critical Diameter (D_I)
D_carbon = 25.4 * np.sqrt(df['C'])
f_Mn = 1 + 4.10 * df['Mn']
f_Cr = 1 + 2.83 * df['Cr']
f_Mo = 1 + 3.0 * df['Mo']
f_Si = 1 + 0.64 * df['Si']
f_Ni = 1 + 0.52 * df['Ni']

df['D_I'] = D_carbon * f_Mn * f_Cr * f_Mo * f_Si * f_Ni

# Output
print("--- Calculated Hardenability Properties ---")
print(df[['Alloy', 'C', 'HRc_max', 'D_I']])

# Set up the X-axis (Distance from 0mm to 50mm)
# np.linspace creates an array of 100 evenly spaced numbers between 0 and 50
distances = np.linspace(0, 50, 100)

# We create a new empty DataFrame to store our final curves for export
results_df = pd.DataFrame({'Distance_mm': distances})

# Material Selector Criteria ---
TARGET_DISTANCE = 5  # mm
TARGET_HRC = 40       # Minimum required hardness at target distance
passing_alloys = []

# --- FEATURE: Real-World Manufacturing Target ---
BAR_DIAMETER = float(input("Enter Bar Diameter: "))
QUENCH_MEDIUM = input("Enter Quench Medium: ").upper()
TARGET_MIN_HRC = float(input("Enter Target Minimum Hardness: "))

# Calculate the Equivalent Jominy Distance for the center of our specific bar
EJD_center = get_equivalent_jominy_distance(BAR_DIAMETER, QUENCH_MEDIUM)

# Create the canvas for the plot
plt.figure(figsize=(12, 7))

# Loop through the DataFrame to plot each alloy
# iterrows() lets us read the DataFrame one row at a time
for index, row in df.iterrows():
    
    # Calculate the exponential decay curve for THIS specific row/alloy
    hardness_profile = 20 + (row['HRc_max'] - 20) * np.exp(-0.05 * distances * (25 / row['D_I']))
    results_df[f"Alloy_{row['Alloy']}_HRC"] = hardness_profile
    
     # Predict hardness at the EXACT CENTER of our manufactured bar
    hardness_at_center = np.interp(EJD_center, distances, hardness_profile)
    
    if hardness_at_center >= TARGET_MIN_HRC:
        passing_alloys.append(row['Alloy'])
        line_style = '-'
        alpha_val = 1.0
    else:
        line_style = '--'
        alpha_val = 0.5
        
    plt.plot(distances, hardness_profile, 
             label=f"{row['Alloy']} ({hardness_at_center:.1f} HRC @ Center)", 
             linewidth=2, linestyle=line_style, alpha=alpha_val)

results_df.to_csv('jominy_results_export.csv', index=False)

# 6. Print the Manufacturing Report to the terminal
print("\n" + "="*50)
print(f"MANUFACTURING PREDICTION REPORT")
print(f"Component: {BAR_DIAMETER}mm Round Bar")
print(f"Quench Medium: {QUENCH_MEDIUM.capitalize()}")
print(f"Equivalent Jominy Distance at Center: {EJD_center:.1f} mm")
print(f"Requirement: Minimum {TARGET_MIN_HRC} HRC at the core.")
print(f"Passing Alloys: {passing_alloys}")
print("="*50 + "\n")

# 7. Make the graph look professional
plt.title(f'Core Hardness Prediction: {BAR_DIAMETER}mm Bar in {QUENCH_MEDIUM.capitalize()}', fontsize=16, fontweight='bold')
plt.xlabel('Jominy Distance (mm)', fontsize=12)
plt.ylabel('Hardness (HRC)', fontsize=12)

# Draw our new Real-World limits
plt.axvline(x=EJD_center, color='purple', linestyle='-', linewidth=2, label=f'Bar Center (EJD: {EJD_center:.1f}mm)')
plt.axhline(y=TARGET_MIN_HRC, color='red', linestyle=':', label='Target Min Hardness')

plt.xlim(0, 50)
plt.ylim(20, 65)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title="Steel Grades & Core Performance", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

print("Calculations complete! Opening graph...")
plt.show()