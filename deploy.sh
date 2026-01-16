pi=pi@192.168.1.69
f="$(mktemp /tmp/myscript.XXXXXX)"
tar --exclude='./JJ_Print/RPi' --exclude='./.git' -zcvf $f .
echo "file created at:"
echo $f
scp $f $pi:~/thermal-printer-deploy.tar
ssh $pi 'rm ~/thermal-printer -R'
ssh $pi 'mkdir thermal-printer'
ssh $pi 'tar -C ~/thermal-printer -xvzf thermal-printer-deploy.tar'
echo "cleanup"
rm $f
echo "running"
ssh $pi 'python -u thermal-printer/main.py --config thermal-printer/config/config.json'
echo "fin"
