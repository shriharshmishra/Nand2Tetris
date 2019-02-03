from CompilationEngine import CompilationEngine

if __name__ == '__main__':
    import sys
    import os
    path = sys.argv[1]

    if os.path.isdir(path):
        files = [ os.path.join(path, file) for file in os.listdir(path) ]
    else:
        files = [path]

    for file in files:
        if file.endswith(".jack"):
            idx = file.index('.jack')
            print("Input-File: ", file)
            opfilename = file[:idx] + '.xml'
            print("Output-File: ", opfilename)
            CompilationEngine(file, opfilename).exportXML()
