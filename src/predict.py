import time
import base64
import os
from PIL import Image
from io import BytesIO

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

def predict_wbc(files):
    """
    Placeholder function. Receives a list of image files.
    Returns an HTML string visualizing batch prediction results.
    """
    if not files:
        error_html = "<h4 style='color: #dc3545; font-family: sans-serif; font-weight: 500;'>Please upload at least one image before analyzing.</h4>"
        return error_html

    # Simulate AI processing time
    time.sleep(1.5)

    html_content = "<div style='display: flex; flex-direction: column; gap: 15px; margin-top: 10px;'>"
    
    for idx, file_obj in enumerate(files):
        # Extract file path
        if hasattr(file_obj, 'name'):
            file_path = file_obj.name
        else:
            file_path = str(file_obj)
            
        filename = os.path.basename(file_path)
        img_b64 = image_to_base64_thumbnail(file_path)
        
        # Simulated prediction outcomes
        dummy_wbc_class = "Neutrophil" if idx % 3 != 0 else "Lymphocyte"
        dummy_confidence = 0.85 + (idx % 15) * 0.01
        
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
                <h4 style="margin: 0 0 8px 0; color: #222; font-size: 16px;">Type: <span style="color: #007bff;">{dummy_wbc_class}</span></h4>
                <div style="background-color: #f0f0f0; border-radius: 4px; height: 10px; width: 100%; overflow: hidden;">
                    <div style="background-color: #007bff; border-radius: 4px; height: 100%; width: {dummy_confidence * 100}%;"></div>
                </div>
                <div style="font-size: 13px; color: #555; margin-top: 4px; font-weight: 500;">Confidence: {int(dummy_confidence * 100)}%</div>
            </div>
            
            <div style="flex-shrink: 0; padding: 12px; border-radius: 4px; background-color: {status_color}; border: 1px solid {border_color}; width: 220px; text-align: center;">
                <h5 style="color: {text_color}; margin: 0 0 6px 0; font-size: 15px;">{status_text}</h5>
                <div style="font-size: 12px; color: #444; line-height: 1.3;">{desc}</div>
            </div>
        </div>
        """
        
    html_content += "</div>"
    return html_content