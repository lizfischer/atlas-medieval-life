import os

folders = [f for f in os.listdir('.') if os.path.isdir(f)]

for i in range(0,len(folders)):
    os.rename(folders[i], f"Batch {i+102}")