FROM intersystems/iris-community:latest-cd

USER root
WORKDIR /opt/iris

RUN chown ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /opt/iris
COPY deployment/ .
RUN chmod +x ./irissession.sh

USER ${ISC_PACKAGE_MGRUSER}

COPY src/IrisKafkaSink src/IrisKafkaSink

SHELL ["./irissession.sh"]

RUN \
  do $SYSTEM.OBJ.Load("./Installer.cls", "ck") \
  set sc = ##class(App.Installer).Setup()

# bringing the standard shell back
SHELL ["/bin/bash", "-c"]