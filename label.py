import argparse
import base64

import googleapiclient.discovery

def main(photo_file):

    service = googleapiclient.discovery.build('vision', 'v1')

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()
        texts = response['responses'][0]['labelAnnotations']
        for text in texts:
                text_val = text['description']
                print('Found label: %s for %s' % (text_val, photo_file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
