import gradio as gr
import os
from src.predict import predict_wbc

theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Prompt"), "sans-serif"]
)

with gr.Blocks(title="LUEATTOK-AI") as demo:
    # Header & Subheader
    gr.Markdown(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto; padding-top: 20px;">
            <h1>LUEATTOK-AI: White Blood Cell Analyzer</h1>
            <p style="font-size: 16px; color: #555;">
                Upload cropped white blood cell images to analyze types and detect abnormalities. Batch processing is supported.
            </p>
        </div>
        """
    )
    
    with gr.Row():
        # Left Column: Input
        with gr.Column(scale=1):
            gr.Markdown("### Input Data")
            image_input = gr.File(
                label="Upload Blood Smear Images (Multiple allowed)",
                file_count="multiple",
                file_types=["image"],
                elem_id="image_upload"
            )
            
            with gr.Row():
                clear_btn = gr.Button("Clear", variant="secondary")
                analyze_btn = gr.Button("Analyze", variant="primary")
                
        # Right Column: Output
        with gr.Column(scale=1):
            gr.Markdown("### Analysis Results")
            
            # Box 1: HTML Report for batch results
            batch_output = gr.HTML(
                label="Batch Analysis Report"
            )
            
    # Bottom: Examples
    gr.Markdown("---")
    gr.Markdown("### Examples")
    gr.Markdown("Click the example below to instantly test the system with sample images.")
    
    # Fetch example images
    examples_dir = os.path.join("data", "examples")
    example_images = []
    
    if os.path.exists(examples_dir):
        valid_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
        for f in os.listdir(examples_dir):
            if os.path.splitext(f)[1].lower() in valid_exts:
                example_images.append(os.path.join(examples_dir, f))
                
    if example_images:
        gr.Examples(
            examples=[[example_images]],
            inputs=image_input,
            label="Sample Batch"
        )
    else:
        gr.Markdown("*No example images found in data/examples directory.*")

    # --- Event Listeners ---
    
    # 1. Analyze Button
    analyze_btn.click(
        fn=predict_wbc,
        inputs=image_input,
        outputs=batch_output
    )
    
    # 2. Clear Button
    clear_btn.click(
        fn=lambda: (None, ""),
        inputs=[],
        outputs=[image_input, batch_output]
    )

if __name__ == "__main__":
    demo.launch(theme=theme)
