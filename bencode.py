from collections import OrderedDict

class BencodeDecoder:
    def __init__(self) -> None:
        self.data = None
        self.index = 0

    def decode(self, data: bytes):
        try:
            self.data = data
            self.index = 0
            if self.index >= len(self.data):
                raise Exception("!ERROR! => Unexpected end of data")
            else:
                char = chr(self.data[self.index])

                if char == 'i':
                    return self.decode_integer()
                elif char == 'l':
                    return self.decode_list()
                elif char == 'd':
                    return self.decode_dictionary()
                elif char.isdigit():
                    return self.decode_string()
                else:
                    raise Exception(f"!ERROR! => Invalid bencode data with index {self.index}")
        except Exception as e:
            print(f"!ERROR! => Decode DATA error: {e}")
            return None

    def decode_integer(self):
        try:
            self.index += 1
            end_index = self.data.find(b'e', self.index)

            if end_index == -1:
                raise Exception("Invalid integer format")
            else:
                number_str = self.data[self.index:end_index].decode('ascii')

                if not (number_str.isdigit() or (number_str.startswith('-') and number_str[1:].isdigit())):
                    raise Exception(f"Invalid integer value: {number_str}")
                else:
                    number = int(number_str)
                    self.index = end_index + 1
                    return number
        except Exception as e:
            print(f"!ERROR! => Decode INT error: {e}")
            return None

    def decode_string(self):
        try:
            colon_index = self.data.find(b':', self.index)
            if colon_index == -1:
                raise Exception("Invalid string length format")
            else:
                length_str = self.data[self.index:colon_index].decode('ascii')
                if not length_str.isdigit():
                    raise Exception(f"Invalid string length: {length_str}")
                else:
                    length = int(length_str)
                    self.index = colon_index + 1
                    end_index = self.index + length
                    if end_index > len(self.data):
                        raise Exception("Unexpected end of string data")
                    else:
                        string = self.data[self.index:end_index]
                        self.index = end_index
                        return string
        except Exception as e:
            print(f"!ERROR! => Decode STR error: {e}")
            return None

    def decode_list(self):
        try:
            self.index += 1
            result = []

            while chr(self.data[self.index]) != 'e':
                result.append(self.decode(self.data[self.index:]))
            self.index += 1

            return result
        except Exception as e:
            print(f"!ERROR! => Decode LIST error: {e}")
            return None

    def decode_dictionary(self):
        try:
            self.index += 1
            result = OrderedDict()

            while chr(self.data[self.index]) != 'e':
                key = self.decode_string()
                value = self.decode(self.data[self.index:])
                result[key] = value
            self.index += 1

            return result
        except Exception as e:
            print(f"!ERROR! => Decode DICT error: {e}")
            return None
        
class BencodeEncoder:
    def encode(self, data):
        if isinstance(data, int):           
            return self.encode_integer(data)
        elif isinstance(data, str):
            return self.encode_string(data.encode('utf-8'))
        elif isinstance(data, bytes):
            return self.encode_string(data)
        elif isinstance(data, list):
            return self.encode_list(data)
        elif isinstance(data, dict):
            return self.encode_dictionary(data)
        else:
            raise TypeError("!ERROR! => Unsupported DATA type")

    def encode_integer(self, integer):
        return b"i" + str(integer).encode('ascii') + b"e"

    def encode_string(self, string):
        length = str(len(string)).encode('ascii')
        return length + b":" + string

    def encode_list(self, lst):
        encoded_list = bytearray(b"l")
        for item in lst:
            encoded_list.extend(self.encode(item))
        encoded_list.extend(b"e")
        return encoded_list

    def encode_dictionary(self, dct):
        encoded_dict = bytearray(b"d")
        ordered_dict = sorted(dct.items())
        for key, value in ordered_dict:
            encoded_dict.extend(self.encode(key))
            encoded_dict.extend(self.encode(value))
        encoded_dict.extend(b"e")
        return encoded_dict