import sys
import socket

def main(args):
    #"Straight up" GET!
    address = args[1]
    port = args[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, int(port)))
    s.send("GET / HTTP/1.0\r\n\r\n")

    result = ""
    while True:
        data = s.recv(1000)
        if not data:
            break
        result += data

    s.close()

    resultTest = "<a href='content'>a file</a>" in result
    assert resultTest != False, resultTest

def image_test(args):
    #Test get of the image
    address = args[1]
    port = args[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, int(port)))
    s.send("GET /helmet HTTP/1.0\r\n\r\n")

    fp = s.makefile("request_image")

    for line in fp:
        if "Content-Length: " in line:
            fileSize = int(line.strip("Content-Length: "))
            break

    fp1 = open("Spartan-helmet-Black-150-pxls.gif","r")

    result = ""
    for line in fp1:
        result+=line

    s.close()

    resultTest = len(result)

    assert resultTest == fileSize, resultTest
    
def form_test(args):
    address = args[1]
    port = args[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, int(port)))
    s.send("GET /recv?firstname=Aaron&lastname=Bob HTTP/1.0\r\n\r\n")

    result = ""
    while True:
        data = s.recv(1000)
        if not data:
            break
        result += data
    s.close()

    resultTest = "First name: Aaron; last name: Bob" in result 
    assert resultTest != False, resultTest
    
    
if __name__ == '__main__':
    main(sys.argv)
    image_test(sys.argv)
    form_test(sys.argv)
