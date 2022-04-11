def DataGaurd(val,func = None, process = 'decrypt'):
    """   
    DataGaurd is a encryption and decryption tool that can help you encrypt your dictionary or JSON data
    for added security over API while allowing you to decide how your data is encrypted
    
     just create your encryption or decryption function that takes one value e.g
     
      def  encrypto(value) :
          result = encrypt_my_data(value)
          return result
          
      then pass it to the DataGaurd function
      
      DataGaurd(my_data, func=encrypto, process= 'encode')
    
    note: without func being passed default encoding is used
    
    """
    import base64 as b
    from threading import Thread as tr
    middler = {}
    result = {}
    encoder = 'ascii'
    
    def decrypt(v):
        v = v.encode(encoder)
        v = b.b64decode(v)
        v = v.decode(encoder)
        return v
    def encrypt(v):
         v = v.encode(encoder)
         v = b.b64encode(v)
         v = v.decode(encoder)
         return v
    def convert_from_string_with_type(val):
        # splitting received val into data and type
        val_data, val_type = val.split('-->>')
        # checking the data type and evaluating the result  
        if val_type == 'str':
            result = val_data
        elif val_type == 'int':
            result = int(val_data) 
        else:
            result = eval(val_data)
        return result    
         
    def convert_to_string_with_type(val):
        # checking the type of the value passed and getting its name in string
        val_type = str(type(val)).split()[1].split('>')[0].split("'")[1]
        result = f'{val}-->>{val_type}'
        return  result

    
    
    
    
    if func == None:
        if process == 'decrypt':
            func = decrypt
        elif process == "encrypt":
            func = encrypt
        else:
            raise Exception('PROCESS ERROR : process can only be encrypt or decrypt')
    
    if type(func) != type(decrypt):
        raise Exception('please you didn\'t pass a function to func keyword')
    
    
    def make_crypted_data_key(middler_key):
        for crypted in val.keys():
            if middler_key == crypted:
                result[middler[middler_key]] = val[crypted]
                
                
    def make_crypted_data_value(key):
        if process == 'decrypt':
            value = func(result[key]) 
            result[key] = convert_from_string_with_type(value)
        elif process == "encrypt":
            value = convert_to_string_with_type(result[key])
            result[key] = func(value)
    
    # getting all keys from the
    for key in val.keys():
        decrypted_key = func(key)
        middler[key] = decrypted_key
    
    # encrypting encrypted keys
    for key in middler.keys():
        t = tr(target=make_crypted_data_key, args=(key,))
        t.start()
    t.join()
    
    # encrypting or decrypting data value
    for key in result.keys():
        t = tr(target=make_crypted_data_value, args=(key,))
        t.start()
    t.join()
    
    return result

 
##  test cases
# a = {'help'  : 'wisdom', 'asl':'wel'}
#a = {'aGVscA==': 'd2lzZG9tLS0+PnN0cg==', 'YXNs': 'd2VsLS0+PnN0cg=='}
# print(DataGaurd(a, process= 'encrypt'))