from common_ports import ports_and_services
import socket

socket.setdefaulttimeout(2)

def get_open_ports(target, port_range, verbose = False):
    open_ports = []

    url = None
    if target[-1].isalpha(): # url supplied
      url = target
      try:
        target = socket.gethostbyname(url)
      except socket.gaierror:
          return "Error: Invalid hostname"
    else:
      try:
        url, _, _ = socket.gethostbyaddr(target)
      except socket.herror:
        pass
      except socket.gaierror:
        return "Error: Invalid IP address"

    for port in range(port_range[0], port_range[1] + 1):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
        result = s.connect((target, port))
      except socket.timeout:
        print("timeout: " + target + ":" + str(port))
        pass
      except ConnectionRefusedError:
        print("connection refused: " + target + ":" + str(port))
        pass
      else:
        open_ports.append(port)
      s.close();

    if verbose:
      if url == None:
        out = "Open ports for " + target + "\n"
      else:
        out = "Open ports for " + url + " (" + target + ")\n"
      out += "PORT     SERVICE\n"
      for port in open_ports:
        if port != open_ports[0]:
          out += "\n"
        out += pad_num(port, 5) + "    " + ports_and_services[port]
      return out
    else:
      return open_ports

def pad_num(num, length):
  curr_length = len(str(num))
  spaces_to_add = length - curr_length
  spaces_to_add = max(0, spaces_to_add)
  out = str(num)
  for i in range(0, spaces_to_add):
    out += " "
  return out