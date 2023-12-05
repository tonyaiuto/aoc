
go:
	-mkdir mov
	python3 day13.py

breakout.mov:
	cd mov ; ffmpeg -r 60 -f image2 -s 1920x1080 -i frame%05d.png \
	  -vcodec libx264 -crf 25 -pix_fmt yuv420p breakout.mp4
