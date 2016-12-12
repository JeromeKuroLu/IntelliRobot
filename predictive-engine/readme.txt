Guidline
// You may get libary from "\\maed-w7\public\python library for machine learning"

===For SGD/ Naivebayes
1. Install python 3.5.1 via exe installer (latest version at 5Jan16)
	1. Install it
	2. Add %python% and %python%/scripts to Path variable
		%python% = C:\Users\maed\AppData\Local\Programs\Python\Python35
2. Install nltk 3.1 via exe installer (latest version at 5Jan16)
3. Install all nltk package (need seveal ten mins)
	1. Open cmd
	2. python
	3. import nltk
	4. nltk.download('all')
4. Install sklearn
	1. Open cmd
	2. pip install sklearn 
5. Install wheel (otherwise, cannot install numpy) 
	1. Open cmd
	2. pip install wheel
	PS: Have to install Microsoft .NET Framework 4.6.1 and Visual Studio. By default, installing VS does not include C++ package. Have to check it out manaully
6. Install numpy-1.10.4+mkl-cp35-none-win_amd64
	1. Open cmd
	2. Go to numpy file directory
	3. pip install <numpy file>
7. Install WinPython-64bit-3.4.3.7 (for window only, latest version at 7Jan16)
8. Install MinGW-w64
9. Install http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
	1. Choose scipy-0.17.0rc1-cp35-none-win_amd64 (latest version at 7Jan16)
	2. Open cmd
	3. go to the folder
	4. pip install scipy-0.17.0rc1-cp35-none-win_amd64.whl
10. Install flask for web
	1. pip install Flask

=== For association rule mining
1. Install above library
2. Install pandas
	1. Open cmd
  2. pip install pandas
3. Install xlwt (for outputing excel file)
  1. Open cmd
  2. pip install xlwt










KB
1. UnicodeEncodeError: 'charmap' codec can't encode character
	A: Open Cmd, then "chcp 65001"

