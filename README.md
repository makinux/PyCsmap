## PyCsmap
Implementation of csmap(https://github.com/frogcat/csmap/) in python2.7

## Require
* PIL
* numpy
* requests

## Usage
``` 
python CSMapMake.py 7303 7306 3105 3106 13 --outputPath output_dir
``` 

arg1：指定する範囲の始点となるタイルのx方向の位置

arg3：指定する範囲の始点となるタイルのy方向の位置

arg4：指定する範囲の終点となるタイルのy方向の位置

arg2指定する範囲の終点となるタイルのx方向の位置

arg5：zoom level

--outputPath：出力先ディレクトリの指定。省略可。デフォルトは"./"
