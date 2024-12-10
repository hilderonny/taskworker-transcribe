@ECHO OFF
c:
cd \github\hilderonny\taskworker-transcribe
git pull
.\python\python.exe transcribe.py --taskbridgeurl http://192.168.0.152:42000/ --worker RH-WORKBOOK --device cuda --model large-v2