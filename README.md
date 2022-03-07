# README
This is an cli command line to sort media files via dates

# WHAT IS LEFT TO DO
- Add all pillow reading capability to regex
- already contains (digit), dont add another
- Rename also video to date
- threading
- Detect duplicate with a comparaison algorithm
- Skip already named to good format
- Make compatible for linux
- create a backup, with tick

# KNOWN BUGS
- It only reads a layer of subfolder, not all types of layer


# DOC
python3 sorter.py [path] [attributes]

### KEEP IN MIND
- without tick -s, it won't look to subfolders

## Attributes
-s : will sort also sub-folder

## Examples
python3 sorter.py /home/johndoe/desktop/myjourney -s
