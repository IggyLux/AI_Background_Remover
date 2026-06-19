import gradio as gr
from rembg import remove
from PIL import Image
import tempfile
import uuid
import os
import warnings

# Hides harmless internal warnings (keeps the console clean for non-tech users)
warnings.filterwarnings("ignore", category=UserWarning, module="gradio")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="starlette")

def process_image(input_img, replace_bg, alpha_matting, bg_color_hex):
    if input_img is None:
        return None, None, "Please upload or drag an image."

    # Convert to RGB/RGBA to handle any weird AI-generated color profiles
    if input_img.mode != "RGBA" and input_img.mode != "RGB":
        input_img = input_img.convert("RGB")

    # Parse the hex color picker value (e.g., #FFFFFF)
    bg_color = (255, 255, 255, 255)  # default: solid white
    if bg_color_hex:
        try:
            hex_color = bg_color_hex.lstrip('#')
            if len(hex_color) == 6:
                bg_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        except:
            pass

    try:
        # Core AI processing (CPU ONLY)
        output = remove(
            input_img,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_structure_size=10
        )
    except Exception as e:
        return None, None, f"❌ Error: {str(e)}"

    result_img = None
    if replace_bg:
        # Paste the extracted subject onto a solid color background
        bg_img = Image.new("RGBA", output.size, bg_color)
        bg_img.paste(output, (0, 0), output)
        result_img = bg_img
        status_msg = "✅ Background replaced with solid color."
    else:
        result_img = output
        status_msg = "✅ Background removed (transparent PNG)."

    # Save as PNG to a temporary file for download
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"bg_removed_{uuid.uuid4().hex}.png")
    result_img.save(temp_path, format="PNG")  # FORCED PNG OUTPUT

    return result_img, temp_path, status_msg


# ---------- Build the GUI ----------
with gr.Blocks(title="Local Background Remover") as demo:
    gr.Markdown("# 🖌️ AI Background Remover (Local & CPU Only)")
    gr.Markdown("Drag & drop an image onto the box below, or click to browse your files.")

    with gr.Row(equal_height=True):
        with gr.Column():
            input_img = gr.Image(
                label="📤 Upload Image", 
                type="pil", 
                height=400, 
                sources=["upload"]  # Enables drag-drop + file browser
            )
            
            with gr.Row():
                replace_toggle = gr.Checkbox(
                    label="🟦 Replace with Solid Color", 
                    value=False
                )
                alpha_toggle = gr.Checkbox(
                    label="✨ Smooth Edges (Alpha Matting)", 
                    value=True
                )
            
            bg_color = gr.ColorPicker(
                label="🎨 Pick Background Color (if replacing)", 
                value="#FFFFFF"
            )
            
            process_btn = gr.Button("🚀 Remove Background", variant="primary", size="lg")
            
        with gr.Column():
            output_img = gr.Image(
                label="📥 Result", 
                type="pil", 
                height=400, 
                interactive=False
            )
            download_file = gr.File(
                label="💾 Download Result as PNG", 
                interactive=False, 
                visible=True
            )
            status_text = gr.Textbox(label="Status", interactive=False)

    # Connect the button to the processing function
    process_btn.click(
        fn=process_image,
        inputs=[input_img, replace_toggle, alpha_toggle, bg_color],
        outputs=[output_img, download_file, status_text]
    )


if __name__ == "__main__":
    print("🚀 Starting Background Remover...")
    print("🌐 Open http://127.0.0.1:7860 in your browser.")
    # Theme is now applied here to fix the Gradio 6.0 warning
    demo.launch(share=False, theme=gr.themes.Soft(), inbrowser=True)