import usb.core

#58:B0:3E:07:25:14


devices.reset()

if devices.is_kernel_driver_active(interface.bInterfaceNumber):
    devices.detach_kernel_driver(interface.bInterfaceNumber)

devices.set_configuration()

def read(devicess, endpoint):
    answer = devicess.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
    print('read: ' + ''.join([ '%02X' %x for x in answer]) + '\n')
    return answer

def write(devicess, endpoint, hexa, idd):
    devicess.write(endpoint.bEndpointAddress, hexa, 0)
    print('send: ' + idd)

read(devices, readEndpoint)

write(devices, writeEndpoint, '\x04\x20\x01\x00','A')
read(devices, readEndpoint)

write(devices, writeEndpoint, '\x01\x20\x01\x09\x00\x04\x20\x3A\x00\x00\x00\xCA\x00','B')
read(devices, readEndpoint)
read(devices, readEndpoint)
    
write(devices, writeEndpoint, '\x01\x20\x01\x09\x00\x04\x20\x04\x01\x00\x00\x00\x00','C')
read(devices, readEndpoint)

read(devices, readEndpoint)
read(devices, readEndpoint)

write(devices, writeEndpoint, '\x05\x20\x02\x0F\x06\x00\x00\x00\x00\x00\x00\x55\x53\x00\x00\x00\x00\x00\x00','E')

write(devices, writeEndpoint, '\x05\x20\x03\x01\x00','F')
#write(devices, writeEndpoint, '\x0A\x20\x04\x03\x00\x01\x14','G')

#read(devices, readEndpoint)

#write(devices, writeEndpoint, '\x06\x30\x01\x3A\x00\x41\x00\x01\x00\x2C\x01\x01\x00\x28\xD9\xE9\x11\xB1\x9C\x94\x7E\x40\xCA\xE0\xC6\x6C\xDA\xCA\xE3\x28\x94\x82\x7E\x20\xF8\x80\x47\x83\x71\x92\x54\x0C\x52\xEB\x72\x9F\x00\x00\x00\x00\x45\x7B\xAF\xE9\x00\x00\x00\x00\x00\x00\x00\x00','H')
#read(devices, readEndpoint)
#read(devices, readEndpoint)
#write(devices, writeEndpoint, '\x01\x20\x01\x09\x00\x06\x20\x06\x00\x00\x00\x00\x00','I')

#write(devices, writeEndpoint, '\x06\x30\x02\x0E\x00\x42\x00\x02\x00\x54\x00\x00\x00\x00\x00\x00\x00\x00','J')
#read(devices, readEndpoint)
#read(devices, readEndpoint)

#write(devices, writeEndpoint, '\x01\x20\x02\x09\x00\x06\x20\x3A\x00\x00\x00\x20\x00','K')
#read(devices, readEndpoint)

#write(devices, writeEndpoint, '\x01\x20\x02\x09\x00\x06\x20\x5A\x00\x00\x00\x00\x00','L')
#read(devices, readEndpoint)


read(devices, readEndpoint)
read(devices, readEndpoint)
read(devices, readEndpoint)
read(devices, readEndpoint)
read(devices, readEndpoint)
read(devices, readEndpoint)
read(devices, readEndpoint)

