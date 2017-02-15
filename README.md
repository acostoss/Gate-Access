# Gate Access
##### or like anything else that needs a relay fired via web

Simple app to expose the ability to set a pin HIGH and LOW. This pin, in the original use case, is attached to a relay's signal pin (along w/ VCC and GND pins fromn the pi) so that when the button is pressed on the web page eposed by the software, the relay is triggered, thus opening an automated security gate. Code is adapted from a project to lower a projector screen, play a video, and raise the screen when finished.

### Requirements
* Raspberry Pi
* A relay (single channel is fine)
* Python 3
* A few packages (`pip install gunicorn flask`)
* Some cables

### Usage
Gate Access is run through Gunicorn, which is easily triggered by running the included `gate.sh`. This creates a UNIX sock connection, gate.sock, that can easily be served through Nginx with something similar to the following:


```Nginx
server {
        listen 80;
        server_name gate.example.com;

        location / {
                include proxy_params;
                proxy_pass http://unix:/home/pi/gate/gate.sock;
        }
}
```