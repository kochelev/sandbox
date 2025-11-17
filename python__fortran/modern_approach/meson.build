project('fortran_example', 'fortran')

py_mod = import('python')
py3 = py_mod.find_installation('python3')

numpy_dep = py3.extension_module(
  'example',
  'example.f90',
  dependencies: [py3.dependency()],
  install: true,
)
