import cv2
import random
import os
from time import sleep
key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
sleep(2)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/mppil/code/scav/VisionDemo-6e8e38ef92aa.json'

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
    return objects


font = cv2.FONT_HERSHEY_SIMPLEX 
org = (0, 100)
fontScale = 2
color = (0, 255, 255) 
thickness = 2

target = random.choice(['Cat'])


while True:
    try:
        check, frame = webcam.read()
        print(check) #prints true as long as the webcam is running
        print(frame) #prints matrix values of each framecd 
        
        image = cv2.putText(frame, f'Show me: {target}', org, font, fontScale, color, thickness, cv2.LINE_AA) 

        cv2.imshow("Capturing", image)
        key = cv2.waitKey(1)
        if key == ord('s'): 
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            webcam.release()
            print("Processing image...")
            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
    
            print("Image saved!")
            
            break
        
        elif key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break
    
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break

org1 = (0,412)
if os.path.exists('saved_img.jpg'):
    objs = localize_objects('saved_img.jpg')
    found = 0
    frame = cv2.imread('saved_img.jpg')

    for obj in objs:
        if obj.name.lower() == target.lower():
            image = cv2.putText(frame, 'You found it!', org1, font, fontScale, color, thickness, cv2.LINE_AA) 
            #cv2.imshow("Win", image)
            found = 1
            print("You win!")
    if found == 0:
        image = cv2.putText(frame, 'You lose :(', org1, font, fontScale, color, thickness, cv2.LINE_AA) 
        #cv2.imshow("Loss", image)

while True:
    cv2.imshow("Win", image)
    key = cv2.waitKey(1)
    if key == ord('q'): 
        exit(1)
