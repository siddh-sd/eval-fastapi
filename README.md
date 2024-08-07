# Eval

This Microservice contains the eval modules for the **GDMP** project. The app is currently providing the following modules:
- User Eval Module: This module provides APIs for handling user-related operations and interactions within the evaluation application.
- Evaluation Module: This module offers APIs for comprehensive management of evaluations and associated processes within the project.
- Broker: We have integrated RabbitMQ as our message broker, facilitating seamless communication between various microservices within the project.
- Database: Our project utilizes MongoDB as the primary database, complemented by Beanie, Motor, and Pydantic for efficient data modeling and interaction.

## Installation
The whole app has been dockerised for the ease of development and deployment. For this it is crucial to have [Docker](https://www.docker.com) installed in the machine for running and developing the app. The following steps are required to install the app successfully:

1. [Docker](https://www.docker.com) comes in two variants: [Docker Desktop](https://docs.docker.com/desktop/) and [Docker Engine](https://docs.docker.com/engine/). Though [Docker Engine](https://docs.docker.com/engine/) is the core of [Docker](https://www.docker.com), but [Docker Desktop](https://docs.docker.com/desktop/) is much easier to work and supports all terminal or command prompt commands of [Docker Engine](https://docs.docker.com/engine/).

	The links for installing [Docker Desktop](https://docs.docker.com/desktop/) for different environment are given below:
	- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
	- [Docker Desktop for MacOS](https://docs.docker.com/desktop/install/mac-install/)
	- [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/). For specific distros the links are provided below:
		- [Docker for Debian](https://docs.docker.com/desktop/install/debian/)
		- [Docker for Fedora](https://docs.docker.com/desktop/install/fedora/)
		- [Docker for Ubuntu](https://docs.docker.com/desktop/install/ubuntu/)
		- [Docker for Arch](https://docs.docker.com/desktop/install/archlinux/)

	The links for installing [Docker Engine](https://docs.docker.com/engine/) in different Linux Distros and from binaries are provided below:
	- [Docker for CentOS](https://docs.docker.com/engine/install/centos/)
	- [Docker for Debian](https://docs.docker.com/engine/install/debian/)
	- [Docker for Fedora](https://docs.docker.com/engine/install/fedora/)
	- [Docker for RHEL](https://docs.docker.com/engine/install/rhel/)
	- [Docker for SLES](https://docs.docker.com/engine/install/sles/)
	- [Docker for Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
	- [Docker from Binaries](https://docs.docker.com/engine/install/binaries/)
	
	We would also need to install [Docker Compose](https://docs.docker.com/compose/). [Docker Compose](https://docs.docker.com/compose/) can be enable with ease in [Docker Desktop](https://docs.docker.com/desktop/), but in case of [Docker Engine](https://docs.docker.com/engine/), the steps provided in [Docker Compose Installation](https://docs.docker.com/compose/install/) need to be followed.

2. After successfully installing either [Docker Desktop](https://docs.docker.com/desktop/) or [Docker Engine](https://docs.docker.com/engine/), clone the repository to a specific directory.

3. Enter the following command in terminal or command prompt to run the app only after the *.env* has been created.
	```sh
	docker-compose up --build
	```
