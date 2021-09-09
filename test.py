from testcontainers.core.container import DockerContainer



tck_image = "gcr.io/akkaserverless-public/akkaserverless-tck:0.7.0-beta.14"

#container = DockerContainer(tck_image, {"TCK_SERVICE_HOST": "host.testcontainers.internal" }, {"8080"}).start()

#with DockerContainer(tck_image, {"TCK_SERVICE_HOST": "host.testcontainers.internal" }, {"8080"}) as d:
with DockerContainer(tck_image) as container:
  container.getLogs({})
