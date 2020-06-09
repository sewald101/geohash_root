## Geohash runs locally in a Web browser and returns top-trending hashtags and tweet volumes by geographical area at select worldwide (default), country, and metro grains.

### Requirements:

1) Docker installed
2) An AWS account with Access Key and Secret Access Key
3) Twitter API credentials stored in an AWS Secret

### To run geohash locally in a web browser:
1) Edit Dockerfile and enter AWS Key and AWS Secret Key where shown
## SECURITY ALERT: DO NOT COMMIT THIS EDITED DOCKERFILE TO REMOTE VERSION CONTROL, WHICH COULD EXPOSE YOUR AWS CREDENTIALS!!!
2) `$ docker build -t geohash -f Dockerfile .` (Don't forget the dot at the end!)
3) `$ docker run -it -p 80:8888 geohash
4) In browser, visit localhost/geohash/
