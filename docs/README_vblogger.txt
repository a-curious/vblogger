
20250731
[TODO]
* collect more music pieces

[BUG]
* .heic and .heif pictures all missing
* some pictures mistakenly narrowed 
* timestamp order not correct

[FEATURE]
* automatically adjust picture sizes
* support more options for subtitles
* parametrize music, title, color etc.
* add special effects when transitioning
* build interface like picassa 
	o order by timeline
	o thumbnail view
	o select and generate
* use AI to detect the location, search for human readable name, and add subtitles
* use AI to detect people, actions, emotions etc.
* use AI to change face


20250227: 
[TASK]
1. asked ChatGPT to provide code
2. create venv and activate it
3. create a requirements.txt and run pip install -r requirements.txt
4. install ImageMagick (used by TextClip)


[BLOCKER]
* aspect ratio 
* Reason: iPhone internally has rotation aspect ratio (checking rotation does not help)
[FIX]
1. ffprobe -v error -select_streams v:0 -show_entries stream=width,height,display_aspect_ratio sample.mp4
	width=1920
	height=1080
	display_aspect_ratio=9:16
2. ffmpeg -i sample.mp4 -vf "scale=ih*9/16:ih,setdar=9/16" -c:a copy output_fixed.mp4

Downloaded to: D:\projects\tools\ffmpeg-7.1.1-essentials_build\bin


20250227: 
[PLANNING]
1. 会有很多张照片，需要在里面筛选
2. 按照时间线，对应当地的具体信息，给大家背景对照
3. 可能会需要做几个不同主线的vblog
4. 提出建议， 比如
	* 按个人主题
	* 按景点主题
	* 按氛围主题
5. 加注字幕
6. 配音乐


