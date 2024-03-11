from turtle import color
from webbrowser import BackgroundBrowser
from PIL import Image,ImageDraw
import azure.ai.vision as sdk
from matplotlib import pyplot as plt

image_file = "images\grocery.jpg"
endpoint = "https://analyzeimagess.cognitiveservices.azure.com/"
key = "5a1ecd24c57e4aaf876314675ba6c752"

authentication = sdk.VisionServiceOptions(endpoint,key)

analysis_options =sdk.ImageAnalysisOptions()

analysis_options.features = (

        sdk.ImageAnalysisFeature.CAPTION |
        sdk.ImageAnalysisFeature.DENSE_CAPTIONS |
        sdk.ImageAnalysisFeature.OBJECTS|
        sdk.ImageAnalysisFeature.PEOPLE

)

image = sdk.VisionSource(image_file)
image_analyzer = sdk.ImageAnalyzer(authentication,image,analysis_options)

result = image_analyzer.analyze()

print("\nCaption: ")
print(result.caption.content)

print("\nDense caption: ")
for capt in result.dense_captions:
    print("Caption: '{}'(Confidence:{:.2f})".format(capt.content,capt.confidence*100))
    # print(capt.content + ":",str(round(capt.confidence*100))+"%")


print("\nDetected Objects: ")
for detected_object in result.objects:
    # Replace 'name_attribute' with the actual attribute for the object name in your SDK
    object_name = getattr(detected_object, 'name_attribute', 'Unknown Object')
    print("Object: '{}' (Confidence: {:.2f})".format(object_name, detected_object.confidence*100))


######## objects
    
# print("\n Analyzing objects")
# image = Image.open(image_file)
# fig = plt.figure(figsize=(image.width/100,image.height/100))
# plt.axis('off')
# draw = ImageDraw.Draw(image)
# color = "cyan"

# for detected_objects in result.objects:
#     r = detected_objects.bounding_box
#     bouding_box = ((r.x,r.y),(r.x + r.w, r.y + r.h))
#     draw.rectangle(bouding_box,outline=color,width=3)
#     plt.annotate(detected_objects.name,(r.w,r.y),backgroundcolor=color)

# print(plt.imshow(image))
# output = "objects.jpg"
# fig.savefig(output)
# print("Results are saved in ",output)



############ people detection ##########


print("\n Analyzing Pople:")
image = Image.open(image_file)
fig = plt.figure(figsize=(image.width/100,image.height/100))
plt.axis('off')
draw = ImageDraw.Draw(image)
color = "cyan"

for detected_objects in result.people:
    r = detected_objects.bounding_box
    bouding_box = ((r.x,r.y),(r.x + r.w, r.y + r.h))
    draw.rectangle(bouding_box,outline=color,width=3)


print(plt.imshow(image))
output = "people.jpg"
fig.savefig(output)
print("Results are saved in ",output)
