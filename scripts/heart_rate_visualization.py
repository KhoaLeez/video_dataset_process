import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = r'D:/Stream_data_process/heart_rate_logs/ARE YOU BRAVE ENOUGH？ ｜ Five Nights at Freddys 4 - Part 1_heartrate_log.csv'

try:
    # Read full file with confirmed separator and encoding
    chunk_size = 10000
    chunks = pd.read_csv(file_path, sep=',', header=0, 
                         names=['Timestamp (s)', 'Heart Rate (BPM)'], 
                         chunksize=chunk_size, dtype={'Timestamp (s)': float, 'Heart Rate (BPM)': float}, 
                         encoding='utf-8', on_bad_lines='skip')
    df = pd.concat(chunks, ignore_index=True)

    # Check if DataFrame is empty
    if df.empty:
        print("Error: DataFrame is empty after loading.")
        exit()
    
    print(f"Full data loaded. Total rows: {len(df)}")
    print("First few rows:")
    print(df.head(10))
    
    # Check heart rate range
    print("Heart Rate (BPM) summary:")
    print(df['Heart Rate (BPM)'].describe())
    
    # Filter out invalid (zero) heart rate values
    df_valid = df[df['Heart Rate (BPM)'] > 0]
    if df_valid.empty:
        print("Error: No valid heart rate data (all BPM values are zero).")
        exit()
    
    print(f"Valid data rows (BPM > 0): {len(df_valid)}")
    print("First few valid rows:")
    print(df_valid.head(10))

    # Convert timestamps to minutes
    df_valid['Time (min)'] = df_valid['Timestamp (s)'] / 60.0
    
    # Smooth heart rate data (window ~3 seconds assuming 0.03s intervals)
    window_size = 100  # Adjust based on data frequency
    df_valid['Smoothed BPM'] = df_valid['Heart Rate (BPM)'].rolling(window=window_size, center=True).mean()
    
    # Downsample for plotting if needed
    if len(df_valid) > 1000:
        df_plot = df_valid.iloc[::10]
        print(f"Downsampled to {len(df_plot)} rows for plotting.")
    else:
        df_plot = df_valid

    # Line Plot (Recommended)
    plt.figure(figsize=(12, 6))
    plt.plot(df_plot['Time (min)'], df_plot['Smoothed BPM'], linewidth=1, color='blue', label='Smoothed Heart Rate')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Heart Rate (BPM)')
    plt.title('Smoothed Heart Rate Over Time (FNAF 4 Gameplay)')
    plt.grid(True)
    plt.legend()
    plt.ylim(50, 150)  # Typical heart rate range
    plt.tight_layout()
    plt.show()

    # Optional Bar Chart (per minute)
    bin_size = 60  # 1 minute
    df_agg = df_valid.copy()
    df_agg['Time Bin (min)'] = (df_agg['Timestamp (s)'] // bin_size).astype(int)
    df_agg = df_agg.groupby('Time Bin (min)')['Heart Rate (BPM)'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.bar(df_agg['Time Bin (min)'], df_agg['Heart Rate (BPM)'], 
            width=0.4, color='skyblue', edgecolor='black')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Average Heart Rate (BPM)')
    plt.title('Average Heart Rate per Minute (FNAF 4 Gameplay)')
    plt.grid(True, axis='y')
    plt.ylim(50, 150)
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"Error: File not found at {file_path}. Please check the file path.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")