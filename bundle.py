import os, sys

bundle = open(sys.argv[1], 'a')
bundle.write(open('glue.js', 'r').read())
bundle.write('''
this['CadEngine'] = Module; /* With or without a closure, the proper usage is CadEngine.* */
''')
bundle.close()

