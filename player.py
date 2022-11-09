from sql import *
from volume import *
import os
import subprocess
import time



def play_mp3_local(fi, a):
   vl = 0
   start_dir = os.path.dirname(os.path.realpath(__file__))
   if os.name == "nt":
      #player = start_dir+"\\ffplay.exe"
      player = start_dir+"\\cmdmp3win.exe"
      player.replace("\\","\\\\",0)
      fi.replace("\\","\\\\",0)
      set_volume(a)
      #p = subprocess.Popen([player, '-autoexit', fi],shell=False)
      p = subprocess.Popen([player, fi],shell=False)
      while p.poll() is None:
         #print(p.poll())
         if vl != a[1]:
            set_volume(a[1])
            vl = int(a[1])
         time.sleep(1) 
   else:
      p = subprocess.Popen(['mpg123', '-q', fi])
      while p.poll() is None:
         #print(p.poll())
         if vl != a[1]:
            set_volume(a[1])
            vl = int(a[1])
         time.sleep(1)


def threader(n, a):
    breaker = 1
    while(breaker == 1): 
            if n.value == 1:
                fi = select_play_threadQ()
                if len(fi) == 0:
                    n.value = 0
                    if a[2] != 0: 
                       a[3] = a[2]
                    a[2] = 0
                else:
                    if a[2] != 0:
                       a[3] = a[2]
                    a[2] = fi[0]
                    play_mp3_local(fi[1], a)
                    update_data_entry(fi)
            elif n.value == 0:
                if a[2] != 0: 
                   a[3] = a[2]
                a[2] = 0               
                time.sleep(2)
            if os.name == "nt":
               print(a[0])
               print(n.value)
               import ctypes
               kernel32 = ctypes.windll.kernel32
               SYNCHRONIZE = 0x100000
               process = kernel32.OpenProcess(SYNCHRONIZE, 0, a[0])
               if process != 0:
                  kernel32.CloseHandle(process)
                  breaker = 1
               else:
                  breaker = 0
            else:
               try:
                 os.kill(a[0], 0)
               except OSError:
                   breaker = 0
               else:
                   breaker = 1


