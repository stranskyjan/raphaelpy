# runs all examples
set -e
for d in . raphaeljs; do
	cd $d
	rm -f *.svg
	for f in *.py; do
		echo $f
		python $f
	done
done
