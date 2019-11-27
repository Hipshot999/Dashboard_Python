import hashlib

def md5Checksum(filePath):
    try:
        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    except (KeyboardInterrupt):
             con.commit()
             cur.close()
             con.close()
             print ("User exit at file " + currentPath_File + " Handled " + str(file_counter) + " files.")
             raise
