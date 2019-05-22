if [ $1 == 'zip' ]
then
    zip submit.zip box.py union_box.py union_interface.py LANGUAGE
else
    rm submit.zip
fi
