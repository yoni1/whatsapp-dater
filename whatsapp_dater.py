import os
import re
import sys
from datetime import datetime

WHATSAPP_FILENAME_RE = re.compile(r"^WhatsApp (?:Video|Image) (\d{4})\-(\d{2})\-(\d{2}) " \
                                   "at (\d{2})\.(\d{2})\.(\d{2})(?: \(\d+\))?\.(?:jpeg|mp4)$")

def do_file(filename):
    try:
        re_result = WHATSAPP_FILENAME_RE.findall(os.path.basename(filename))
        if len(re_result) != 1:
            print(f"{filename}: Not a Whatsapp media file")
            return False
    
        re_result = re_result.pop()
        if len(re_result) != 6:
            print(f"{filename}: Unexpected parse result")
            return False
    
        year, month, day, hour, minute, second = (int(x) for x in re_result)
        ts = datetime(year, month, day, hour, minute, second).timestamp()
        os.utime(filename, (ts, ts))
        print(f"{filename}: OK")
        return True
        
    except Exception as e:
        print(f"{filename}: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: whatsapp_dater.py [path to file or directory]", file=sys.stderr)
        return

    pathname = sys.argv[1]
    if os.path.isfile(pathname):
        do_file(pathname)
    elif os.path.isdir(pathname):
        succeeded = 0
        failed = 0
        
        for top, dirs, files in os.walk(pathname):
            print(f"Entering directory: {top}")
            for fn in files:
                filename = os.path.join(top, fn)
                if do_file(filename):
                    succeeded += 1
                else:
                    failed += 1

        print(f"Summary: {succeeded} files succeeded, {failed} files failed")
    else:
        print(f"{pathname}: Not a file or a directory")

if __name__ == '__main__':
    main()
