# Project purpose
This project allows to get more benefits from three point estimation. 
For details please refer to base [notebook](https://github.com/shnax0210/work_estimation/blob/master/base_estimation.ipynb).

# How to run
- install [Docker](https://www.docker.com/products/docker-desktop);
- pull image from Docker Hub by next command in console: `docker pull shnax0210/work_estimation`
- create and run container from pulled image by next command in console: `docker run -p 8888:8888 --name work_estimate shnax0210/work_estimation`
- copy link with security token from console to open jupyter notebook at first time: [example](https://www.evernote.com/client/snv?noteGuid=621213e6-6c80-4dad-a476-4c068af1ed9b&noteKey=aea612c0787d98cd&sn=https%3A%2F%2Fwww.evernote.com%2Fshard%2Fs747%2Fsh%2F621213e6-6c80-4dad-a476-4c068af1ed9b%2Faea612c0787d98cd&title=Link%2Bwith%2Bsecurity%2Btocken%2Bfor%2Bjuputer%2Bnotebook);
- open base jupyter notebook with name **base_estimation.ipynb**;
- run all steps to check all functionality works;
- do actions required for your task and rerun all steps.

# How to use
- it uses jupyter notebook so please refer to its [documentation](https://jupyter.org/documentation);
- use **base_estimation.ipynb** as entry point. Modify it for your needs;
- upload excel files with tasks to container through [jupyter notebook upload functionality](https://support.sas.com/software/products/university-edition/faq/jn_accessfiles.htm).
