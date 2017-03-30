FROM openshift/origin:latest

USER root

RUN yum -y install python-pip && \
    pip install kubernetes
RUN git clone https://github.com/pycontribs/jenkinsapi.git && \
    cd jenkinsapi && \
    pip install .

ENV JENKINS_SERVICE_URL="http://jenkins"

COPY bin/* /usr/bin/

ENTRYPOINT ["/usr/bin/oc", "observe", "secrets", \
               "--names=secret-names.py", \
               "--delete=secret-delete.py", \
               "-a", "{ .metadata.annotations.ci\.openshift\.io/jenkins-secret-id }", \
               "--", "secret-added.py"]
