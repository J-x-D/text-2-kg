Text2KG is an application developed by my students and me during my PhD. More details will follow soon.


# LXS Text to KG (MonoRepo)

Welcome to the home of the LXS Text to KG application.

We have split the application into three parts:

- [Frontend](./frontend/README.md) - A Next.js application that is built using React and Typescript and Material UI.
- [Backend](./backend/README.md) - A python application that is responsible for converting text to a knowledge graph.

## Getting Started

### Run with Docker Compose

To run the entire application (Frontend, Backend, and Database) with a single command:

```bash
docker-compose up --build
```

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Database**: localhost:5433

## Ontology example

Here is an example of an ontology that you can use:

`https://raw.githubusercontent.com/owlcs/pizza-ontology/master/pizza.owl`
