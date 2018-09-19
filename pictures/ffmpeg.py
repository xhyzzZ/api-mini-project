import subprocess

cmd = ['ffmpeg', '-framerate', '0.5', '-i', 'img%03d.jpg', '-pix_fmt', 'yuv420p', 'output.mp4']
retcode = subprocess.call(cmd)
if not retcode == 0:
   raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))