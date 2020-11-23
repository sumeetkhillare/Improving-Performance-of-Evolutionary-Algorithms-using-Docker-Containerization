# Improving Performance of Evolutionary Algorithms using Docker Containerization
## Sanket Pathak<br/>
## Sumeet Khillare<br/>
## Vaibhav Dighole<br/>

## Mentor
## Dr A.J.Umbarkar sir<br/>
Commands:<br/>
cd python-container<br/>
docker build .<br/>
docker run -it image-name-after-build<br/>

Django Sorting Container <br/>
Before running the containers make sure to change ip address in views.py[line no-14,15] of main container and add it in allowed host for all containers[settings.py line no-28].<br/>
Commands:<br/>
Docker compose command<br/>
docker-compose up --build<br/>
Alternatives-><br/>
For all containers having sorting code:<br/>
docker build .<br/>
docker run -p p-no:8000 img-nm<br/>
For main container which interacts with users:<br/>
docker build .<br/>
docker run -p 8000:8000 --net="host" img-nm<br/>
