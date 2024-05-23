from collections import OrderedDict

class BencodeDecoder:
    def __init__(self) -> None:
        try:
            self.data = None
            self.index = 0
        except Exception as e:
            print(f"!ERROR! => Initialization error: {e}")

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
                raise Exception("!ERROR! => Invalid integer format")
            else:
                number_str = self.data[self.index:end_index].decode('ascii')

                if not (number_str.isdigit() or (number_str.startswith('-') and number_str[1:].isdigit())):
                    raise Exception(f"!ERROR => Invalid integer value: {number_str}")
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
                raise Exception("!ERROR! => Invalid string length format")
            else:
                length_str = self.data[self.index:colon_index].decode('ascii')
                if not length_str.isdigit():
                    raise Exception(f"!ERROR! => Invalid string length: {length_str}")
                else:
                    length = int(length_str)
                    self.index = colon_index + 1
                    end_index = self.index + length
                    if end_index > len(self.data):
                        raise Exception("!ERROR! => Unexpected end of string data")
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
        try:
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
        except Exception as e:
            print(f"!ERROR! => Encode DATA error: {e}")
            return None

    def encode_integer(self, integer):
        try:
            return b"i" + str(integer).encode('ascii') + b"e"
        except Exception as e:
            print(f"!ERROR! => Encode INT error: {e}")
            return None

    def encode_string(self, string):
        try:
            length = str(len(string)).encode('ascii')
            return length + b":" + string
        except Exception as e:
            print(f"!ERROR! => Encode STR error: {e}")
            return None

    def encode_list(self, lst):
        try:
            encoded_list = bytearray(b"l")
            for item in lst:
                encoded_list.extend(self.encode(item))
            encoded_list.extend(b"e")
            return encoded_list
        except Exception as e:
            print(f"!ERROR! => Encode LIST error: {e}")
            return None

    def encode_dictionary(self, dct):
        try:
            encoded_dict = bytearray(b"d")
            ordered_dict = sorted(dct.items())
            for key, value in ordered_dict:
                encoded_dict.extend(self.encode(key))
                encoded_dict.extend(self.encode(value))
            encoded_dict.extend(b"e")
            return encoded_dict
        except Exception as e:
            print(f"!ERROR! => Encode DICT error: {e}")
            return None