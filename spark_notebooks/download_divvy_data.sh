set -e

YEAR=$1 # 2020

URL_PREFIX="https://divvy-tripdata.s3.amazonaws.com"
LOCAL_PREFIX="data/raw/divvy/${YEAR}"

for MONTH in {1..12}; do
  FMONTH=`printf "%02d" ${MONTH}`  # Format month as two digits (01, 02, ..., 12)
  URL="${URL_PREFIX}/${YEAR}${FMONTH}-divvy-tripdata.zip"  # Construct the URL for each month
  
  LOCAL_FILE="${YEAR}${FMONTH}-divvy-tripdata.zip"
  LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

  echo "Downloading ${URL} to ${LOCAL_PATH}"
  mkdir -p ${LOCAL_PREFIX}
  wget ${URL} -O ${LOCAL_PATH}

  # Extract the ZIP file
  echo "Extracting ${LOCAL_PATH}"
  unzip -o ${LOCAL_PATH} -d ${LOCAL_PREFIX}

done
