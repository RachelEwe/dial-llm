
output=plot

for i in $(seq 200); do
	cp base.json ./plots/$output$i.json
	./dial.py -c writer_plot.json me.json -o ./plots/$output$i.json -d >/dev/null
	echo $i
done
