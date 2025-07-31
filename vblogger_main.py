from pixPicker import process_media
from composer import build_video


if __name__ == "__main__":
    testing = False
    # folder = "D:\\projects\\AI_Projects\\vblog_creator\\code\\images"
    # title="Table Rocks Lost City",
    # subtitle="July 26, 2025"
    # final_file = "tableRocks20250726.mp4"

    folder = "D:\\projects\\AI_Projects\\vblog_creator\\code\\20250413-17_Wuhan"
    title="Unforgettable Wuhan"
    subtitle="April, 2025"
    final_file = "wuhan.mp4"
    
    if testing:
        folder = "D:\\projects\\AI_Projects\\vblog_creator\\code\\img"
    
    segments = process_media(folder)
    totalCnt = 1
    for i, segment in enumerate(segments):
        print(f"\n--- Segment {i+1} ---")
        for item in segment:            
            print(f"{item['timestamp']} | {item['type'].upper()} | {item['file']}")
            totalCnt += 1
    print(f"\n--- {totalCnt} ---")

    if testing:
        build_video(segments, "tableRocks_short.mp4", "Summer.m4a")
    else:
        build_video(segments, final_file, title, subtitle, "Summer.m4a")
    

