# from urllib import response
# from flask_ngrok import run_with_ngrok
# from flask import Flask, request,jsonify, Response, make_response
# from flask import send_file, after_this_request
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
# from TreeCounting import*
# from PIL import Image
# import base64
# import io
import boto3
# import os
from base64 import b64decode, b64encode
# import gc
from wtprediction import*
import uuid
import json

# model_path= '/models/detectqutzV1.tflite'
# ocr_model='/models/OCR_CNN_v6_quntz_v1.tflite'

# app = Flask(__name__)
# CORS(app)
# run_with_ngrok(app)
# path = os.getcwd() #"/content/"
# UPLOAD_FOLDER =os.path.join(path, 'uploads')
# if not os.path.isdir(UPLOAD_FOLDER):
#     os.mkdir(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ACCESS_KEY = ''
SECRET_KEY = ''
# key='detectTree_v2.tflite'
bucket_name='sroybucket'
# modelBucket='facerecogmodel'

aws_session=boto3.Session(aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

s3_client = aws_session.client('s3')#,aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def upload_to_aws(local_file, bucket, s3_file):
    print ('the file to be uploaded ', local_file)
    s3 = s3_client
    # s3_resource = boto3.resource('s3')
    # s3_resource.Object('facerecogmodel',key).put(Body=local_file)
    try:
        s3.upload_fileobj(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    # except NoCredentialsError:
    #     print("Credentials not available")
    #     return False

# app = Flask(__name__)

#pathOut="/content/113124_trimb_demoPrdctBoxKPS10.mp4"

#Function for prediction  
#

# def handler(event, context):
#     print('start')
#     output_directory=str(uuid.uuid4())
#     fname=output_directory+'.tif'
#     if not os.path.isdir(output_directory):
#                 os.mkdir(output_directory)
#     bucket_name = bucket_name #event['Records'][0]['s3']['bucket']['name']
#     key = fname #event['Records'][0]['s3']['object']['key']
#     # obj_name = key.split('/')[-1]
#     # full_path = f's3://{bucket_name}/{key}'
#     s3 = boto3.client('s3')
#     s3.upload_fileobj(output_directory, bucket_name, key)
#     input_image = s3_client.generate_presigned_url('get_object', 
#                                                              Params = {'Bucket': bucket_name, 
#                                                                        'Key': fname}, ExpiresIn = 100)
#     prdData=splitraster(input_image,output_directory,save_vrt=False)
#     print ('done!')
#     # csvFile='windTur.csv'
#     # file = open(csvFile, 'a+', newline ='')
#     fields=['Lat','Long']
#     # writing the data into the file
#     # with file:
#     #     write = csv.writer(file)
#     #     write.writerow(fields)
#     #     write.writerows(prdData)
#     shutil.rmtree(output_directory)
#     return {
#         'statusCode': 200,
#         'body': json.dumps(prdData)
#     }


# @app.route("/windturb/",methods= ['POST','GET'])
# def windturb():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         fname = uploaded_file.filename
#         print (fname)
#         if uploaded_file !='':
#             upload_to_aws(uploaded_file,bucket_name,fname)
#             input_image = s3_client.generate_presigned_url('get_object', 
#                                                              Params = {'Bucket': bucket_name, 
#                                                                        'Key': fname}, ExpiresIn = 100)

#             output_directory=str(uuid.uuid4())
#             if not os.path.isdir(output_directory):
#                 os.mkdir(output_directory)

#             # x_size,y_size=521,512
#             prdData=splitraster(input_image,output_directory,save_vrt=False)
#             print ('done!')
#             csvFile='windTur.csv'
#             file = open(csvFile, 'a+', newline ='')
#             fields=['Lat','Long']
#             # writing the data into the file
#             with file:
#                 write = csv.writer(file)
#                 write.writerow(fields)
#                 write.writerows(prdData)
#             shutil.rmtree(output_directory)
        
#     return prdData

# if __name__ == '__main__':
#     #app.run(ssl_context=('/home/ubuntu/0ml_crt.pem','/home/ubuntu/0ml_key.pem'),host='0.0.0.0',port=5001, debug=False)
#     app.run(host='0.0.0.0',port=5001)
#     # app.run()

