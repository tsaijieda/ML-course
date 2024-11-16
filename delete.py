import os

# Function to read log file and extract filenames
def extract_filenames_from_log(log_file_path):
    filenames = []
    try:
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("File:"):
                    filenames.append(line.split(":")[1].strip())  # Extract the filename
    except Exception as e:
        print(f"Error reading log file: {e}")
    return filenames

# Function to delete files
def delete_files(files, directory):
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

# Main function to execute the script
def main():
    log_file_path = 'warnings_and_errors.log'  # Replace with the path to your warning log
    directory = "rawdata"  # Replace with the path to your files

    # Extract filenames from the log
    filenames_to_delete = extract_filenames_from_log(log_file_path)

    # Delete the files
    delete_files(filenames_to_delete, directory)

# Run the script
main()

