import time
import base64
import os
from PIL import Image
from io import BytesIO
import cv2

def image_to_base64_thumbnail(img_path, max_size=(100, 100)):
    try:
        if hasattr(img_path, 'name'):
            path = img_path.name
        else:
            path = str(img_path)
            
        with Image.open(path) as img:
            img.thumbnail(max_size)
            buffered = BytesIO()
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        print(f"Error creating thumbnail for {img_path}: {e}")
        return ""


def crop_and_label_objects(result):
    """
    Extracts bounding boxes from a YOLO result, crops them from the clean image,
    and grabs the associated class labels.
    
    Args:
        result: A single Ultralytics Results object.
        
    Returns:
        list: A list of dictionaries, each containing the cropped image array, 
              the class ID (int), and the class name (string).
    """
    extracted_data = []
    
    # Get the clean original image and convert to RGB
    orig_img_rgb = cv2.cvtColor(result.orig_img, cv2.COLOR_BGR2RGB)
    
    # Get the dictionary mapping class IDs to class names (e.g., {0: 'cell_x', 1: 'cell_y'})
    class_names = result.names
    
    for box in result.boxes:
        # 1. Get coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # 2. Get the label
        # box.cls[0] is a tensor, so we use .item() to get the raw Python number, then cast to int
        class_id = int(box.cls[0].item()) 
        class_name = class_names[class_id]
        
        # 3. Crop the image
        crop = orig_img_rgb[y1:y2, x1:x2]

        conf_decimal = box.conf[0].item()
        
        # 4. Store them together if the crop is valid
        if crop.size > 0:
            extracted_data.append({
                "image": crop,
                "class_id": class_id,
                "class_name": class_name,
                "confidence": conf_decimal
            })
            
    return extracted_data


def predict_wbc(files):

    """
    Placeholder function. Receives a list of image files.
    Returns an HTML string visualizing batch prediction results.
    """
    if not files:
        error_html = "<h4 style='color: #dc3545; font-family: sans-serif; font-weight: 500;'>Please upload at least one image before analyzing.</h4>"
        return error_html

    # Simulate AI processing time

    # Model Setup.
    from ultralytics import YOLO
    model_weights = "models/weights/best.pt"
    
    if not os.path.exists(model_weights):
        error_html = f"<h4 style='color: #dc3545; font-family: sans-serif; font-weight: 500;'>Model file '{model_weights}' not found. Please ensure the model weights file is in the correct directory.</h4>"
        return error_html
    
    model = YOLO(model_weights)
    #print(f"Model loaded with classes: {model.names}")
    
    time.sleep(1.5)

    html_content = "<div style='display: flex; flex-direction: column; gap: 15px; margin-top: 10px;'>"
    
    for idx, file_obj in enumerate(files):
        # Extract file path
        if hasattr(file_obj, 'name'):
            file_path = file_obj.name
        else:
            file_path = str(file_obj)

        # Model Predicting.
        results = model.predict(file_path)
        wbc_class = None
        confidence = None
        for i, r in enumerate(results):

            detected_objects = crop_and_label_objects(r)
            print(f"\n--- Image {i+1}: Found {len(detected_objects)} objects ---")

            for j, obj_data in enumerate(detected_objects):
                    
                # Unpack the dictionary
                crop_array = obj_data["image"]
                label_id = obj_data["class_id"]
                wbc_class = obj_data["class_name"]
                wbc_class = wbc_class[:1].upper() + wbc_class[1:]
                label_name = obj_data["class_name"]
                confidence = obj_data["confidence"]
                
                print(f"Object {j+1}: It's a '{label_name}' (Class ID: {label_id})")
        
                # Show the image (optional)
                im = Image.fromarray(crop_array)
                #im.show() # Uncomment to pop open the images
        
                # ---> Pass `crop_array` AND `label_id` to your CNN here <---
                
                
        filename = os.path.basename(file_path)
        img_b64 = image_to_base64_thumbnail(file_path)

        # Use safe defaults when the model didn't detect any objects
        display_confidence = float(confidence) if confidence is not None else 0.0
        display_wbc_class = wbc_class if wbc_class else "Unknown"

        # Simulated prediction outcomes
        #dummy_wbc_class = label_name
        #dummy_confidence = 0.85 + (idx % 15) * 0.01
        
        # Alternate anomaly status for simulation
        if idx % 2 == 0:
            status_color = "#f8f9fa"
            border_color = "#e9ecef"
            text_color = "#198754"
            status_text = "Normal"
            desc = "No structural abnormalities detected."
        else:
            status_color = "#f8f9fa"
            border_color = "#e9ecef"
            text_color = "#dc3545"
            status_text = "Abnormal"
            desc = "Possible Atypical Lymphocyte or Blast cell."

        html_content += f"""
        <div style="display: flex; align-items: center; padding: 15px; border-radius: 4px; border: 1px solid #dee2e6; background-color: #ffffff; margin-bottom: 5px;">
            <div style="flex-shrink: 0; margin-right: 20px; text-align: center;">
                <img src="{img_b64}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 6px; border: 1px solid #ddd;" />
                <div style="font-size: 11px; margin-top: 5px; color: #777; width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{filename}">
                    {filename}
                </div>
            </div>
            
            <div style="flex-grow: 1; margin-right: 20px;">
                <h4 style="margin: 0 0 8px 0; color: #222; font-size: 16px;">Type: <span style="color: #007bff;">{display_wbc_class}</span></h4>
                <div style="background-color: #f0f0f0; border-radius: 4px; height: 10px; width: 100%; overflow: hidden;">
                    <div style="background-color: #007bff; border-radius: 4px; height: 100%; width: {display_confidence * 100}%;"></div>
                </div>
                <div style="font-size: 13px; color: #555; margin-top: 4px; font-weight: 500;">Confidence: {int(display_confidence * 100)}%</div>
            </div>
            
            <div style="flex-shrink: 0; padding: 12px; border-radius: 4px; background-color: {status_color}; border: 1px solid {border_color}; width: 220px; text-align: center;">
                <h5 style="color: {text_color}; margin: 0 0 6px 0; font-size: 15px;">{status_text}</h5>
                <div style="font-size: 12px; color: #444; line-height: 1.3;">{desc}</div>
            </div>
        </div>
        """
        
    html_content += "</div>"
    return html_content

