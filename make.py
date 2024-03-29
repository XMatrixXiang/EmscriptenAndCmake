#!/usr/bin/python

import os, sys, re, json, shutil, multiprocessing
from subprocess import Popen, PIPE, STDOUT

# Definitions

INCLUDES = [
os.path.join('Exc', 'CExport.h'),
os.path.join('Exc', 'ClassTest.h'),
os.path.join('..', 'ExportToJavaScript', 'idl_templates.h')]

# Startup

stage_counter = 0

def which(program):
  for path in os.environ["PATH"].split(os.pathsep):
    exe_file = os.path.join(path, program)
    if os.path.exists(exe_file):
      return exe_file
  return None

def build():
  EMSCRIPTEN_ROOT = os.environ.get('EMSDK')
  if not EMSCRIPTEN_ROOT:
    emcc = which('emcc')
    EMSCRIPTEN_ROOT = os.path.dirname(emcc)
  else:
    EMSCRIPTEN_ROOT = os.path.join(EMSCRIPTEN_ROOT,'fastcomp','emscripten')

  if not EMSCRIPTEN_ROOT:
    print "ERROR: EMSCRIPTEN_ROOT environment variable (which should be equal to emscripten's root dir) not found"
    sys.exit(1)

  sys.path.append(EMSCRIPTEN_ROOT)
  import tools.shared as emscripten

  # Settings

  '''
            Settings.INLINING_LIMIT = 0
            Settings.DOUBLE_MODE = 0
            Settings.PRECISE_I64_MATH = 0
            Settings.CORRECT_SIGNS = 0
            Settings.CORRECT_OVERFLOWS = 0
            Settings.CORRECT_ROUNDINGS = 0
  '''

  wasm = 'wasm' in sys.argv
  closure = 'closure' in sys.argv
  add_function_support = 'add_func' in sys.argv

  args = '-O3 --llvm-lto 1 -s NO_EXIT_RUNTIME=1 -s NO_FILESYSTEM=1 -s EXPORTED_RUNTIME_METHODS=["UTF8ToString"]'
  if add_function_support:
    args += ' -s RESERVED_FUNCTION_POINTERS=20 -s EXTRA_EXPORTED_RUNTIME_METHODS=["addFunction"]'  
  if not wasm:
    args += ' -s WASM=0 -s AGGRESSIVE_VARIABLE_ELIMINATION=1 -s ELIMINATE_DUPLICATE_FUNCTIONS=1 -s SINGLE_FILE=1 -s LEGACY_VM_SUPPORT=1'
  else:
    args += ''' -s WASM=1 -s BINARYEN_IGNORE_IMPLICIT_TRAPS=1 -s BINARYEN_TRAP_MODE="clamp"'''
  if closure:
    args += ' --closure 1 -s IGNORE_CLOSURE_COMPILER_ERRORS=1' # closure complains about the bullet Node class (Node is a DOM thing too)
  else:
    args += ' -s NO_DYNAMIC_EXECUTION=1'

  emcc_args = args.split(' ')

  emcc_args += ['-s', 'TOTAL_MEMORY=%d' % (64*1024*1024)] # default 64MB. Compile with ALLOW_MEMORY_GROWTH if you want a growable heap (slower though).
  #emcc_args += ['-s', 'ALLOW_MEMORY_GROWTH=1'] # resizable heap, with some amount of slowness

  emcc_args += '-s EXPORT_NAME="CadEngine" -s MODULARIZE=1'.split(' ')

  target = 'CadEngine.js' if not wasm else 'CadEngine.wasm.js'

  print
  print '--------------------------------------------------'
  print 'Building CadEngine.js, build type:', emcc_args
  print '--------------------------------------------------'
  print

  '''
  import os, sys, re

  infile = open(sys.argv[1], 'r').read()
  outfile = open(sys.argv[2], 'w')

  t1 = infile
  while True:
    t2 = re.sub(r'\(\n?!\n?1\n?\+\n?\(\n?!\n?1\n?\+\n?(\w)\n?\)\n?\)', lambda m: '(!1+' + m.group(1) + ')', t1)
    print len(infile), len(t2)
    if t1 == t2: break
    t1 = t2

  outfile.write(t2)
  '''

  # Utilities

  def stage(text):
    global stage_counter
    stage_counter += 1
    text = 'Stage %d: %s' % (stage_counter, text)
    print
    print '=' * len(text)
    print text
    print '=' * len(text)
    print

  # Main

  try:
    this_dir = os.getcwd()

#  Create Emscripten  build dir
    if not os.path.exists('Builds'):
      os.makedirs('Builds')
    os.chdir('Builds')
    if not os.path.exists('EmscritenBuild'):
       os.makedirs('EmscritenBuild')
    os.chdir('EmscritenBuild')

    stage('Generate bindings')

    Popen([emscripten.PYTHON, os.path.join(EMSCRIPTEN_ROOT, 'tools', 'webidl_binder.py'), os.path.join(this_dir,'ExportToJavaScript', 'CadEngine.idl'), 'glue']).communicate()
    assert os.path.exists('glue.js')
    assert os.path.exists('glue.cpp')

    stage('Build bindings')

    args = ['-I../../Source', '-c','-std=c++14']
    for include in INCLUDES:
      args += ['-include', include]
    emscripten.Building.emcc('glue.cpp', args, 'glue.o')
    assert(os.path.exists('glue.o'))

    # Configure with CMake on Windows and  Unix.
    cmake_build = True

    os.chdir(this_dir)
    if cmake_build:
      if not os.path.exists('CMakeCache.txt'):
        stage('Configure via CMake')
        emscripten.Building.configure([emscripten.PYTHON, os.path.join(EMSCRIPTEN_ROOT, 'emcmake'), 'cmake', '-S' + this_dir, '-B'+ os.path.join(this_dir,'Builds','EmscritenBuild','GunBuild'), '-DCMAKE_BUILD_TYPE=Release'])
  

    stage('Make')

    CORES = multiprocessing.cpu_count()
    os.chdir('Builds/EmscritenBuild/GunBuild')
    if emscripten.WINDOWS:
      emscripten.Building.make(['mingw32-make', '-j', str(CORES)])
    else:
      emscripten.Building.make(['make', '-j', str(CORES)])

    stage('Link')

    os.chdir(this_dir)
    os.chdir('Builds/EmscritenBuild')

    if cmake_build:
      bullet_libs = []

    stage('emcc: ' + ' '.join(emcc_args))

    
    exportDir = os.path.join('..','JavaScriptSDK')
    temp = os.path.join(exportDir, target)
    if not os.path.exists(exportDir):
      os.makedirs(exportDir)
    emscripten.Building.emcc('-DNOTHING_WAKA_WAKA', emcc_args + ['glue.o'] + bullet_libs + ['--js-transform', 'python %s' % os.path.join('..', '..', 'bundle.py')],
                            temp)

    assert os.path.exists(temp), 'Failed to create script code'

    stage('wrap')

    wrapped = '''
  // This is CadEngine.js.
  ''' + open(temp).read()

    open(temp, 'w').write(wrapped)

  finally:
    os.chdir(this_dir);

if __name__ == '__main__':
  build()

