
import random
from pathlib import Path

video_path = input("Enter the MP4 file path: ").strip('"')
video = Path(video_path)

if not video.exists() or video.suffix.lower() != ".mp4":
    print("Invalid MP4 file!")
else:
    try:
        bit_count = int(input("How many bits should be changed? "))

        if bit_count < 1:
            print("Enter a number greater than zero.")
        else:
            print("Converting MP4 to TXT...")

            data = bytearray(video.read_bytes())
            total_bits = len(data) * 8

            if bit_count > total_bits:
                print("There are not enough bits in the file!")
            else:
                text = ''.join(f'{byte:08b}' for byte in data)

                txt_path = video.with_suffix(".txt")
                txt_path.write_text(text)

                print("Changing random bits...")

                positions = random.sample(
                    range(total_bits),
                    bit_count
                )

                for position in positions:
                    text = (
                        text[:position]
                        + ('1' if text[position] == '0' else '0')
                        + text[position + 1:]
                    )

                txt_path.write_text(text)

                print("Converting TXT back to MP4...")

                modified_data = bytearray(
                    int(text[i:i + 8], 2)
                    for i in range(0, len(text), 8)
                )

                output_path = video.with_name(
                    video.stem + "_modified.mp4"
                )

                output_path.write_bytes(modified_data)

                print("Done!")
                print("Bits changed:", bit_count)
                print("TXT file:", txt_path)
                print("Modified MP4:", output_path)

    except ValueError:
        print("Please enter a valid whole number.")
