# Explore Binary Classification Model Metrics

This repository features code that will generate plots of important binary classification metrics and provide the resulting figures and reports both in easy-to-consume form for users who are not as familiar with the metrics as well as presentation-ready notebooks for interactive demos.

## How this repository works:

The following tools are used in this directory:

#### Depedencies:

[Docker](https://docs.docker.com/) - Container software to keep all dependencies in one place

[Pipenv](https://docs.pipenv.org/en/latest/) - Python package management -- Can be replaced by Docker

#### Tools:

[Papermill](https://papermill.readthedocs.io/en/latest/) - A tool that enables the parameterization of Jupyter notebooks. This is how we inject parameters to execute a jupyter notebook

[Jupyter Notebooks](https://jupyter.org/) - A tool for writing code and displaying results in notebook format

[nbconvert](https://github.com/jupyter/nbconvert) - A tool for converting jupyter notebooks to other formats, such as pdf, etc.

[RISE](https://rise.readthedocs.io/en/stable/) - Allow for interactive slides in Jupyter Notebooks


## Docker (Setting up the environment):

After cloning the repository, you can build the docker container by navigating to the top-level directory and running

```sh
sudo docker build -t classification_metrics .
```

This should install everything in the docker container.
Then, in order to enter an interactive session of the docker container, you will need to run the following:

```sh
sudo docker run -it -p 8888:8888 -v $(pwd):/app/ classification_metrics bash
```

For those new to docker, the `-p` flag indicates that we want to port-forward 8888 from the container to 8888 on the host. This is so that if you run the jupyter notebook inside the container, you will still be able to see it on your host machine. If you are already running something on port 8888 (for example another jupyter notebook), you will have to change this port. 

The -v flag indicates that you will mount your current directory `$(pwd)` to `/app` inside the container. 

The -it flag stands for interactive, which lets you interact with the console.

From here, you can start the jupyter notebook by using:

```jupyter notebook --ip 0.0.0.0 --port 8888 --allow-root```

## Steps to run scripts
1. The input file must be a 2-column csv of model results. Following the `sklearn` convention, the first column will be the output (0 or 1) and the second column will have the predictions. If the file is not formatted correctly, the rest of the process will fail, so make sure the file is in the correct format.

2. Run the generate_plot_data.py script and place the results in a directory that can be read from `papermill <path_to_metrics_template.ipynb> <path_to_output.ipynb> -p parameter1 value1 -p parameter2 value2`

where the parameters can be found at the top of the `Metrics Template.ipynb`

## How to develop

1. Clone this repository and change to the development branch

```sh
git clone https://github.com/michaelgao8/classification-metrics.git
git checkout development
```


2. Create a new branch to work on an issue (make sure you start from the development branch)

```sh
git checkout -b <your_name>/issue-description
```

3. After you have finished making your changes:

```sh
git push -u origin <your_name>/issue-description
```

4. Submit a pull request on Github for your change

