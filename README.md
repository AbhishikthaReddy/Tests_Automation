# Partner Output File Validation

## Installation

### Mac OS X

Homebrew stuffs

    # python & pip version 3
    brew install python3 pip3

    # freetds
    # uninstall any newer versions if present
    brew install homebrew/versions/freetds091

Then dependencies:

    pip3 install -r requirements.txt

or Individual dependencies:

    # behave
    pip3 install behave

    # pymssql
    pip3 install --no-cache-dir git+https://github.com/pymssql/pymssql.git

For reference, see:

 * [https://groups.google.com/forum/#!topic/pymssql/nyXD3Rsxv38](https://groups.google.com/forum/#!topic/pymssql/nyXD3Rsxv38)
 * [http://stackoverflow.com/questions/35819148/error-importing-pymssql](http://stackoverflow.com/questions/35819148/error-importing-pymssql)

### Windows

Install git.  Grab the installer from [here](https://git-scm.com/download/win).  Accept all the defaults.

Install Python3.  Grab the Windows x86-64 executable installer from [here](https://www.python.org/ftp/python/3.6.1/python-3.6.1-amd64.exe).

 * Advanced Install
 * Install for all users
 * Install pip
 * Install Pandas
 * Install PyHamcrest
 * Add Python to environment variables
 * Add `py` utility for easier running of scripts
 * Add the remote drive as a network drive to your local machine

Permissions:

 * Make sure `C:\Program Files\Python36\Scripts` folder has write permissions for Users - this allows the dependency installs below to complete successfully.

Then dependencies (from Git Bash command line utility):

 * Grab [pymssql](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql) precompiled module.  Add to `lib` folder in this local repo's folder.
 * Grab [behave](https://pypi.python.org/packages/e6/9f/5232e488461eb4f6eec04d49da22050f32f54eebf212525d67ef198f2527/behave-1.2.5-py2.py3-none-any.whl) precompiled module.  Add to `lib` folder in this local repo's folder.
 * Grab [pyHamcrest](https://pypi.python.org/packages/9a/d5/d37fd731b7d0e91afcc84577edeccf4638b4f9b82f5ffe2f8b62e2ddc609/PyHamcrest-1.9.0-py2.py3-none-any.whl#md5=c19e2fa6d567fb7542d8023dcd8f6f3e).          Add to `lib` folder in this local repo's folder.

        export PATH=/C/Program\ Files/Python36/Scripts:$PATH
        pip install lib/pymssql*
        pip install lib/behave*
		pip install lib/pyHamc*
    


## Execution

* Inside the project folder create a folder called `data` and copy your data files into it
* create one more folder inside the project folder on client's name (Ex: `sanuk`) and copy master file
* After the installations and setting up the project, run the following command in the behave command line

=

    behave \
        -D date="20170504" \
        -D masterfile_loc="location of masterfile with name" \
        -D resultsfiles_loc="results files location" \
        -D timestamp="153737"
        --no-capture



