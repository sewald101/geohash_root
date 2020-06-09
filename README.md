## Geohash, a Django web app, runs locally in a web browser and returns top-trending hashtags and tweet volumes by geographical area at select worldwide (default), country, and metro grains.

### Prerequisites to run geohash locally:

* Docker installed on the local machine
* An AWS account with Access Key and Secret Access Key
* Twitter API credentials stored in an AWS Secret

### To run geohash locally in a web browser:
1) Edit geohash_root/Dockerfile and enter AWS Key and AWS Secret Key where shown.
## SECURITY ALERT: DO NOT COMMIT THIS EDITED DOCKERFILE TO REMOTE VERSION CONTROL, WHICH COULD EXPOSE YOUR AWS CREDENTIALS!!!
2) `$ docker build -t geohash -f Dockerfile .` (Don't forget the dot at the end!)
3) `$ docker ps -a` Note multi-character ID of geohash container and save for clean up.
4) `$ docker run -it -p 80:8888 geohash`
5) In a web browser, visit: localhost/geohash/

### To quit and clean up:
6) `CNTL-C` to shut down local geohash django server.
7) `$ docker stop <ID noted above in Step 3>`
8) To re-run app, repeat Step 4 above.
9) To delete geohash Docker container: `docker rm <ID noted above in Step 3>`
