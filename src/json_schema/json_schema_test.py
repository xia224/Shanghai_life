import sys, getopt
import json
from jsonschema import validate

def main(argv):
  s_file = ''
  c_file = ''
  try:
    opts, args = getopt.getopt(argv, "hs:c:")
  except getopt.GetoptError:
    print("python3 json_schema_test.py -s <schemaFile> -c <configFile>")
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print("python3 json_schema_test.py -s <schemaFile> -c <configFile>")
      sys.exit() 
    elif opt == '-s':
      s_file = arg
    elif opt == '-c':
      c_file = arg
  if s_file == '' or c_file == '':
    print("Must specify schema file and config file at the same time")
    print("python3 json_schema_test.py -s <schemaFile> -c <configFile>")
    sys.exit()

  print("schema file: {}, config file: {}".format(s_file, c_file))
  with open('j_schema.json') as schema_file:
    schema_data = json.load(schema_file)
    with open('j_instance.json') as ins_file:
      ins_data = json.load(ins_file)
      res0 = validate(ins_data, schema=schema_data)
      if res0 is None:
        print("Json format is correct")
      else:
        print("Json format is invaild")

if __name__ == "__main__":
  main(sys.argv[1:])
