"""
Created on Tue Aug 21 18:11:02 2018

@author: selva
main
"""

import Grabcut, Mask, Synthesis
import sys

def get_photo(src, background):
    """
        usage:
          get_photo(src, background)

        Args:
          src -> soucre image
          background -> backgroung image

        Return:
          path -> path of saved image (defined at Synthesis.py)
    """
    # Extract backgroung
    res = Grabcut.grabCut(src)
    mask_res = Mask.mask(res)
    # Compose
    path = Synthesis.synthesis(res, background, mask_res)
    #print("[+] File path : ", path)
    print(path)
    return path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[+] Required more arguments")
        exit()
    get_photo(sys.argv[1], sys.argv[2])
