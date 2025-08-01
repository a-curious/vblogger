from pixPicker import process_media
from composer import build_video


if __name__ == "__main__":
    testing = False

    folder = r"D:\projects\AI_Projects\vblog_creator\code\images"
    title="Table Rocks Lost City"
    subtitle="July 26, 2025"
    final_file = "Table_Rocks_20250726.mp4"
    music = "Summer.m4a"

    # folder = r"D:\projects\AI_Projects\vblog_creator\code\20250413-17_Wuhan"
    # title="Unforgettable Wuhan"
    # subtitle="April, 2025"
    # final_file = "wuhan.mp4"
    # music = "Summer.m4a"
    
    if testing:
        folder = r"D:\projects\AI_Projects\vblog_creator\code\temp"
        final_file = "test.mp4"
    
    segments = process_media(folder)
    totalCnt = 1
    for i, segment in enumerate(segments):
        print(f"\n--- Segment {i+1} ---")
        for item in segment:            
            print(f"{item['timestamp']} | {item['type'].upper()} | {item['file']}")
            totalCnt += 1
    print(f"\n--- {totalCnt} ---")

    if testing:
        build_video(segments, final_file, title, subtitle, music)
    else:
        build_video(segments, final_file, title, subtitle, music)
    

