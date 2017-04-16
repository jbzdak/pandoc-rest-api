# A pandoc http api in docker container

Will mostly be used to convert markdown to other formats, 
so I really checked only markdown input. 

App is dead simple so if you want to edit it it should be 
straightforward. 

There is no authorization whatsoever (I want to deploy this as
part of docker deployment where this service will be private.)

You can see this on dockerhup here: https://hub.docker.com/r/jbzdak/pandoc-rest-api/ 

API format is ``/v0/convert/<in_format>/<out_format>``, input contents 
are in raw post data and output is in raw post response. 

To test locally: 

0. Go to repository folder
1. ``docker-compose up``
2. ``curl -X POST --data-binary @test.md http://localhost:5000/v0/convert/markdown_github/latex > test.pdf``


