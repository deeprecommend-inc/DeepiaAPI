import replicate

def exec_stable_diffusion_video(prompt):
    output = replicate.run(
        "nateraw/stable-diffusion-videos:2d87f0f8bc282042002f8d24458bbf588eee5e8d8fffb6fbb10ed48d1dac409e",
        input={"prompts": prompt}
    )
    return output
