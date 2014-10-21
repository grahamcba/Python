__author__ = 'graham'
import pyimgur

def imgur(path):
    f = open('Imgur_auth_file.txt')
    lines = f.readlines()
    f.close()
    API_KEY = lines[0].strip()
    CLIENT_ID = lines[1].strip()
    # PATH = "Radar.jpg"
    print "Uploading " + path + " to Imgur..."
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(path)
    url = uploaded_image.link[0:-4]
    print "URL: " + url

    return (url)


if __name__ == '__main__':
    imgur('1.JPG')