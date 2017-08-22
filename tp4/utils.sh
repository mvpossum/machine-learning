#!/bin/bash

get_data () {
	URL=$1
	wget -q -O tmp.zip "$URL"
	unzip tmp.zip >/dev/null
	rm tmp.zip
}

gen_net () {
	ORIG="$1"
	DEST="$2"
	cp "$DATADIR/$ORIG.tmpl" "$DEST"
	shift
	shift
	
	while [ $# -gt 1 ]; do
		sed -i "s/$1/$2/" "$DEST"
		shift
		shift
	done
}
export -f gen_net

clean_test () {
	rm "$1.data" "$1.test"
}

# Random number >= 1
rand () {
	od -vAn -N2 -tu2 < /dev/urandom | awk '{print 1+$1}'
}
export -f rand
