gst-launch-1.0 nvarguscamerasrc num-buffers=1 ! nvvidconv ! 'video/x-raw(memory:NVMM), format=I420' ! nvjpegenc ! filesink location=test.jpg > /dev/null
