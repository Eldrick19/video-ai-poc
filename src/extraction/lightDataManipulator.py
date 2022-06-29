import numpy as np
import pandas as pd

# Gets FPS from video 
def format_data(person_tracking_array, fps):
    df = pd.DataFrame(person_tracking_array, columns=['d_id','start_s', 'left', 'top', 'right', 'bottom'])
    df = df.sort_values(by=['start_s']) # Sort by Start time
    df = df.reset_index(drop=True)
    df['start_s'] = df['start_s'].multiply(fps) # Convert to frames
    df.rename(columns={"start_s": "start_f"}, inplace=True) # Rename columns to describe fps

    return df