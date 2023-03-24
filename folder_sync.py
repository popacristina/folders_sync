import os
import hashlib
import time
import sys


# Function for writing in log.txt file
def log(message, log_path):
    log_file = open(log_path, 'a') 
    log_file.write(message+'\n')
    log_file.close()


# Function to compare the contents of both files with the same name
def compare_2_files(source, replica, file):
    path_a = source + '/' + file
    path_b = replica + '/' + file
    file_a = open(path_a, 'rb') # reads the file in binary mode to include files other than text(e.g images)
    file_b = open(path_b, 'rb')

    # Compare the 128-bit hashes of the 2 files
    if hashlib.md5(file_a.read()).hexdigest() != hashlib.md5(file_b.read()).hexdigest():
        return False
    else:
        return True
    

# Function to compare the two folders
def compare_folders(source, replica):
    files_source = os.listdir(source) 
    files_replica = os.listdir(replica)

    # Case 1: the lists are different sizes -> they are not identical
    if len(files_source) != len(files_replica) :
        return False
    
    # Case 2: the lists are the same size -> need to compare the files
    for file in files_source:
        if file in files_replica:
            if not compare_2_files(source, replica, file):
                return False
        else: return False
    
    return True


def sync_replica(source, replica, log_path):
    files_source = os.listdir(source)
    files_replica = os.listdir(replica)

    for file in files_replica:
        if file not in files_source:
            # Delete the extra file in the replica folder
            message = f"Delete '{file}' in replica folder"
            print(message)
            log(message, log_path)
            os.remove(replica+'/'+file)
        else:
            # Update the replica file with source file
            if not compare_2_files(source, replica, file):
                message = f"Update '{file}' in replica folder"
                print(message)
                log(message, log_path)
                os.remove(replica+'/'+file)
                os.system('cp '+source+'/'+file+' '+replica)

    for file in files_source:
        if file not in files_replica:
            # Copy the missing file in the replica folder
            message = f"Copy '{file}' from source to replica"
            print(message)
            log(message, log_path)
            source_file_path = source + '/' + file
            os.system(f'cp {source_file_path} {replica}')


file_name = sys.argv[0]
source_path = sys.argv[1]
replica_path = sys.argv[2]
log_path = sys.argv[3]
sync_time = int(sys.argv[4])


while True:
    # Verify if the source and the replica are the same
    if compare_folders(source_path, replica_path):
        time.sleep(sync_time)
        continue
    # Otherwise sync the two folders
    else:
        sync_replica(source_path, replica_path, log_path)
        time.sleep(sync_time)
        