import cv2
import insightface
import matplotlib.pyplot as plt

# Initialize the face analysis model
model = insightface.app.FaceAnalysis(name='buffalo_l', root='./models')  # models will be saved in './models'
model.prepare(ctx_id=-1)  # -1 means CPU, 0 means first GPU

# Load an image
img_path = r"C:\Users\ekong\CNN face recognition\insightface-master\Images\Lucresia.jpg" # <-- CHANGE THIS to an actual image path
img = cv2.imread(img_path)
if img is None:
    print("Error: Could not load image. Check the path.")
    exit()

# Detect faces
faces = model.get(img)

print(f"Found {len(faces)} face(s).")

# Draw bounding boxes on the image
for face in faces:
    bbox = face.bbox.astype(int)
    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
    # You can also add landmarks, age, gender etc.
    # For example: print(face.landmark)

# Convert BGR to RGB for displaying with matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.axis('off')
plt.show()