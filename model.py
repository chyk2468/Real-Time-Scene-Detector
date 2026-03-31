from ultralytics import YOLO
import cv2
import os

# Load model once
model = YOLO("model.pt")

def detect_and_guess_scene(image_path, output_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found or invalid")

    # Object detection
    results = model(img)
    boxes = results[0].boxes

    # Count objects
    object_counts = {}
    for box in boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        object_counts[label] = object_counts.get(label, 0) + 1

    # Scene guessing
    scene = guess_scene(object_counts)

    # Draw detections
    output_img = results[0].plot()

    # Put scene text
    cv2.putText(
        output_img,
        f"Scene: {scene}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imwrite(output_path, output_img)

    return object_counts, scene, output_path


def guess_scene(obj):
    # Normalized counts for cleaner logic
    person = obj.get("person", 0)
    car = obj.get("car", 0)
    bus = obj.get("bus", 0)
    truck = obj.get("truck", 0)
    traffic_light = obj.get("traffic light", 0)
    bench = obj.get("bench", 0)
    chair = obj.get("chair", 0)
    couch = obj.get("couch", 0)
    potted_plant = obj.get("potted plant", 0)
    bed = obj.get("bed", 0)
    dining_table = obj.get("dining table", 0)
    tv = obj.get("tv", 0)
    laptop = obj.get("laptop", 0)
    mouse = obj.get("mouse", 0)
    keyboard = obj.get("keyboard", 0)
    cell_phone = obj.get("cell phone", 0)
    microwave = obj.get("microwave", 0)
    oven = obj.get("oven", 0)
    toaster = obj.get("toaster", 0)
    sink = obj.get("sink", 0)
    refrigerator = obj.get("refrigerator", 0)
    cup = obj.get("cup", 0)
    bottle = obj.get("bottle", 0)
    wine_glass = obj.get("wine glass", 0)
    knife = obj.get("knife", 0)
    fork = obj.get("fork", 0)
    spoon = obj.get("spoon", 0)
    bird = obj.get("bird", 0)
    cat = obj.get("cat", 0)
    dog = obj.get("dog", 0)
    tree = obj.get("tree", 0)

    # --- INDOOR SCENES ---
    
    # Office / Workspace
    if (laptop > 0 or mouse > 0 or keyboard > 0) and (chair > 0 or desk_check(obj)):
        return "Office / Workspace"

    # Kitchen
    if (microwave > 0 or oven > 0 or toaster > 0) or (sink > 0 and refrigerator > 0):
        return "Kitchen"

    # Dining Room
    if dining_table > 0 or (wine_glass > 0 and (knife > 0 or fork > 0)):
        return "Dining Room"

    # Living Room
    if couch > 0 and (tv > 0 or potted_plant > 0):
        return "Living Room"

    # Bedroom
    if bed > 0:
        return "Bedroom"

    # Bathroom
    if obj.get("toilet", 0) > 0 or (sink > 0 and obj.get("toothbrush", 0) > 0):
        return "Bathroom"

    # --- OUTDOOR / PUBLIC SCENES ---

    # Market / Crowded
    if person > 8 and (car > 1 or obj.get("backpack", 0) > 2 or obj.get("handbag", 0) > 2):
        return "Market / Crowded Area"

    # Street / Traffic
    if (car + bus + truck) > 2 or traffic_light > 0:
        return "Street / Traffic"

    # Park
    if (bench > 0 or person > 0) and (tree > 0 or bird > 0 or dog > 0):
        return "Park / Outdoor"

    # Restaurant / Cafe
    if dining_table > 0 and person > 2 and (cup > 0 or bottle > 0):
        return "Restaurant / Cafe"

    # --- FALLBACKS ---
    
    if person > 0:
        return "Public Place / Generic"

    if bird > 0 or cat > 0 or dog > 0:
        return "Animal / Nature"

    return "Unknown Scene"

def desk_check(obj):
    # Heuristic for a desk if 'dining table' is detected but context suggests work
    return obj.get("dining table", 0) > 0
