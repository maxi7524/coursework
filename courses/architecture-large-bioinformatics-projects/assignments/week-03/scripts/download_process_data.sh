#!/bin/bash

echo "Downloading folder from Google Drive..."
# 1. Download files (ADPB/week_3_data.zip) from private storage 
gdown --folder https://drive.google.com/drive/folders/1-YH1oQS5HV0UeFZxxsYD1BAg6H1fx8XQ -O download_data

echo "Extracting 'data' folder..."
# 2. Extract ONLY the 'data/*' content from week_3_data.zip
# '-o' flag- overwrite '-n' to never overwrite files
unzip -q -n download_data/ADPB/week_3_data.zip "data/*" -d .

echo "Cleaning up unnecessary files..."
# 3. Remove the entire downloaded folder (including the zip file and everything else)
rm -r download_data

echo "Done! The 'data' folder is ready to use."