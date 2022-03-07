import os
import re

# Pillow
from PIL import Image
from PIL.ExifTags import TAGS

class Sorter:
    def __init__(self):
        self.pillowRegex = '''\.(jpeg|jpg|bmp|png)$'''
    
    '''
    Get the datetime from img, (pillow supported inventory)
    '''
    def GetDateFromImg(self, path, filename):
        # try to read meta
        try:
            meta = Image.open(path+'\\'+filename).getexif()
        except:
            print('Couldnt read '+filename)
            return

        # if there is no meta
        if meta is None:
            print(filename+' has no meta')
            return

        # read meta
        for (k,v) in meta.items():
            # if there is a date time
            if TAGS.get(k) == 'DateTime':

                # remove : and replace space with _ , add file extension
                FileDate = v.replace(' ', '_').replace(':','')+filename[-4:]

                i = 0  # init var

                # as long as there is a file, increment i
                while os.path.exists(v):
                    i += 1  # increment the number

                    # Add a number at the end
                    FileDate = path+'\\'+v[:-4]+'('+str(i)+')'+v[-4:]

                return FileDate


    ''' 
    Get the creation and modification date-time from .mov metadata.
    Returns None if a value is not available.
    '''
    def GetDateFromMov(self, filename):
        from datetime import datetime as DateTime
        import struct

        ATOM_HEADER_SIZE = 8
        # difference between Unix epoch and QuickTime epoch, in seconds
        EPOCH_ADJUSTER = 2082844800

        creation_time = modification_time = None

        # search for moov item
        with open(filename, "rb") as f:
            while True:
                atom_header = f.read(ATOM_HEADER_SIZE)
                #~ print('atom header:', atom_header)  # debug purposes
                if atom_header[4:8] == b'moov': break  # found
                else:
                    atom_size = struct.unpack('>I', atom_header[0:4])[0]
                    f.seek(atom_size - 8, 1)

            # found 'moov', look for 'mvhd' and timestamps
            atom_header = f.read(ATOM_HEADER_SIZE)
            if atom_header[4:8] == b'cmov':
                raise RuntimeError('moov atom is compressed')
            elif atom_header[4:8] != b'mvhd':
                raise RuntimeError('expected to find "mvhd" header.')
            else:
                f.seek(4, 1)
                creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
                creation_time = DateTime.fromtimestamp(creation_time)
                if creation_time.year < 1990:  # invalid or censored data
                    creation_time = None

                modification_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
                modification_time = DateTime.fromtimestamp(modification_time)
                if modification_time.year < 1990:  # invalid or censored data
                    modification_time = None

        return creation_time, modification_time

    def Sort(self, path):
        # if path exist
        if not os.path.exists(path): return f"\'{path}\' doesnt exist"

        # get file from directory
        filenames = next(os.walk(path), (None, None, []))[2]  # [] if no file

        # if there is no file
        if len(filenames) == 0: return "There is no media detected in \'"+path+"\'"

        # for each file
        for f in filenames:

            # if its an supported pillow image format
            if re.search(self.pillowRegex, f, re.IGNORECASE) is not None:
                date = self.GetDateFromImg(path, f)

            # if its a MOV
            elif ".mov" or '.MOV' in f:
                #date = self.GetDateFromMov(path+'\\'+f)
                date = 'mov'
                print('This is a MOV')

            else:
                # if there is no date, continue
                print(f'Cannot read {path}\\{f}')
                continue


            #os.rename(path+'\\'+f, path+'\\'+date)
            print(f'Renamed {path}\\{f} to {path}\\{date}')

    def SubfolderSort(self, path):
        # for each sub directory, sort it
        for subdir, dirs, files in os.walk(path):
            # for each directory sort it
            for d in dirs: 
                # print the current directory sorting
                print('--- '+d+' ---')
                self.Sort(path+d)