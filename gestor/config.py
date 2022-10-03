import sys

DATABASE_PATH = "gestor/clientes.csv"

if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/clientes_test.csv" #Con esto las pruebas irán a buscar el nuevo fichero
