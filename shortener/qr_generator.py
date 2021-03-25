import base64,io,qrcode
from qrcode import constants


def generate_qrcode_as_base64(data:str):
    """
    function that returns qrcode data.
    """
    qr=qrcode.QRCode(error_correction=constants.ERROR_CORRECT_H)
    qr.add_data(data=data)                                                      # add the data to the qr object
    img=qr.make_image()                                                         # generate qr image
    binary_image_data=io.BytesIO()                                              # create a binary IO stream
    img.save(binary_image_data,format='PNG')                                    # save the image data to the binary stream
    b64_encoded_data = base64.b64encode(binary_image_data.getvalue())           # base64 encode the binary data
    return b64_encoded_data


def qr_code(db_data,host_url):
    """
    function that calls the generate_qrcode_as_base64() to generate qrcode and
    return it as a dictionary.
    """
    qr_data_of_tiny_url = generate_qrcode_as_base64(host_url+'/'+db_data.tiny_url).decode('ascii')
    qr_data_of_full_url = generate_qrcode_as_base64(db_data.full_url).decode('ascii')
    return {
        'qr_full_url':qr_data_of_full_url,
        'qr_tiny_url':qr_data_of_tiny_url,
        }

if __name__ =="__main__":
    # a demo usage
    b64_data = generate_qrcode_as_base64("hello")
    print(b64_data.decode('ascii'))