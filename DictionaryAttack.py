import time
import os, argparse
from zipfile import is_zipfile, ZipFile
from tqdm import tqdm


def checkZip(path): 
    """Verify argument type received for zip files (to use with argparse) 
    Returns only the filename of the zip, if it exists and it is a zip
    """
    pathZip, zipfilename = os.path.split(path) 
    if pathZip:
        os.chdir(pathZip)
    if not is_zipfile(zipfilename):
        raise argparse.ArgumentTypeError('argument filename must be of type *.zip')
    return zipfilename


def main(): 
    """Program that does a dictionary attack to find the password of a password protected ZIP file
    """
    brute_file_path = os.getcwd()
    # Argument and command-line options parsing
    parser = argparse.ArgumentParser(description='Brute-force dictionary attack for a ZIP file.')
    parser.add_argument('-l', required=True, metavar='Dictionary File', dest='dictionary', help='Specify Dictionary File')
    parser.add_argument('-f', required=True, metavar='Zip File', dest='zipfilename', type=checkZip, help='Specify ZIP File')
    args = parser.parse_args()

    password_found = False
    st = time.time()
    with ZipFile(args.zipfilename, 'r') as zip_file:
        zip_file_path = os.getcwd()
        os.chdir(brute_file_path)
        # Brute force through dictionary entries 
        with open(args.dictionary, 'r') as f:
            os.chdir(zip_file_path)
            for line in tqdm(f.readlines()):
                password = line.strip("\n")
                bytes_pass = password.encode('utf-8')
                try:
                    zip_file.extractall(pwd=bytes_pass)
                    password_found = True
                    break
                except:
                    pass

    ed = time.time()
    if password_found:
        print(f"\n---SUCCESSFULLY CRACKED THE PASSWORD---\nThe password found: {password}")
    else:
        print("Password Not Found\n")
    
    print(f"\n\nTotal Time Taken: {(ed - st):.3f} sec")

if __name__ == '__main__': 
    main()