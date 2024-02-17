
# This is the configuration file, the variables 
# that are used in various functions are stored 
# here and do not change over time
configuration = {
    'connection': {
        'Sddi': 'Dani',
        'Password': '123456789',
    },
    'requests': {
        'Url': 'http://192.168.48.15:80/api/send_data',
        'Datanumber': '1'
    },
    'bno055':{
        'scl_pin' : '22',
        'sda_pin' : '21'
    },
    'gps' : {
        'tx_pin' : '16',
        'time_zone' : '-5'
    },
    'motor' : {
        'dir_pin' : '15',
        'step_pin' : '4',
        'enable_pin' : '23',
        'revolution' : '200'
    },
    'rele' : {
        'rele_pin' : '32'
    }
}