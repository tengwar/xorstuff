xorstuff
========

Recover key from xored file using files signatures.

mostly usefull in ctf.

Input arguments :
-----------------
usage: xorstuff.py [-h] [-f FILENAME] [-t {wav,bmp,elf,png,jpg}]
                   [-l KEY_LENGTH] [-x XOR_KEY]

xor stuff with other stuff

optional arguments:

    -h, --help            show this help message and exit
    -f FILENAME, --file FILENAME
    -t {wav,bmp,elf,png,jpg}, --type {wav,bmp,elf,png,jpg}
    -l KEY_LENGTH, --length KEY_LENGTH
    -x XOR_KEY, --xor XOR_KEY (xor with given key)

Usage :
-------

####xor file with known key:

    foo@bar ~/xorstuff> /xorstuff.py -f input_file.png -x my_key > ./output_file.png 

####Recover key with known length:

    foo@bar ~/xorstuff> ./xorstuff.py -f ./test_files/xored_file.png -t png -l 6
    my_key
    
####Recover key with unknown length:
    
    foo@bar ~/xorstuff> ./xorstuff.py -f ./test_files/xored_file.png -t png
    my_keymy
    
key length == known header length

####bruteforce last bytes :
    foo@bar ~/xorstuff> ./xorstuff.py -f ./test_files/xored_file.png -t png -l 10
    secretsecr
    secretsecs
    [........]
    secretse<,
    secretse<-

Use you brain for extracting the correct key (repetition, key not complete, existing words, etc)

####Add your customs headers and headers with unknown bytes
    Modify xorstuff.py and add your custom header in the list_types dictionary.

    If the header contains unknown bytes, replace them with %s, the script will bruteforce them.
