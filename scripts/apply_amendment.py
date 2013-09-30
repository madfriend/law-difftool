import sys

with open(sys.argv[1]) as f:
  buffer = []
  facts = []

  collect_properties = False
  for line in f:
    line = line.strip()

    if line == '{':
      # print("Facts start")
      facts.append({buffer.pop().strip(): "\n".join(buffer)})
      collect_properties = True
      continue

    if line == '}':
      # print("Facts stop")
      collect_properties = False
      buffer = []
      continue
    
    if collect_properties:
      # print("Collecting props")
      # print(line.split('='))
      name, value = map(lambda x: x.strip(), line.split('='))
      facts[-1][name] = value
      continue

    # print("Lead")
    buffer.append(line)


print(facts)
