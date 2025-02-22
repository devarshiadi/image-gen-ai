import argparse
import requests
from gradio_client import Client, handle_file

def generate_images(prompt, image_url=None, image_file=None, img_format="landscape", number_of_images=1):
    client = Client("yanze/PuLID-FLUX")

    # Determine input image
    if image_url:
        id_image = handle_file(image_url)
    elif image_file:
        id_image = handle_file(image_file)
    else:
        return "Error: Please provide an image URL or upload an image file."

    # Set dimensions based on chosen format
    if img_format == "landscape":
        width, height = 1280, 720
    elif img_format == "mobile":
        width, height = 1080, 1920
    elif img_format == "instagram":
        width, height = 1080, 1080
    else:
        width, height = 896, 1152  # default fallback

    base_url = "https://yanze-pulid-flux.hf.space/file="

    urls = []
    for i in range(number_of_images):
        try:
            result = client.predict(
                prompt=prompt,
                id_image=id_image,
                start_step=0,
                guidance=4,
                seed="-1",
                true_cfg=1,
                width=width,
                height=height,
                num_steps=20,
                id_weight=1,
                neg_prompt="bad quality, worst quality, text, signature, watermark, extra limbs",
                timestep_to_start_cfg=1,
                max_sequence_length=128,
                api_name="/generate_image"
            )

            file_path = result[0]
            full_url = f"{base_url}{file_path}"

            # Download and save image
            response = requests.get(full_url)
            if response.status_code == 200:
                image_filename = f"output_image_{i+1}.jpg"
                with open(image_filename, "wb") as f:
                    f.write(response.content)
                print(f"Image saved as {image_filename}")
            urls.append(full_url)
        except Exception as e:
            print(f"Error during prediction for image {i+1}: {str(e)}")
            urls.append(None)
    return urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images using PuLID-FLUX")
    parser.add_argument("--prompt", type=str, required=True, help="Text prompt for the image generation")
    parser.add_argument("--image_url", type=str, default=None, help="Optional image URL")
    parser.add_argument("--image_file", type=str, default=None, help="Optional local image file path")
    parser.add_argument("--format", type=str, choices=["landscape", "mobile", "instagram"], default="landscape",
                        help="Image format preset: landscape, mobile, or instagram")
    parser.add_argument("--numberofimages", type=int, default=1, help="Number of images to generate (max 5)")

    args = parser.parse_args()

    if args.numberofimages > 5:
        print("Max number of images is 5. Setting numberofimages to 5.")
        args.numberofimages = 5

    output_urls = generate_images(args.prompt, args.image_url, args.image_file, args.format, args.numberofimages)
    for idx, url in enumerate(output_urls, start=1):
        print(f"Generated Image {idx} URL: {url}")
