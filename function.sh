#!/sbin/openrc-run

D_PATH="`whoami`/initsexample/daemon.py"

start(){
	python3 $D_PATH
	echo hello
}
stop()
{
	kill -9 `pgrep -f $D_PATH`
	echo Goodbye
}
restart()
{
	echo "Restarting program"
	stop
	start
}
