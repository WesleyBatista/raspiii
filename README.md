# raspiii
sync raspberry pictures to AWS S3


# Setup

1. `mkdir -p /home/pi/camera_service/images`
2. `pip3 install -r requirements.txt`

> FYI: we are using python 3.7.3 _(installed with pyenv-installer)_


# Dev workflow

```
pi@raspberrypi2:~ $ rm ~/camera_service/main.py; nano ~/camera_service/main.py
```

```
pi@raspberrypi2:~ $ python -u ~/camera_service/main.py
```

## `systemd` service


```
~/devel/camera on  master! ⌚ 0:44:25
$ scp raspiii.service pi@raspberrypi2.local:~/
```

```
root@raspberrypi2:/home/pi# mv raspiii.service /etc/systemd/system/
root@raspberrypi2:/home/pi# systemctl enable raspiii
root@raspberrypi2:/home/pi# systemctl cat raspiii
root@raspberrypi2:/home/pi# systemctl start raspiii
root@raspberrypi2:/home/pi# systemctl status raspiii
● raspiii.service - Raspiii
   Loaded: loaded (/etc/systemd/system/raspiii.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2019-06-04 23:59:53 BST; 4min 50s ago
 Main PID: 539 (python)
   CGroup: /system.slice/raspiii.service
           ├─ 539 python -u main.py
           ├─2636 /bin/sh -c raspistill --mode 0 -o /home/pi/camera_service/images/image_20190604T230443.jpg --noprev
           └─2637 raspistill --mode 0 -o /home/pi/camera_service/images/image_20190604T230443.jpg --nopreview --expos

Jun 05 00:04:26 raspberrypi2 python[539]: > uploaded image_20190604T230425.jpg
Jun 05 00:04:28 raspberrypi2 python[539]: > uploaded image_20190604T230426.jpg
Jun 05 00:04:30 raspberrypi2 python[539]: > uploaded image_20190604T230428.jpg
Jun 05 00:04:32 raspberrypi2 python[539]: > uploaded image_20190604T230430.jpg
Jun 05 00:04:34 raspberrypi2 python[539]: > uploaded image_20190604T230432.jpg
Jun 05 00:04:36 raspberrypi2 python[539]: > uploaded image_20190604T230434.jpg
Jun 05 00:04:37 raspberrypi2 python[539]: > uploaded image_20190604T230436.jpg
Jun 05 00:04:39 raspberrypi2 python[539]: > uploaded image_20190604T230437.jpg
```

