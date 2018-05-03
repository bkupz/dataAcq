echo "starting script" >> /home/pi/Desktop/sr_design/startupLog.txt
#for use with terminal window #sudo -u pi 
sleep 20
env DISPLAY=:0 lxterminal -e python /home/pi/Desktop/sr_design/archPlate.py &>> /home/pi/Desktop/sr_design/startupLog.txt 
