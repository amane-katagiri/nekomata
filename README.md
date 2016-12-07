# Nekomata
A simple ARP packet logger.

## usage
```
nekomata [-e regex_of_message] [-f path/to/regex_of_message.txt] [-g name_of_function_returns_message] [-l logger] [--config path/to/config.toml] [MA:C_:AD:DR:ES:S1] [MA:C_:AD:DR:ES:S2] ...
```
If Nekomata recieves ARP packet (duplicate address detection mode) from `MA:C_:AD:DR:ES:S1`, `MA:C_:AD:DR:ES:S2`, ..., `MA:C_:AD:DR:ES:Sn`, Nekomata sends a message which meets `regex_of_message` or `regex_of_message.txt` to `logger`.

note:
* Nekomata needs root privileges.
* If you don't specify `-e`, `-f` and `-g`, Nekomata sends recieved MAC address.
* If you don't specify `-l`, Nekomata uses `StreamHandler`.
* If you don't specify MAC address or use `00:00:00:00:00:00`, Nekomata react the packets from all clients.
* Configuration of `00:00:00:00:00:00` in `--config` will be overwritten by other explicit options.

## installation
```
git clone https://github.com/amane-katagiri/nekomata.git
cd nekomata
pip install -e .
```

## configuration

Write configuration file in toml format. You can change loggers and messages per MAC address. If you specify the behavior of `01:23:45:67:89:ab`, set the title of section `["01:23:45:67:89:ab"]`. You can use `["00:00:00:00:00:00"]` to react the packets from all clients.

Sample files are in samples/.

* handler: handler name
* log_format_text: regex of message (literal)
* log_format_file: regex of message (file)
* log_format_func: regex of message (name of Python function(MAC address(str) -> message(str)))
* senders: additional MAC address list (empty ok)
* option: table of params which are passed to handler
