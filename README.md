xorstuff
========

Recover key from xored file using files signatures.

mostly usefull in ctf.

Input arguments :
-----------------
usage: main.py [-h] [-f FILENAME] [-t {wav,bmp,elf,png,jpg}]
                   [-l KEY_LENGTH] [-x XOR_KEY]

xor stuff with other stuff

optional arguments:

    -h, --help            show this help message and exit
    -f FILENAME, --file FILENAME
    -t {wav,bmp,elf,png,jpg,text}, --type {wav,bmp,elf,png,jpg,text}
    -l KEY_LENGTH, --length KEY_LENGTH
    -x XOR_KEY, --xor XOR_KEY (xor with given key)
    -g, --grep            Search pattern in result

Usage :
-------

####xor file with known key:

    foo@bar ~/xorstuff> /mai.py -f input_file.png -x my_key > ./output_file.png 

####Recover key with known length:

    foo@bar ~/xorstuff> ./main.py -f ./test_files/xored_file.png -t png -l 6
    [*] Open file
    [*] Key length set to 6
    [*] Start searching password
    secret
    
####Recover key with unknown length:
    
    foo@bar ~/xorstuff> ./main.py -f ./test_files/xored_file.png -t png
    [*] Open file
    [*] Guess key length
    [*] Probable key length
        1 : 39.1%
        6 : 27.3%
        9 : 18.7%
        12 : 14.8%
    [*] Most probable key length is 3*n
    [*] Key length set to 1
    [*] Start searching password
    [*] Key length set to 6
    [*] Start searching password
    secret

####Add your customs headers and headers with unknown bytes
    Add your custom class in ./modules/ and extends ModuleBaseClass
    look at ModuleBaseClass.py for doc and ./modules/*.py for examples.

####TODO
 - Add validation in modules elf and wav
