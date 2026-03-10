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
                label="Upload Blood Smear Images (Drag & Drop or Click)",
                file_count="multiple",
                file_types=["image"],
                elem_id="image_upload"
            )
            
            # State to accumulate uploaded files
            accumulated_files = gr.State([])
            
            # Gallery to visually show all accumulated images
            image_gallery = gr.Gallery(
                label="Accumulated Images",
                show_label=True,
                elem_id="image_gallery",
                columns=4,
                height=250,
                object_fit="contain"
            )
            
            with gr.Row():
                clear_btn = gr.Button("Clear All", variant="secondary")
                analyze_btn = gr.Button("Analyze All", variant="primary")
                
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

    # Helper function to accumulate files and clear the upload input
    def add_files(new_files, current_files):
        if not current_files:
            current_files = []
        if new_files:
            # Combine current files with new ones, avoiding duplicates by filename
            current_names = [os.path.basename(f) if isinstance(f, str) else os.path.basename(f.name) for f in current_files]
            for f in new_files:
                path = f if isinstance(f, str) else f.name
                name = os.path.basename(path)
                if name not in current_names:
                    current_files.append(path)
                    current_names.append(name)
        # Returns: Accumulated State, Gallery Component, File Input Content (cleared)
        return current_files, current_files, None

    print("AJSDLADLJAS")
    # When files are uploaded, add them to state, show in gallery, and clear the upload box
    image_input.upload(
        fn=add_files,
        inputs=[image_input, accumulated_files],
        outputs=[accumulated_files, image_gallery, image_input]
    )
    
    # 1. Analyze Button uses accumulated state
    analyze_btn.click(
        fn=predict_wbc,
        inputs=accumulated_files,
        outputs=batch_output
    )
    
    # 2. Clear Button clears input, state, gallery, and output
    clear_btn.click(
        fn=lambda: (None, [], None, ""),
        inputs=[],
        outputs=[image_input, accumulated_files, image_gallery, batch_output]
    )

if __name__ == "__main__":
    demo.launch(theme=theme)
