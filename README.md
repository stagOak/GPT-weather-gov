# Project Title

This project demonstrates a local Python development environment to build, host, and expose an API (e.g., using FastAPI) that translates OpenAI's requests into official National Weather Service (NWS) API calls.

FastAPI will translate between OpenAI's ChatGPT and the National Weather Service (NWS). FastAPI acts as a lightweight middleware to connect OpenAI's ChatGPT and the NWS API.

OpenAI uses JSON formats for ChatGPT plugins or actions and the NWS uses its own protocols.

Your local computer will host a FastAPI bridge that takes the AI's question, translates it into a format the NWS understands, gets the official weather, and translates it back into perfect AI-talk.

System Architecture Schematic

<img src="images/system_architecture_schematic.png" alt="System Architecture Schematic" width="30%"> 



Here is how it was built.

Phase 1: Set Up Your Workshop (Local Environment)\
Install Python\
Create a Project Folder\
Create a Virtual Environment\
Install Your Tools\

Phase 2: Build the Translator (The FastAPI Code)\
Write a Python script that creates endpoints (doors that OpenAI can knock on).

See https://share.google/aimode/EGRJBznWNYKMOsKjm to learn about the work here.