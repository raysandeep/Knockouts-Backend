<p align="center">
<a href="https://dscvit.com">
	<img src="https://user-images.githubusercontent.com/30529572/72455010-fb38d400-37e7-11ea-9c1e-8cdeb5f5906e.png" />
</a>
	<h2 align="center"> KnockOuts Backend </h2>
	<h4 align="center"> A Competetive Coding Portal Backend  <h4>
</p>

---
[![DOCS](https://img.shields.io/badge/Documentation-see%20docs-green?style=flat-square&logo=appveyor)](https://documenter.getpostman.com/view/8653133/T17Nbjz8) 
  [![UI ](https://img.shields.io/badge/User%20Interface-Link%20to%20UI-orange?style=flat-square&logo=appveyor)](https://knockouts.dscvit.com/)

#####Link for Forntend Repo : <a href="https://github.com/GDGVIT/competitive-edge-web">Knockouts-Frontend</a>

## Functionalities
- [x]  Run Code
- [x]  Submit Code
- [x]  Check Score
- [x]  Auto Assign Rooms
- [x]  Create Rounds
- [x]  Adding multiple members to room
- [x]  Disqualify and qualify people automatically
- [x]  Google and Github OAUTH

<br>

## Database ER Diagram
![ER_Diagram](./er.png)

## Instructions to run

* Pre-requisites:
	-  Docker
	-  Python
	-  GOOGLE RECAPTCHA SETUP
	-  Firebase Project for Authentication
	-  JudgeAPI Self Deployed server for Run and Submit Code

* Directions to install
    - Place your Firebase Config file in app dir as knockoutsfb.json
    - Deploy <a href="https://api.judge0.com/">Judge API</a>
    - Navigate to ```traefik.toml``` file and configure domain and email. For changing default password <a href="https://docs.traefik.io/middlewares/basicauth/#general">check this out</a>
    - Before deploying configure DNS with a CNAME Address pointing to the server's IP. By default Traefik is configured to HTTPS.
    - For running in localhost ignore the above two steps
    - Fill your Frontend Host Details in ```settings.py``` file for CORS.
    - Fill all your env variables using the below commands.
    - Use ```test_case_tester.py``` file to test uploaded testcases.
    - Use ```questions.ipynb``` file to replicate questions and testcases
```bash
cp example.env .env
nano .env 
```

* Directions to execute

```bash
docker-compose build
docker-compose up -d
docker exec -it traefik sh
chmod 600 acme.json
```
After this step Traefik will request for SSL Certificate and it will be stored in ```acme.json``` file

## Contributors

<table>
<tr align="center">


<td>

Sai Sandeep Rayanuthala<br><br>
```Backend ```
<p align="center">
<img src = "https://avatars0.githubusercontent.com/u/43823311?s=460&u=e0da23e03034950789b46d08e02c836c4f72f404&v=4" width="150" height="150" alt="Sai Sandeep Rayanuthala">
</p>
<p align="center">
<a href = "https://github.com/raysandeep/"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/sai-sandeep-r/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>

<td>

Amogh Lele<br><br>
```Deployment ```


<p align="center">
<img src = "https://media-exp1.licdn.com/dms/image/C5103AQGhU06DpqXIqw/profile-displayphoto-shrink_200_200/0?e=1603929600&v=beta&t=UZD0D8RDaLbssdQi5Hiap5JZmUH9JGhMM2kQ3m5BQ6o" width="150" height="150" alt="Amogh Lele">
</p>
<p align="center">
<a href = "https://github.com/ATechnoHazard"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/amogh-lele-830131a4/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>







</tr>
  </table>

<br>
<br>

<p align="center">
	Made with ♥️ by <a href="https://dscvit.com">DSC VIT</a>
</p>
