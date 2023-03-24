# folders_sync

## Program description:

The **folder_sync.py** is a python script that performs a one-way synchronization of two local folders. It does so by following the next steps:

  - The script receives 4 arguments using the sys.argv library as such:
  
  `python folder_sync.py <source_path> <replica_path> <log_path> <sync_time>`
  
  - Then it checks if the two folders provided are the same using **compare_folders** function:
  
    - If compare_folders returns true then both folders are identical. Next step is to wait and check again whether the source folder has changed.
    
    - If compare_folders returns false then source and replica folders are not the same. It means that either:
    
      1. There is an extra file in the replica folder -> delete the file:
    
      `rm replica/file`
    
      2. There is a missing file in the replica folder -> copy the file:
      
      `cp source/file1 replica`
      
      3. There are the same number of files in both folders but they are not the same -> update the file:
      
      `rm replica/file`
      `cp source/file replica`
      
  - All the file operations (copy/delete/update) are logged into a text file using the log function and they are also printed to the terminal.      
      
        
       
