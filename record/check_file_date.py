import os
import time
import logging
from datetime import date, timedelta
from send2trash import send2trash
import argparse

# === CONFIGURATION ===
TARGET_PATH = ""
DAYS_THRESHOLD = 7
LOG_FILE = "cleanup_log.txt"

# === LOGGING SETUP ===
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === FUNCTION ===
def move_old_dirs_to_recycle_bin(path, days):
    now = time.time()
    cutoff = now - (days * 86400)

    if not os.path.exists(path):
        logging.error(f"Target path does not exist: {path}")
        return

    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            try:
                modified_time = os.path.getmtime(full_path)
                if modified_time < cutoff:
                    # send2trash(full_path)
                    logging.info(f"Moved to Recycle Bin: {full_path}")
                else:
                    logging.info(f"Skipped (recent): {full_path}")
            except Exception as e:
                logging.error(f"Error processing {full_path}: {e}")

def start():
  logging.info(f"Starting cleanup in: {TARGET_PATH}")
  move_old_dirs_to_recycle_bin(TARGET_PATH, DAYS_THRESHOLD)
  logging.info("Cleanup finished.\n")

  old_date = date.today() - timedelta(days = 7)
  old_year = old_date.strftime("%Y")
  old_month = old_date.strftime("%m")
  old_day = "{}-{}-{}".format(old_year, old_month, old_date.strftime("%d"))
  old_dir = "D:\_temp\stream\{}".format(old_day)
  logging.info(f"Moved to Recycle Bin: {old_dir}")
  # send2trash(old_dir)

def init():
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--path", help = "target directory path")
  
  args = parser.parse_args()
  if args.path != None:
    TARGET_PATH = args.path
  print(TARGET_PATH)

  # start()

# === MAIN ===
if __name__ == "__main__":
  init()
    
